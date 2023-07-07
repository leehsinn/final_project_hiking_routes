# Final project 健行筆記步道客製化篩選介面

此專案旨在設計一個客製化篩選步道的介面，因為作者認為現有網頁篩選條件有限，無法完全符合個人需求。

## 介面設計與檔案說明

- 使用動態爬蟲 Selenium 抓取網頁資料：[selenium_hiking_0602.ipynb](selenium_hiking_0602.ipynb)
- 資料ETL，儲存成 pandas 格式：[hiking_with_pandas.ipynb](hiking_with_pandas.ipynb)
- 製作 GUI 介面，串接 Python：
  - GUI 介面檔案：[2ndmain.ui](2ndmain.ui) 轉成 [twomainwindow.py](twomainwindow.py)
  - 主要操作介面：[get_final.py](get_final.py) (import twomainwindow.py)
  
## 使用說明

請參考 `get_final.py` 中的 GUI 主程式碼來執行此專案。
