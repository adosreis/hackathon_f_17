import nltk
import random
import pickle
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
#from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
#from sklearn.linear_model import LogisticRegression, SGDClassifier
#from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
from newspaper import Article

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
# for catergory in movie_reviews.categories():
# 	for fileid in movie_reviews.fileids(catergory):
# 		documents.append((list(movie_reviews.words(fileid)),catergory))
tech_docs_f = open('techdocs.pickle','rb')
tech_docs = pickle.load(tech_docs_f)
tech_docs_f.close()


for doc in tech_docs:
	documents.append((list(doc.split()),'pos'))

nontech_docs_f = open('nontechdocs.pickle','rb')
non_tech_docs = pickle.load(nontech_docs_f)
nontech_docs_f.close()

for doc in non_tech_docs:
	documents.append((list(doc.split()),'neg'))

random.shuffle(documents)
word_banks = []
for w in movie_reviews.words():
	word_banks.append(w.lower())
word_banks = nltk.FreqDist(word_banks)

w_features = list(word_banks.keys())

def find_features(document):
	words = set(document)
	features = {}
	for w in w_features:
		features[w] = (w in words)
	return features

feature_set = [(find_features(rev), catergory) for (rev, catergory) in documents]

training = feature_set

classifier = nltk.NaiveBayesClassifier.train(training)
# MNB_Classifier = SklearnClassifier(MultinomialNB()).train(training)
# BNB_Classifier = SklearnClassifier(BernoulliNB()).train(training)
# LR_Classifier = SklearnClassifier(LogisticRegression()).train(training)
# SGD_Classifier = SklearnClassifier(SGDClassifier()).train(training)
# LSVC_Classifier = SklearnClassifier(LinearSVC()).train(training)
# NSVC_Classifier = SklearnClassifier(NuSVC()).train(training)

classifier.show_most_informative_features(100)
#voted_classifier = VoteClassifier(classifier,MNB_Classifier,BNB_Classifier,LR_Classifier,SGD_Classifier,LSVC_Classifier,NSVC_Classifier)

def guess(url):
	a = Article(url = 'https://www.newscientist.com/article/2150282-online-school-wants-to-train-arts-students-in-cybersecurity/', language = 'en')
	a.download()
	a.parse()
	a_features = find_features(a.text)
	answer = classifier.classify(a_features)
	return a ,answer

def update(a, answer):
	if answer is 'pos':
		non_tech_docs.append(a.text)
	else:
		tech_docs.append(a.text)
	tech_docs_f = open('techdocs.pickle','wb')
	pickle.dump(tech_docs,tech_docs_f)
	tech_docs_f.close()
	nontech_docs_f = open('nontechdocs.pickle','wb')
	pickle.dump(non_tech_docs,nontech_docs_f)
	tech_docs_f.close()


t,b= guess('https://www.wired.com/story/googles-learning-software-learns-to-write-learning-software/')
if b is 'neg':
	print("WRONG!")
	update(t,b)
