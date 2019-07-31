import warnings
warnings.filterwarnings("ignore")

import pandas as pd

import requests
from bs4 import BeautifulSoup

from keras.models import load_model
from keras.preprocessing import text, sequence

from get_labeled_dfs import *
from process_text import *

import matplotlib.pyplot as plt
import seaborn as sns

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class front_page:

    def __init__(self, source):
        
        self.source = source

    def get_headlines(self): 
        
        if self.source == 'npr':
            
            request_npr = requests.get('https://www.npr.org')
            soup = BeautifulSoup(request_npr.content, features="lxml")
            headlines = soup.findAll('h3', class_='title')
            npr_front_page = [i.text for i in headlines]
            return npr_front_page
            
        elif self.source == 'slate':
            
            request_slate = requests.get('https://slate.com')
            soup = BeautifulSoup(request_slate.content, features="lxml")
            headlines = soup.findAll('h3', class_='story-teaser__headline')
            slate_front_page = [i.text.replace('\n', '').strip() for i in headlines]
            slate_front_page = [i.replace('Podcast Episode', '') for i in slate_front_page]
            slate_front_page = [i.replace('\n', '').strip() for i in slate_front_page]
            return slate_front_page
        
        elif self.source == 'fox':
            
            request_fox = requests.get('https://www.foxnews.com')
            soup = BeautifulSoup(request_fox.content, features="lxml")
            headlines = soup.findAll('h2', class_='title')
            fox_front_page = [i.text.replace('\n', '') for i in headlines]
            return fox_front_page
        
        elif self.source == 'breitbart':
            
            request_breitbart = requests.get('https://www.breitbart.com')
            soup = BeautifulSoup(request_breitbart.content, features="lxml")
            headlines = soup.findAll('h2')
            breitbart_headlines = [headlines[i].text for i in range(len(headlines))]
            
            # Since section titles are in all caps, check to see if there is a lower case letter
            breitbart_front_page = []
            for i in breitbart_headlines:
                title_checker = []
                for j in i:
                    if j.islower() or j==' ':
                        title_checker.append(True)
                    else:
                        title_checker.append(False)
                if sum(title_checker)>1:
                    breitbart_front_page.append(i)
            return breitbart_front_page
        
        else:
            print("I don't know that source. Please choose: npr, slate, fox, or breitbart.")

    def details(self):
    
        corpus_df_RNN, _, _ = get_labeled_dfs()
        processor = Process_Text_Data()
        processor.transform(corpus_df_RNN, RNN=True)
        tokenizer = text.Tokenizer()
        tokenizer.fit_on_texts(list(corpus_df_RNN['text']))
        
        #get headlines
        headline_list = self.get_headlines()
    
        # load saved model     
        model = load_model('RNN_multiclass_emotion.h5')
    
        # make headlines lowercase and remove punctuation (except '?' and '!')    
        corpus = pd.DataFrame({'text': headline_list})
        processor = Process_Text_Data()
        processor.transform(corpus, RNN=True)     
    
        # transform list of headlines into sequences and pad with zeros     
        new_sequence = tokenizer.texts_to_sequences(headline_list)
        padded_new = sequence.pad_sequences(new_sequence, maxlen=15, padding='post')
    
        # make predictions
        preds = model.predict(padded_new)>.5
        pred_proba = model.predict(padded_new)
    
        # create df of predictions, probabilities    
        df_preds = pd.DataFrame({'anger':[i[0] for i in preds],
                                 'disgust':[i[1] for i in preds],
                                 'fear':[i[2] for i in preds],
                                 'joy':[i[3] for i in preds],
                                 'sadness':[i[4] for i in preds],
                                 'suprise':[i[5] for i in preds]})
        df_pred_proba = pd.DataFrame({'anger':[i[0] for i in pred_proba], 
                                      'disgust':[i[1] for i in pred_proba],
                                      'fear':[i[2] for i in pred_proba],
                                      'joy':[i[3] for i in pred_proba],
                                      'sadness':[i[4] for i in pred_proba],
                                      'suprise':[i[5] for i in pred_proba]})
        
        # use VADER Sentiment Intensity Analyzer to get polarity scores
        
        SIA = SentimentIntensityAnalyzer()
        
        neg = []
        neu = []
        pos = []
        comp = []
        for headline in headline_list:
            score = SIA.polarity_scores(headline)
            neg.append(score['neg'])
            neu.append(score['neu'])
            pos.append(score['pos'])
            comp.append(score['compound'])
        polarity_df = pd.DataFrame({'neg':neg, 'neu':neu, 'pos':pos, 'comp':comp})
        
        # print report
        
        plt.style.use('ggplot')
        plt.figure(figsize=(10,5))
        
        plt.subplot(1,2,1)
        norm = df_preds.sum()/len(headline_list)
        norm.plot(kind='bar')
        plt.title("Percentage of Headlines \nContaining Each Emotion")
        
        plt.subplot(1,2,2)
        polarity_df.boxplot()
        plt.title('Positive, Negative, and Neutral \nWord Distributions')
        plt.show()
    
        for i,v in enumerate(headline_list):
            print(v)
            if df_preds['anger'][i]==True:
                print('    \U0001F620 Anger:' + str(round(df_pred_proba['anger'][i], 2)*100) + "%")
            if df_preds['disgust'][i]==True:
                print('    \U0001F62C Disgust:' + str(round(df_pred_proba['disgust'][i], 2)*100) + "%")
            if df_preds['fear'][i]==True:
                print('    \U0001F628 Fear:' + str(round(df_pred_proba['fear'][i], 2)*100) + "%")
            if df_preds['joy'][i]==True:
                print('    \U0001F600 Joy:' + str(round(df_pred_proba['joy'][i], 2)*100) + "%") 
            if df_preds['sadness'][i]==True:
                print('    \U0001F622 Sadness:' + str(round(df_pred_proba['sadness'][i], 2)*100) + "%") 
            if df_preds['suprise'][i]==True:
                print('    \U0001F92D Surprise:' + str(round(df_pred_proba['suprise'][i], 2)*100) + "%") 
            print('Word Polarities:\n', SIA.polarity_scores(v))
            print('\n')
            
    def summary(self):
    
        corpus_df_RNN, _, _ = get_labeled_dfs()
        processor = Process_Text_Data()
        processor.transform(corpus_df_RNN, RNN=True)
        tokenizer = text.Tokenizer()
        tokenizer.fit_on_texts(list(corpus_df_RNN['text']))
        
        #get headlines
        headline_list = self.get_headlines()
    
        # load saved model     
        model = load_model('RNN_multiclass_emotion.h5')
    
        # make headlines lowercase and remove punctuation (except '?' and '!')    
        corpus = pd.DataFrame({'text': headline_list})
        processor = Process_Text_Data()
        processor.transform(corpus, RNN=True)     
    
        # transform list of headlines into sequences and pad with zeros     
        new_sequence = tokenizer.texts_to_sequences(headline_list)
        padded_new = sequence.pad_sequences(new_sequence, maxlen=15, padding='post')
    
        # make predictions
        preds = model.predict(padded_new)>.5
        pred_proba = model.predict(padded_new)
    
        # create df of predictions, probabilities    
        df_preds = pd.DataFrame({'anger':[i[0] for i in preds],
                                 'disgust':[i[1] for i in preds],
                                 'fear':[i[2] for i in preds],
                                 'joy':[i[3] for i in preds],
                                 'sadness':[i[4] for i in preds],
                                 'suprise':[i[5] for i in preds]})
        df_pred_proba = pd.DataFrame({'anger':[i[0] for i in pred_proba], 
                                      'disgust':[i[1] for i in pred_proba],
                                      'fear':[i[2] for i in pred_proba],
                                      'joy':[i[3] for i in pred_proba],
                                      'sadness':[i[4] for i in pred_proba],
                                      'suprise':[i[5] for i in pred_proba]})
    
         # use VADER Sentiment Intensity Analyzer to get polarity scores
        
        SIA = SentimentIntensityAnalyzer()
        
        neg = []
        neu = []
        pos = []
        comp = []
        for headline in headline_list:
            score = SIA.polarity_scores(headline)
            neg.append(score['neg'])
            neu.append(score['neu'])
            pos.append(score['pos'])
            comp.append(score['compound'])
        polarity_df = pd.DataFrame({'neg':neg, 'neu':neu, 'pos':pos, 'comp':comp})
        
        # print report
        
        plt.style.use('ggplot')
        plt.figure(figsize=(10,5))
        
        plt.subplot(1,2,1)
        norm = df_preds.sum()/len(headline_list)
        norm.plot(kind='bar')
        plt.title("Percentage of Headlines \nContaining Each Emotion")
        
        plt.subplot(1,2,2)
        polarity_df.boxplot()
        plt.title('Positive, Negative, and Neutral \nWord Distributions')
        plt.show()
    
