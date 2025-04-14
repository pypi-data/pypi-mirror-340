#1.Inverted Index
import nltk
from nltk.corpus import stopwords
#1.Inverted Index construction algorithm
document1 = "The quick brown fox jumped over a lazy dog"
document2 = "The lazy dog slept in the sun"

nltk.download('stopwords')
stopWords = stopwords.words('english')

tokens1 = document1.lower().split()
tokens2 = document2.lower().split()
terms = list(set(tokens1 + tokens2))

inverted_index = {}
occ_num_doc1 = {}
occ_num_doc2 = {}

for term in terms:
    if term in stopWords:
        continue

    document = []
    
    if term in tokens1:
        document.append("Document 1")
        occ_num_doc1[term] = tokens1.count(term)
    
    if term in tokens2:
        document.append("Document 2")
        occ_num_doc2[term] = tokens2.count(term)

    inverted_index[term] = document

for term, documents in inverted_index.items():
    print(term, "->", end="")
    for doc in documents:
        if doc == "Document 1":
            print(f"{doc}({occ_num_doc1.get(term, 0)})", end=", ")
        else:
            print(f"{doc}({occ_num_doc2.get(term, 0)})", end=", ")
    print()
