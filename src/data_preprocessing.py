# File: src/data_preprocessing.py

import os
from xml.etree import ElementTree

def extract_text_from_xml(file_path):
    """Extract text content from an XML file."""
    try:
        tree = ElementTree.parse(file_path)
        root = tree.getroot()
        # Assuming the text content is within 'TEXT' tags
        # Update this XPath expression based on the actual structure of your XML files
        text = "\n".join([elem.text for elem in root.findall('.//TEXT') if elem.text])
        return text.strip()
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"

def read_data_from_directory(directory_path):
    """Read and extract text from all XML files in the specified directory."""
    extracted_texts = {}
    print(os.getcwd())
    for file_name in os.listdir(directory_path):
        if file_name.endswith(('j', 'f')):  # Adjust this condition based on your file naming convention
            file_path = os.path.join(directory_path, file_name)
            extracted_texts[file_name] = extract_text_from_xml(file_path)
    return extracted_texts

# Path to the directory containing XML files
# Update this path to match your project directory structure
xml_directory = 'data/DUC_TEXT/'

# Extract text from XML files
extracted_texts = read_data_from_directory(xml_directory)

# For demonstration, print the extracted text from the first few files
for file_name, text in list(extracted_texts.items())[:5]:
    print(f"Text from {file_name}:\n{text[:500]}\n{'-'*50}\n")  # Print the first 500 characters for brevity
