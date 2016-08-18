# -*- coding: utf-8 -*-
import json, time, re, sys
reload(sys)
sys.setdefaultencoding('utf-8')

def clear_song(song_name):
    """对歌名做清理，去除多余字符"""
    #print song_name
    song_name = song_name.strip('0123456789.-:、')
    dirty_zifu = [u'\u2022', u'\u2013']   #-再［］中一定要放在最后，除非是表示范围
    for d in dirty_zifu:
        song_name = re.sub(d, '', song_name).strip()
    if '「'  in song_name and '」' in song_name:
        song_name = song_name[song_name.index('「')+1:song_name.index('」')]
    if '(' in song_name:
        song_name = song_name[:song_name.index('(')]


    #print song_name
    return song_name


def music_handle():
    """对音乐原始数据处理提取每个专辑的所有单曲"""
    f_music = open('/Users/jason/Desktop/douban_music/douban_music002.json', 'r')
    music_file  = open('/Users/jason/Desktop/douban_music/douban_song_002.json','w+')
    movies = f_music.readlines()
    try:
        for m in movies:
            try:
                m_dic = {'song_name':'', 'singer':'', 'zhuanji':'', 'concept':u'音乐类型',}
                new_m = json.loads(m)
                if new_m['music_entity']['attrs'].has_key('tracks'):
                    songs = new_m['music_entity']['attrs']['tracks'][0]
                    s = songs.split('\n')
                    for i in s:
                        m_dic['song_name'] = clear_song(i)
                        if new_m['music_entity']['attrs'].has_key('singer'):
                            m_dic['singer'] = new_m['music_entity']['attrs']['singer'][0]
                        m_dic['zhuanji'] = new_m['music_entity']['title']
                        music_file.write(json.dumps(m_dic) + '\n')
            except Exception,e:
                print str(e)
                print m

    finally:
        f_music.close()
        music_file.close()

start = time.clock()
print 'starting'
music_handle()
end = time.clock()
print end - start
