import ollama
import re

def classify_with_llm(log_msg):
    """
    Classify the log message into:
    (1) Workflow Error, (2) Deprecation Warning, or (Unclassified).
    Category must be inside <category> </category> tags.
    """
    prompt = f"""Classify the log message into one of these categories:
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Put the category inside <category> </category> tags. 
    Log message: {log_msg}"""

    response = ollama.chat(
        model='llama3.2:3b',
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.5}
    )

    content = response["message"]["content"]

    # Extract category from <category> tags
    match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    category = "Unclassified"
    if match:
        category = match.group(1).strip()

    return category


if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."
    ))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"
    ))
    print(classify_with_llm(
        "System reboot initiated by user 12345."
    ))
