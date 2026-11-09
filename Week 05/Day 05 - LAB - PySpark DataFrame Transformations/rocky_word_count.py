import os
import re
import warnings
warnings.filterwarnings("ignore")

# Hide Spark/Java startup warnings in the terminal so only the result is shown
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 2)

import nltk
from nltk.corpus import stopwords
from pyspark.sql import SparkSession

# 1. Start SparkSession & SparkContext
spark = SparkSession.builder \
    .appName("Rocky_Article_Top5_Words") \
    .master("local[*]") \
    .getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# 2. Load NLTK English Stopwords ('the', 'is', 'and', 'to', 'a', etc.)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# 3. Read the local Rocky article (from https://en.wikipedia.org/wiki/Rocky)
article_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "article.txt")
article_rdd = sc.textFile(article_path)

# 4. Split lines into lowercase words (stripping punctuation & numbers)
words_rdd = article_rdd.flatMap(lambda line: re.findall(r'[a-z]+', line.lower()))

# 5. Top 5 Words AFTER removing NLTK stopwords
filtered_words_rdd = words_rdd.filter(lambda w: w not in stop_words)
word_kv = filtered_words_rdd.map(lambda w: (w, 1))
word_counts = word_kv.reduceByKey(lambda a, b: a + b)
top5_without_stopwords = word_counts.takeOrdered(5, key=lambda x: -x[1])

for word, count in top5_without_stopwords:
    print(f"({word},{count})")

spark.stop()
