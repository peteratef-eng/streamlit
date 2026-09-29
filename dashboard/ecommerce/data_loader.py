from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "ecommerce"

# StockCodes that are not physical products (postage, fees, manual accounting
# adjustments). POST / DOT / M are already excluded upstream in the source
# notebook before net_product_sales.csv is exported; these are the ones that
# still appear in the shipped file.
NON_PRODUCT_STOCK_CODES = {"C2", "PADS", "S", "D", "BANK CHARGES", "CRUK", "AMAZONFEE"}


def _data_dir(data_dir: str | None = None) -> Path:
    return Path(data_dir or os.getenv("ECOMMERCE_DATA_DIR", DEFAULT_DATA_DIR))


@st.cache_data(show_spinner=False)
def load_monthly_net_sales(data_dir: str | None = None) -> pd.DataFrame:
    df = pd.read_csv(_data_dir(data_dir) / "monthly_net_sales.csv")
    df["period"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2) + "-01")
    df = df.sort_values("period").reset_index(drop=True)
    last_period = df["period"].max()
    df["is_partial"] = df["period"] == last_period
    return df


@st.cache_data(show_spinner=False)
def load_country_net_sales(data_dir: str | None = None) -> pd.DataFrame:
    return pd.read_csv(_data_dir(data_dir) / "country_net_sales.csv")


@st.cache_data(show_spinner=False)
def load_net_product_sales(data_dir: str | None = None) -> pd.DataFrame:
    df = pd.read_csv(_data_dir(data_dir) / "net_product_sales.csv")
    return df[~df["StockCode"].astype(str).str.upper().isin(NON_PRODUCT_STOCK_CODES)].reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_customer_summary(data_dir: str | None = None) -> pd.DataFrame:
    return pd.read_csv(_data_dir(data_dir) / "customer_summary.csv")


@st.cache_data(show_spinner=False)
def load_top_average_order_customers(data_dir: str | None = None) -> pd.DataFrame:
    return pd.read_csv(_data_dir(data_dir) / "top_average_order_customers.csv")
