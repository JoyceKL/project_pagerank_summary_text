# File: src/pagerank.py

from data_preprocessing import get_all_sentences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import networkx as nx
import os

def build_linkage_matrix(sentences):
    # Chuyển đổi danh sách các câu thành danh sách văn bản
    sentences_text = [sentence.textvalue for sentence in sentences]

    # Vector hóa các câu sử dụng TF-IDF
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(sentences_text)

    # Tính toán ma trận tương đồng cosine
    similarity_matrix = cosine_similarity(sentence_vectors)

    # Chuyển đổi ma trận tương đồng thành ma trận liên kết dựa trên ngưỡng
    linkage_matrix = np.where(similarity_matrix > 0.5, 1, 0)  # Ngưỡng là 0.5

    return linkage_matrix
    
def normalize_linkage_matrix(linkage_matrix):
    # Tính tổng của mỗi hàng trong ma trận liên kết
    row_sums = linkage_matrix.sum(axis=1)

    # Tránh chia cho 0 bằng cách thay thế 0 bằng 1
    row_sums[row_sums == 0] = 1

    # Chia mỗi phần tử cho tổng của hàng tương ứng để chuẩn hóa
    normalized_matrix = linkage_matrix / row_sums[:, np.newaxis]

    return normalized_matrix

def apply_pagerank(normalized_matrix):
    # Tạo một đồ thị có hướng từ ma trận liên kết đã được chuẩn hóa
    G = nx.from_numpy_array(normalized_matrix, create_using=nx.DiGraph)

    # Áp dụng thuật toán PageRank
    pagerank_scores = nx.pagerank(G)
    

    return pagerank_scores

all_sentences = get_all_sentences()
linkage_matrix = build_linkage_matrix(all_sentences)  # Gọi hàm xây dựng ma trận liên kết
normalized_matrix = normalize_linkage_matrix(linkage_matrix)  # Chuẩn hóa ma trận liên kết
pagerank_scores = apply_pagerank(normalized_matrix)  # Áp dụng PageRank
# In ra điểm số PageRank để kiểm tra
# print(pagerank_scores)

# Giả sử `normalized_matrix` là ma trận liên kết đã được chuẩn hóa
pagerank_scores = apply_pagerank(normalized_matrix)

# In ra xếp hạng PageRank để kiểm tra
for idx, score in pagerank_scores.items():
    print(f"Sentence {idx} - PageRank Score: {score}")
    
def select_important_sentences(pagerank_scores, sentences, num_sentences=5):
    # Sắp xếp các câu dựa trên điểm PageRank từ cao xuống thấp
    sorted_sentences = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Lựa chọn các chỉ số của num_sentences câu hàng đầu
    selected_indices = [idx for idx, score in sorted_sentences[:num_sentences]]
    
    # Lấy các câu tương ứng từ danh sách câu gốc
    selected_sentences = [sentences[idx] for idx in selected_indices]
    
    return selected_sentences

# Giả sử pagerank_scores là một từ điển chứa điểm số PageRank của mỗi câu
# và all_sentences là danh sách các câu trong văn bản gốc

# Lựa chọn các câu quan trọng
important_sentences = select_important_sentences(pagerank_scores, all_sentences)

# In ra các câu quan trọng để xem tóm tắt
for sentence in important_sentences:
    print(sentence.textvalue)
#way_1
def summarize_text_fixed_number(sentences, pagerank_scores, num_sentences=5):
    # Sắp xếp các câu dựa trên điểm PageRank từ cao xuống thấp
    sorted_sentences = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Lựa chọn các chỉ số của num_sentences câu hàng đầu
    selected_indices = [idx for idx, score in sorted_sentences[:num_sentences]]
    
    # Lấy các câu tương ứng từ danh sách câu gốc
    summary = [sentences[idx].textvalue for idx in selected_indices]
    
    return " ".join(summary)

#way_2
def summarize_text_threshold(sentences, pagerank_scores, threshold=0.05):
    # Lọc các câu có điểm PageRank cao hơn ngưỡng
    selected_indices = [idx for idx, score in pagerank_scores.items() if score > threshold]
    
    # Lấy các câu tương ứng từ danh sách câu gốc
    summary = [sentences[idx].textvalue for idx in selected_indices]
    
    return " ".join(summary)



def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Tạo thư mục cho cả hai phương pháp
ensure_directory_exists('data/DUC_RES')
ensure_directory_exists('DUC_RES/WAY_1')
ensure_directory_exists('DUC_RES/WAY_2')



def save_summary_to_file(summary, file_name, method='fixed_number'):
    directory = 'DUC_RES/WAY_1' if method == 'fixed_number' else 'DUC_RES/WAY_2'
    file_path = os.path.join(directory, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(summary)
    print(f"Summary saved to {file_path}")

def summarize_and_save(file_path):
    # Xử lý file và rút trích câu
    sentences = extract_sentences_from_xml(file_path)
    
    # Xây dựng và chuẩn hóa ma trận liên kết
    linkage_matrix = build_linkage_matrix(sentences)
    normalized_matrix = normalize_linkage_matrix(linkage_matrix)
    
    # Áp dụng PageRank
    pagerank_scores = apply_pagerank(normalized_matrix)
    
    # Tóm tắt sử dụng cố định số lượng câu
    summary_fixed = summarize_text_fixed_number(sentences, pagerank_scores, num_sentences=5)
    file_name = os.path.basename(file_path).replace('.xml', '_fixed.txt')
    save_summary_to_file(summary_fixed, file_name, method='fixed_number')
    
    # Tóm tắt sử dụng ngưỡng
    summary_threshold = summarize_text_threshold(sentences, pagerank_scores, threshold=0.05)
    file_name = os.path.basename(file_path).replace('.xml', '_threshold.txt')
    save_summary_to_file(summary_threshold, file_name, method='threshold')

def process_all_files(directory_path):
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if file_path.endswith('.xml'):
            print(f"Processing {file_name}...")
            summarize_and_save(file_path)

# Đường dẫn đến thư mục chứa các file cần tóm tắt
xml_directory = 'DUC_TEXT/'

# Xử lý và tóm tắt tất cả các file
process_all_files(xml_directory)

# Gọi hàm process_all_files nếu script được chạy trực tiếp
if __name__ == "__main__":
    xml_directory = 'DUC_TEXT/'
    process_all_files(xml_directory)