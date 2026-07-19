import streamlit as st
import time
from extractor.parser import extract_text_from_pdf
from extractor.ai_extract import extract_invoice_data
from extractor.validator import validate_invoice_data
from extractor.exporter import export_to_csv
import os

# Set up the webpage
st.set_page_config(page_title="AI Invoice Extractor", page_icon="📄", layout="wide")

st.title("📄 AI Invoice Extractor")
st.markdown("Upload messy PDF invoices below. The AI will extract the data into structured JSON, validate the math, and flag any errors for human review.")

# 1. The Drag-and-Drop Uploader
uploaded_files = st.file_uploader("Upload PDF Invoices", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Process Invoices"):
        all_results = []
        
        # 2. Visual Progress Bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            status_text.text(f"Processing {file.name}...")
            
            # Step 1: Parser (Extract raw text)
            raw_text = extract_text_from_pdf(file)
            
            # Step 2: AI Brain (Extract structured data)
            extracted_data = extract_invoice_data(raw_text)
            
            # Step 3: Validator (Check the math)
            validation_result = validate_invoice_data(extracted_data)
            
            # Step 4: Save the results into a clean dictionary format
            all_results.append({
                "Filename": file.name,
                "Supplier": extracted_data.supplier_name,
                "Date": extracted_data.invoice_date,
                "Subtotal": extracted_data.subtotal,
                "Tax": extracted_data.tax_amount,
                "Total": extracted_data.total_amount,
                "Currency": extracted_data.currency,
                "Status": validation_result["status"],
                "Warnings": " | ".join(validation_result["warnings"]) if validation_result["warnings"] else "None"
            })
            
            # Update progress bar
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        status_text.text("Processing complete!")
        
        # 5. Display the results in a beautiful UI table
        st.subheader("Extraction Results")
        st.dataframe(all_results, width="stretch")
        
        # 6. CSV Export Button
        csv_path = export_to_csv(all_results)
        with open(csv_path, "rb") as file:
            st.download_button(
                label="📥 Download CSV",
                data=file,
                file_name="extracted_invoices.csv",
                mime="text/csv"
            )
