from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from pymongo import MongoClient
import pandas as pd

# documents = ["This little kitty came to play when I was eating at a restaurant.",
#              "Merley has the best squooshy kitten belly.",
#              "Google Translate app is incredible.",
#              "If you open 100 tab in google you get a smiley face.",
#              "Best cat photo I've ever taken.",
#              "Climbing ninja cat.",
#              "Impressed with google map feedback.",
#              "Key promoter extension for Google Chrome."]
#
# vectorizer = TfidfVectorizer(stop_words='english')
# X = vectorizer.fit_transform(documents)
#
# true_k = 2
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
# model.fit(X)
#
# print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i),
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind]),
#     print
#
# print("\n")
# print("Prediction")
#
# Y = vectorizer.transform(["chrome browser to open."])
# prediction = model.predict(Y)
# print(prediction)
#
# Y = vectorizer.transform(["My cat is hungry."])
# prediction = model.predict(Y)
# print(prediction)




client = MongoClient('localhost', 27017)

DB_SOLCODE = client.DB_SOLCODE


COLL_URL = DB_SOLCODE.COLL_URL
COLL_SOL = DB_SOLCODE.COLL_SOL
COLL_ABI = DB_SOLCODE.COLL_ABI
COLL_BYTE = DB_SOLCODE.COLL_BYTE
COLL_BZZR = DB_SOLCODE.COLL_BZZR
COLL_CHECK = DB_SOLCODE.COLL_CHECK


documents = []
n = 1

for i in COLL_SOL.find():
    documents.append(i['SOLCODE'])
    n += 1
    if n == 2100:
        break

# print documents[1]

train = documents
test = documents
# print len(documents)

vectorizer = TfidfVectorizer(stop_words=[
    'bytes32','function','the','if','_hash','hash','o_hash',
    'to','of','uint','value','param','address','data',
    'owners','owner','id','public','uint256','assert',
    'new_owner','holders','holder','myid','datasource',
    'string','_b','_a','2017','08','22','00','10000',
    '_amount','_token','token','tokens','contract','_to'
    'balances','balance','_h','_value','free','_from',
    'external','return','m_owners','m_numowners','ownerindex',
    '_to','m_ownerindex','operation','_operation','limit','return','returns',
    'msg','today','methods','_r','transaction','transactions','count','_owners',
    'balances','_to','constant','10','_required','for','dev','and','else',
    'an','in','be','this','is','bytes','_data','just','users','length','user',
    '100','bool','uint128','index','default','define'

                              ])
X = vectorizer.fit_transform(train)

true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :30]:
        print(' %s' % terms[ind]),
    print


print("\n")
print("Prediction")

pred_class = []
for i in test:
    Y = vectorizer.transform([i])
    prediction = model.predict(Y)
    pred_class.append(prediction)

pred_class = pd.DataFrame({'pred_class':pred_class})
num_class = pred_class['pred_class'].value_counts().sort_index()
print num_class




