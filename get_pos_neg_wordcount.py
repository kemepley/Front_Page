import pandas as pd
import string

def get_pos_neg_wordcount():
    pos_neg_words = pd.read_excel("/Users/flatironschool/Desktop/Final_Project/inquirerbasic.xls")

    pos_words_list = []

	# getting a list of positive words
    for i in range(len(pos_neg_words['Positiv'])):
        if pos_neg_words['Positiv'][i]=='Positiv':
            pos_words_list.append(pos_neg_words['Entry'][i])
        
	# removing punctuation and numbers from entries listed for multiple meanings and removing duplicates
    pos_words_list = [i.lower() for i in pos_words_list]
    pos_words_list = [i.translate(str.maketrans('', '', string.punctuation)) for i in pos_words_list]
    pos_words_list = [i.translate(str.maketrans('', '', string.digits)) for i in pos_words_list]
    pos_words_list = list(set(pos_words_list))

    neg_words_list = []

	# getting a list of positive words
    for i in range(len(pos_neg_words['Negativ'])):
        if pos_neg_words['Negativ'][i]=='Negativ':
            neg_words_list.append(str(pos_neg_words['Entry'][i]))

	# removing punctuation and numbers from entries listed for multiple meanings and removing duplicates        
    neg_words_list = [i.lower() for i in neg_words_list]
    neg_words_list = [i.translate(str.maketrans('', '', string.punctuation)) for i in neg_words_list]
    neg_words_list = [i.translate(str.maketrans('', '', string.digits)) for i in neg_words_list]
    neg_words_list = list(set(neg_words_list))

    corpus_df = pd.read_csv('corpus_df.csv')
    pos_neg_wordcounts_df = corpus_df.copy()

    def count_pos_words(row):
        count = 0
        for i in row.split():
            if i in pos_words_list:
                count += 1
        return count

    def count_neg_words(row):
        count = 0
        for i in row.split():
            if i in neg_words_list:
                count += 1
        return count

    pos_neg_wordcounts_df['positive_count'] = pos_neg_wordcounts_df.text.apply(count_pos_words)
    pos_neg_wordcounts_df['negative_count'] = pos_neg_wordcounts_df.text.apply(count_neg_words)

    return pos_neg_wordcounts_df