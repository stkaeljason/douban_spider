# -*- coding: utf-8 -*-
import random
"""生成器的高级用法，将来理解"""
def get_data():
    """返回0到9之间的3个随机数"""
    return random.sample(range(10), 3)

def consume():
    """显示每次传入的整数列表的动态平均值"""
    running_sum = 0
    data_items_seen = 0

    while True:
        data = yield
        data_items_seen += len(data)
        running_sum += sum(data)
        print('The running average is {}'.format(running_sum / float(data_items_seen)))

def produce(consumer):
    """产生序列集合，传递给消费函数（consumer）"""
    while True:
        data = get_data()
        print('Produced {}'.format(data))
        consumer.send(data)
        yield

if __name__ == '__main__':
    consumer = consume()
    consumer.send(None)  # send是生成器的内建函数
    producer = produce(consumer)


    for _ in range(10):
        print('Producing...')
        next(producer)  # next()是python的内建函数，用来获取迭代器的下个值