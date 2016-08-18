# -*- coding: utf-8 -*-
__author__ = 'jason'

import json, sys, requests, random, time
from settings import File_config, proxy_http_list, args, parser
from ThreadUtils import ThreadPoolManager, RunConfig

start = time.clock()
header={
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'cookies':'bid=_OtrB0BbBJI; ll="118318"; gr_user_id=87bc83e6-ff84-4f4e-81e1-527ed4d7db2d; viewed="15851441_25851442_26248182_26812955_26812953_26812952"; _vwo_uuid_v2=0044EC5238D516B8BD00770546534503|75f28ad71c5696546f9bdab1dbd31304; ap=1; __utma=30149280.893089337.1466948560.1469514352.1469605348.7; __utmc=30149280; __utmz=30149280.1469514352.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'
        }
f1 = open(File_config['filename'], 'w+')
f2 = open(File_config['err_name'], 'w+')
f3 = open(File_config['success_name'], 'w+')
f4 = open(File_config['notfound_filename'], 'w+')
base_url ='api.douban.com/v2/' + args.api + '/'
count = 0


class RunDouban(RunConfig):
    def __init__(self):
        RunConfig.__init__(self)

    def request_data(self, tmp, id, pro_ip):
        response = requests.get(tmp + base_url + id, headers=header, proxies=pro_ip, timeout=10)
        print pro_ip,response.url, response.status_code
        return response

    """请求成功时将得到的数据写入f1文件对象中，并把成功的id写入f3文件"""
    def success_handle(self, response, id):
        data_dict = {'book_entity': ''}
        data_dict['book_entity'] = response.json()
        f1.write(json.dumps(data_dict)+'\n')
        f3.write(id+'\n')

    def get_proxyip(self):
        proxy_ip = ''
        proxy_index = 0
        while True:
            proxys = random.choice(proxy_http_list)
            if proxys[1] == True:
                proxy_ip = proxys[0]
                proxy_index = proxy_http_list.index(proxys)
                break
            elif proxys[1] == False:
                forbid_time = time.time() - proxys[2]
                if forbid_time >= 5400.0:
                    proxy_ip = proxys[0]
                    proxy_index = proxy_http_list.index(proxys)
                    break
        return proxy_ip, proxy_index

    """循环换ip请求，直到返回码为200或者404以及异常时退出循环"""
    def request_circle(self,argv):
            while True:
                pro_tuple = self.get_proxyip()
                pro_ip = pro_tuple[0]
                proxy_index = pro_tuple[1]
                tmp = 'http://'
                if (pro_ip.has_key('https')):
                    tmp = 'https://'
                response = self.request_data(tmp=tmp, id=argv[0], pro_ip=pro_ip)
                # 返回码是403时把代理ip列表中对应的ip标志位设为False
                if response.status_code == 403:
                    proxy_http_list[proxy_index][1] = False
                    proxy_http_list[proxy_index][2] = time.time()
                elif response.status_code == 200:
                    self.success_handle(response=response, id=argv[0])
                    proxy_http_list[proxy_index][1] = True
                    break
                # 返回码是404时把id写入对应的404文件
                elif response.status_code == 404:
                    proxy_http_list[proxy_index][1] = True
                    f4.write(argv[0]+'\n')
                    break
                else:
                    proxy_http_list[proxy_index][1] = True
                    pass

    def run(self, argv):
        try:
            # 循环换ip请求，直到返回码为200或者404以及异常时退出循环
            self.request_circle(argv=argv)

        except Exception, e:
            # 有异常出现时再执行两次
            try:
                self.request_circle(argv=argv)

            except Exception, e:
                try:
                    self.request_circle(argv=argv)
                except Exception, e:
                    print str(e)
                    f2.write(argv[0]+'\n')
        time.sleep(0.1)


def tasks(start, stop):
    return xrange(start,stop)


def run(start_point, stop_point, threadcount):
    start = time.time()
    print "start %s" % start
    config = RunDouban()
    config.setTask(tasks(start_point, stop_point))
    config.setThreadCount(threadcount)
    manager = ThreadPoolManager(config)
    try:
        manager.waitingForComplete()
    finally:
        f1.close()
        f2.close()
        f3.close()
        f4.close()
    end = time.time()
    print "cost all time: %s" % (end-start)


if __name__ == '__main__':
    if args.start is None or args.stop is None or args.thread is None or args.api is None:
        parser.print_help()
        sys.exit()
    print args.start, args.stop
    run(int(args.start), int(args.stop), threadcount=int(args.thread))

