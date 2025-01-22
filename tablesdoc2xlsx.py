import os
import pandas as pd
import win32com.client as win32

def extract_tables_from_doc(file_path):
    """Extracts all tables from a .doc file and returns them as a list of DataFrames."""
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(file_path)
    tables = []
    for table in doc.Tables:
        data = []
        for r in range(1, table.Rows.Count + 1):
            row_data = []
            for c in range(1, table.Columns.Count + 1):
                try:
                    cell_text = table.Cell(r, c).Range.Text.strip().replace('\r', '').replace('\x07', '')
                except Exception:
                    cell_text = ""  # Handle inaccessible cells (e.g., merged cells)
                row_data.append(cell_text)
            data.append(row_data)
        tables.append(pd.DataFrame(data))
    doc.Close(False)
    word.Quit()
    return tables

def combine_tables_from_directories(root_dir, output_file):
    """Combines tables from .doc files in all directories (recursive) and writes them to an Excel file."""
    all_data = []

    # Traverse all directories and subdirectories
    for dir_path, _, files in os.walk(root_dir):
        # Get sorted list of .doc files in the directory
        doc_files = sorted([
            os.path.join(dir_path, f) for f in files
            if f.endswith(".doc") and not f.startswith("~$")  # Skip temporary files
        ])

        for file_path in doc_files:
            if os.path.exists(file_path):  # Ensure the file exists
                print(file_path)
                tables = extract_tables_from_doc(file_path)
                for table in tables:
                    all_data.append(table)

    # Combine all DataFrames into one giant DataFrame
    combined_df = pd.concat(all_data, ignore_index=True, axis=0)

    # Write to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False, header=False, sheet_name='Combined Tables')



if __name__ == "__main__":
    root_directory = os.getcwd()
    output_excel_file = os.path.join(root_directory, "combined_table.xlsx")

    combine_tables_from_directories(root_directory, output_excel_file)
    print(f"Tables combined and saved to {output_excel_file}")
