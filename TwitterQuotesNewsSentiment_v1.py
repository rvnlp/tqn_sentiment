import sys
import nltk
import xlrd
import twitter

def main():

# The Quotes corpora is downloaded as an Excel file. The file is opened using the XLRD module and the necessary columns are read

	quote_corpora = xlrd.open_workbook('2010_JRC_1590-Quotes-annotated-for-sentiment.xls')
	sheet_to_open = quote_corpora.sheet_by_name(u'Quotations')
	quotes_col = sheet_to_open.col_values(1)
	sent_col = sheet_to_open.col_values(6)

# The quotes and the corresponding sentiments are stored as a list
	input_list_1 = [('quote1','POS'),('quote2','NEG')]

	counter_2 = 0

	for quote in quotes_col:
		input_list_1.append((quote, sent_col[counter_2]))
		counter_2 = counter_2 + 1

# There could be several quotes without sentiment classification. We take only those quotes that are classified

	input_list_2 = [('quote1','POS'),('quote2','NEG')]

	for inputitem in input_list_1:
		if ((inputitem[1] == 'POS') or (inputitem[1] == 'NEG')):
			input_list_2.append(inputitem)


# Words of size 2 and lesser are removed here and all other words are taken in lower case. 

	tweets = []
	for (content, sentiment) in input_list_2:
		text_filtered = [specific_word.lower() for specific_word in content.split() if len(specific_word) > 2]
		tweets.append((text_filtered, sentiment))


# This function makes a list of all words used
	
	def separate_tweets_to_words(tweets):
	    list_of_words = []
	    for (content, sentiment) in tweets:
	      list_of_words.extend(content)
#	    print list_of_words
#	    print tweets
	    return list_of_words

# A list of all distinct words used is created, and is sorted starting with the most used words

	def find_features(wordlist):
	    wordlist = nltk.FreqDist(wordlist)
	    features_to_get = wordlist.keys()
	    return features_to_get

# Feature extraction - a dictionary is created which indicates which words in the tweet are present in the list of inputs

	def feature_extracter(document):
	    document_words = set(document)
	    feature_extract = {}
	    for word in features_to_get:
		feature_extract['contains(%s)' % word] = (word in document_words)
	    return feature_extract


	features_to_get = find_features(separate_tweets_to_words(tweets))


# We apply the features using the method apply_features and create the training set

	training_set = nltk.classify.apply_features(feature_extracter,tweets)

# We train the classifier using the training set.

	classifier = nltk.NaiveBayesClassifier.train(training_set)

# Connecting to the Twitter API to get the latest 20 feeds of 'BBCBreaking' news feed

	api = twitter.Api()
	statuses = api.GetUserTimeline('BBCBreaking')
	tweetset = []
	
	for s in statuses:
		tweetset.append([s.text])
	
	tweetset.pop(19)

# The classifier that learned from our training set is now applied on the BBC newsfeed

	for tweet in tweetset:
		tweet = tweet[0]
		print classifier.classify(feature_extracter(tweet.split()))


if __name__ == '__main__':
	main()









