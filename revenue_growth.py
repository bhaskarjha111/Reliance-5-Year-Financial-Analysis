import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Reliance 5-Year Financial Growth Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# Title Section
# ----------------------------------------------------
st.title("📊 Reliance Industries: 5-Year Revenue & Profit Growth Dashboard")

st.markdown("""
This dashboard analyzes the 5-year financial performance of **Reliance Industries Ltd**
using consolidated Profit & Loss data from **Screener.in**.

The project focuses on:
- Revenue growth
- Net profit growth
- Year-over-year growth trends
- Net profit margin analysis
- Business interpretation for recruiters and interviewers
""")

# ----------------------------------------------------
# Data Section
# Data Source: Screener.in, Consolidated Profit & Loss
# ----------------------------------------------------
data = {
    "Year": [2022, 2023, 2024, 2025, 2026],
    "Revenue": [694673, 876396, 899041, 962820, 1057219],
    "Net Profit": [67845, 74088, 79020, 81309, 95754]
}

df = pd.DataFrame(data)

# ----------------------------------------------------
# Calculated Columns
# ----------------------------------------------------
df["Revenue YoY Growth %"] = df["Revenue"].pct_change() * 100
df["Profit YoY Growth %"] = df["Net Profit"].pct_change() * 100
df["Net Profit Margin %"] = (df["Net Profit"] / df["Revenue"]) * 100

# CAGR Calculation
start_revenue = df["Revenue"].iloc[0]
end_revenue = df["Revenue"].iloc[-1]
start_profit = df["Net Profit"].iloc[0]
end_profit = df["Net Profit"].iloc[-1]
years = len(df) - 1

revenue_cagr = ((end_revenue / start_revenue) ** (1 / years) - 1) * 100
profit_cagr = ((end_profit / start_profit) ** (1 / years) - 1) * 100
avg_margin = df["Net Profit Margin %"].mean()

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------
st.subheader("📌 Key Financial Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Latest Revenue",
        value=f"₹{end_revenue:,.0f} Cr",
        delta=f"{df['Revenue YoY Growth %'].iloc[-1]:.2f}% YoY"
    )

with col2:
    st.metric(
        label="Latest Net Profit",
        value=f"₹{end_profit:,.0f} Cr",
        delta=f"{df['Profit YoY Growth %'].iloc[-1]:.2f}% YoY"
    )

with col3:
    st.metric(
        label="Revenue CAGR",
        value=f"{revenue_cagr:.2f}%"
    )

with col4:
    st.metric(
        label="Profit CAGR",
        value=f"{profit_cagr:.2f}%"
    )

# ----------------------------------------------------
# Data Table
# ----------------------------------------------------
st.subheader("📄 Financial Data Table")

display_df = df.copy()
display_df["Revenue"] = display_df["Revenue"].map(lambda x: f"₹{x:,.0f} Cr")
display_df["Net Profit"] = display_df["Net Profit"].map(lambda x: f"₹{x:,.0f} Cr")
display_df["Revenue YoY Growth %"] = display_df["Revenue YoY Growth %"].map(
    lambda x: "-" if pd.isna(x) else f"{x:.2f}%"
)
display_df["Profit YoY Growth %"] = display_df["Profit YoY Growth %"].map(
    lambda x: "-" if pd.isna(x) else f"{x:.2f}%"
)
display_df["Net Profit Margin %"] = display_df["Net Profit Margin %"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(display_df, use_container_width=True)

# ----------------------------------------------------
# Dual Axis Chart: Revenue vs Net Profit
# ----------------------------------------------------
st.subheader("📈 Revenue vs Net Profit Trend")

fig_dual = go.Figure()

fig_dual.add_trace(
    go.Scatter(
        x=df["Year"],
        y=df["Revenue"],
        name="Revenue",
        mode="lines+markers",
        line=dict(width=4),
        yaxis="y1"
    )
)

fig_dual.add_trace(
    go.Scatter(
        x=df["Year"],
        y=df["Net Profit"],
        name="Net Profit",
        mode="lines+markers",
        line=dict(width=4, dash="dot"),
        yaxis="y2"
    )
)

fig_dual.update_layout(
    title="Dual-Axis Line Chart: Revenue vs Net Profit",
    xaxis=dict(title="Financial Year"),
    yaxis=dict(title="Revenue ₹ Cr", side="left"),
    yaxis2=dict(
        title="Net Profit ₹ Cr",
        overlaying="y",
        side="right"
    ),
    hovermode="x unified",
    template="plotly_white",
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig_dual, use_container_width=True)

# ----------------------------------------------------
# YoY Growth Bar Chart
# ----------------------------------------------------
st.subheader("📊 Year-over-Year Growth Analysis")

growth_df = df.dropna().copy()

fig_growth = go.Figure()

fig_growth.add_trace(
    go.Bar(
        x=growth_df["Year"],
        y=growth_df["Revenue YoY Growth %"],
        name="Revenue YoY Growth %"
    )
)

fig_growth.add_trace(
    go.Bar(
        x=growth_df["Year"],
        y=growth_df["Profit YoY Growth %"],
        name="Profit YoY Growth %"
    )
)

fig_growth.update_layout(
    title="Revenue Growth vs Profit Growth",
    xaxis_title="Financial Year",
    yaxis_title="Growth %",
    barmode="group",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig_growth, use_container_width=True)

# ----------------------------------------------------
# Net Profit Margin Trend
# ----------------------------------------------------
st.subheader("📉 Net Profit Margin Trend")

fig_margin = px.line(
    df,
    x="Year",
    y="Net Profit Margin %",
    markers=True,
    title="Net Profit Margin Trend Over 5 Years"
)

fig_margin.update_traces(line=dict(width=4))
fig_margin.update_layout(
    xaxis_title="Financial Year",
    yaxis_title="Net Profit Margin %",
    template="plotly_white"
)

st.plotly_chart(fig_margin, use_container_width=True)

# ----------------------------------------------------
# Advanced Insight Section
# ----------------------------------------------------
st.subheader("🧠 Automated Business Insights")

best_revenue_growth_year = growth_df.loc[growth_df["Revenue YoY Growth %"].idxmax()]
best_profit_growth_year = growth_df.loc[growth_df["Profit YoY Growth %"].idxmax()]
best_margin_year = df.loc[df["Net Profit Margin %"].idxmax()]
lowest_margin_year = df.loc[df["Net Profit Margin %"].idxmin()]

st.markdown(f"""
### Key Observations

1. **Highest revenue growth** was recorded in FY {int(best_revenue_growth_year["Year"])}  
   with revenue growing by **{best_revenue_growth_year["Revenue YoY Growth %"]:.2f}%**.

2. **Highest profit growth** was recorded in FY {int(best_profit_growth_year["Year"])}  
   with net profit growing by **{best_profit_growth_year["Profit YoY Growth %"]:.2f}%**.

3. The company achieved its **highest net profit margin** in FY {int(best_margin_year["Year"])}  
   at **{best_margin_year["Net Profit Margin %"]:.2f}%**.

4. The company recorded its **lowest net profit margin** in FY {int(lowest_margin_year["Year"])}  
   at **{lowest_margin_year["Net Profit Margin %"]:.2f}%**.

5. Revenue increased from **₹{start_revenue:,.0f} Cr in FY 2022** to  
   **₹{end_revenue:,.0f} Cr in FY 2026**, showing consistent long-term growth.

6. Net profit increased from **₹{start_profit:,.0f} Cr in FY 2022** to  
   **₹{end_profit:,.0f} Cr in FY 2026**, indicating improvement in profitability.
""")

# ----------------------------------------------------
# Recruiter-Focused Interpretation
# ----------------------------------------------------
st.subheader("💼 Business Interpretation")

st.markdown(f"""
Reliance Industries has shown strong top-line growth over the 5-year period.
The revenue CAGR of **{revenue_cagr:.2f}%** indicates that the company has expanded
its business scale significantly.

The profit CAGR of **{profit_cagr:.2f}%** shows that profitability has also improved,
although profit growth was not always proportional to revenue growth. This difference
highlights the impact of operating costs, depreciation, interest, tax expenses, and
business segment performance.

The average net profit margin during the period was **{avg_margin:.2f}%**.
A stable margin trend suggests that the company has been able to maintain profitability
despite operating at a very large scale.
""")

# ----------------------------------------------------
# Download Button
# ----------------------------------------------------
st.subheader("⬇️ Download Processed Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV File",
    data=csv,
    file_name="reliance_5_year_financial_growth.csv",
    mime="text/csv"
)

# ----------------------------------------------------
# Data Source
# ----------------------------------------------------
st.subheader("🔗 Data Source")

st.markdown("""
Financial data source: **Screener.in — Reliance Industries Ltd, Consolidated Profit & Loss section**

Note: Revenue is taken as Sales from the Profit & Loss statement.
""")
