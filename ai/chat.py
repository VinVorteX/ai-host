from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_CHAT, SYSTEM_PROMPT
from .knowledge import simple_rag_lookup, faq_system

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(question: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """
    Get response from ChatGPT with FAQ fallback first.
    
    Args:
        question: User's question
        system_prompt: System context
        
    Returns:
        str: AI response
    """
    print("🔍 Checking FAQ database...")
    
    # Try enhanced FAQ first
    faq_answer = simple_rag_lookup(question)
    if faq_answer:
        print("✅ Used enhanced FAQ match.")
        return faq_answer
    
    # Fallback to ChatGPT
    print("🤖 No FAQ match, querying ChatGPT...")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL_CHAT,
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        print(f"🤖 ChatGPT response generated.")
        return text
    except Exception as e:
        print(f"❌ ChatGPT error: {e}")
        return "I apologize, but I'm having trouble connecting right now. Please try again in a moment."

def add_new_faq(question: str, answer: str):
    """
    Add a new FAQ to the knowledge base.
    
    Args:
        question: The FAQ question
        answer: The FAQ answer
    """
    faq_system.add_faq(question, answer)

def get_faq_stats() -> dict:
    """
    Get statistics about the FAQ system.
    
    Returns:
        dict: FAQ statistics
    """
    return {
        "total_faqs": faq_system.get_faq_count(),
        "faq_questions": faq_system.list_faqs()
    }