# Front Page

#### Detecting Emotions in Headlines
##### Dr. Kelly Epley

![img1](images/personal-2923048_1920.jpg)

I've created a model to help news media outlets classify headlines based on the emotions they convey so that they can select the right ones to keep readers interested in their content. 
 

# Background

Headlines are designed to grab readers' attention so that they'll read articles and keep coming back for more content.

The most effective way to get our attention is to make us feel something: afraid, angry, surprised, delighted. When we experience emotions, we experience a cascade of automatic physiological and cognitive changes, and changes in the direction of our attention are chief among these (Brady). Typically, the more intense the emotion, the stronger these effects will be. 

![img2](images/Attachment-1-2.jpeg)

As you might expect, researchers have found evidence of a relationship between high emotion content and social media sharing behaviors. Stieglitz and Dang-Xuan (2013) showed that people are more likely to share content that causes high phsyiologial arrousal, such as anger and amusement. Berger (2011) showed that news stories that elicit strongly negative emotions are quicker to turn viral than content that is emotionally neutral or positive.

This is a strong incentive for news media to rely on negative headlines in an attempt to increase sharing. However, there are good reasons to offer plenty of positive content as well. Positive content may not be as quick to turn viral, but Ferrara and Yang (2015) found that it has greater staying power in the long run. Positive stories get more interactions--shares, Facebook likes, and so forth--over time than negative stories.  

News and media providers have an interest in finding a balance of emotions on their front pages and personalized recommendations. I've developed a tool that makes it easier to know whether an appropriate balance has been achieved.

# The Data

For this project, I analyzed a set of 1250 headlines (Source: [SemEval 2007](http://web.eecs.umich.edu/~mihalcea/affectivetext/)). 

According to the dataset's authors, the headlines were collected from a variety of news sources. For each headline, annotators assigned an intensity rating between 0 and 100 for six emotion categories: anger, disgust, fear, joy, sadness, and surprise. 0 indicates that the emotion is not present. 100 indicates that it is present in its max intensity. Annotators were instructed to assign ratings according to their first intuition about the emotional import of the headlines, taking into account both the emotion-evoking words in the text and the overall impact of the it (Strapparava and Mihalcea 2007, p. 2-3).

The dataset also came with a second set of labels with overall positive or negative valence ratings.

It's important to note that annotating emotions in text is a difficult task (Alm et al 2005). Emotions are inferred from context as well as from the literal meaning of what is said. Also, annotators' personal histories and background beliefs may result in different reactions to a given subject matter. The same subject matter may be perceived as threatenening to one annotator, eliciting fear, antagonistic to another annotator, eliciting anger, and buffonish to another, eliciting disgust (Gaspar et al. 2016). We can be fairly confident in the reasonability of the labels in the dataset becuase they were labeled by six independent annotators. 

The headlines in the dataset have an average length of six words and a maximum length of 15. The most common emotion (in any amount) is surprise and the most common maximum emotion rating is joy. Disgust is the least common, and also has the lowest average intensity.

I checked the headlines for presence of emotion words from the WordNet emotion lexicon and the positive and negative words from the General Inquirer lexicon. Just over 100 of the headlines contained words from the emotion lexicon and just under half of the headlines contained words from the positive and negative words lexicon. 

Of the headlines with words appearing in the emotion lexicon, the emotion labels matched 85% of the time. However, less than 10% of the data contained words from the lexicon and the vast majority are rated above zero for one or more emotions.  

There was little correspondence between the positive and negative words lexicon and the valence labels, which matched only 27% of the time.

I also looked at the most common words in the dataset, the most common word pairs, and the most common words for each label. See the results in the notebook titled "Exploratory_Data_Analysis."


# Predictions

Predicting emotions is a multilabel classification problem. Instead of predicting a single class out of two or more options as multi*class* models do, multilabel models make two or more independent predictions--one for each label. 

I tried various multilabel classifiers from the skmultilearn package paired with a variety of estimators. In choosing a multilabel classifier, it matters whether there is correlation among labels. There is strong correlation (65%) between disgust and anger and moderate correlation between several other labels. To test whether modeling would improve with a classifier that takes label correlation into account, I compared a Binary Relevance Classifier with a Classifier Chain. Binary Relevance Classifiers independently model each label. Classifier Chains also model each label, but pass label predictions from one model to the next. Their overall scores were very similar, but the Classifier Chain had notably greater success in predicting disgust.

My best model was a Recurrent Neural Network(RNN). RNN is well suited to data that is sequential because it utilizes Long Short Term Memory(LSTM) to retain information from previously seen data. This allows it to learn features of emotion language (syntax, context) that other models that rely on Bag-of-Words representations cannot.  


# The Front Page Report

![img2](newspaper-973048_1920.jpg)

To demonstrate my RNN's utility, I created a Python class: front_page. 

The front page object is instantiated with one attribute: source. Options include: 'npr', 'slate', 'fox', and 'breitbart'. 

It has three methods:

##### 1) get_headlines
Fetches headlines currently on the source's front page and returns them as a list

##### 2) details
Returns a report which contains:
    * each headline currently on the source's front page
    * a list of emotions present in each headline, as predicted by my model
    * valence of the words contained in each headline, predicted by VADER
    * summay information
    
I included VADER's valence predictions in my reports as some additional helpful information about the headline. This would be particularly useful, for example, when my model predicts all 6 emotion categories. The valence rating will give users an indication of whether the overall thrust of the headline is positive or negative.

For details on VADER, see [here](https://github.com/cjhutto/vaderSentiment)

##### 3) summary
Returns only the summary information from the report.


# Works Cited 

1. Berger, J. 2011. Arousal increases social transmission of information. Psychological Science 22.7, 891–893.

2. Ferrara E. and Yang, Z. 2015. Quantifying the effect of sentiment on information diffusion in social media, PeerJ Computer Science 1.26. 

3. Gaspar, R., Pedro, C., Panagiotopoulos, P., and Seibt, B. 2016. Beyond positive or negative: Qualitative sentiment analysis of social media reactions to unexpected stressful events. Computers in Human Behavior 56, 179-191.

4. Stefan Stieglitz & Linh Dang-Xuan. 2013. Emotions and Information Diffusion in Social Media—Sentiment of Microblogs and Sharing Behavior, Journal of Management Information Systems, 29.4, 217-248, DOI: 10.2753/MIS0742-1222290408

5. Strapparava, C. and Mihalcea, R. 2007. SemEval-2007 Task 14: Affective Text. https://www.aclweb.org/anthology/S07-1013








