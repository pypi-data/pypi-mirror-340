# ================================
#         A/B ANALYSIS TOOLKIT
# ================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest
from itertools import combinations

# --------------------------------
# 1. Очистка выбросов
# --------------------------------
def clean_outliers(data, method='percentile', lower=0.05, upper=0.95):
    if method == 'percentile':
        low = data.quantile(lower)
        high = data.quantile(upper)
        return data[(data >= low) & (data <= high)]
    elif method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return data[(data >= Q1 - 1.5 * IQR) & (data <= Q3 + 1.5 * IQR)]
    elif method == 'winsor':
        low = data.quantile(lower)
        high = data.quantile(upper)
        return data.clip(lower=low, upper=high)
    elif method == 'isolation_forest':
        from sklearn.ensemble import IsolationForest
        clf = IsolationForest(contamination=0.05)
        preds = clf.fit_predict(data.values.reshape(-1, 1))
        return data[preds == 1]
    elif method == 'dbscan':
        from sklearn.cluster import DBSCAN
        db = DBSCAN(eps=0.5, min_samples=5)
        labels = db.fit_predict(data.values.reshape(-1, 1))
        return data[labels != -1]
    return data

# --------------------------------
# 2. Определение нормальности
# --------------------------------
def determine_distribution(data, alpha=0.05):
    stat, p_value = stats.normaltest(data)
    return p_value > alpha, p_value

# --------------------------------
# 3. Бутстреп-анализ
# --------------------------------
def bootstrap_test(sample1, sample2, n_iter=1000, func=np.median, alpha=0.05):
    observed_diff = func(sample2) - func(sample1)
    boot_diffs = []
    for _ in range(n_iter):
        resample1 = np.random.choice(sample1, size=len(sample1), replace=True)
        resample2 = np.random.choice(sample2, size=len(sample2), replace=True)
        boot_diffs.append(func(resample2) - func(resample1))
    ci_lower = np.percentile(boot_diffs, 100 * alpha / 2)
    ci_upper = np.percentile(boot_diffs, 100 * (1 - alpha / 2))
    is_significant = not (ci_lower <= 0 <= ci_upper)
    return {
        'test': 'bootstrap_CI',
        'observed_diff': observed_diff,
        'ci': (ci_lower, ci_upper),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'is_significant': is_significant,
        'p_value': None,
        'p_value_corrected': None,
        'significant': is_significant
    }

# --------------------------------
# 4. Статистический тест (non-stratified)
# --------------------------------
def perform_stat_test(data, metric_type='mean', test_type=None, equal_var=True, n_bootstrap=1000, alpha=0.05):
    groups = data['group'].unique()
    group_data = {g: data[data['group'] == g]['metric'].values for g in groups}

    if test_type is None or test_type == 'auto':
        if metric_type == 'mean':
            normal_flags = [determine_distribution(vals)[0] for vals in group_data.values()]
            chosen_test = 't-test' if all(normal_flags) else 'mannwhitney'
        elif metric_type == 'conversion':
            all_binary = all(set(np.unique(vals)).issubset({0, 1}) for vals in group_data.values())
            chosen_test = 'z-test' if all_binary else 't-test'
        elif metric_type == 'median':
            chosen_test = 'bootstrap'
        else:
            chosen_test = 't-test'
    else:
        chosen_test = test_type

    func = np.mean if metric_type == 'mean' else np.median
    comparisons = {}
    for g1, g2 in combinations(groups, 2):
        if g1 > g2:
            g1, g2 = g2, g1
        x1 = group_data[g1]
        x2 = group_data[g2]
        mean1 = np.mean(x1)
        mean2 = np.mean(x2)
        diff = (mean2 - mean1) / mean1 if mean1 != 0 else np.nan

        if chosen_test == 't-test':
            stat_val, p = stats.ttest_ind(x1, x2, equal_var=equal_var)
            comparisons[(g1, g2)] = {
                'test': 't-test', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'mannwhitney':
            stat_val, p = stats.mannwhitneyu(x1, x2)
            comparisons[(g1, g2)] = {
                'test': 'mannwhitney', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'z-test':
            successes = [x1.sum(), x2.sum()]
            nobs = [len(x1), len(x2)]
            stat_val, p = proportions_ztest(successes, nobs)
            comparisons[(g1, g2)] = {
                'test': 'z-test', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'bootstrap':
            result = bootstrap_test(x1, x2, n_iter=n_bootstrap, func=func, alpha=alpha)
            result['observed_diff'] = diff
            comparisons[(g1, g2)] = result

    return comparisons
    
# --------------------------------
# 5. Поправка на множественные сравнения
# --------------------------------
def adjust_multiple_comparisons(p_value_dict, alpha=0.05, method='bonferroni'):
    pairs = [pair for pair in p_value_dict if 'p_value' in p_value_dict[pair]]
    if len(pairs) <= 1:
        return p_value_dict
    raw_pvals = [p_value_dict[p]['p_value'] for p in pairs]
    reject, pvals_corr, _, _ = multipletests(raw_pvals, alpha=alpha, method=method)
    for i, pair in enumerate(pairs):
        p_value_dict[pair]['p_value_corrected'] = pvals_corr[i]
        p_value_dict[pair]['significant'] = reject[i]
    return p_value_dict

# --------------------------------
# 6. CUPED
# --------------------------------
def perform_cuped(data_exp, data_pre, user_col='user_id', group_col='group', metric_col='metric', min_corr=0.1):
    merged = data_exp.merge(
        data_pre[[user_col, group_col, metric_col]],
        on=[user_col, group_col],
        suffixes=('', '_pre')
    )
    adjusted_rows = []
    cuped_usage, correlations = {}, {}

    for group, group_data in merged.groupby(group_col):
        x_pre, x_exp = group_data[f'{metric_col}_pre'], group_data[metric_col]
        corr = np.corrcoef(x_pre, x_exp)[0, 1]
        correlations[group] = corr
        if abs(corr) >= min_corr:
            theta = np.cov(x_pre, x_exp)[0, 1] / np.var(x_pre)
            x_adj = x_exp - theta * (x_pre - np.mean(x_pre))
            cuped_usage[group] = True
        else:
            x_adj = x_exp
            cuped_usage[group] = False
        adj = group_data.copy()
        adj[metric_col] = x_adj
        adjusted_rows.append(adj.drop(columns=f'{metric_col}_pre'))

    return pd.concat(adjusted_rows), cuped_usage, correlations

# --------------------------------
# 7. Вспомогательный отчёт
# --------------------------------
# Обновим build_analysis_report так, чтобы всегда возвращался original_data внутри report
def build_analysis_report(results_dict, original_data, metric_type='mean', alpha=0.05):
    group_summary = (
        original_data.groupby('group')['metric']
        .agg(['count', 'mean', 'median', 'std'])
        .rename(columns={'count': 'n_users'}).reset_index()
    )

    strat_used = 'stratified_test' in results_dict
    cuped_used = 'CUPED' in results_dict and isinstance(results_dict['CUPED'], dict)

    def is_multiple_comparisons_applied(results):
        if isinstance(results, dict):
            return any(
                isinstance(v, dict) and 'p_value_corrected' in v and v['p_value_corrected'] is not None
                for v in results.values()
            )
        return False

    mc_used = any(
        is_multiple_comparisons_applied(results_dict.get(key))
        for key in ['non_stratified_test', 'stratified_test']
    )

    flags = {
        'Stratification used': strat_used,
        'CUPED applied': cuped_used,
        'Multiple comparisons used': mc_used
    }

    pairwise_rows = []

    def extract_rows(results, label=None):
        if not isinstance(results, dict):
            return
        for (g1, g2), r in results.items():
            row = {
                'group_1': g1,
                'group_2': g2,
                'test': r.get('test'),
                'observed_diff': r.get('observed_diff') or r.get('diff'),
                'p_value': r.get('p_value'),
                'p_value_corrected': r.get('p_value_corrected'),
                'ci_lower': r.get('ci_lower'),
                'ci_upper': r.get('ci_upper'),
                'significant': r.get('significant') if 'significant' in r else (
                    (r.get('p_value_corrected') < alpha) if r.get('p_value_corrected') is not None else
                    (r.get('p_value') < alpha) if r.get('p_value') is not None else None
                )
            }
            if label:
                row['label'] = label
            pairwise_rows.append(row)

    extract_rows(results_dict.get('non_stratified_test'), label='non_stratified')
    extract_rows(results_dict.get('stratified_test'), label='stratified')
    if 'CUPED' in results_dict and isinstance(results_dict['CUPED'], dict):
        extract_rows(results_dict['CUPED'].get('non_stratified'), label='cuped_non_stratified')
        extract_rows(results_dict['CUPED'].get('stratified'), label='cuped_stratified')

    pairwise_df = pd.DataFrame(pairwise_rows)

    return {
        'group_summary': group_summary,
        'analysis_flags': flags,
        'pairwise_comparisons': pairwise_df,
        'original_data': original_data.copy()
    }
def print_analysis_summary(report):
    """
    Выводит интерактивный отчет о результатах A/B теста, включая групповой summary, настройки анализа,
    результаты попарных сравнений и график распределения метрики.
    """
    if 'group_summary' not in report:
        print("Нет данных для отчета.")
        return

    group_summary = report['group_summary']
    settings = report.get('settings', {})
    comparisons = report.get('pairwise_results', pd.DataFrame())

    # ===== GROUP SUMMARY =====

    print("📊 GROUP SUMMARY")
    display(report['group_summary'])

    print("\n📈 ANALYSIS SETTINGS")
    for k, v in report['analysis_flags'].items():
        print(f"{k:<30}: {v}")

    print("\n🧪 PAIRWISE COMPARISONS")
    display(report['pairwise_comparisons'])


    # ===== ГРАФИК РАСПРЕДЕЛЕНИЯ =====
    if 'original_data' in report:
        data = report['original_data']
        if 'group' in data.columns and 'metric' in data.columns:
            fig = go.Figure()
            groups = data['group'].unique()
            colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
            for i, group in enumerate(groups):
                group_data = data[data['group'] == group]['metric']
                fig.add_trace(go.Histogram(
                    x=group_data,
                    name=str(group),
                    opacity=0.6,
                    marker_color=colors[i % len(colors)],
                    nbinsx=50
                ))

            fig.update_layout(
                barmode='group',  # Отображать бары рядом
                title='Распределение метрики по группам',
                xaxis_title='Значение метрики',
                yaxis_title='Количество пользователей',
                legend_title='Группа',
                template='plotly_white'
            )
            fig.show()

# --------------------------------
# 8. Финальная функция анализа
# --------------------------------
def run_ab_analysis(data, metric_type='mean', pre_period_data=None, stratification_column=None,
                    cleaning_method='none', alpha=0.05, test_type=None, cuped_flag=True,
                    n_bootstrap=1000, external_weights=None, mc_method='bonferroni'):
    result = {}
    data = data.copy()
    if cleaning_method != 'none':
        data['metric'] = clean_outliers(data['metric'], method=cleaning_method)
    base_result = perform_stat_test(data, metric_type, test_type, n_bootstrap=n_bootstrap, alpha=alpha)
    if any('p_value' in r for r in base_result.values()) and len(data['group'].unique()) > 2:
        base_result = adjust_multiple_comparisons(base_result, alpha=alpha, method=mc_method)
    result['non_stratified_test'] = base_result

    if pre_period_data is not None and cuped_flag:
        if 'user_id' in data.columns and 'user_id' in pre_period_data.columns:
            data_cuped, cuped_usage, correlations = perform_cuped(data, pre_period_data)
            result['CUPED'] = {
                'non_stratified': perform_stat_test(data_cuped, metric_type, test_type, n_bootstrap, alpha),
                'cuped_usage_by_group': cuped_usage,
                'correlations': correlations
            }
    result['report'] = build_analysis_report(result, data, metric_type, alpha)
    # print("To print report use: print_analysis_summary(result['report'])")
    print_analysis_summary(result['report'])
    return result