# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
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

