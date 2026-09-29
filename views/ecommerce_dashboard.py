from __future__ import annotations

import html

import streamlit as st

from dashboard.ecommerce import charts
from dashboard.ecommerce.data_loader import (
    load_country_net_sales,
    load_customer_summary,
    load_monthly_net_sales,
    load_net_product_sales,
    load_top_average_order_customers,
)
from ui.components import app_header, chart_card
from ui.theme import current_theme


theme = current_theme()

app_header(
    "E-Commerce Sales Analysis",
    "Net Sales, Products, and Customer Value",
    "Sales performance for a UK-based online retailer, built from cleaned and reconciled net-sales data "
    "(cancellations and returns removed from revenue).",
    "dashboard",
)

try:
    monthly = load_monthly_net_sales()
    countries = load_country_net_sales()
    products = load_net_product_sales()
    customers = load_customer_summary()
    top_avg_customers = load_top_average_order_customers()
except FileNotFoundError:
    st.error("E-commerce dataset unavailable.")
    st.stop()

total_net_sales = float(monthly["TotalPrice"].sum())
customer_net_sales = float(customers["net_sales"].sum())


def kpi_row(items: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value, note) in zip(columns, items):
        with column:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{html.escape(label)}</div>
                    <div class="kpi-value">{html.escape(value)}</div>
                    <div class="kpi-note">{html.escape(note)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


kpi_row(
    [
        ("Net Sales", f"£{total_net_sales:,.0f}", "Full dataset, cancellations & returns removed"),
        ("Customers", f"{len(customers):,}", "Distinct customers with a linked order"),
        ("Products", f"{len(products):,}", "Physical products, non-product codes excluded"),
        ("Countries", f"{len(countries):,}", "Distinct shipping countries"),
    ]
)

st.markdown(
    f"""
    <div class="dashboard-methodology" style="margin-top: 1.2rem;">
        <p><strong>From the full analysis (541,909 transactions):</strong>
        gross sales were approximately £10.64M; cancellations and returns reduced revenue by
        approximately £894K (8.4%), leaving £{total_net_sales:,.0f} in net sales. The United Kingdom
        accounted for approximately 84% of net sales.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Monthly Net Sales Trend")
with st.container(key="ecommerce_chart_monthly_trend"):
    chart_card(
        "Net Sales by Month",
        "December 2010 through December 2011. The final month is marked as partial — the source data ends "
        "on December 9, 2011, so it should not be read as a decline.",
    )
    st.plotly_chart(
        charts.monthly_net_sales_trend(monthly, theme),
        width="stretch",
        key="ecommerce_monthly_trend",
        config={"displayModeBar": False, "responsive": True},
    )

st.subheader("Top Countries by Net Sales")
with st.container(key="ecommerce_chart_countries"):
    chart_card("Top 10 Countries", "Ranked by net sales across the full dataset.")
    top_countries = countries.sort_values("TotalPrice", ascending=False).head(10)
    st.plotly_chart(
        charts.bar(top_countries, "Country", "TotalPrice", "Net sales", theme, value_prefix="£"),
        width="stretch",
        key="ecommerce_top_countries",
        config={"displayModeBar": False, "responsive": True},
    )

st.subheader("Top Products by Net Sales")
with st.container(key="ecommerce_chart_products"):
    chart_card(
        "Top 10 Products",
        "Non-product codes (postage, fees, and manual accounting adjustments such as CARRIAGE, "
        "BANK CHARGES, AMAZON FEE, and discounts) were excluded.",
    )
    top_products = products.sort_values("TotalPrice", ascending=False).head(10)
    st.plotly_chart(
        charts.bar(top_products, "Description", "TotalPrice", "Net sales", theme, value_prefix="£"),
        width="stretch",
        key="ecommerce_top_products",
        config={"displayModeBar": False, "responsive": True},
    )

st.subheader("Top Customers")
customer_choice = st.radio(
    "Customer chart",
    ["By Net Sales", "By Average Order Value"],
    horizontal=True,
    label_visibility="collapsed",
    key="ecommerce_customer_chart_choice",
)
st.caption(
    f"Customer-level totals cover £{customer_net_sales:,.0f} in net sales — lower than the "
    f"£{total_net_sales:,.0f} sitewide total because roughly 25% of transactions have no linked "
    "CustomerID (guest or unlinked orders) and are excluded from customer analysis."
)
if customer_choice == "By Net Sales":
    with st.container(key="ecommerce_chart_customers_net"):
        chart_card("Top 10 Customers by Net Sales", "Highest total spend per customer.")
        top_customers = customers.sort_values("net_sales", ascending=False).head(10).copy()
        top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)
        st.plotly_chart(
            charts.bar(top_customers, "CustomerID", "net_sales", "Net sales", theme, value_prefix="£"),
            width="stretch",
            key="ecommerce_top_customers_net",
            config={"displayModeBar": False, "responsive": True},
        )
else:
    with st.container(key="ecommerce_chart_customers_avg_order"):
        chart_card("Top 10 Customers by Average Order Value", "Customers with 5+ orders.")
        top_avg = top_avg_customers.sort_values("avg_order_value", ascending=False).head(10).copy()
        top_avg["CustomerID"] = top_avg["CustomerID"].astype(str)
        st.plotly_chart(
            charts.bar(top_avg, "CustomerID", "avg_order_value", "Average order value", theme, value_prefix="£"),
            width="stretch",
            key="ecommerce_top_customers_avg_order",
            config={"displayModeBar": False, "responsive": True},
        )

st.markdown(
    '<div class="dashboard-compact-footer">Built by Peter Atef &middot; '
    '<a href="https://github.com/peteratef-eng/ecommerce-sales-analysis" rel="noopener noreferrer">GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)
