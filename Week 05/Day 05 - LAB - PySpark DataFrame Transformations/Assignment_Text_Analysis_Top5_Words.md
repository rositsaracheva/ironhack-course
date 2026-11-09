# Week 05 - Day 05: Class Assignment — Real-World Text Analysis in Spark (Top 5 Words)

> **Assignment for today:**
> - **Text analysis in real world → Frequency of words:** Find out any article of your interest. Return top 5 words.
> - **Guessing what the article is about:** Exclude prepositions (`is`, `the`, `and`, so on).
> - **In English it is known as stop words:** Use the **NLTK list of stopwords** → (exclude these).
> - **Use Spark based on this logic.**

---
## Steps I followed :

## 1. Selected Article: *Rocky* (1976 Film)

- **Source Link**: https://en.wikipedia.org/wiki/Rocky
- **Local Text File**: [article.txt](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2005/Day%2005%20-%20LAB%20-%20PySpark%20DataFrame%20Transformations/article.txt) (Intro + Plot summary from the Wikipedia article, 5,506 characters)
- **Runnable PySpark Script**: [rocky_word_count.py](file:///Users/rosi/Documents/IronHack%20Course%20/Week%2005/Day%2005%20-%20LAB%20-%20PySpark%20DataFrame%20Transformations/rocky_word_count.py)

---

## 2. PySpark Code & Terminal Output

```python
import os
import re
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

print("Top 5 words (WITHOUT NLTK stopwords):", top5_without_stopwords)
spark.stop()
```

### Terminal Output

```text
=================================================================
SOURCE ARTICLE: https://en.wikipedia.org/wiki/Rocky (article.txt)
=================================================================
Top 5 words (WITHOUT NLTK stopwords): [('rocky', 33), ('apollo', 13), ('film', 11), ('fight', 9), ('stallone', 6)]
=================================================================
```

---

## 3. Scala Execution & Terminal Output (`spark-shell`)

```scala
scala> import org.apache.spark.ml.feature.StopWordsRemover

scala> val stopWords = StopWordsRemover.loadDefaultStopWords("english").toSet
scala> val articleRdd = sc.textFile("article.txt")
val articleRdd: org.apache.spark.rdd.RDD[String] = article.txt MapPartitionsRDD[1] at textFile at <console>:1

scala> val cleanRdd = articleRdd.map(_.toLowerCase.replaceAll("[^a-z]", " "))
val cleanRdd: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[2] at map at <console>:1

scala> val wordsRdd = cleanRdd.flatMap(_.split("\\s+")).filter(_.nonEmpty)
val wordsRdd: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[4] at filter at <console>:1

scala> val filteredWords = wordsRdd.filter(w => !stopWords.contains(w))
val filteredWords: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[5] at filter at <console>:1

scala> val wordKv = filteredWords.map(w => (w, 1))
val wordKv: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[6] at map at <console>:1

scala> val wordCounts = wordKv.reduceByKey((a, b) => a + b)
val wordCounts: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[7] at reduceByKey at <console>:1

scala> val top5 = wordCounts.sortBy(_._2, ascending = false).take(5)
val top5: Array[(String, Int)] = Array((rocky,33), (apollo,13), (film,11), (fight,9), (stallone,6))

scala> top5.foreach(println)
(rocky,33)
(apollo,13)
(film,11)
(fight,9)
(stallone,6)
```

---

## 4. Top 5 Words Summary

| Rank | Word (Excluding NLTK Stopwords) | Count |
| :---: | :--- | :---: |
| **1** | **`rocky`** | 33 |
| **2** | **`apollo`** | 13 |
| **3** | **`film`** | 11 |
| **4** | **`fight`** | 9 |
| **5** | **`stallone`** | 6 |

