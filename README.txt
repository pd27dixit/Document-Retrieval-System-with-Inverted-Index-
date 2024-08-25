20CS30069

Python 3.12.4  //version of python used here

python.exe -m pip install --upgrade pip
python -m pip install --upgrade pip
pip3 install nltk

Vocabulary Length: 9646

Preprocessing Pipeline:
Tokenization: Splits text into individual words.
Stop Words Removal: Filters out common words that don’t add significant meaning (e.g., "the", "is").
Punctuation Removal: Excludes punctuation marks.
Lemmatization: Reduces words to their base or root form (e.g., "running" to "run").


python Assignment1_20CS30069_indexer.py Datasets/CISI/CISI.ALL
python Assignment1_20CS30069_parser.py Datasets/CISI/CISI.QRY
python Assignment1_20CS30069_bool.py model_queries_20CS30069.bin queries_20CS30069.txt


I have included the Datasets folder locally where my coded .py files are mentioned.

The instruction to "treat each query as an AND of the individual words" means that for each query, you need to retrieve documents that contain all the specified words from the query. This involves performing an AND operation across the lists of documents for each term in the query.
Each query consists of multiple terms (words). For instance, if a query is "Australian embassy bombing," it implies that we are interested in documents that contain all three terms: "Australian," "embassy," and "bombing."

My Merging Approach:
For merging in the Boolean retrieval process:

1. Initialize with the First Term's List: Start with the list of document IDs associated with the first term in the query.

2. Intersect with Each Subsequent Term's List: For each additional term, update the current list by intersecting it with the list of document IDs for that term. This operation ensures that only documents that contain all the query terms remain.

3. Handle Terms Not Found: If a term isn't present in the inverted index, the intersection results in an empty set, which means no documents match the query.

Why This Approach:
Efficiency: Using set intersections is fast and efficient for finding common documents.
Accuracy: Ensures only documents containing all query terms are retrieved