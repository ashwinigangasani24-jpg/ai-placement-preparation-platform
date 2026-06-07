import os
import sys
from dotenv import load_dotenv

# Load env before importing app modules to ensure GROQ_API_KEY is available
load_dotenv()

from app.services.ai_service import get_llm
from langchain_core.prompts import PromptTemplate

def test():
    try:
        llm = get_llm(temperature=0.1)
        prompt = PromptTemplate.from_template("Say hello")
        chain = prompt | llm
        response = chain.invoke({})
        print("Success:", response.content)
    except Exception as e:
        print("Error Type:", type(e))
        print("Error Details:", str(e))
        if hasattr(e, 'response'):
            print("Response:", e.response.text)

if __name__ == "__main__":
    test()
