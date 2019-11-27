from yahoo_historical import Fetcher
from itertools import islice
import codecs, time, random

with codecs.open('.\\data\\symbols.txt', mode='r', encoding='utf-8') as f:
    while True:
        lines = list(islice(f, 5))

        if not lines:
            break


        for qm in lines:
            try:
                hold = qm.replace('\r', '')
                hold = hold.replace('\n', '')
                data = Fetcher(hold, [2002,1,29], [2012,7,20])
                data.getHistorical().to_csv('.\\data\\%s.csv' % hold)
            except:
                pass
            time.sleep(10) #+ random.uniform(0, 1) * 20