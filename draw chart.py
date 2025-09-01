import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------
# 1️⃣ 讀取價格資料 (Excel 多工作表)
# ----------------------------
price_file = "https://raw.githubusercontent.com/vivian1174/ng_price/main/ngpricedata.xlsx"

# 讀取工作表 '0_Prices'，header 在第 3 列 (index=3)
df_price = pd.read_excel(price_file, sheet_name="0_Prices", header=3)

# 選取需要的欄位
df_price_selected = df_price.iloc[:, [3, 4, 7, 10, 12, 16, 20]]

# 重命名欄位
df_price_selected.columns = [
    "Date",
    "TexasGas",
    "ColumbiaGulf",
    "HH_Spot",
    "HH_Futures",
    "JKM",
    "TTF"
]

# 日期轉 datetime
df_price_selected["Date"] = pd.to_datetime(df_price_selected["Date"], errors="coerce")
df_price_selected = df_price_selected.dropna(subset=["Date"])
price_cols = ["TexasGas","ColumbiaGulf","HH_Spot","HH_Futures","JKM","TTF"]
df_price_selected[price_cols] = df_price_selected[price_cols].apply(pd.to_numeric, errors="coerce")

# ----------------------------
# 2️⃣ 讀取庫存資料 (ngihistory.xls)
# ----------------------------
storage_file = r"https://raw.githubusercontent.com/vivian1174/ng_price/main/ngstoragedata.xlsx"

# 讀取 HTML report history，header 第 8 列
df_storage = pd.read_excel(storage_file, sheet_name="html_report_history", header=8)

# 選取日期(A)與庫存量(J)
df_storage_selected = df_storage.iloc[:, [0, 9]]
df_storage_selected.columns = ["Date", "Storage"]

# 日期轉 datetime
df_storage_selected["Date"] = pd.to_datetime(df_storage_selected["Date"], errors="coerce")
df_storage_selected = df_storage_selected.dropna(subset=["Date"])

# ----------------------------
# 3️⃣ Streamlit 繪圖
# ----------------------------
st.title("天然氣價格與庫存 Dashboard")

# 折線圖：各地區價格 (Altair)
st.subheader("價格折線圖 (USD/MMBtu)")
df_price_melted = df_price_selected.melt(id_vars="Date", var_name="Region", value_name="Price")

chart_price = (
    alt.Chart(df_price_melted)
    .mark_line()
    .encode(
        x=alt.X("Date:T", title="月份 (YYYY-MM)", axis=alt.Axis(format="%Y-%m")),
        y=alt.Y("Price:Q", title="價格 (USD/MMBtu)"),
        color="Region:N"
    )
    .properties(width=800, height=400)
)

st.altair_chart(chart_price, use_container_width=True)

# 柱狀圖：庫存量 (Altair)
st.subheader("庫存量柱狀圖 (Bcf)")
chart_storage = (
    alt.Chart(df_storage_selected)
    .mark_bar()
    .encode(
        x=alt.X("Date:T", title="月份 (YYYY-MM)", axis=alt.Axis(format="%Y-%m")),
        y=alt.Y("Storage:Q", title="庫存量 (Bcf)")
    )
    .properties(width=800, height=400)
)

st.altair_chart(chart_storage, use_container_width=True)

# ----------------------------
# 4️⃣ 可選：顯示原始數據
# ----------------------------
if st.checkbox("顯示原始價格資料"):
    st.dataframe(df_price_selected)

if st.checkbox("顯示原始庫存資料"):
    st.dataframe(df_storage_selected)
