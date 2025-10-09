from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_CHAT, SYSTEM_PROMPT, MAX_TOKENS, TEMPERATURE, HTTP_TIMEOUT, MAX_RETRIES
from .knowledge import simple_rag_lookup, faq_system

client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=HTTP_TIMEOUT,
    max_retries=MAX_RETRIES
)


def ask_chatgpt_stream(question: str, system_prompt: str = SYSTEM_PROMPT):
    """
    Queries the knowledge base first, falling back to a streaming OpenAI call if no match is found.

    This function is a generator that yields response chunks as they are received.
    
    Args:
        question: The user's question.
        system_prompt: The system prompt to provide context to the model.
        
    Yields:
        str: Chunks of the generated response.
    """
    print("INFO: Checking knowledge base...")
    
    faq_answer = simple_rag_lookup(question)
    if faq_answer:
        print("INFO: Found a match in the knowledge base.")
        yield faq_answer
        return

    print("INFO: No match found. Querying OpenAI model...")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    try:
        stream = client.chat.completions.create(
            model=OPENAI_MODEL_CHAT,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=True
        )
        
        print("INFO: OpenAI stream initiated...")
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        print(f"ERROR: An exception occurred with the OpenAI API: {e}")
        yield "An error occurred while connecting to the service. Please try again shortly."

def add_new_faq(question: str, answer: str):
    """
    Adds a new question-answer pair to the knowledge base.
    
    Args:
        question: The question to add.
        answer: The corresponding answer.
    """
    faq_system.add_faq(question, answer)

def get_faq_stats() -> dict:
    """
    Retrieves statistics about the knowledge base.
    
    Returns:
        A dictionary containing statistics.
    """
    return {
        "total_faqs": faq_system.get_faq_count(),
        "faq_questions": faq_system.list_faqs()
    }