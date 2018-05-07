import couchdb
from topic import prepare_text_for_lda

db = couchdb.Server("http://localhost:5984/")['tweets']
print(db)

text_data = []
for item in db.view('_design/allan/_view/content-time', limit=10):
    # token = prepare_text_for_lda(item.value[0])
    # print(token)
    token = prepare_text_for_lda(item.value['text'])
    print(item.value['created_at'])


