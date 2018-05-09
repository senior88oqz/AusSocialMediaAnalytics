import couchdb
from topic import prepare_text_for_lda

db = couchdb.Server("http://localhost:5984/")['tweets']
print(db)

text_data = []
for item in db.view('_design/dabao/_view/content-time', limit=400000):
    # token = prepare_text_for_lda(item.value[0])
    # print(token)
   # print(item.value['row'])
    text_data.append(item.value['text'])

print('done, number of tweets: ',len(text_data))

