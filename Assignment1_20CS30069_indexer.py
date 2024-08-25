from datetime import date
import os
import sys
import nltk
import pickle
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string


# These lines download necessary NLTK date for tokenization, stop words and lemmatization
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# export inverted index to a text file.
def export_index_as_text(inverted_idx, file_name):
    with open(file_name, 'w') as output_file:   #open file in write mode
        for term, doc_list in inverted_idx.items(): #iterating over the inverted index, key (term) is token, value (doc_list) is list of document IDs
            doc_ids_str = ' '.join(map(str, doc_list)) #transforming the list of docIDs to space separated string for formatting 
            output_file.write(f"{term}: {doc_ids_str}\n") #write to the file.
    print("Text file created successfully.")


# extract all the documents from the file.
def extract_documents(file_location):
    doc_collection = {} #empty dict, to store docIDs and content.
    with open(file_location, 'r') as input_file: #open file in read mode
        content = input_file.read().strip().split('.I ') #read entire content as 1 string, remove leading and trailing whitespaces, break string into parts whenevr it finds '.I ' and remove it from resulting pieces. content[0] is empty.
        for doc_segment in content[1:]: #iterate through the broken parts from index 1 
            lines = doc_segment.split('\n') #split each part to lines.
            doc_identifier = int(lines[0].strip()) #converting the docID to int
            document_content = ""
            in_w_section = False
            for line in lines:
                if line.startswith('.W'):
                    in_w_section = True
                    continue
                if line.startswith('.X'):
                    break
                if in_w_section:
                    document_content += line.strip() + " " #concatenates all lines within .W section into a single string, strip() and adding a space " ".
            doc_collection[doc_identifier] = document_content.strip() #store docID and content in the dict
    return doc_collection

# def preprocess_text(text):
#     """
#     Preprocesses the input text by performing tokenization, removing stop words, 
#     filtering out punctuation, and applying lemmatization.

#     Parameters:
#     text (str): The raw text to be processed.

#     Returns:
#     List[str]: A list of processed tokens.
#     """
    
#     # Define a set of English stop words to filter out common words that don't contribute to meaning
#     stop_words = set(stopwords.words('english'))
    
#     # Initialize the WordNetLemmatizer, which will help in reducing words to their base or root form
#     lemmatizer = WordNetLemmatizer()
    
#     # Tokenize the text into individual words and convert them to lowercase to ensure uniformity
#     tokens = word_tokenize(text.lower())
    
#     # Process each token:
#     # - Exclude tokens that are common stop words (like 'the', 'and', etc.)
#     # - Exclude punctuation marks that do not contribute to the content
#     # - Apply lemmatization to reduce words to their base form (e.g., 'running' to 'run')
#     processed_tokens = []
#     for token in tokens:
#         if token not in stop_words and token not in string.punctuation:
#             # Perform lemmatization on the token
#             lemmatized_token = lemmatizer.lemmatize(token)
#             # Add the lemmatized token to the list of processed tokens
#             processed_tokens.append(lemmatized_token)
    
#     return processed_tokens


# preprocessing and cleaning raw data.
def clean_text(text_input):
    stop_words_set = set(stopwords.words('english')) #retrieve set of English stpwords
    lemmatizer = WordNetLemmatizer() #init the lemmatizer
    tokens = word_tokenize(text_input.lower()) #split the input lower case input text to individaul tokens/words.
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words_set and token not in string.punctuation] #lemmatize the remaining words that are not stopwords and punctuations.
    return tokens


#constructing the inverted index.
def construct_inverted_index(docs):
    inv_index = defaultdict(list)
    # used deafaultdict instead of regular {}.
    # dont need to manually check for existence of key for access or append (auto creates a key with default value)
    # can achieve a small speedup as not explicit checks.
    for doc_id, content in docs.items():
        tokens = clean_text(content) #cleans and tokenize content
        
        # print(f"Document ID: {doc_id}") # Print the first 10 tokens from this document for debugging purposes
        # print("First 10 tokens:")
        # print(tokens[:10])
        # print()
        
        for term in set(tokens):  # eliminate duplicate entries
            inv_index[term].append(doc_id) # add the docID to the list for that particular term.
    return inv_index


# persist inverted index to binary file.
def persist_inverted_index(inv_idx, file_name):
    with open(file_name, 'wb') as binary_file: #open file in write binary mode
        pickle.dump(inv_idx, binary_file) #serialise and save in binary file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Assignment1_20CS30069_indexer.py <path to CISI file>")
        sys.exit(1)

    # cisi_folder = sys.argv[1]
    # cisi_all_path = os.path.join(cisi_folder, 'CISI.ALL')
    cisi_input_file = sys.argv[1] #get the input file path.
    
    documents = extract_documents(cisi_input_file)
    
    # print("First 10 document entries:")  # Print first 10 entries
    # for i, (doc_id, text) in enumerate(documents.items()):
    #     if i >= 10:
    #         break
    #     print(f"Doc ID: {doc_id}")
    #     print(f"Text: {text}")  # Print first 200 characters of the document text
    #     print()
    
    inverted_idx = construct_inverted_index(documents)
    
    # Display the first 10 entries of the inverted index
    # print("First 10 entries of the inverted index:")
    # counter = 0
    # for term, doc_list in inverted_idx.items():
    #     if counter >= 10:
    #         break
    #     print(f"Token: {term}")
    #     print(f"Document IDs: {doc_list}")
    #     print()
    #     counter += 1
    
    persist_inverted_index(inverted_idx, 'model_queries_20CS30069.bin')
    print("\nInverted index created and saved successfully.")
    
    # export_index_as_text(inverted_idx, 'dummy_model_queries.txt')
