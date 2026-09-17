from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
parser = StrOutputParser()

# Research both topics first 
prompt_research = ChatPromptTemplate.from_template(
    """
    You are a research assistant.
    List 5 important facts and development about: {topic}
    Be factual and concise. Use bullet points.
    """
)

# summarise both topics
prompt_summary = ChatPromptTemplate.from_template(
    """
    You are a summarizer.
    Given these research points about {topic}:

    {research}

    Write a concise 2-paragraph summary of the most important ideas.
    """
)

# Compare both topics 
prompt_compare = ChatPromptTemplate.from_template(
    """
    You are an expert analyst.
    Compare these two topics based on their summaries below.

    Topic A: {topic_a}
    Summary A:
    {summary_a}

    Topic B: {topic_b}
    Summary B:
    {summary_b}

    Provide a structured comparison covering:
    - Key similarities
    - Key differences
    - Strengths of each
    - Weaknesses of each
    - Which is better suited for what use case
    """
)

# Final report
prompt_report = ChatPromptTemplate.from_template(
    """
    You are a professional report writer.
    Using the summaries and comparison analysis below,
    write a polished comparison digest with these sections:

    ## Overview
    ## {topic_a} — Key Strengths
    ## {topic_b} — Key Strengths
    ## Head to Head Comparison
    ## Verdict — Which Should You Choose?
    ## Conclusion

    Topic A Summary: {summary_a}
    Topic B Summary: {summary_b}
    Comparison Analysis: {comparison}
    """

)

# Chains 
chain_research = prompt_research | model | parser
chain_summary = prompt_summary | model | parser
chain_compare = prompt_compare | model | parser
chain_report = prompt_report | model | parser

# pipeline 
def run_comparison(topic_a: str, topic_b: str) -> dict:
    research_a = chain_research.invoke({"topic": topic_a})
    research_b = chain_research.invoke({"topic": topic_b})

    summary_a = chain_summary.invoke({"topic": topic_a, "research": research_a})
    summary_b = chain_summary.invoke({"topic": topic_b, "research": research_b})

    comparison = chain_compare.invoke({
        "topic_a": topic_a,
        "topic_b": topic_b,
        "summary_a": summary_a,
        "summary_b": summary_b
    })

    report = chain_report.invoke({
        "topic_a": topic_a,
        "topic_b": topic_b,
        "summary_a": summary_a,
        "summary_b": summary_b,
        "comparison": comparison
    })

    return {
        "topic_a": topic_a,
        "topic_b": topic_b,
        "research_a": research_a,
        "research_b": research_b,
        "summary_a": summary_a,
        "summary_b": summary_b,
        "comparison": comparison,
        "report": report
    }



    



