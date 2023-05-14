# ipl-teams-twitter-sentiment-analysis
This Repo is a simple python code to do twitter sentiment and subjectivity analysis using TextBlob. Tweets are being analysed in batches using pyspark.

# What does this python script does? 
We have stored 200-300 tweets per IPL team in *ipl_data* directory. This script takes 10 tweets in a batch and generate subjectivity and sentiment scores of each tweet and generate a three dataframes: 

a. A DF containing following columns: **[tweet_text, sentiment_score, subjectivity_score, sentiment_type, subjectivity_type]**

b. A DF containing count of all tweets of respective sentiment_type ie. good, bad and nuetral 

c. A DF containing count of all tweets of respective subjectivity_type ie. objective and subjective. 


# Quick Start

1. Install Requirements
```bash 
pip3 install -r requirements.txt 
```
2. Install Apache Spark and Apache Hadoop on your system. 

3. You can do analysis of already stored tweets of a specific ipl team. Available team options: **["csk", "mi", "gt", "rcb", "pbks", "lsg", "srh", "rr"]**
```bash 
python3 main.py csk
```

4. You can also do analysis of all the available tweets by giving `all` as an argument. 
```bash
python3 main.py all
```
