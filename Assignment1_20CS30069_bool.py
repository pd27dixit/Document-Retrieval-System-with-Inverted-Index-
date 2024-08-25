import os
import sys
import pickle

def load_index_from_file(file_path):
    with open(file_path, 'rb') as file_handle:
        return pickle.load(file_handle)

def load_query_data(file_path):
    query_data = {}
    with open(file_path, 'r') as file_handle:
        for line in file_handle:
            components = line.strip().split('\t')
            query_id = int(components[0])
            query_terms = components[1].split()
            query_data[query_id] = query_terms
    return query_data

def perform_boolean_search(index_data, query_data):
    search_results = {}
    for query_id, terms in query_data.items():
        if not terms:
            search_results[query_id] = []
            continue

        # Initialize with the document IDs of the first term
        if terms[0] in index_data:
            document_ids = set(index_data[terms[0]])
        else:
            document_ids = set()

        # Execute AND operation with the document IDs of the remaining terms
        for term in terms[1:]:
            if term in index_data:
                document_ids &= set(index_data[term])
            else:
                document_ids = set()
                break

        search_results[query_id] = sorted(document_ids)
    return search_results

def write_results_to_file(result_data, output_file_path):
    with open(output_file_path, 'w') as file_handle:
        for query_id, doc_ids in result_data.items():
            doc_ids_str = ' '.join(map(str, doc_ids))
            file_handle.write(f"{query_id} : {doc_ids_str}\n")
            
def calculate_vocabulary_length(index_data):
    unique_terms = set(index_data.keys())
    return len(unique_terms)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Assignment1_20CS30069_bool.py <path to index file> <path to query file>")
        sys.exit(1)

    index_file_path = sys.argv[1]
    query_file_path = sys.argv[2]

    index_data = load_index_from_file(index_file_path)
    
    vocabulary_length = calculate_vocabulary_length(index_data)
    print(f"Vocabulary Length: {vocabulary_length}")
    
    query_data = load_query_data(query_file_path)
    search_results = perform_boolean_search(index_data, query_data)
    write_results_to_file(search_results, 'Assignment1_20CS30069_results.txt')
    print("\nBoolean search completed and results written successfully.")
