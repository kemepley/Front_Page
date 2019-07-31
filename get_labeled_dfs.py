import tarfile
import pandas as pd


def emotion_labels(row):
    if row>0:
        label=1
    else:
        label=0
    return label



def get_labeled_dfs():

# used the tarfile ilbrary to open the tarfile and the getmembers() method to get a list of filenames
	tar = tarfile.open('data/AffectiveText.Semeval.2007.tar')
	members = tar.getmembers()
	members

# used extractfile() to get the information in each file and put it in dataframes
	corpus_df = pd.read_csv(tar.extractfile(members[1]), sep='\n')
	valence_df = pd.read_csv(tar.extractfile(members[3]), sep=' ', header=None)
	emotion_df = pd.read_csv(tar.extractfile(members[4]), sep=' ', header=None)

	corpus_df_2 = pd.read_csv(tar.extractfile(members[8]), sep='\n')
	valence_df_2 = pd.read_csv(tar.extractfile(members[6]), sep=' ', header=None)
	emotion_df_2 = pd.read_csv(tar.extractfile(members[7]), sep=' ', header=None)

# closing the tar file I opened above
	tar.close



# cleaning the target files
# labeling the columns of the target dfs and dropping the duplicate index columns
	valence_df = valence_df.drop([0], axis=1)
	valence_df.columns = ['valence']

	emotion_df = emotion_df.drop([0], axis=1)
	emotion_df.columns = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

	valence_df_2 = valence_df_2.drop([0], axis=1)
	valence_df_2.columns = ['valence']

	emotion_df_2 = emotion_df_2.drop([0], axis=1)
	emotion_df_2.columns = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

# putting the dfs together
	valence_df = pd.concat([valence_df, valence_df_2], axis=0, ignore_index=True)
	emotion_df = pd.concat([emotion_df, emotion_df_2], axis=0, ignore_index=True)


# cleaning the corpus dfs
# there is a footer in the last column that needs to be dropped
	corpus_df = corpus_df.drop([1000], axis=0)
	corpus_df_2 = corpus_df_2.drop([250], axis=0)
    
# putting the dfs together
	corpus_df = pd.concat([corpus_df, corpus_df_2], axis=0, ignore_index=True)

# getting rid of the html tags by splitting on the "<>" characters 
	corpus_df['split'] = corpus_df.iloc[:, 0].apply(lambda x: x.split(">"))
	corpus_df['text_with_html_tag'] = corpus_df.split.apply(lambda x: x[1])
	corpus_df['text_with_html_tag_split'] = corpus_df.text_with_html_tag.apply((lambda x: x.split("<")))
	corpus_df['text'] = corpus_df.text_with_html_tag_split.apply(lambda x: x[0])

# drop the original column and the split columns
	corpus_df = corpus_df.drop(['<corpus task="affective text">','split','text_with_html_tag', 'text_with_html_tag_split'], axis=1)



# preparing class labels for the emotion dfs
# setting up a target colum with a numeric category for the emotion with the strongest intensity rating
	emotion_df['max'] = emotion_df[['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']].idxmax(axis=1)
	emotion_df['anger_label'] = emotion_df['anger'].apply(emotion_labels)
	emotion_df['disgust_label'] = emotion_df['disgust'].apply(emotion_labels)
	emotion_df['fear_label'] = emotion_df['fear'].apply(emotion_labels)
	emotion_df['joy_label'] = emotion_df['joy'].apply(emotion_labels)
	emotion_df['sadness_label'] = emotion_df['sadness'].apply(emotion_labels)
	emotion_df['surprise_label'] = emotion_df['surprise'].apply(emotion_labels)



# preparing class labels for the valence dfs
	valence_df['label'] = valence_df['valence'].apply(lambda x: 2 if (x>-15) & (x<15) else x)
	valence_df['label'] = valence_df['label'].apply(lambda x: 1 if x>=15 else x)
	valence_df['label'] = valence_df['label'].apply(lambda x: 0 if (x<=-15) else x)

    

	return corpus_df, emotion_df, valence_df

