#Text Categorization, Naive Bayes
import numpy as np
import re

class NaiveBayesClassifier:
    def __init__(self):
        self.vocab = []
        self.positive_counts = None
        self.negative_counts = None
        self.positive_prior = 0
        self.negative_prior = 0

    def preprocess_review(self, review):
        tokens = re.findall(r'\b\w+\b', review.lower())
        return tokens

    def vectorize_review(self, review):
        vector = np.zeros(len(self.vocab))
        for word in review:
            if word in self.vocab:
                vector[self.vocab.index(word)] += 1
        return vector

    def train(self, X_train, Y_train):
        all_tokens = []
        for review in X_train:
            tokens = self.preprocess_review(review)
            all_tokens.extend(tokens)
        self.vocab = list(set(all_tokens))  # Unique words

        self.positive_counts = np.zeros(len(self.vocab))
        self.negative_counts = np.zeros(len(self.vocab))

        X_train_vectorized = [self.vectorize_review(self.preprocess_review(review)) for review in X_train]

        positive_count = 0
        for i in range(len(X_train_vectorized)):
            if Y_train[i] == 'positive':
                self.positive_counts += X_train_vectorized[i]
                positive_count += 1
            else:
                self.negative_counts += X_train_vectorized[i]

        self.positive_prior = positive_count / len(Y_train)
        self.negative_prior = 1 - self.positive_prior

    def predict(self, X_test):
        predictions = []
        for review in X_test:
            review_vectorized = self.vectorize_review(self.preprocess_review(review))

            positive_prob = (self.positive_counts + 1) / (sum(self.positive_counts) + len(self.vocab))
            negative_prob = (self.negative_counts + 1) / (sum(self.negative_counts) + len(self.vocab))

            positive_likelihood = np.prod(positive_prob ** review_vectorized) * self.positive_prior
            negative_likelihood = np.prod(negative_prob ** review_vectorized) * self.negative_prior

            if positive_likelihood > negative_likelihood:
                predictions.append('positive')
            else:
                predictions.append('negative')

        return predictions

# Training Data
positive_review = ["The movie was amazing, I like great acting and an engaging plot"]
negative_review = ["I hate this movie so much, it's terrible!"]
X_train = positive_review + negative_review
Y_train = ['positive'] * len(positive_review) + ['negative'] * len(negative_review)
X_test = ["The acting was superb!"]
Y_test = ['positive']

# Train the classifier
classifier = NaiveBayesClassifier()
classifier.train(X_train, Y_train)

# Predictions
predictions = classifier.predict(X_test)
print("Predicted class for the new review:", predictions[0])

# Accuracy Calculation
accuracy = sum(1 for true_label, predicted_label in zip(Y_test, predictions) if true_label == predicted_label) / len(Y_test)
print("Accuracy of the model:", accuracy)
