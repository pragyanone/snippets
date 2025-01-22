import os
import win32com.client as win32

def convert_doc_to_docx(file_path):
    """Converts a .doc file to .docx format."""
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(file_path)
    
    # Save the file as .docx
    new_file_path = file_path + 'x'
    doc.SaveAs(new_file_path, FileFormat=16)  # 16 corresponds to wdFormatXMLDocument
    doc.Close()
    word.Quit()
    
    return new_file_path

def batch_convert_doc_to_docx(directory):
    """Converts all .doc files in the directory (and subdirectories) to .docx."""
    for dir_path, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.doc') and not file.startswith('~$'):  # Skip temporary files
                file_path = os.path.join(dir_path, file)
                try:
                    new_file = convert_doc_to_docx(file_path)
                    print(f"Converted: {file_path} -> {new_file}")
                except Exception as e:
                    print(f"Failed to convert {file_path}: {e}")

if __name__ == "__main__":
    root_directory = os.getcwd()  # Change this to your desired directory
    batch_convert_doc_to_docx(root_directory)
