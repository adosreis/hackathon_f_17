import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers

	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)
	def confidence(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		choice_votes = votes.count(mode(votes))
		conf = choice_votes / len(votes)
		return conf

run_con = 'new'

documents = []
for catergory in movie_reviews.categories():
	for fileid in movie_reviews.fileids(catergory):
		documents.append((list(movie_reviews.words(fileid)),catergory))

random.shuffle(documents)
word_banks = []
for w in movie_reviews.words():
	word_banks.append(w.lower())
word_banks = nltk.FreqDist(word_banks)

w_features = list(word_banks.keys())[:3000]

def find_features(document):
	words = set(document)
	features = {}
	for w in w_features:
		features[w] = (w in words)

	return features

feature_set = [(find_features(rev), catergory) for (rev, catergory) in documents]

training = feature_set[:1900]
testing = feature_set[1900:]

#LogisticRegression, SGDClassifier
#SVC, LinearSVC, NuSVC


classifier = nltk.NaiveBayesClassifier.train(training)
MNB_Classifier = SklearnClassifier(MultinomialNB()).train(training)
#GNB_Classifier = SklearnClassifier(GaussianNB())
BNB_Classifier = SklearnClassifier(BernoulliNB()).train(training)
LR_Classifier = SklearnClassifier(LogisticRegression()).train(training)
SGD_Classifier = SklearnClassifier(SGDClassifier()).train(training)
SVC_Classifier = SklearnClassifier(SVC()).train(training)
LSVC_Classifier = SklearnClassifier(LinearSVC()).train(training)
NSVC_Classifier = SklearnClassifier(NuSVC()).train(training)

classifier.show_most_informative_features(100)
#print("Original accuracy %: ", (nltk.classify.accuracy(classifier, testing))*100)
#print("MNB accuracy %: ", (nltk.classify.accuracy(MNB_Classifier, testing))*100)
#print("GNB accuracy %: ", (nltk.classify.accuracy(GNB_Classifier, testing))*100)
#print("BNB accuracy %: ", (nltk.classify.accuracy(BNB_Classifier, testing))*100)
#print("LR accuracy %: ", (nltk.classify.accuracy(LR_Classifier, testing))*100)
#print("SGD accuracy %: ", (nltk.classify.accuracy(SGD_Classifier, testing))*100)
#print("LSVC accuracy %: ", (nltk.classify.accuracy(LSVC_Classifier, testing))*100)
#print("NSVC accuracy %: ", (nltk.classify.accuracy(NSVC_Classifier, testing))*100)

if(run_con is 'new'):
	voted_classifier = VoteClassifier(classifier,MNB_Classifier,BNB_Classifier,LR_Classifier,SGD_Classifier,LSVC_Classifier,NSVC_Classifier)

else:
	voted_classifier_f = open('voted_classifier.pickle','rb')
	voted_classifier = pickle.load(voted_classifier_f)
	voted_classifier_f.close()

print("Voted classifier accuracy %: ", (nltk.classify.accuracy(voted_classifier, testing))*100)
print("Classification:", voted_classifier.classify(testing[0][0]), "Confidence %:", (voted_classifier.confidence(testing[0][0])*100))

if(run_con is 'new'):
	voted_classifier_f = open('voted_classifier.pickle','wb')
	pickle.dump(voted_classifier, voted_classifier_f)
	voted_classifier_f.close()
