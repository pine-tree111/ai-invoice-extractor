import os
from pydantic import BaseModel, Field
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Loads secret API keys from the .env file
load_dotenv()

# This is Structured Output Schema (The JSON rules) 
# The AI return data in this EXACT format.
class InvoiceData(BaseModel):
    is_valid_invoice: bool = Field(description="True if the text appears to be an invoice or receipt, False otherwise")
    supplier_name: Optional[str] = Field(None, description="Name of the company issuing the invoice")
    invoice_date: Optional[str] = Field(None, description="Date the invoice was issued (YYYY-MM-DD)")
    subtotal: Optional[float] = Field(None, description="Amount before tax")
    tax_amount: Optional[float] = Field(None, description="Total tax amount applied")
    total_amount: Optional[float] = Field(None, description="Final total amount including tax")
    currency: Optional[str] = Field(None, description="3-letter currency code (e.g. USD, GBP)")

def extract_invoice_data(raw_text: str) -> InvoiceData:
    """
    Sends the raw text to Openrouter and forces it to return our InvoiceData schema.
    """
    # If the parser gave an error, don't even bother calling the AI
    if raw_text.startswith("Error"):
        return InvoiceData(is_valid_invoice=False)
        
    try:
        # Initialize the OpenAI client and point it to OpenRouter's URL
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        
        prompt = f"""
        You are an expert data entry assistant.
        Please extract the invoice details from the following raw text.
        If the text is NOT an invoice (like a menu or book), set is_valid_invoice to false.
        
        Raw Text:
        {raw_text}
        """
        
        # asking OpenRouter for the response using OpenAI's 'parse' helper for Pydantic
        response = client.beta.chat.completions.parse(
            model='google/gemini-2.5-flash',
            messages=[
                {"role":"user", "content": prompt}
            ],
            response_format=InvoiceData,
            temperature=0.1, # 0.1 means strictly factual, absolutely no creativity
            max_tokens=1000  # Prevent OpenRouter from complaining about credit limits
        )
        
        # The library parses the JSON response directly into Pydantic object
        return response.choices[0].message.parsed
        
    except Exception as e:
        print(f"AI Extraction failed: {e}")
        return InvoiceData(is_valid_invoice=False)
