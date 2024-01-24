* 本範例使用 OpenAI API 建構, 因此需要先於 .env 中填寫公司所使用的 OpenAI Key
* 其次參考 hp_storage.py, 將 landscaping_insight_report_2021.pdf, landscaping_insight_report_2022.pdf, landscaping_insight_report_2023.pdf 三個檔案放入 static_file_path 中
* 執行 hp_storage.py, 將 static_file_path 中的 PDF 檔依次讀取, 各自建立 vectorstore, 並另外將三個索引資料庫合併, 另建一個 vectorstore
* hp_task.py 為 FastAPI 框架所使用的應用程式, 內含一隻 hp API, 可以透過 hp.html 輸入 prompt 並引用索引資料庫進行問答
 
* 主要的設計理念是將個別 PDF 檔文字, 表格, 圖片等建立索引, 並透過 OpenAI API 判定 prompt 與 哪一些索引內容相關, 再將相關的索引資料庫做為 retriever 使用, 以 streaming 的方式回傳對應結果至前端頁面, 並以 markdown 格式呈現. 限於近期工作繁忙, 僅完成文字部分索引, 且未依照 prompt 判定相關索引資料庫

* 本專案最大的挑戰在於索引資料庫的建立, 需要整合表格及圖片等資料. 雖然已知有相關的 langchain libraries 可以使用, 但尚未有足夠時間測試
* 其次, 由於範例資料量大, 且包含敏感性資料, 不容易測試索引的準確度, 需要花費較長時間研究資料, 進一步清理, 才能提高模型準確度
