# coding: utf-8
# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au

import time
import pandas
import couchdb
import vincent

if __name__ == "__main__":
    start_time = time.time()
    dates_ITAvWAL = []
    db = couchdb.Server("http://localhost:5984/")['tweets']
    print(db)

    dates_ITAvWAL = []
    for item in db.view('_design/dabao/_view/content-time'):
        dates_ITAvWAL.append(item.value['created_at'])

    print('number of tweets:', len(dates_ITAvWAL))

    # a list of "1" to count the hashtags
    ones = [1] * len(dates_ITAvWAL)
    # the index of the series
    idx = pandas.DatetimeIndex(dates_ITAvWAL)
    # the actual series (at series of 1s for the moment)
    ITAvWAL = pandas.Series(ones, index=idx)

    # Resampling / bucketing
    # per_minute = ITAvWAL.resample('1Min', how='sum').fillna(0)
    per_minute = ITAvWAL.resample('30T').sum().fillna(0)

    # time_chart = vincent.Line(ITAvWAL)
    time_chart = vincent.Line(per_minute)

    time_chart.axis_titles(x='Time', y='Freq')
    time_chart.to_json('/share/app/visu/time_chart.json')
    time_chart.to_json('/share/app/web/webroot/data/time_chart.json')
    print("--- %s seconds ---" % (time.time() - start_time))

