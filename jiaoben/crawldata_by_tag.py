# -*- coding: utf-8 -*-
import requests, json, time, sys
from tag_set import tag_list

reload(sys)
sys.setdefaultencoding('utf-8')


f1 = open('data.json', 'w+')
f2 = open('url.json', 'w+')
f3 = open('err_url.json', 'w+')
base_url = 'http://api.douban.com/v2/book/search?tag='
tag_list = tag_list

def get_data():
    module_name = 'books'
    data_dic_name = 'book_entity'
    url_1 = [(base_url + t +'&count=100&start=' ) for t in tag_list]
    for u in url_1:
        for i in xrange(0, 130000, 100):
            url = u + str(i)
            try:
                r = requests.get(url)
                print r.url, r.status_code

                if r.status_code == 200:
                    f2.write(url + ' '+str(r.status_code)+'\n')
                    data = r.json()[module_name]
                    if data:
                        for d in data:
                            dict_data = {data_dic_name:''}
                            dict_data[data_dic_name] = d
                            f1.write(json.dumps(dict_data) + '\n')

                    else:
                        break
                elif r.status_code == 403:
                    f3.write(url + ' '+str(r.status_code)+'\n')
                    print 'rest for an hour for 403'
                    time.sleep(3600)
                else:
                    f3.write(url + ' '+str(r.status_code)+'\n')
            except Exception, e:
                f3.write(url + '  '+str(e)+'\n')

            time.sleep(4)   # 每个标签的每个请求之间间隔4秒
        print 'rest for 10 mins'
        time.sleep(600)     # 每个标签之间间隔10分
        
if __name__ == '__main__':
    try:
        get_data()
    finally:
        f1.close()
        f2.close()
        f3.close()
