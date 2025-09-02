import streamlit as st
import pandas as pd
import altair as alt
st.cache_data.clear()

# ----------------------------
# 1️⃣ 讀取價格資料 (Excel 多工作表)
# ----------------------------
price_file = "https://raw.githubusercontent.com/vivian1174/ng_price/main/ngpricedata.xlsx"

df_price = pd.read_excel(price_file, sheet_name="0_Prices", header=3)
df_price_selected = df_price.iloc[:, [3, 4, 7, 10, 12, 16, 20]]
df_price_selected.columns = [
    "Date", "TexasGas", "ColumbiaGulf", "HH_Spot", "HH_Futures", "JKM", "TTF"
]
df_price_selected["Date"] = pd.to_datetime(df_price_selected["Date"], errors="coerce")
df_price_selected = df_price_selected.dropna(subset=["Date"])
price_cols = ["TexasGas","ColumbiaGulf","HH_Spot","HH_Futures","JKM","TTF"]
df_price_selected[price_cols] = df_price_selected[price_cols].apply(pd.to_numeric, errors="coerce")

# ----------------------------
# 2️⃣ 讀取庫存資料
# ----------------------------
storage_file = r"https://raw.githubusercontent.com/vivian1174/ng_price/main/ngstoragedata.xlsx"
df_storage = pd.read_excel(storage_file, sheet_name="html_report_history", header=8)
df_storage_selected = df_storage.iloc[:, [0, 9]]
df_storage_selected.columns = ["Date", "Storage"]
df_storage_selected["Date"] = pd.to_datetime(df_storage_selected["Date"], errors="coerce")
df_storage_selected = df_storage_selected.dropna(subset=["Date"])

# ----------------------------
# 3️⃣ Streamlit 繪圖
# ----------------------------
st.title("天然氣價格與庫存 Dashboard")

# 折線圖：各地區價格 (Altair)
st.subheader("價格折線圖 (USD/MMBtu)")
df_price_melted = df_price_selected.melt(id_vars="Date", var_name="Region", value_name="Price")

# 建立 hover 選擇器（最近日期）
hover = alt.selection_single(
    fields=["Date"],
    nearest=True,
    on="mouseover",
    empty="none",
    clear="mouseout"
)

# 折線圖
line = (
    alt.Chart(df_price_melted)
    .mark_line()
    .encode(
        x=alt.X("Date:T", title="月份 (YYYY-MM)", axis=alt.Axis(format="%Y-%m")),
        y=alt.Y("Price:Q", title="價格 (USD/MMBtu)"),
        color=alt.Color("Region:N", legend=alt.Legend(orient="bottom"))
    )
)

# 選擇器層（透明點，讓整個 x 軸可被 hover）
selectors = (
    alt.Chart(df_price_melted)
    .mark_point(opacity=0)
    .encode(x="Date:T")
    .add_selection(hover)
)

# hover 顯示的點
points = (
    alt.Chart(df_price_melted)
    .mark_point(size=60)
    .encode(
        x="Date:T",
        y="Price:Q",
        color="Region:N",
    )
    .transform_filter(hover)
)

# 垂直輔助線
rule = (
    alt.Chart(df_price_melted)
    .transform_pivot(
        "Region",        # 把 Region 欄位展開成多欄
        value="Price",
        groupby=["Date"]
    )
    .mark_rule(color="Lavender")
    .encode(
        x="Date:T",
        tooltip=[
            alt.Tooltip("Date:T", title="日期"),
            alt.Tooltip("HH_Spot:Q", title="HH Spot"),
            alt.Tooltip("HH_Futures:Q", title="HH Futures"),
            alt.Tooltip("JKM:Q", title="JKM"),
            alt.Tooltip("TTF:Q", title="TTF"),
        ]
    )
    .transform_filter(hover)
)

# 合併圖層
chart_price = (
    alt.layer(line, selectors, points, rule)
    .resolve_tooltip(independent=True)  # 👈 關鍵
    .properties(width=800, height=400)
    .interactive()
)

st.altair_chart(chart_price, use_container_width=True)
# 柱狀圖：庫存量 (Altair)
st.subheader("庫存量柱狀圖 (Bcf)")
chart_storage = (
    alt.Chart(df_storage_selected)
    .mark_bar()
    .encode(
        x=alt.X("Date:T", title="月份 (YYYY-MM)", axis=alt.Axis(format="%Y-%m")),
        y=alt.Y("Storage:Q", title="庫存量 (Bcf)"),
        tooltip=["Date:T", "Storage:Q"]
    )
    .properties(width=800, height=400)
    .interactive()
)
st.altair_chart(chart_storage, use_container_width=True)

# ----------------------------
# 4️⃣ 可選：顯示原始數據
# ----------------------------
if st.checkbox("顯示原始價格資料"):
    st.dataframe(df_price_selected)

if st.checkbox("顯示原始庫存資料"):
    st.dataframe(df_storage_selected)
