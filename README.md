# Front Page

#### Detecting Emotions in Headlines
##### Dr. Kelly Epley

![img1](images/personal-2923048_1920.jpg)

Front Page is a tool that classifies headlines based on the emotions they convey. Based on research on the kinds of social media interactions different emotions garner, it's designed to help news media outlets maintain the right combinations of headlines to keep readers interested in their content. 

# Repo Contents

 - README:
Description of the project goals, process, and results

 - Final Notebook:
Jupyter notebook containing the code for the model deployed in front_page. Compares the model with other modeling strategies.

 - Exploratory Data Analysis:
Jupyter notebook containing examination of label distributions, word distrubtions among the labels, and the presence of words from the WordNet Affect lexicon.

 - Front Page Presentation:
Slide deck describing the project in brief

 - class_front_page:
Py file containing the code for front_page

 - Assorted py files:
Code used to clean and process data

 - Folders:
     - Notebooks: Notebooks used at various points in the development process 
     - Model: h5 file with the saved model
     - Images: images used in the repo
 

# Background

Headlines are designed to grab readers' attention so that they'll read articles and keep coming back for more content.

The most effective way to get our attention is to make us feel something: afraid, angry, surprised, delighted. When we experience emotions, we experience a cascade of automatic physiological and cognitive changes that prepare us for action, and changes in the direction of our attention are chief among these (Brady 2014). Typically, the more intense the emotion, the stronger these effects will be. 

![img2](images/john-schnobrich-FlPc9_VocJ4-unsplash.jpg)

As you might expect, researchers have found evidence of a relationship between high emotion content and social media sharing behaviors. Stieglitz and Dang-Xuan (2013) showed that people are more likely to share content that causes high phsyiologial arrousal, such as anger and amusement. Berger (2011) showed that news stories that elicit strongly negative emotions are quicker to turn viral than content that is emotionally neutral or positive.

This is a strong incentive for news media to rely on negative headlines in an attempt to increase sharing. However, there are good reasons to offer plenty of positive content as well. Positive content may not be as quick to turn viral, but Ferrara and Yang (2015) found that it has greater staying power in the long run. Positive stories get more interactions--shares, Facebook likes, and so forth--over time than negative stories.  

News and media providers have an interest in finding a balance of emotions on their front pages to optimize engagement with their content. I've developed a tool that makes it easier to know whether an appropriate balance has been achieved.

# The Data

For this project, I analyzed a set of 1,250 [headlines](http://web.eecs.umich.edu/~mihalcea/affectivetext/). 

According to the dataset's authors, the headlines were collected from a variety of news sources. For each headline, annotators assigned an intensity rating between 0 and 100 for six emotion categories: anger, disgust, fear, joy, sadness, and surprise. 0 indicates that the emotion is not present. 100 indicates that it is present in its maximum intensity. Annotators were instructed to assign ratings according to their first intuition about the emotional import of the headlines, taking into account both the emotion-evoking words in the text and the overall impact of the it (Strapparava and Mihalcea 2007, p. 2-3).

The dataset also came with a second set of labels with overall positive or negative valence ratings.

It's important to acknowelge that annotating emotions in text is a difficult task (Alm et al 2005). Emotions are inferred from context as well as from the literal meaning of what is said. Also, annotators' personal histories and background beliefs may result in different reactions to a given subject matter. The same subject matter may be perceived as threatenening to one annotator, eliciting fear, antagonistic to another annotator, eliciting anger, and buffonish to another, eliciting disgust (Gaspar et al. 2016). We can be fairly confident in the reasonability of the labels in the dataset becuase they were labeled by six independent annotators. 

The headlines in the dataset have an average length of six words and a maximum length of 15. The most common emotion (in any amount) is surprise and the most common maximum emotion rating is joy. Disgust is the least common, and also has the lowest average intensity.

I checked the headlines for presence of emotion words from the [WordNet](https://wordnet.princeton.edu) emotion lexicon and the positive and negative words from the [General Inquirer](http://www.wjh.harvard.edu/~inquirer/) lexicon. Just over 100 of the headlines contained words from the emotion lexicon and just under half of the headlines contained words from the positive and negative words lexicon. 

Of the headlines with words appearing in the emotion lexicon, the emotion labels matched 85% of the time. However, less than 10% of the data contained words from the lexicon and the vast majority are rated above zero for one or more emotions.  

I also looked at the most common words in the dataset, the most common word pairs, and the most common words for each label. See the results in the notebook titled "Exploratory_Data_Analysis."


# Predictions

Predicting emotions is a multilabel classification problem. Instead of predicting a single class out of two or more options as multi*class* models do, multilabel models make two or more independent predictions--one for each label. 

I tried various multilabel classifiers from the skmultilearn package paired with a variety of estimators. In choosing a multilabel classifier, it matters whether there is correlation among labels. There is strong correlation (65%) between disgust and anger and moderate correlation between several other labels. To test whether modeling would improve with a classifier that takes label correlations into account, I compared a Binary Relevance Classifier with a Classifier Chain. Binary Relevance Classifiers model each label independently. Classifier Chains also model each label, but pass label predictions from one model to the next. The two classifiers performed similarly in terms of their overall scores (Jaccard Score, Hamming Loss), but the Classifier Chain had notably greater success in predicting disgust.

My best model was a Recurrent Neural Network(RNN). RNN is well suited to data that is sequential because it utilizes Long Short Term Memory(LSTM) to retain information from previously seen data. This allows it to learn features of emotion language (syntax, context) that other models which rely on Bag-of-Words representations of text cannot.  


# The Front Page Report

![img2](images/newspaper-973048_1920.jpg)

To demonstrate my RNN's utility, I created a Python class: front_page. 

The front page object is instantiated with one attribute: source. Options include: 'npr', 'slate', 'fox', and 'breitbart'. 

It has three methods:

##### 1) get_headlines
Fetches headlines currently on the source's front page and returns them as a list

##### 2) details
Returns a report which contains:
 - each headline currently on the source's front page
 - a list of emotions present in each headline, as predicted by my model
 - valence of the words contained in each headline, predicted by VADER
 - summay information
    
VADER is a model built on a sophisticated lexicon of positive and negative word, where each word has an intensity rating produced by 20 highly vetted annotators. The VADER's sentiment intensity analyzer produces a report of a document's polarity in the form of a python dictionary. The dictionary keys are: 'pos' for positive words, 'neg' for negative words, 'neu' for neutral words, and 'compound' for the overall polarity. The values assigned to each of the first three are the percentages of words containing positive, negative, or neutral valence (of any amount) in each headline. The compound score is a sum of the intensity scores for all the words in the headline. The sum is normalized so that every score is a number between -1 and 1. 

I included VADER's valence predictions in my reports as some additional helpful information about the headlines. This would be particularly useful, for example, when my model predicts all 6 emotion categories. The valence ratings will give users an indication of whether the overall thrust of the headline is positive or negative.

For more details on VADER, see [here](https://github.com/cjhutto/vaderSentiment)

##### 3) summary
Returns only the summary information from the report.


# Works Cited 

1. Berger, J. (2011). Arousal increases social transmission of information. Psychological Science 22.7, 891–893.

2. Brady, M. S. (2014). Emotion, Attention, and the Nature of Value,’ in S. Roeser and C. Todd (eds) Emotion and Value. Oxford: Oxford University Press, 52– 71.

3. Ferrara E. & Yang, Z. (2015). Quantifying the effect of sentiment on information diffusion in social media, PeerJ Computer Science 1.26. 

4. Gaspar, R., Pedro, C., Panagiotopoulos, P., & Seibt, B. (2016). Beyond positive or negative: Qualitative sentiment analysis of social media reactions to unexpected stressful events. Computers in Human Behavior 56, 179-191.

5. Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

6. Stieglitz, S. & Dang-Xuan, L. (2013). Emotions and Information Diffusion in Social Media—Sentiment of Microblogs and Sharing Behavior, Journal of Management Information Systems 29.4, 217-248.

7. Strapparava, C. & Mihalcea, R. (2007). SemEval-2007 Task 14: Affective Text. https://www.aclweb.org/anthology/S07-1013.








