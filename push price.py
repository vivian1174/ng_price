import os
import subprocess
from datetime import datetime
import shutil

# 你的 Excel 路徑
price_source_excel = r"\\Tpfpccpre20175\礦權管理\3_經析-市場行情\data_每日天然氣市場報告_天然氣價格資料_v20250901.xlsx"
storage_source_excel = r"C:\Users\N000189549\natural gas price bot\ngshistory.xls"
# GitHub repo 內 Excel 檔路徑
price_repo_excel = r"C:\Users\N000189549\natural gas price bot\Github\ng_price\ngpricedata.xlsx"
storage_repo_excel = r"C:\Users\N000189549\natural gas price bot\Github\ng_price\ngstoragedata.xls"
repo_path = r"C:\Users\N000189549\natural gas price bot\Github\ng_price"

# 複製 Excel 到 repo
shutil.copy2(price_source_excel, price_repo_excel)
shutil.copy2(storage_source_excel, storage_repo_excel)

# Git 操作
os.chdir(repo_path)
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"更新價格數據 {datetime.now().strftime('%Y-%m-%d')}"])
subprocess.run(["git", "push"])
