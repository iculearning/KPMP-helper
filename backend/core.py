import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone

from helper import get_key

# initialize pinecone vector store
index_name = get_key("PINCONE_INDEX_NAME")
api_key = get_key("PINECONE_API_KEY")
environment = get_key("PINECONE_ENV")
pinecone.init(api_key=api_key, environment=environment)

# initialize OpenAI chat llm
openai_api_key = get_key("OPENAI_API_KEY")
model = "gpt-3.5-turbo"
temperature = 0
max_tokens = 4000


def run_llm(query: str):
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embedding)
    llm = ChatOpenAI(openai_api_key=openai_api_key, model=model, temperature=temperature)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    return qa.run(query)


if __name__ == "__main__":
    question = "At what hemoglobin drop does the patient need to be monitored?"
    result = run_llm(query=question)
    print(result)

    print(run_llm("What are the inclusion criteria for patients with CKD?"))
