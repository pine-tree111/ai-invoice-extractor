import pandas as pd
from typing import List
from .ai_extract import InvoiceData

def export_to_csv(extracted_results: List[dict], output_path: str = "sample_output/extracted_data.csv"):
    """
    Takes the clean data and saves it to a CSV file.
    """
    # pandas takes the list of dictionaries and turns it into a perfect spreadsheet instantly
    df = pd.DataFrame(extracted_results)
    
    # Save it to a file, without the ugly index numbers on the left side
    df.to_csv(output_path, index=False)
    
    return output_path
