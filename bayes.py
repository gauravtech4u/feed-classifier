import operator, math, re


removelist=["a", "an", "as", "at", "before", "but", "by", "for", "from",
            "is", "in", "into", "like", "of", "off", "on", "onto", "per",
            "since", "than", "the", "this", "that", "to", "up", "via",
            "with","The","also","A","its"]


class TrainClassifier(object):

    def __init__(self,category=None,training_data={}):
        self.category=category
        self.training_data=training_data
        self.feature_count=0

    def train(self,word):
        word=word.lower()
        if self.training_data.get(word):
            self.training_data[word]+=1.00
        else:self.training_data[word]=1.00
        self.feature_count+=1.00

    def untrain(self,word):
        self.training_data.pop(word)
        self.feature_count-=1.00

    @classmethod
    def train_classifier(cls,category_dict={}):
        category_set=[]
        for category,feature_list in category_dict.items():
            obj=TrainClassifier(category=category)
            obj.training_data={}
            for feature in feature_list:
                obj.train(feature)
            category_set.append(obj)
        return category_set

class ConstructTrainingData(object):

    @classmethod
    def construct(cls,data,training_dict):
        data=re.sub("[(,),\",.,\,',]",'',data)
        word_list=set(data.split(' '))-set(removelist)
        for word in word_list:
            for category in training_dict.keys():
                training_dict[category].append(word)
                wordcount=training_dict[category].count(word)
                if wordcount > 5:
                    tempcount=0
                    temp_category_list=training_dict.keys()
                    temp_category_list.remove(category)
                    for cat in temp_category_list:
                        tempcount+=training_dict[cat].count(word)
                    if tempcount/len(temp_category_list) < 5:
                        for cat in training_dict:
                            training_dict[cat].remove(word)
        return training_dict


"""
   Formula Used - Consider Category Set S={S1,S2,....,Sm}
                  Training Set for each category F={f11,f12,....,f1n} for category S1
                  According to Naive Bayes Classifer, P(S1) = (p(S1)p(f11/S1)p(f12/S1)....p(f1n/S1)) / evidence
                  Here, evidence = p(S1)p(f11/S1)p(f12/S1)....p(f1n/S1) + p(S2)p(f11/S2)p(f12/S2)....p(f1n/S2) + .... + p(Sm)p(f11/Sm)p(f12/Sm)....p(f1n/Sm)
    
"""


class BayesClassifier(object):

    def __init__(self,category_set=[]):
        self.category_set=category_set

    def refine_data(self,data):
        data=re.sub("[(,),\",.,\,',]",'',data)
        word_list=set(data.split(' '))-set(removelist)
        doc_obj=TrainClassifier()
        doc_obj.training_data={}
        for word in word_list:
            doc_obj.train(word.lower())
        return doc_obj

    def find_posterior(self,data):
        doc_obj=self.refine_data(data)
        evidence_dict={}
        vocabulary_count=float(sum(map(lambda obj:obj.feature_count,self.category_set)))
        for category in self.category_set:
            PofWords,matchcount=0.0,0
            for word,wordcount in doc_obj.training_data.items():
                # laplace smoothing
                fetch_word=category.training_data.get(word.lower(),0.00)
                if fetch_word > 0.00:matchcount+=1
                testprop=(fetch_word+1.00)/(len(self.category_set)+vocabulary_count)

                PofWords+=wordcount*math.log(testprop)
            if matchcount > 0:evidence_dict[category.category]=math.exp(PofWords)
        sorted_list= sorted(evidence_dict.iteritems(), key=operator.itemgetter(1))
        sorted_list.reverse()
        doc_obj.category_list=sorted_list[:2]
        return doc_obj


