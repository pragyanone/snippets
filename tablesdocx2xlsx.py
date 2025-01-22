import os
from docx import Document
import pandas as pd

def extract_tables_from_docx(file_path):
    """Extracts all tables from a .docx file and returns them as a list of DataFrames."""
    doc = Document(file_path)
    tables = []
    for table in doc.tables:
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        tables.append(pd.DataFrame(data))
    return tables

def combine_tables_from_directories(root_dir, output_file):
    """Combines tables from .docx files in ne
    sted directories and writes them to an Excel file."""
    all_data = []

    # Traverse all directories and subdirectories
    for root, _, files in os.walk(root_dir):
        for file_name in sorted(files):
            if file_name.endswith(".docx") and not file_name.startswith("~$"):
                file_path = os.path.join(root, file_name)
                print(file_path)
                try:
                    tables = extract_tables_from_docx(file_path)
                    for table in tables:
                        all_data.append(table)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Combine all DataFrames into one DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True, axis=0)
    else:
        combined_df = pd.DataFrame()  # Empty DataFrame if no tables found

    # Write to Excel
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False, header=False, sheet_name='Combined Tables')

if __name__ == "__main__":
    root_directory = os.getcwd()  # Replace with the root directory path
    output_excel_file = os.path.join(root_directory, "outputtable.xlsx")  # Replace with the desired output path

    combine_tables_from_directories(root_directory, output_excel_file)
    print(f"Tables combined and saved to {output_excel_file}")
