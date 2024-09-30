import requests

azure_endpoint = "https://gpt-4omniwithimages.openai.azure.com/"
api_key = "your_api_key"  # Replace with your actual API key
api_version = "2024-02-01"
model = "GPT-40-mini"

def summarize_page(page_text, previous_summary, page_number):
    """Summarize a single page's text using LLM."""
    prompt_message = (
        f"Summarize the following page (Page {page_number}) with context from the previous summary.\n\n"
        f"Previous summary: {previous_summary}\n\n"
        f"Text:\n{page_text}\n"
    )

    response = requests.post(
        f"{azure_endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an assistant that summarizes text with context."},
                {"role": "user", "content": prompt_message}
            ],
            "temperature": 0.0
        }
    )
    
    if response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content'].strip()
        return summary
    else:
        return f"Error: {response.status_code}, {response.text}"

def ask_question(document_data, question):
    """Answer a question based on the summarized content of the PDF."""
    combined_content = " ".join([page['text_summary'] for page in document_data["pages"]])
    response = requests.post(
        f"{azure_endpoint}/openai/deployments/{model}/chat/completions?api-version={api_version}",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an assistant that answers questions based on provided summaries."},
                {"role": "user", "content": f"Based on the following summaries, answer the question: {question}\n\nSummaries:\n{combined_content}"}
            ],
            "temperature": 0.0
        }
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"
