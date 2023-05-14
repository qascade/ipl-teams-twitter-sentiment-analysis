import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from textblob import TextBlob

def CreateSparkSession(): 
    spark = SparkSession.builder.appName("SentimentAnalysis").getOrCreate()
    return spark

def analyze_batch(batch):
    # Create lists to store the results
    tweets = []
    sentiments = []
    subjectivities = []
    sentiment_words = []
    subjectivity_words = []
    # Loop through the tweets in the batch
    for tweet in batch:
        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(tweet)
        sentiment = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        # Classify sentiment in human words
        if sentiment > 0:
            sentiment_word = "positive"
        elif sentiment < 0:
            sentiment_word = "negative"
        else:
            sentiment_word = "neutral"
        # Classify subjectivity in human words
        if subjectivity > 0.5:
            subjectivity_word = "subjective"
        else:
            subjectivity_word = "objective"
        # Add the results to the lists
        sentiments.append(sentiment)
        subjectivities.append(subjectivity)
        sentiment_words.append(sentiment_word)
        subjectivity_words.append(subjectivity_word)
        tweets.append(tweet)
    # Return the lists of results
    return tweets, sentiments, subjectivities, sentiment_words, subjectivity_words


def analyze_team(team): 
    spark = CreateSparkSession()
    path = "ipl_data/" + team + ".json"
    tweets = spark.read.json(path)
    tweetsText = tweets.select("text")
    print(tweetsText.show())
    batch_size = 10
    # Create a new column with the batch number
    tweets = tweets.withColumn("batch", (F.monotonically_increasing_id() - 1) / batch_size)

    # Group the tweets by batch and apply the analyze_batch function to each group
    # The resulting RDD contains a tuple of four lists for each batch: sentiments, subjectivities, sentiment_words, subjectivity_words
    sentiment_data = tweets.groupby("batch").agg(F.collect_list("text").alias("texts")).rdd.map(lambda x: analyze_batch(x.texts))

    # Convert the RDD of tuples into a list of tuples and flatten the lists of results
    sentiment_data = sentiment_data.collect()
    tweets = [item for sublist in sentiment_data for item in sublist[0]]
    sentiments = [item for sublist in sentiment_data for item in sublist[1]]
    subjectivities = [item for sublist in sentiment_data for item in sublist[2]]
    sentiment_words = [item for sublist in sentiment_data for item in sublist[3]]
    subjectivity_words = [item for sublist in sentiment_data for item in sublist[4]]

    # Create a dataframe with the sentiment data
    sentiment_df = spark.createDataFrame(zip(tweets, sentiments, subjectivities, sentiment_words, subjectivity_words), schema=["tweet_text","sentiment", "subjectivity", "sentiment_word", "subjectivity_word"])


    # Compute the average sentiment and subjectivity
    averages = sentiment_df.agg(F.avg("sentiment").alias("average_sentiment"), F.avg("subjectivity").alias("average_subjectivity")).collect()

    # Print the results
    print("Average sentiment: {}".format(averages[0]["average_sentiment"]))
    print("Average subjectivity: {}".format(averages[0]["average_subjectivity"]))

    # Count the number of good, bad, neutral, subjective, and objective tweets
    sentiment_counts = sentiment_df.groupBy("sentiment_word").count().toPandas()
    subjectivity_counts = sentiment_df.groupBy("subjectivity_word").count().toPandas()

    sentiment_counts_df = spark.createDataFrame(sentiment_counts)
    subjectivity_counts_df = spark.createDataFrame(subjectivity_counts)

    # Show the resulting DataFrame
    sentiment_counts_df.show()
    subjectivity_counts_df.show()