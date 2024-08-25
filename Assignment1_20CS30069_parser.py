import os
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

#parsing the query file 
def parse_query_file(file_location):
    query_dict = {} # init empty dict, key=query id, value=query content.
    
    # same steps in Task A 
    with open(file_location, 'r') as file_handle:
        raw_content = file_handle.read().strip().split('.I ')
        for query_section in raw_content[1:]:
            lines = query_section.split('\n')
            query_id = int(lines[0].strip())
            query_content = ""
            start_w_section = False
            for line in lines:
                if line.startswith('.W'):
                    start_w_section = True
                    continue
                if start_w_section:
                    query_content += line.strip() + " "
            query_dict[query_id] = query_content.strip()
    return query_dict

#  same as Task A
def clean_and_process_text(raw_text):
    stop_words_set = set(stopwords.words('english'))
    lemmatizer_tool = WordNetLemmatizer()
    token_list = word_tokenize(raw_text.lower())
    cleaned_tokens = [lemmatizer_tool.lemmatize(token) for token in token_list if token not in stop_words_set and token not in string.punctuation]
    return ' '.join(cleaned_tokens)

def store_queries_to_file(query_data, output_filename):
    with open(output_filename, 'w') as output_file:
        # count = 0
        for query_id, content in query_data.items():
            cleaned_content = clean_and_process_text(content)
            
            # if count < 10: # Print the first 10 entries of processed_text
            #     print(f"Query ID: {qry_id}")
            #     print(f"Processed Text: {' '.join(processed_text)}")
            #     print()
            #     count += 1
            
            output_file.write(f"{query_id}\t{cleaned_content}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Assignment1_20CS30069_parser.py <path to CISI.QRY>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    
    parsed_queries = parse_query_file(input_file_path)
    
    # print("First 10 queries:") # Print the first 10 queries
    # count = 0
    # for qry_id, text in queries.items():
    #     if count >= 10:
    #         break
    #     print(f"Query ID: {qry_id}")
    #     print(f"Query Text: {text}")
    #     print()
    #     count += 1
    
    store_queries_to_file(parsed_queries, 'queries_20CS30069.txt')
    print("\nQueries processed and saved successfully.")
