import tarfile
import string
import pandas as pd

def get_emotion_wordcount():

    tar = tarfile.open('/Users/flatironschool/Desktop/Final_Project/WordNetAffectEmotionLists.tar')
    members = tar.getmembers()

    anger_words = pd.read_csv(tar.extractfile(members[1]), header=None)
    anger_words['split'] = anger_words[0].apply(lambda x: x.split())
    anger_words['split'] = anger_words['split'].apply(lambda x: x[1:])

    anger_words_list = []
    for lst in anger_words['split']:
        for word in lst:
            if word not in anger_words_list:
                anger_words_list.append(word)

    disgust_words = pd.read_csv(tar.extractfile(members[2]), header=None)
    disgust_words['split'] = disgust_words[0].apply(lambda x: x.split())
    disgust_words['split'] = disgust_words['split'].apply(lambda x: x[1:])

    disgust_words_list = []
    for lst in disgust_words['split']:
        for word in lst:
            disgust_words_list.append(word)

    fear_words = pd.read_csv(tar.extractfile(members[3]), header=None)
    fear_words['split'] = fear_words[0].apply(lambda x: x.split())
    fear_words['split'] = fear_words['split'].apply(lambda x: x[1:])

    fear_words_list = []
    for lst in fear_words['split']:
        for word in lst:
            if word not in fear_words_list:
                fear_words_list.append(word)

    joy_words = pd.read_csv(tar.extractfile(members[4]), header=None)
    joy_words['split'] = joy_words[0].apply(lambda x: x.split())
    joy_words['split'] = joy_words['split'].apply(lambda x: x[1:])

    joy_words_list = []
    for lst in joy_words['split']:
        for word in lst:
            if word not in joy_words_list:
                joy_words_list.append(word)

    sadness_words = pd.read_csv(tar.extractfile(members[5]), header=None)
    sadness_words['split'] = sadness_words[0].apply(lambda x: x.split())
    sadness_words['split'] = sadness_words['split'].apply(lambda x: x[1:])

    sadness_words_list = []
    for lst in sadness_words['split']:
        for word in lst:
            if word not in sadness_words_list:
                sadness_words_list.append(word)

    surprise_words = pd.read_csv(tar.extractfile(members[6]), header=None)
    surprise_words['split'] = surprise_words[0].apply(lambda x: x.split())
    surprise_words['split'] = surprise_words['split'].apply(lambda x: x[1:])

    surprise_words_list = []
    for lst in surprise_words['split']:
        for word in lst:
            if word not in surprise_words_list:
                surprise_words_list.append(word)

    tar.close()

    corpus_df = pd.read_csv('corpus_df.csv')
    emotion_wordcounts_df = corpus_df.copy()

    def count_anger_words(row):
        count = 0
        for i in row.split():
            if i in anger_words_list:
                count += 1
        return count

    def count_disgust_words(row):
        count = 0
        for i in row.split():
            if i in disgust_words_list:
                count += 1
        return count

    def count_fear_words(row):
        count = 0
        for i in row.split():
            if i in fear_words_list:
                count += 1
        return count

    def count_joy_words(row):
        count = 0
        for i in row.split():
            if i in joy_words_list:
                count += 1
        return count

    def count_sadness_words(row):
        count = 0
        for i in row.split():
            if i in sadness_words_list:
                count += 1
        return count

    def count_surprise_words(row):
        count = 0
        for i in row.split():
            if i in surprise_words_list:
                count += 1
        return count
      
    emotion_wordcounts_df['anger_count'] = emotion_wordcounts_df.text.apply(count_anger_words)
    emotion_wordcounts_df['disgust_count'] = emotion_wordcounts_df.text.apply(count_disgust_words)
    emotion_wordcounts_df['fear_count'] = emotion_wordcounts_df.text.apply(count_fear_words)
    emotion_wordcounts_df['joy_count'] = emotion_wordcounts_df.text.apply(count_joy_words)
    emotion_wordcounts_df['sadness_count'] = emotion_wordcounts_df.text.apply(count_sadness_words)
    emotion_wordcounts_df['surprise_count'] = emotion_wordcounts_df.text.apply(count_surprise_words)
    
    return emotion_wordcounts_df