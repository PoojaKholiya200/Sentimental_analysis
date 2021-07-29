import string
from collections import Counter

import matplotlib.pyplot as plt
from nltk.corpus import stopwords #list of stopwords into corpus(collection of text)
from nltk.tokenize import word_tokenize# spilitting 
from nltk.sentiment.vader import SentimentIntensityAnalyzer #tells sentiments
import GetOldTweets3 as got
def get_tweets():
    
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('narendra modi')\
                                           .setSince("2020-10-01")\
                                           .setUntil("2021-02-30")\
                                           .setMaxTweets(100)

    #list of objects gets stored in'tweets' variable
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # iterating through tweets list . storing them temp in tweet variable.
    #get text and store is as a list inside text_tweet
    text_tweets = [[tweet.text]for tweet in tweets]
    return text_tweets

text = ""
text_tweets = get_tweets()
length = len(text_tweets)
   
for i in range(0,length):
    text =text_tweets[i][0] + " " + text
    
#converting lower case
lower_case = text.lower()

# removing puntuation
cleaned_text = lower_case.translate(str.maketrans('','',string.punctuation))

#splitting words into text
tokenized_words=word_tokenize(cleaned_text,"english")


# removing stop words from the tokenized words list
final_words=[]
for word in tokenized_words:
    if (word not in stopwords.words('english')):
        final_words.append(word)

emotion_list = []
with open('emotions.txt','r')as file:
    for line in file:
        clear_line = line.replace('\n','').replace(',','').replace("'",'').strip()
        word, emotion =clear_line.split(':')

        if  word in final_words:
            emotion_list.append(emotion)

            print(emotion_list)
            w = Counter(emotion_list)
            print(w)

            def sentiment_analyse(sentiment_text):
                score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
                pos = score['pos']
                neg = score['neg']
                if pos > neg:
                    print("positive sentiment")
                elif neg > pos:
                    print("negative sentiment")
                else:
                    print("neutral vibe")
sentiment_analyse(cleaned_text)
#plotting the emotion on graph 

fig, ax1 = plt.subplots()
ax1.bar(w.keys(),w.values())
fig.autofmt_xdate()
plt.savefig('graph6.png')
plt.show()
