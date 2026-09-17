from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)

def invoke_chain(prompt_template: str, variables: dict) -> str:
    prompt = ChatPromptTemplate.from_template(prompt_template)
    messages = prompt.format_messages(**variables)
    response = model.invoke(messages)
    return response.content

def run_pipeline(topic: str) -> dict:
    # Step 1: Research
    research = invoke_chain(
        """
        You are a research assistant.
        List 5 important and recent developments about: {topic}
        Be factual and concise. Use bullet points.
        """, {"topic": topic})

    # Step 2: Summarize
    summary = invoke_chain("""
        You are a summarizer.
        Given these research points:

        {research}

        Write a concise 3-paragraph summary capturing the most important ideas.
        """, {"research": research})

    # Step 3: Critic
    critique = invoke_chain(
        """
        You are a critical analyst.
        Given this summary:

        {summary}

        Identify 3 important gaps, open questions, or counterpoints
        that were not addressed. Be specific.
        """, {"summary": summary})

    # Step 4: Report
    report = invoke_chain("""
        You are a professional report writer.
        Using the summary and critical analysis below,
        write a polished research digest with these sections:

        ## Overview
        ## Key Findings
        ## Open Questions
        ## Conclusion

        Summary:
        {summary}

        Critical Analysis:
        {critique}
        """, {"summary": summary, "critique": critique})

    return {
        "topic": topic,
        "research": research,
        "summary": summary,
        "critique": critique,
        "report": report
    }