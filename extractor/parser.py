import pdfplumber

def extract_text_from_pdf(file_obj) -> str:
    """
    Extracts all text from a PDF file object or file path.
    """
    text_content = []
    
    try:
        # pdfplumber opens a string file path or a Streamlit uploaded file object
        with pdfplumber.open(file_obj) as pdf:
            # SAFETY CHECK: Prevent processing massive 5,000-page books
            if len(pdf.pages) > 15:
                return "Error: File is too large. Maximum 15 pages allowed for invoices."
                
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                    
        return "\n".join(text_content)
        
    except Exception as e:
        return f"Error reading PDF: {e}"
