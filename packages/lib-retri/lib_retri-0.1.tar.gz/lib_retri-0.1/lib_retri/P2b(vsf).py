#Implement the vector space model with TF-IDF weighting and cosine similarity

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import nltk
from nltk.corpus import stopwords
import numpy as np
from numpy.linalg import norm

# Training and testing datasets
train_set = ["The sky is blue.", "The sun is bright."]
test_set = ["The sun in the sky is bright."]

# Download stopwords and set them
nltk.download('stopwords')
stopWords = stopwords.words('english')

# Create CountVectorizer and TfidfTransformer
vectorizer = CountVectorizer(stop_words=stopWords)
transformer = TfidfTransformer()

# Fit and transform the training set
trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
testVectorizerArray = vectorizer.transform(test_set).toarray()

# Print vectorized results
print("Fit Vectorizer to train set:", trainVectorizerArray)
print("Transformer Vectorizer to test set:", testVectorizerArray)

# Cosine similarity function
cx = lambda a, b: round(np.inner(a, b) / (norm(a) * norm(b)), 3)

# Compute cosine similarity
for vector in trainVectorizerArray:
    print(vector)

    for testV in testVectorizerArray:
        print(testV)
        cosine = cx(vector, testV)
        print(cosine)

# Fit the TF-IDF transformer
transformer.fit(testVectorizerArray)
print()
print(transformer.transform(trainVectorizerArray).toarray())

transformer.fit(testVectorizerArray)
print()

# Transform test set using TF-IDF
tfidf = transformer.transform(testVectorizerArray)
print(tfidf.todense())
