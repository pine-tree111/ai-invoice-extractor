from .ai_extract import InvoiceData

def validate_invoice_data(data: InvoiceData) -> dict:
    """
    Checks the math and logic of the extracted data.
    This is the "Hallucination Moat" that protects the business.
    """
    # 1. Did the AI say this wasn't even an invoice
    if not data.is_valid_invoice:
        return {"status": "rejected", "warnings": ["Document is not recognized as an invoice"]}
        
    warnings = []
    
    # 2. Check if critical data missing
    if data.total_amount is None:
        warnings.append("Missing total amount")
        
    # 3. Check the AI's math
    if data.subtotal is not None and data.tax_amount is not None and data.total_amount is not None:
        # Using round() because computers sometimes do weird decimal math (like 10.0 + 2.0 = 12.000000001)
        calculated_total = round(data.subtotal + data.tax_amount, 2)
        
        if calculated_total != round(data.total_amount, 2):
            warnings.append(f"Math mismatch: Subtotal + Tax ({calculated_total}) does not equal the Total ({data.total_amount})")
            
    # 4. Final Verdict
    if len(warnings) > 0:
        return {"status": "needs_review", "warnings": warnings}
        
    return {"status": "approved", "warnings": []}
