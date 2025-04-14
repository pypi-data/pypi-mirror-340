def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(doc1, doc2):
    tfidf_matrix = TfidfVectorizer().fit_transform([doc1, doc2])
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    cosine_similarity(tfidf_matrix)[0, 1]
doc1 = "This is the first document."
doc2 = "This document is the second document."
similarity = compute_similarity(doc1, doc2)
print("Similarity between the two documents:", similarity)

    '''
    print(code)