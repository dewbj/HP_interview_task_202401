import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

embeddings = OpenAIEmbeddings()
static_file_path = "./static/files/"
index_db_path = "./index/"

def create_vectorstore(file_name):
    file_path = static_file_path + file_name
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(docs, embeddings)
    db_path = index_db_path + file_name.replace(".pdf", "")
    db.save_local(db_path)

def db_retriever(file_name, prompt):
    db_path = index_db_path + file_name.replace(".pdf", "")
    db = FAISS.load_local(db_path, embeddings)
    retriever = db.as_retriever()
    retrieved_docs = retriever.invoke(
        prompt
    )
    question = prompt + " according to: " + retrieved_docs[0].page_content

    print(db)

def merge_vectorstore(db_name, index_list):

    db = FAISS.from_texts([""], embeddings)
    db_path = index_db_path + db_name
    db.save_local(db_path)    

    for index in index_list:

        index_path = index_db_path + index
        db = FAISS.load_local(db_path, embeddings)
        db_index = FAISS.load_local(index_path, embeddings)
        db.merge_from(db_index)
        db.save_local(db_path)

index_list = []

for year in range(2021, 2024):
    file_name = "landscaping_insight_report_" + str(year) + ".pdf"
    index_list.append(file_name.replace(".pdf", ""))
    create_vectorstore(file_name)

merge_vectorstore("landscaping_insight_report", index_list)
