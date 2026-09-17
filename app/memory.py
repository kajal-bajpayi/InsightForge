from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
parser = StrOutputParser()

# prompt with memory slot 
prompt = ChatPromptTemplate.from_messages([
    ("system", """"You are a research assistant for InsightForge.
    You have access to research report on the topic below.
    Answer follow up questions based on this report only. 
    
    Report:
    {report}"""), 
    MessagesPlaceholder(variable_name="history"),
    ("human","{question}")
])

chain = prompt | model | parser

# in memory conversation store 
sessions = {}

def start_session(session_id: str, report:str):
    sessions[session_id] = {
        "report": report,
        "history": []
    }

    return {"session_id": session_id, "status":"session_started"}


def chat(session_id: str, question: str) -> str:
    if session_id not in sessions:
        return "Session not found. Please start a new session first"

    session = sessions[session_id]

    # run chain with history 
    response = chain.invoke({
        "report": session["report"],
        "history": session["history"],
        "question": question
    })

    # saving history 
    session["history"].append(HumanMessage(content=question))
    session["history"].append(AIMessage(content=response))

    return response




