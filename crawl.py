import feedparser, re, unicodedata
from models import CollectionMapping
from bayes import BayesClassifier, TrainClassifier, ConstructTrainingData


news_training_dict={
    "apple":["apple","mac","iphone","ipads","steve"],
    "android":["samsung","os","tablet"],
    "yahoo":["yahoo","marissa","news"],
    "youtube":["youtube","movies","streaming",],
    "google":["google","search",],
    "skype":["skype","call","conference"],
    "windows":["microsoft","gates","windows","windows"],
    "nokia":["nokia","mobile","smartphones","nokia"],
    "samsung":["samsung","mobile","smartphones","samsung"],
    "facebook":["facebook","facebook","social","zukerberg"],
    "htc":["htc","android","htc","smartphone","phone"],
    }

news_dict={
    "news_news":{
        'wired.com':['http://feeds.wired.com/wired/index'],
        'mit.edu':['http://web.mit.edu/newsoffice/topic/mathematics.feed','http://web.mit.edu/newsoffice/science.feed','http://web.mit.edu/newsoffice/engineering.feed'],
        'siliconrepublic.com':['http://www.siliconrepublic.com/feeds/'],
        'zdnet.com':['http://www.zdnet.com/news/rss.xml'],
        'computerweekly.com':['http://www.computerweekly.com/rss/All-Computer-Weekly-content.xml'],
        'geek.com':['http://www.geek.com/feed/'],
        'cnet.com':['http://feeds.feedburner.com/cnet/tcoc?format=xml'],
        'SiliconIndia.com':['http://feeds.feedburner.com/sitechnews?format=xml'],
        'technologyreview.com':['http://feeds.technologyreview.com/technology_review_top_stories'],
        'slashdot.org':['http://rss.slashdot.org/Slashdot/slashdot'],
        },

}
removelist=["a", "an", "as", "at", "before", "but", "by", "for", "from",
            "is", "in", "into", "like", "of", "off", "on", "onto", "per",
            "since", "than", "the", "this", "that", "to", "up", "via",
            "with","own","here","there","where","no","yes","and","Are","What","what","Which","which","list","week","was"]


def slugify(data):
    slug = unicode(re.sub('[^\w\s-]', '', data).strip().lower())
    slug=re.sub('[-\s]+', '-', slug)
    return slug

def parse_data(tablename,site,url_list):
    for url in url_list:
        data=feedparser.parse(url)
        for news in data.entries:
            title=news['title']
            link=news['link']
            try:
                description=news['content'][0]['value']
                description=re.sub('<.*>','',description)

            except:
                description=news['summary']
            description=re.sub('<.*>','',description)
            slug=slugify(title)
            collection_obj=CollectionMapping(tablename)
            collection_obj.load_json({'site':site,'slug':slug,'name':title,'description':description,'link':link,})

if __name__ == "__main__":

    # delete old news
    CollectionMapping('news_news').delete_all()
    CollectionMapping('news_category').delete_all()
    # fetch news feed
    for tablename, url_dict in news_dict.items():
        for site,url in url_dict.items():
            parse_data(tablename,site,url)
    # add training data
    category_set=TrainClassifier.train_classifier(news_training_dict)
    category_dict=dict([(slugify(category),1) for category in news_training_dict.keys()])
    # classify each document 
    for news in CollectionMapping('news_news').objects.all():
        bayes_obj=BayesClassifier(category_set)
        # returns each obj with category_list attribute ordered according to their score
        obj=bayes_obj.find_posterior("%s %s"%(news.name,news.description))
        news.update(category_list=map(lambda category:category[0],obj.category_list))
        for category,score in obj.category_list:category_dict[category]+=1
    category_obj=CollectionMapping('news_category')
    category_obj.save(type="education",category=category_dict)

