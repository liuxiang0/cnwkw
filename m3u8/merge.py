'''
merge.py - 处理 m3u8文件，下载分段视频格式(*.ts), 合并多段视频，输出一个MP4文件

method 1 - download(m3u, new_filename), 产生临时碎片文件

method 2 - save_m3u(m3u, new_filename), 内存中交换，不产生中间临时文件

m3u8是苹果公司推出一种视频播放标准，是m3u的一种，其编码方式是utf-8，是一种文件检索格式，将视频切割成一小段一小段的ts格式的视频文件，然后存在服务器中（现在为了减少I/o访问次数，一般存在服务器的内存中），通过m3u8解析出来路径，然后去请求。

'''


import os
import requests
import datetime
from shutil import rmtree   # 删除非空文件夹
from fake_useragent import UserAgent
from m3u8.model import M3U8


def download(m3u, savedfile):
    '''download(m3u, savedfile) - 下载分段视频，生成临时文件，保存在时间目录下，并合并成一个视频文件！

    param m3u: given m3u object from M3U8 class
        savedfile: output file name for saving video

    '''

    # 新建日期文件夹, 为了保存临时分段视频文件 *.ts
    download_path = os.path.join('', datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))  
    #%f	Microsecond as a decimal number, zero-padded on the left.(000000)
    #%f for dealing with error - FileExistsError: [WinError 183]
    # 当文件已存在时，无法创建该文件。: '20200312_055315'
    os.mkdir(download_path)

    # save all segment-ts-files into doanload_path directory
    ts_list = get_tslist(m3u.segments)   # include base_path
    download_ts(ts_list, download_path)

    # merge all ts-flies and save one video file name(mp4)
    merge_ts(m3u.files, savedfile, download_path)
    #delete temp ts file and its directory
    rmtree(download_path, ignore_errors=True)


def save_m3u(m3u, video_filename):
    ''' save_m3u(ts_list, video_filename): 下载所有碎片 ts 文件, 并合并成一个MP4文件: video_filename
    param ts_list:   all *.ts filename list including base_url
    result: merge all *.ts to one mp4 file under local disk
    '''

    ts_list = get_tslist(m3u.segments)
    # 伪装成浏览器访问，直接以爬虫方式访问web, 容易被拒绝！
    user_agent = UserAgent().random
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    header = {'User-Agent': user_agent}
    if os.path.isfile(video_filename):
        os.remove(video_filename)

    for ts in ts_list:   # read and merge ts files one by one
        resquest = requests.get(ts, headers=header)
        with open(video_filename, 'ab') as savedfile:  # must be 'ab',merge all ts files
            savedfile.write(resquest.content)  # save ts file
            #savedfile.flush()  no need this operation because of with ... as ...
            # 把文件从内存buffer（缓冲区）中强制刷新到硬盘中，同时清空缓冲区。此处不需要！


def get_tslist(segments):
    ''' Retrieve ts-file lists 获取 ts 文件列表 '''
  
    return [str(ts).rsplit('\n', 1)[-1] for ts in segments if str(ts).rstrip().endswith('.ts')]

def download_ts(ts_list, download_path):
    ''' down_ts(ts_list, download_path) - 下载所有碎片ts文件

    param ts_list:   all *.ts filename list
        download_path: the temp directory for saving ts files
    
    result: save all *.ts to local disk
    '''

    # 伪装成浏览器访问，直接以爬虫方式访问web, 容易被拒绝！
    user_agent = UserAgent().random
    header = {'User-Agent': user_agent}

    for ts in ts_list:   # read and save ts file one by one
        resquest = requests.get(ts, headers=header)
        with open(os.path.join(download_path, ts.rsplit('/', 1)[-1]), 'wb') as tsfile:
            tsfile.write(resquest.content)  # save ts file to local disk


def merge_ts(ts_list, vfile, download_path):
    ''' 合并多个 ts 文件成一个 mp4 文件 '''

    # loop for each piece file, then merge all ts into one video file
    if os.path.isfile(vfile):
        os.remove(vfile)

    for ts in ts_list:
        with open(os.path.join(download_path, ts), 'rb') as tsfile:
            with open(vfile, 'ab') as savedfile:  # must be 'ab'
                savedfile.write(tsfile.read())  # must using read()


if __name__ == '__main__': 
    user_agent = UserAgent().random
    header = {'User-Agent': user_agent}

    #url = 'http://video.cnwkw.cn/WeiKe/video/201606/1317/3aada1af15784a9db60ae35b1365b9c0-HD.m3u8'
    
    #_url = "http://video.cnwkw.cn/WeiKe/video/201711/1909/a5453e133c19433395868bc0c91a7fd4-HD.m3u8"

    #url = 'http://video.cnwkw.cn/WeiKe/video/201606/1122/e4ee0791acba4211a8836d23b9487c53-HD.m3u8'
    
    url = "http://video.cnwkw.cn/WeiKe/video/201606/1308/d0158bd0889c49cebf24a69f0d21edf1-HD.m3u8"

    base_path = url.rsplit('/',1)[0]
    all_content = requests.get(url, headers=header).text
    m3u = M3U8(all_content, base_path=base_path)
    save_m3u(m3u, 'testm3u.mp4')
    download(m3u, 'testmp4.mp4')

    '''
    elapsed_time1 = timeit.timeit(download(m3u, 'testmp4.mp4'), number=100)/100
    print(elapsed_time1)

    elapsed_time2 = timeit.timeit(save_m3u(m3u, 'testm3u.mp4'), number=100)/100
    print(elapsed_time2)
    print(elapsed_time1 > elapsed_time2)
    '''
