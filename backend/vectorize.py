import os

import pinecone
from langchain.document_loaders import UnstructuredMarkdownLoader, PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from backend.helper import get_key


def load_and_split_md(
    directory: str,
    splitter=RecursiveCharacterTextSplitter,
    chunk_size=400,
    chunk_overlap=50,
):
    """Loads markdown files in a directory, then splits them using tiktoken encoder. Returns split documents."""
    # obtain files in the directory
    files = os.listdir(path=directory)
    files = [f for f in files if ".md" in f]
    print(f"Located {files} in {directory}")
    # initialize text splitter
    text_splitter = splitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n"]
    )
    # read the files into documents
    raw_documents = []
    for f in files:
        doc = UnstructuredMarkdownLoader(file_path=f"{directory}/{f}").load()
        raw_documents += doc
    # split raw documents
    split_docs = text_splitter.split_documents(raw_documents)
    print(
        f"Read {len(raw_documents)} documents and splitted them into {len(split_docs)} documents"
    )
    return split_docs


def load_and_split_pdf(
    directory: str,
    splitter=RecursiveCharacterTextSplitter,
    chunk_size=400,
    chunk_overlap=50,
):
    """Loads PDF files in a directory, then splits them using tiktoken encoder. Returns split documents."""
    # obtain files in the directory
    files = os.listdir(path=directory)
    files = [f for f in files if ".pdf" in f]
    print(f"Located {files} in {directory}")
    # initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n"]
    )
    # read the files into documents
    raw_documents = PyPDFDirectoryLoader(path=directory).load()
    # split raw documents
    split_docs = text_splitter.split_documents(raw_documents)
    print(
        f"Read {len(raw_documents)} documents and splitted them into {len(split_docs)} chunks"
    )
    return split_docs


def embed_into_vectorstore(docs: list, dbpath: str, store="Chroma"):
    """Embeds a list of documents into a vector store or a database"""
    embedding = OpenAIEmbeddings(openai_api_key=get_key("OPENAI_API_KEY"))
    if store == "Chroma":
        db = Chroma.from_documents(docs, embedding, persist_directory=dbpath)
        db.persist()
    elif store == "Pinecone":
        index_name = get_key("PINCONE_INDEX_NAME")
        api_key = get_key("PINECONE_API_KEY")
        environment = get_key("PINECONE_ENV")
        pinecone.init(api_key=api_key, environment=environment)
        db = Pinecone.from_documents(docs, embedding, index_name=index_name)
    else:
        db = None
        Exception("No database store is specified")

    print(f"created database at {dbpath}")
    return db


if __name__ == "__main__":
    md_path = "../md-kpmp-oct-23"
    pdf_path = "../pdf-kpmp-oct-23"
    db_path = "../db-kpmp-oct-23"
    split_docs_md = load_and_split_md(md_path)
    split_docs_pdf = load_and_split_pdf(pdf_path)
    # db = embed_into_vectorstore(split_docs_pdf, db_path, store="Chroma")
    # db = embed_into_vectorstore(split_docs_pdf, db_path, store="Pinecone")
