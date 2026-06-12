import json
import os

NOTEBOOK_PATH = r'e:\PROJECT\01_Data_Analytics\Operation Analytics\DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS\Notebooks\Phase2_Newsvendor_Risk_Optimization.ipynb'

# Redesigned code blocks for target cells

# Cell 2: Setup
SETUP_CODE = [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from scipy import stats\n",
    "from scipy.optimize import differential_evolution\n",
    "import matplotlib.pyplot as plt   \n",
    "import seaborn as sns\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Apply clean corporate theme defaults\n",
    "plt.rcParams.update({\n",
    "    'figure.figsize': (12, 7), 'font.family': 'sans-serif', 'font.size': 11,\n",
    "    'axes.titlesize': 14, 'axes.labelsize': 12, 'axes.titleweight': 'bold',\n",
    "    'figure.dpi': 120,\n",
    "    'axes.spines.top': False, 'axes.spines.right': False,\n",
    "    'axes.edgecolor': '#94A3B8', 'axes.linewidth': 0.8,\n",
    "    'grid.color': '#E2E8F0', 'grid.linestyle': '--', 'grid.linewidth': 0.5,\n",
    "})\n",
    "sns.set_style(\"white\")\n",
    "print(\"✅ Libraries loaded\")"
]

# Cell 8: sufficient_cats display
CELL_8_CODE = [
    "# Corporate table styling function\n",
    "def style_corporate_table(df):\n",
    "    return df.style.set_properties(**{\n",
    "        'font-family': 'sans-serif',\n",
    "        'font-size': '12px',\n",
    "        'padding': '8px 12px',\n",
    "        'border-bottom': '1px solid #E2E8F0',\n",
    "        'color': '#334155'\n",
    "    }).set_table_styles([\n",
    "        {'selector': 'thead th', 'props': [\n",
    "            ('background-color', '#F8FAFC'),\n",
    "            ('color', '#1E3A8A'),\n",
    "            ('font-weight', 'bold'),\n",
    "            ('border-bottom', '2px solid #CBD5E1'),\n",
    "            ('text-align', 'center'),\n",
    "            ('padding', '10px 12px')\n",
    "        ]},\n",
    "        {'selector': 'tbody tr:hover', 'props': [('background-color', '#F1F5F9')]}\n",
    "    ])\n",
    "\n",
    "# Display sufficient categories table\n",
    "styled_cats = sufficient_cats[['Category Name', 'mu_demand', 'sigma_demand', 'cv', 'p50_demand', 'p90_demand', 'n_months', 'total_revenue']].copy()\n",
    "styled_cats.columns = ['Category Name', 'Mean Demand (μ)', 'Std Dev (σ)', 'CV', 'Median (p50)', 'Target (p90)', 'Months Count', 'Total Revenue ($)']\n",
    "display(style_corporate_table(styled_cats.round(1).style.format({'Total Revenue ($)': '${:,.0f}'})))\n"
]

# Cell 9: Demand Trend
CELL_9_CODE = [
    "# ─── DEMAND TREND — TOP 5 CATEGORIES ─────────────────────────────────\n",
    "fig, ax = plt.subplots(figsize=(12, 6))\n",
    "top5 = sufficient_cats.head(5)['Category Name'].tolist()\n",
    "# Define a clean corporate color palette for the 5 lines\n",
    "colors_5 = ['#1E3A8A', '#2563EB', '#475569', '#64748B', '#94A3B8']\n",
    "\n",
    "for i, cat in enumerate(top5):\n",
    "    cat_data = demand_panel[demand_panel['Category Name'] == cat].sort_values('order_month')\n",
    "    ax.plot(range(len(cat_data)), cat_data['demand_units'], marker='o', markersize=3,\n",
    "            label=cat, linewidth=1.5, color=colors_5[i])\n",
    "\n",
    "# Left-aligned clean title & subtitle\n",
    "ax.text(0.0, 1.12, 'Monthly Demand Trend — Top 5 Categories by Revenue', \n",
    "        fontsize=14, fontweight='bold', transform=ax.transAxes, color='#1E293B')\n",
    "ax.text(0.0, 1.06, 'Historical monthly demand (units) showing variance over 37 months', \n",
    "        fontsize=11, transform=ax.transAxes, color='#64748B')\n",
    "\n",
    "ax.set_xlabel('Month Index (Timeline)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.set_ylabel('Demand (Units)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.tick_params(colors='#475569', labelsize=9)\n",
    "\n",
    "# Gridlines\n",
    "ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.8)\n",
    "ax.grid(False, axis='x')\n",
    "\n",
    "# Legend\n",
    "ax.legend(fontsize=9, frameon=False, bbox_to_anchor=(1.02, 1), loc='upper left')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Cell 10: Demand Distributions
CELL_10_CODE = [
    "# ─── DEMAND DISTRIBUTIONS ─────────────────────────────────────────────\n",
    "top10 = sufficient_cats.head(10)['Category Name'].tolist()\n",
    "fig, axes = plt.subplots(2, 3, figsize=(16, 9))\n",
    "\n",
    "for ax, cat in zip(axes.flat, top10[:6]):\n",
    "    cat_data = demand_panel[demand_panel['Category Name'] == cat]['demand_units']\n",
    "    \n",
    "    # Clean corporate navy hist bars\n",
    "    ax.hist(cat_data, bins=15, color='#1E3A8A', edgecolor='white', alpha=0.85, rwidth=0.9)\n",
    "    \n",
    "    mu, sigma = cat_data.mean(), cat_data.std()\n",
    "    ax.axvline(mu, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Mean μ={mu:.0f}')\n",
    "    ax.axvline(mu + sigma, color='#F97316', linestyle=':', linewidth=1.5, label=f'μ+σ={mu+sigma:.0f}')\n",
    "    \n",
    "    ax.set_title(f'{cat}\\n(n={len(cat_data)} months)', fontsize=10, fontweight='bold', color='#1E293B', pad=10)\n",
    "    ax.legend(fontsize=8, frameon=False, loc='upper right')\n",
    "    ax.tick_params(colors='#475569', labelsize=8)\n",
    "    \n",
    "    # Apply spines and grids to each subplot\n",
    "    ax.spines['top'].set_visible(False)\n",
    "    ax.spines['right'].set_visible(False)\n",
    "    ax.spines['left'].set_color('#E2E8F0')\n",
    "    ax.spines['bottom'].set_color('#E2E8F0')\n",
    "    ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.7)\n",
    "\n",
    "plt.suptitle('Monthly Demand Distribution — Top 6 Categories', fontsize=14, fontweight='bold', color='#1E293B', y=0.98)\n",
    "plt.tight_layout(rect=[0, 0, 1, 0.95])\n",
    "plt.show()"
]

# Cell 12: Estimate params display
CELL_12_CODE = [
    "# ─── ESTIMATE p, c, s PER CATEGORY ──────────────────────────────────\n",
    "newsvendor_params = []\n",
    "for _, row in sufficient_cats.iterrows():\n",
    "    cat = row['Category Name']\n",
    "    p = row['avg_price']\n",
    "    profit_margin = np.clip(row['avg_profit_ratio'], 0.01, 0.49)\n",
    "    c = p * (1 - profit_margin)\n",
    "    s = p * row['avg_discount_rate']\n",
    "    if s >= c:\n",
    "        s = c * 0.5  # Đảm bảo s < c\n",
    "    cr = np.clip((p - c) / (p - s), 0.01, 0.99)\n",
    "    \n",
    "    newsvendor_params.append({\n",
    "        'Category Name': cat, 'p': round(p, 2), 'c': round(c, 2), \n",
    "        's': round(s, 2), 'critical_ratio': round(cr, 4),\n",
    "        'mu_demand': row['mu_demand'], 'sigma_demand': row['sigma_demand'],\n",
    "        'cv': row['cv'], 'total_revenue': row['total_revenue'],\n",
    "    })\n",
    "\n",
    "params_df = pd.DataFrame(newsvendor_params).sort_values('total_revenue', ascending=False).reset_index(drop=True)\n",
    "\n",
    "# Display corporate styled table\n",
    "styled_params = params_df[['Category Name', 'p', 'c', 's', 'critical_ratio', 'mu_demand', 'sigma_demand']].head(15).copy()\n",
    "styled_params.columns = ['Category Name', 'Price (p)', 'Cost (c)', 'Salvage (s)', 'Critical Ratio (CR)', 'Mean Demand (μ)', 'Std Dev (σ)']\n",
    "display(style_corporate_table(styled_params.style.format({\n",
    "    'Price (p)': '${:,.2f}', 'Cost (c)': '${:,.2f}', 'Salvage (s)': '${:,.2f}',\n",
    "    'Critical Ratio (CR)': '{:.4f}', 'Mean Demand (μ)': '{:,.1f}', 'Std Dev (σ)': '{:,.1f}'\n",
    "})))"
]

# Cell 13: Results display
CELL_13_CODE = [
    "# ─── TÍNH Q* VÀ MONTE CARLO PROFIT ──────────────────────────────────\n",
    "np.random.seed(42)\n",
    "N_SIM = 1000\n",
    "\n",
    "results = []\n",
    "profit_distributions = {}\n",
    "\n",
    "for _, row in params_df.iterrows():\n",
    "    cat = row['Category Name']\n",
    "    p, c, s, cr = row['p'], row['c'], row['s'], row['critical_ratio']\n",
    "    mu, sigma = row['mu_demand'], row['sigma_demand']\n",
    "    \n",
    "    # Lấy demand lịch sử\n",
    "    cat_demand = demand_panel[demand_panel['Category Name'] == cat]['demand_units'].values\n",
    "    \n",
    "    # Q* từ empirical quantile\n",
    "    q_star = max(1, round(np.percentile(cat_demand, cr * 100)))\n",
    "    \n",
    "    # Monte Carlo simulation\n",
    "    demand_sim = np.random.choice(cat_demand, size=N_SIM, replace=True)\n",
    "    sold = np.minimum(demand_sim, q_star)\n",
    "    excess = np.maximum(q_star - demand_sim, 0)\n",
    "    profit_sim = p * sold + s * excess - c * q_star\n",
    "    \n",
    "    results.append({\n",
    "        'Category Name': cat, 'mu_demand': round(mu, 0), 'sigma_demand': round(sigma, 0),\n",
    "        'p': p, 'c': c, 's': s, 'critical_ratio': cr, 'q_star': q_star,\n",
    "        'expected_profit': round(profit_sim.mean(), 2),\n",
    "        'profit_std': round(profit_sim.std(), 2),\n",
    "        'p_loss': round((profit_sim < 0).mean(), 4),\n",
    "        'p05_profit': round(np.percentile(profit_sim, 5), 2),\n",
    "        'total_revenue': row['total_revenue'],\n",
    "    })\n",
    "    if row['total_revenue'] >= params_df['total_revenue'].quantile(0.7):\n",
    "        profit_distributions[cat] = profit_sim\n",
    "\n",
    "results_df = pd.DataFrame(results).sort_values('total_revenue', ascending=False).reset_index(drop=True)\n",
    "\n",
    "# Display corporate styled table\n",
    "styled_results = results_df[['Category Name', 'q_star', 'expected_profit', 'profit_std', 'p_loss', 'p05_profit']].copy()\n",
    "styled_results.columns = ['Category Name', 'Optimal Q*', 'Expected Profit', 'Profit StdDev', 'Loss Probability', '5th Percentile Profit']\n",
    "display(style_corporate_table(styled_results.style.format({\n",
    "    'Optimal Q*': '{:,.0f}', 'Expected Profit': '${:,.2f}', 'Profit StdDev': '${:,.2f}',\n",
    "    'Loss Probability': '{:.2%}', '5th Percentile Profit': '${:,.2f}'\n",
    "})))\n"
]

# Cell 15: Q* vs Mean Demand
CELL_15_CODE = [
    "# ─── Q* vs MEAN DEMAND ───────────────────────────────────────────────\n",
    "top15 = results_df.head(15)\n",
    "fig, ax = plt.subplots(figsize=(12, 6))\n",
    "x = np.arange(len(top15))\n",
    "width = 0.35\n",
    "\n",
    "# Corporate Navy and Coral colors\n",
    "ax.bar(x - width/2, top15['mu_demand'], width, label='Mean Demand (μ)', color='#1E3A8A', alpha=0.9)\n",
    "ax.bar(x + width/2, top15['q_star'], width, label='Optimal Order Q*', color='#EF4444', alpha=0.9)\n",
    "\n",
    "# Labels and styling\n",
    "ax.set_xticks(x)\n",
    "ax.set_xticklabels([c[:18] for c in top15['Category Name']], rotation=35, ha='right', fontsize=9, color='#334155')\n",
    "ax.set_ylabel('Quantity (Units)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.tick_params(colors='#475569', labelsize=9)\n",
    "\n",
    "# Clean left-aligned title & subtitle\n",
    "ax.text(0.0, 1.12, 'Newsvendor Optimal Q* vs Historical Mean Demand', \n",
    "        fontsize=14, fontweight='bold', transform=ax.transAxes, color='#1E293B')\n",
    "ax.text(0.0, 1.06, 'Comparing expected demand (μ) with the risk-adjusted optimal order quantity (Q*) across top 15 categories', \n",
    "        fontsize=11, transform=ax.transAxes, color='#64748B')\n",
    "\n",
    "# Gridlines\n",
    "ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.8)\n",
    "ax.set_axisbelow(True)\n",
    "\n",
    "# Legend\n",
    "ax.legend(fontsize=9, frameon=False, loc='upper right')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Cell 16: Profit Histogram
CELL_16_CODE = [
    "# ─── PROFIT HISTOGRAM — TOP CATEGORY ─────────────────────────────────\n",
    "top_cat = results_df.iloc[0]['Category Name']\n",
    "if top_cat in profit_distributions:\n",
    "    fig, ax = plt.subplots(figsize=(10, 5.5))\n",
    "    pdata = profit_distributions[top_cat]\n",
    "    \n",
    "    # Plot histogram with clean corporate colors\n",
    "    ax.hist(pdata, bins=40, color='#1E3A8A', edgecolor='white', alpha=0.85, rwidth=0.9)\n",
    "    \n",
    "    # Custom vertical lines for key metrics\n",
    "    ax.axvline(pdata.mean(), color='#10B981', linestyle='--', linewidth=2, label=f'Expected Profit E[P] = ${pdata.mean():,.0f}')\n",
    "    ax.axvline(np.percentile(pdata, 5), color='#EF4444', linestyle=':', linewidth=2, label=f'5th Percentile P05 = ${np.percentile(pdata, 5):,.0f}')\n",
    "    ax.axvline(0, color='#64748B', linestyle='-', linewidth=1, alpha=0.7, label='Break-even ($0)')\n",
    "    \n",
    "    # Left-aligned clean title & subtitle\n",
    "    ax.text(0.0, 1.14, f'Profit Distribution at Optimal Q* — {top_cat}', \n",
    "            fontsize=13, fontweight='bold', transform=ax.transAxes, color='#1E293B')\n",
    "    ax.text(0.0, 1.07, f'Monte Carlo simulation of profit scenarios under demand uncertainty (N={N_SIM} runs)', \n",
            fontsize=10.5, transform=ax.transAxes, color='#64748B')\n",
    "    \n",
    "    ax.set_xlabel('Profit ($)', fontsize=10, color='#475569', labelpad=10)\n",
    "    ax.tick_params(colors='#475569', labelsize=9)\n",
    "    \n",
    "    # Format X axis as dollars\n",
    "    from matplotlib.ticker import FuncFormatter\n",
    "    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f\"${x*1e-3:.0f}K\" if x != 0 else \"$0\"))\n",
    "    \n",
    "    ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.8)\n",
    "    ax.set_axisbelow(True)\n",
    "    ax.legend(fontsize=9, frameon=False, loc='upper left')\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()"
]

# Cell 20: Optimization results display
CELL_20_CODE = [
    "# ─── DIFFERENTIAL EVOLUTION OPTIMIZATION ─────────────────────────────\n",
    "risk_budgets = {'strict': 0.10, 'base': 0.15, 'relaxed': 0.25}\n",
    "\n",
    "def objective_penalized(Q, max_std, budget):\n",
    "    tp = compute_total_profit(Q)\n",
    "    penalty = 0\n",
    "    if tp.std() > max_std: penalty += 10000 * (tp.std() - max_std) / max_std\n",
    "    cost = (c_vec * Q).sum()\n",
    "    if cost > budget: penalty += 10000 * (cost - budget) / budget\n",
    "    return -tp.mean() + penalty\n",
    "\n",
    "frontier_results = [{'risk_budget': 'newsvendor_baseline', 'risk_pct': baseline_std/baseline_e,\n",
    "    'expected_profit': round(baseline_e,2), 'profit_std': round(baseline_std,2),\n",
    "    'cv': round(baseline_std/baseline_e,3), 'p_loss': round((baseline_profit<0).mean(),4),\n",
    "    'total_cost': round(baseline_budget,2), 'profit_change_pct': 0, 'risk_change_pct': 0,\n",
    "    'Q_optimal': q_baseline.round(0).astype(int).tolist()}]\n",
    "\n",
    "for name, rpct in risk_budgets.items():\n",
    "    print(f\"\\nOptimizing {name} ({rpct:.0%})...\")\n",
    "    max_std = rpct * baseline_e\n",
    "    bounds = [(max(1, min_q_service[k]*0.5), 2.5*results_df.iloc[k]['mu_demand']) for k in range(K)]\n",
    "    \n",
    "    result = differential_evolution(objective_penalized, bounds, args=(max_std, baseline_budget*1.1),\n",
    "                                     seed=42, maxiter=100, popsize=15, tol=1e-4)\n",
    "    Q_opt = result.x\n",
    "    tp = compute_total_profit(Q_opt)\n",
    "    e, s = tp.mean(), tp.std()\n",
    "    frontier_results.append({\n",
    "        'risk_budget': name, 'risk_pct': rpct,\n",
    "        'expected_profit': round(e,2), 'profit_std': round(s,2),\n",
    "        'cv': round(s/e,3) if e>0 else 999, 'p_loss': round((tp<0).mean(),4),\n",
    "        'total_cost': round((c_vec*Q_opt).sum(),2),\n",
    "        'profit_change_pct': round((e-baseline_e)/baseline_e*100,2),\n",
    "        'risk_change_pct': round((s-baseline_std)/baseline_std*100,2),\n",
    "        'Q_optimal': Q_opt.round(0).astype(int).tolist()\n",
    "    })\n",
    "    print(f\"  E[P]=${e:,.0f}, σ=${s:,.0f}, CV={s/e:.3f}\")\n",
    "\n",
    "frontier_df = pd.DataFrame(frontier_results)\n",
    "\n",
    "# Display corporate styled table\n",
    "styled_frontier = frontier_df[['risk_budget','expected_profit','profit_std','cv','p_loss','total_cost','profit_change_pct','risk_change_pct']].copy()\n",
    "styled_frontier.columns = ['Risk Budget', 'Expected Profit', 'Profit StdDev', 'CV', 'Loss Prob', 'Total Cost', 'Profit Change %', 'Risk Change %']\n",
    "display(style_corporate_table(styled_frontier.style.format({\n",
    "    'Expected Profit': '${:,.2f}', 'Profit StdDev': '${:,.2f}', 'CV': '{:.3f}',\n",
    "    'Loss Prob': '{:.2%}', 'Total Cost': '${:,.2f}', 'Profit Change %': '{:+.2f}%', 'Risk Change %': '{:+.2f}%'\n",
    "})))\n"
]

# Cell 22: Risk-Reward Frontier
CELL_22_CODE = [
    "# ─── RISK-REWARD FRONTIER ─────────────────────────────────────────────\n",
    "fig, ax = plt.subplots(figsize=(10, 6.5))\n",
    "colors = {'newsvendor_baseline': '#1E3A8A', 'strict': '#10B981', 'base': '#F59E0B', 'relaxed': '#EF4444'}\n",
    "markers = {'newsvendor_baseline': 's', 'strict': '^', 'base': 'o', 'relaxed': 'D'}\n",
    "\n",
    "# Curve\n",
    "ax.plot(grid_df['profit_std'], grid_df['expected_profit'], '-', color='#94A3B8', linewidth=2, alpha=0.7, label='Portfolio scaling curve')\n",
    "\n",
    "# Scatter points\n",
    "for _, row in frontier_df.iterrows():\n",
    "    ax.scatter(row['profit_std'], row['expected_profit'],\n",
    "               c=colors.get(row['risk_budget'],'gray'), s=220,\n",
    "               marker=markers.get(row['risk_budget'],'o'),\n",
    "               edgecolors='white', linewidths=1.5,\n",
    "               label=f\"{row['risk_budget'].capitalize()} Policy (CV={row['cv']:.3f})\", zorder=5)\n",
    "\n",
    "# Axis format\n",
    "from matplotlib.ticker import FuncFormatter\n",
    "ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f\"${x*1e-3:.0f}K\"))\n",
    "ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f\"${x*1e-3:.0f}K\"))\n",
    "\n",
    "ax.set_xlabel('Portfolio Risk — StdDev ($)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.set_ylabel('Expected Monthly Profit ($)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.tick_params(colors='#475569', labelsize=9)\n",
    "\n",
    "# Left-aligned clean title & subtitle\n",
    "ax.text(0.0, 1.12, 'Risk-Reward Frontier for Supply Chain Portfolio', \n",
    "        fontsize=14, fontweight='bold', transform=ax.transAxes, color='#1E293B')\n",
    "ax.text(0.0, 1.06, 'Expected portfolio profit vs standard deviation showing trade-offs between risk budgets', \n",
    "        fontsize=11, transform=ax.transAxes, color='#64748B')\n",
    "\n",
    "ax.legend(fontsize=9, frameon=False, loc='lower right')\n",
    "ax.grid(True, axis='both', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.7)\n",
    "ax.set_axisbelow(True)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Cell 23: Q Comparison
CELL_23_CODE = [
    "# ─── Q COMPARISON ────────────────────────────────────────────────────\n",
    "top_k = min(10, K)\n",
    "fig, ax = plt.subplots(figsize=(12, 6))\n",
    "x = np.arange(top_k)\n",
    "n_pol = len(frontier_df)\n",
    "w = 0.85/n_pol\n",
    "offs = np.linspace(-(n_pol-1)/2, (n_pol-1)/2, n_pol)*w\n",
    "\n",
    "# Re-use policy colors\n",
    "pcols = [colors.get(row['risk_budget'], 'gray') for _, row in frontier_df.iterrows()]\n",
    "\n",
    "for i, (_, row) in enumerate(frontier_df.iterrows()):\n",
    "    ax.bar(x+offs[i], row['Q_optimal'][:top_k], w, \n",
    "           label=row['risk_budget'].capitalize(), color=pcols[i], alpha=0.9)\n",
    "\n",
    "ax.set_xticks(x)\n",
    "ax.set_xticklabels([c[:18] for c in categories[:top_k]], rotation=30, ha='right', fontsize=9, color='#334155')\n",
    "ax.set_ylabel('Optimal Order Quantity (Q)', fontsize=10, color='#475569', labelpad=10)\n",
    "ax.tick_params(colors='#475569', labelsize=9)\n",
    "\n",
    "# Left-aligned clean title & subtitle\n",
    "ax.text(0.0, 1.12, 'Optimal Order Quantity (Q*) Comparison by Category', \n",
    "        fontsize=14, fontweight='bold', transform=ax.transAxes, color='#1E293B')\n",
    "ax.text(0.0, 1.06, 'Comparing optimal order quantities across different risk policy budgets for top 10 categories', \n",
    "        fontsize=11, transform=ax.transAxes, color='#64748B')\n",
    "\n",
    "ax.legend(fontsize=9, frameon=False, loc='upper right')\n",
    "ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.8)\n",
    "ax.set_axisbelow(True)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
]

# Cell 24: Profit Distributions comparison
CELL_24_CODE = [
    "# ─── PROFIT DISTRIBUTIONS BY POLICY ──────────────────────────────────\n",
    "fig, axes = plt.subplots(2, 2, figsize=(12, 9))\n",
    "from matplotlib.ticker import FuncFormatter\n",
    "\n",
    "for ax, (_, row) in zip(axes.flat, frontier_df.iterrows()):\n",
    "    Q = np.array(row['Q_optimal'], dtype=float)\n",
    "    tp = compute_total_profit(Q)\n",
    "    c = colors.get(row['risk_budget'], 'gray')\n",
    "    \n",
    "    # Plot histogram with clean rwidth\n",
    "    ax.hist(tp, bins=40, color=c, edgecolor='white', alpha=0.85, rwidth=0.9)\n",
    "    \n",
    "    # Key stats lines\n",
    "    ax.axvline(tp.mean(), color='#10B981', linestyle='--', linewidth=1.5, label=f'E[P]=${tp.mean():,.0f}')\n",
    "    ax.axvline(np.percentile(tp,5), color='#EF4444', linestyle=':', linewidth=1.5, label=f'P05=${np.percentile(tp,5):,.0f}')\n",
    "    ax.axvline(0, color='#64748B', linestyle='-', linewidth=1, alpha=0.5)\n",
    "    \n",
    "    ax.set_title(f'{row[\"risk_budget\"].capitalize()} Policy (CV={row[\"cv\"]:.3f})', \n",
    "                 fontsize=11, fontweight='bold', color='#1E293B', pad=10)\n",
    "    ax.legend(fontsize=8, frameon=False, loc='upper left')\n",
    "    \n",
    "    # Format axes\n",
    "    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f\"${x*1e-3:.0f}K\" if x != 0 else \"$0\"))\n",
    "    ax.tick_params(colors='#475569', labelsize=8)\n",
    "    \n",
    "    # Styles\n",
    "    ax.spines['top'].set_visible(False)\n",
    "    ax.spines['right'].set_visible(False)\n",
    "    ax.spines['left'].set_color('#E2E8F0')\n",
    "    ax.spines['bottom'].set_color('#E2E8F0')\n",
    "    ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='#E2E8F0', alpha=0.7)\n",
    "    ax.set_axisbelow(True)\n",
    "\n",
    "plt.suptitle('Profit Distribution Comparison by Risk Policy', fontsize=14, fontweight='bold', color='#1E293B', y=0.98)\n",
    "plt.tight_layout(rect=[0, 0, 1, 0.95])\n",
    "plt.show()"
]


def main():
    print("Loading notebook...")
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    print("Replacing cells...")
    cells = nb['cells']
    
    # 2: Setup
    cells[2]['source'] = SETUP_CODE
    
    # 8: sufficient_cats
    cells[8]['source'] = CELL_8_CODE
    
    # 9: Demand Trend
    cells[9]['source'] = CELL_9_CODE
    
    # 10: Demand Distributions
    cells[10]['source'] = CELL_10_CODE
    
    # 12: Estimate params
    cells[12]['source'] = CELL_12_CODE
    
    # 13: Results
    cells[13]['source'] = CELL_13_CODE
    
    # 15: Q* vs Mean Demand
    cells[15]['source'] = CELL_15_CODE
    
    # 16: Profit Histogram
    cells[16]['source'] = CELL_16_CODE
    
    # 20: Optimization results table
    cells[20]['source'] = CELL_20_CODE
    
    # 22: Risk-Reward Frontier
    cells[22]['source'] = CELL_22_CODE
    
    # 23: Q Comparison
    cells[23]['source'] = CELL_23_CODE
    
    # 24: Policy Profit Distributions
    cells[24]['source'] = CELL_24_CODE

    print("Writing notebook...")
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print("✅ Notebook successfully updated with redesigned visual layout!")

if __name__ == '__main__':
    main()
