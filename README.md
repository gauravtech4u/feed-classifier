Feed Classifier

Feed Classifier Algorithm is based on  Naive Bayes classifier ( for theory - http://en.wikipedia.org/wiki/Naive_Bayes_classifier )

Dependencies

1. PYTHON  		- Language
2. MONGODB 		- NoSQL Database
3. PYMONGO 		- python module
4. FEEDPARSER 	- python module

How It Works

Add your training data in training_dict.py
File have TRAINING_DICT dictionary with key as category and values is list of Training words for each category. You can add word multiple time to increase the weight of the word for that category.

Add your feed Urls in crawl.py -> news_dict dictionary
You can add multiple urls for any site

Run python crawl.py
It will print a dictionary with key as category and value is no. of news attached to this category
Check in mongo now each news record have a key category_list with categories ordered according to their weights

Sample Data is already added where its needed. To test you simply need to run python crawl.py and check the result. 


