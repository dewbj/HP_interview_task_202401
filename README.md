* 本範例使用 OpenAI API 建構, 因此需要先於 .env 中填寫公司所使用的 OpenAI Key
* 其次參考 hp_storage.py，將 landscaping_insight_report_2021.pdf, landscaping_insight_report_2022.pdf, landscaping_insight_report_2023.pdf 三個檔案放入 static_file_path 中
* 執行 hp_storage.py，將 static_file_path 中的 PDF 檔依次讀取，各自建立 vectorstore，並另外將三個索引資料庫合併，另建一個 vectorstore
* hp_task.py 為 FastAPI 框架所使用的應用程式，內含一隻 hp API，可以透過 hp.html 輸入 prompt 並引用索引資料庫進行問答
