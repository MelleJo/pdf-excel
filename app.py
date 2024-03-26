import streamlit as st
import pandas as pd
from tabula import read_pdf
from io import BytesIO

def pdf_to_excel(pdf_file):
    # Read tables from PDF into a list of DataFrame objects
    dfs = read_pdf(pdf_file, pages="all", multiple_tables=True, stream=True)

    # Combine all DataFrames into a single DataFrame for simplicity
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Convert DataFrame to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False)
    output.seek(0)

    return output

st.title('PDF -> Excel')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    excel_file = pdf_to_excel(uploaded_file)
    st.download_button(label="Download Excel file",
                       data=excel_file,
                       file_name="converted.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
