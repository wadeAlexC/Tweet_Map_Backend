from collections import Counter, defaultdict
import random
import re
import json
import pickle

binary=False


class Data:
    def __init__(self):
        #print 'starting...'
        self.weights=defaultdict()  #Counter() #"""""""


    def parse(self,line):
        # print line
        # words=re.split(' |.|. |-|/|#|,|, |\'' ,line)
        words = re.split(' |\n|\.|,|#|/|-', line)
        words = [word.lower() for word in words if (word and word[0] != '@' and word[0] != '\\' and word[0] != '&')]
        # print words
        return words


    '''def train(self):
        self.raw_bad = 'bad_corpus.txt'
        self.raw_good = 'good_corpus.txt'
        self.clean_bad = parser.raw2clean(self.raw_bad)
        self.clean_good = parser.raw2clean(self.raw_good)
        self.training_data = [(-1, tweet) for tweet in self.clean_good]
        self.training_data.extend([(1, tweet) for tweet in self.clean_bad])
        self.tfidf_training = parser.file_2_tf_idf(self.training_data)
        rho = 0.01
        maxit = 1000
        eta = 0.04
        T = range(len(self.tfidf_training))
        for it in range(maxit):
            error=0
            random.shuffle(T)
            for t in T:
                y, x = self.tfidf_training[t]
                pred_y=-1
                loss = self.dotprod(x)
                if loss>=1: pred_y=1
                if y != pred_y:
                    error+=1
                    self.update_Weights(eta*y, x,)
            if it % 50 == 0: print(it, it, it, error)
        #json.dump(self.weights, open("weights.txt", 'w'))
        with open('weights.txt', 'wb') as handle:
           pickle.dump(self.weights, handle)'''

    def eval(self):
        if not self.weights:
            #self.weights=json.load(open("weights.txt"))
            with open('weightsBigrams.txt', 'rb') as handle:
                self.weights = pickle.loads(handle.read())
        evaluated=list()
        #read tweets from Twitter
        test_data = self.tfidf_training #file_to_tf_idf(ftest)
        # f = open("h.out", 'w')
        for t in range(len(test_data)):
            id, x=test_data[t]
            pred_y = -1
            _, loss = self.dotprod(x)
            # f.write("%d\n" % pred_y)
            evaluated.append((id,pred_y))
        json.dump(evaluated, open("evaluated.txt", 'w'))
        #with open('file.txt', 'wb') as handle:
         #   pickle.dump(a, handle)

    def evalFromJson(self, book):
        if not self.weights:
            #self.weights=json.load(open("weights.txt"))
            with open('weights.txt', 'rb') as handle:
                self.weights = pickle.loads(handle.read())
        blacklist=defaultdict()
        for tw in book['statuses']:
            author=tw['user']['screen_name']
            raw_text=tw['text']
            text=set(self.parse(raw_text))
            y=self.score(text)
            if y>=1:
                if author not in blacklist:
                    blacklist[author]=[raw_text]
                else:
                    blacklist[author].append(raw_text)
        return blacklist

    def score(self,text):
        num = 0.0
        for token in text:
            if token in self.weights:
                num+=self.weights[token]
        return num


    def dotprod(self, x):
        """print 'x,', type(x), x
        print 'w,' , self.weights
        print 'kk'"""
        num = 0.0
        for k, v in x.items():
            #print 'gg'
            if binary: v=1
            if k in self.weights: num += v * self.weights[k]
        return num

    def update_Weights(self, scale, x):
        for token, value in x.items():
            self.weights.setdefault(token, 0)
            if binary: value=1
            self.weights[token] +=  scale * value

