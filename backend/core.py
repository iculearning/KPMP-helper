import os

from langchain.agents import initialize_agent, AgentType
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
from backend.triage import triage_biopsy
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
llm = ChatOpenAI(openai_api_key=openai_api_key, model=model, temperature=temperature)

# initialize query chain
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embedding)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class TriageInput(BaseModel):
    core1_length: float = Field()
    core1_cortex: bool = Field()
    core2_length: float = Field()
    core2_cortex: bool = Field()
    core3_length: float = Field()
    core3_cortex: bool = Field()

tools = [
    StructuredTool(
        name = "triage_biopsy",
        func = triage_biopsy,
        description = "Use this tool to triage a kidney biopsy. It produces instructions to process the biopsy bases on the length of the cores and whether renal or kidney cortext is visualized in them. If cortex is not mentioned in the text, then assume that it was not visualized",
        args_schema = TriageInput
    ), qa]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)


def run_llm(query: str):
    return agent.run(query)


if __name__ == "__main__":
    question = "At what hemoglobin drop does the patient need to be monitored?"
    result = run_llm(query=question)
    print(result)

    print(run_llm("What are the inclusion criteria for patients with CKD?"))
