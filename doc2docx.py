import os
import win32com.client as win32

def convert_doc_to_docx(file_path):
    """Converts a .doc file to .docx format."""
    # Create a unique instance of Word to avoid interfering with manually opened files
    word = win32.DispatchEx('Word.Application')
    word.Visible = False  # Keep Word hidden during processing
    
    try:
        doc = word.Documents.Open(file_path)
        
        # Save the file as .docx
        new_file_path = file_path + 'x'
        doc.SaveAs(new_file_path, FileFormat=16)  # 16 corresponds to wdFormatXMLDocument
        doc.Close()
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        new_file_path = None  # Indicate failure if an error occurs
    finally:
        word.Quit()  # Quit only this instance of Word
    
    return new_file_path

def batch_convert_doc_to_docx(directory):
    """Converts all .doc files in the directory (and subdirectories) to .docx."""
    for dir_path, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.doc') and not file.startswith('~$'):  # Skip temporary files
                file_path = os.path.join(dir_path, file)
                docx_file_path = file_path + 'x'  # Expected .docx file path
                
                # Skip conversion if .docx file already exists
                if os.path.exists(docx_file_path):
                    print(f"Skipped (already converted): {file_path}")
                    continue
                
                try:
                    new_file = convert_doc_to_docx(file_path)
                    if new_file:
                        print(f"Converted: {file_path} -> {new_file}")
                    else:
                        print(f"Failed to convert: {file_path}")
                except Exception as e:
                    print(f"Failed to convert {file_path}: {e}")

if __name__ == "__main__":
    root_directory = os.getcwd()  # Change this to your desired directory
    batch_convert_doc_to_docx(root_directory)
