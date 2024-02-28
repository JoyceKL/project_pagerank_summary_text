# File: src/data_preprocessing.py

import os
import re
from lxml import etree

class Sentence:
    def __init__(self, docid, num, wdcount, textvalue):
        self.docid = docid
        self.num = num
        self.wdcount = wdcount
        self.textvalue = textvalue

    def clean_text(self):
        # Loại bỏ dấu câu
        self.textvalue = re.sub(r'[^\w\s]', '', self.textvalue)
        # Loại bỏ khoảng trắng thừa
        self.textvalue = re.sub(r'\s+', ' ', self.textvalue).strip()

def extract_sentences_from_xml(file_path):
    sentences = []
    try:
        parser = etree.XMLParser(recover=True)  # Sử dụng parser linh hoạt để xử lý XML không hoàn chỉnh
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        print(f"Root element: {root.tag}")
        if root.nsmap:
            print(f"Namespaces: {root.nsmap}")
        
        # Kiểm tra nếu phần tử gốc là tag <s>
        if root.tag == 's':
            docid = root.attrib.get('docid', '')
            num = root.attrib.get('num', '')
            wdcount = root.attrib.get('wdcount', '')
            textvalue = ''.join(root.itertext()).strip()

            # Tạo và làm sạch đối tượng Sentence từ phần tử gốc
            sentence = Sentence(docid, num, wdcount, textvalue)
            sentence.clean_text()
            sentences.append(sentence)
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    return sentences
    #     # Tìm tất cả các tag <s> trong tệp XML
    #     s_tags = root.findall('.//s')  # Định nghĩa s_tags ở đây
    #     print(f"Found {len(s_tags)} <s> tags in {file_path}")  # In số lượng tag <s> tìm thấy
    #     for s in root.findall('.//s'):
    #         print(f"Found tag <s> with docid={s.attrib.get('docid')}, num={s.attrib.get('num')}, wdcount={s.attrib.get('wdcount')}")
    #         docid = s.attrib.get('docid', '')
    #         num = s.attrib.get('num', '')
    #         wdcount = s.attrib.get('wdcount', '')
    #         textvalue = ''.join(s.itertext()).strip()
    #         print(f"Textvalue: {textvalue}")

    #         sentence = Sentence(docid, num, wdcount, textvalue)
    #         print(f"Created Sentence: docid={sentence.docid}, num={sentence.num}, wdcount={sentence.wdcount}, text={sentence.textvalue}")
    #         sentence.clean_text()  # Làm sạch văn bản của câu
    #         sentences.append(sentence)  # Thêm câu đã làm sạch vào danh sách
    # except Exception as e:
    #     print(f"Error processing {file_path}: {str(e)}")
    # return sentences

def read_and_process_xml_directory(directory_path):
    all_sentences = []
    for file_name in os.listdir(directory_path):
        print("================OPEN FILE ===================")
        file_path = os.path.join(directory_path, file_name)
        print(f"Processing file: {file_path}")  # In đường dẫn tệp đang được xử lý
        sentences = extract_sentences_from_xml(file_path)
        all_sentences.extend(sentences)  # Tổng hợp tất cả câu từ tất cả các tệp vào một danh sách
        print(f"Processed {len(sentences)} sentences from {file_name}")  # In số lượng câu rút trích từ mỗi tệp
    print(f"Total sentences extracted: {len(all_sentences)}")  # In tổng số câu rút trích
    return all_sentences

def get_all_sentences():
    # Đường dẫn đến thư mục chứa tệp XML
    xml_directory = 'data/DUC_TEXT/'

    # Xử lý tất cả tệp XML và rút trích câu
    all_sentences = read_and_process_xml_directory(xml_directory)

    return all_sentences

# In ra thông tin của một số câu để kiểm tra
# for sentence in all_sentences[:10]:  # In ra 10 câu đầu tiên
#     print(f"DocID: {sentence.docid}, Num: {sentence.num}, Word Count: {sentence.wdcount}, Text: {sentence.textvalue}\n")
