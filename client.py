import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def print_separator():
    print("\n" + "-"*60 + "\n")

def research_topic():
    topic = input("Enter a topic to research: ")
    print("\n Running research pipeline... please wait\n")

    response = requests.post(f"{BASE_URL}/research", json={"topic": topic})

    if response.status_code == 200:
        data = response.json()
        print_separator()
        print(" RESEARCH REPORT")
        print_separator()
        print(data["report"])
        print_separator()
        print(f" Session ID: {data['session_id']}")
        print(" Report saved to reports/ folder")
        return data["session_id"]
    else:
        print(f" Error: {response.text}")
        return None

def compare_topics():
    topic_a = input("Enter Topic A: ")
    topic_b = input("Enter Topic B: ")
    print("\n Running comparison pipeline... please wait\n")

    response = requests.post(f"{BASE_URL}/compare", json={
        "topic_a": topic_a,
        "topic_b": topic_b
    })

    if response.status_code == 200:
        data = response.json()
        print_separator()
        print(f" COMPARISON REPORT: {topic_a} vs {topic_b}")
        print_separator()
        print(data["report"])
        print_separator()
        print(f" Session ID: {data['session_id']}")
        print(" Report saved to reports/ folder")
        return data["session_id"]
    else:
        print(f" Error: {response.text}")
        return None

def chat_with_report(session_id):
    if not session_id:
        session_id = input("Enter your session ID: ")

    print("\n Chat mode — ask anything about the report (type 'exit' to quit)\n")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print(" Exiting chat.")
            break

        response = requests.post(f"{BASE_URL}/chat", json={
            "session_id": session_id,
            "question": question
        })

        if response.status_code == 200:
            data = response.json()
            print(f"\n InsightForge: {data['answer']}\n")
        else:
            print(f" Error: {response.text}")

def main():
    print("="*60)
    print("         Welcome to InsightForge Client")
    print("="*60)

    session_id = None

    while True:
        print("\nWhat would you like to do?")
        print("  1. Research a topic")
        print("  2. Compare two topics")
        print("  3. Chat about a report")
        print("  4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            session_id = research_topic()
            if session_id:
                follow_up = input("\n Want to chat about this report? (y/n): ")
                if follow_up.lower() == "y":
                    chat_with_report(session_id)

        elif choice == "2":
            session_id = compare_topics()
            if session_id:
                follow_up = input("\n Want to chat about this report? (y/n): ")
                if follow_up.lower() == "y":
                    chat_with_report(session_id)

        elif choice == "3":
            chat_with_report(session_id)

        elif choice == "4":
            print("\n Goodbye!")
            break

        else:
            print(" Invalid choice. Please enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()