import streamlit as st
import pandas as pd

# ----------------------------
# 1️⃣ 讀取價格資料 (Excel 多工作表)
# ----------------------------
price_file = "https://raw.githubusercontent.com/vivian1174/ng_price/main/ngpricedata.xlsx"

# 讀取工作表 '0_Prices'，header 在第 3 列 (index=3)
df_price = pd.read_excel(price_file, sheet_name="0_Prices", header=4)

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

# 日期轉 datetime 並設為 index
df_price_selected["Date"] = pd.to_datetime(df_price_selected["Date"])
df_price_selected.set_index("Date", inplace=True)

# ----------------------------
# 2️⃣ 讀取庫存資料 (ngihistory.xls)
# ----------------------------
storage_file = r"https://raw.githubusercontent.com/vivian1174/ng_price/main/ngstoragedata.xlsx"

# 讀取 HTML report history，header 第 0 列
df_storage = pd.read_excel(storage_file, sheet_name="html_report_history", header=8)

# 選取日期(A)與庫存量(J)
df_storage_selected = df_storage.iloc[:, [0, 9]]
df_storage_selected.columns = ["Date", "Storage"]

# 日期轉 datetime 並設為 index
df_storage_selected["Date"] = pd.to_datetime(df_storage_selected["Date"])
df_storage_selected.set_index("Date", inplace=True)

# ----------------------------
# 3️⃣ Streamlit 繪圖
# ----------------------------
st.title("天然氣價格與庫存 Dashboard")

# 折線圖：各地區價格
st.subheader("價格折線圖")
st.line_chart(df_price_selected)

# 柱狀圖：庫存量
st.subheader("庫存量柱狀圖")
st.bar_chart(df_storage_selected)

# ----------------------------
# 4️⃣ 可選：顯示原始數據
# ----------------------------
if st.checkbox("顯示原始價格資料"):
    st.dataframe(df_price_selected)

if st.checkbox("顯示原始庫存資料"):
    st.dataframe(df_storage_selected)
