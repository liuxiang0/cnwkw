"""
cnwkw.py - 下载 www.cnwkw.cn 的视频（LD 流畅，SD 标清，HD 高清），包括
           m3u8-苹果公司推出的视频播放标准格式 或 MP4 格式

Downloading minor lesson video in www.cnwkw.cn which is free to get from iclassmate (心意答资源平台)

视频分辨率包括 LD-lower definition（流畅）, SD-standard definition（标清）, HD-high definition（高清）

"""


import re
from bs4 import BeautifulSoup as BS 
import urllib
from sys import argv
from time import localtime
from fake_useragent import UserAgent

from m3u8 import M3U8
from m3u8.merge import save_m3u, download
import conf

# define global variables
TXT_dir = conf.T_dir
LD_dir = conf.L_dir
SD_dir = conf.S_dir
HD_dir = conf.H_dir
MP_dir = conf.M_dir


def video_file(resourceID, definition):
    resid = str(resourceID)
    if definition == '高清':
        return HD_dir + resid + '-HD.mp4'
    elif definition == '标清':
        return SD_dir + resid + '-SD.mp4'
    elif definition == '流畅':
        return LD_dir + resid + '-LD.mp4'
    else:
        return MP_dir + resid + '.mp4'


def web_parser(url):
    '''web_parser(url) - 解析给定的视频链接，得到 分段视频 web 链接列表，供视频下载过程使用。
    
    param url: website for crawling, just like `http://www.cnwkw.cn/player?resourceId=[number]`
               where [number] is a valid integer

    return resID, video_list: videos list for downloading, resID for saving video file name.

    '''

    # 匹配 resourceId= 后面的数字(match resourceId tag)
    pattern = re.compile(r'(?<=resourceId=)\d+\.?\d*')
    numberID = pattern.findall(url)[0]

    # 伪装成浏览器访问，直接以爬虫方式访问web, 容易被拒绝！随机产生变化的UA
    ua = UserAgent().random
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    headers = {'User-Agent': ua}
    
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        page_content = response.read()
        # use 'html.parser' to retrieve web page
        soup = BS(page_content, 'html.parser', from_encoding='utf-8')
        response.close()
        # 分解视频文件网址, www.cnwkw.cn 有关的tag = '<li> ... </li>'
        videos_li = soup.find_all('li')
    except Exception as e:
        #raise BaseException("Unknown error: no done for resourceID={0}".format(numberID))
        print("ERROR {0}, Unknown ERR: NO done for resourceID={1}".format(e, numberID))
        return numberID, None

    try:  
        # get('medias')标签保存了视频链接信息
        temp = videos_li[0]['medias']
        temp = temp.replace('null', '')  # delete null
        temp = temp.replace(',,', '')  # replace successive null, we get ',,' 
        video_list = eval(temp)
    except Exception:  
        # include KeyError, NameError, SyntaxError (984, 1010)
        print('EVAL ERROR: skip resourceID={0}'.format(numberID))
        return numberID, None

    # 获取视频文件属性, 并保存为文本文件
    title = soup.h1.string  # 标题
    tag_span = soup.find_all('span', {'class': ['color1', 'user-color', 'colors1']})
    video_attr = {'标题': title}
    for i in range(0, 18, 2):
        video_attr[tag_span[i].string] = tag_span[i+1].string
        # grade = # 年级 course = # 科目 count = # 播放量 book = # 教材 
        # chapter = # 章节 ttype = # 分类 knowledge = # 知识点

    # TODO：how to download qrcode?

    # TODO: file attributes can be saved into database
    with open(TXT_dir + numberID+'.txt', 'w') as fileattr:
        fileattr.write(str(video_attr))
        
    return numberID, video_list


def vido_download(num, videolist):
    '''下载视频文件，cnwkw.cn 网站上的视频分为 '流畅-LD' '标清-SD' '高清-HD'，
    param num, videolist: numberID and video links list
    '''

    print("ResourceID: {0}".format(num))
    for video in videolist:
        # similiar to dict
        # {'definition': '流畅', 'format': 'mp4', 'url': 
        # 'http://video.cnwkw.cn/WeiKe/video/201506/0215/928c9efb778f4c598449401f984603ca-LD.mp4'}
        # {'definition': '高清', 'format': 'm3u8', 'url': 
        # 'http://video.cnwkw.cn/WeiKe/video/201710/1008/d9557690d81e4287a6fc3d41e39e05cf-HD.m3u8'}

        filename = video['url'].split('/')[-1]  # 解析内部文件名
        #suffix = video['url'].split('-')[-1]  # 解析文件名后缀，含分辨率 LD，SD，HD和文件格式

        print("Definition: {0}, Format: {1}, Filename: {2}, ...".format(video['definition'], video['format'], filename))
        
        # KEY: Copy a network object to a local file by using urllib.request.urlretrieve(URL, local_filename)
        
        # '高清' 视频（多为 m3u8 播放格式）下载, 可以借鉴 u3u8 module(from model.py)
        if video['format'].lower() == 'm3u8':
            url = video['url']
            base_path = url.rsplit('/',1)[0]
            request = urllib.request.Request(url, headers={'User-Agent': UserAgent().random})
            response = urllib.request.urlopen(request)
            all_content = response.read()  # return 'bytes-object'
            all_content = all_content.decode('utf-8')  # return 'string' after decoding by 'utf-8'
            response.close()
            #all_content = requests.get(url, headers=header).text  # replaced by Request/urlopen

            # 通过文本内容，调用m3u8模块中的类M3U8，和save_m3u过程
            m3u = M3U8(all_content, base_path=base_path)
            m3u_filename = video_file(num, video['definition'])
            #print("M3U Fielname: {0}".format(m3u_filename))
            save_m3u(m3u, m3u_filename)
            #download(num, video['definition'], video['url'])
        elif video['format'].lower() == 'mp4':
            mp4_filename = video_file(num, video['definition'])
            print('MP4 Filename: {0}'.format(mp4_filename))
            #urllib.request.urlretrieve(video['url'], mp4_filename)
            #MP_dir + num+'-'+suffix)  #'.'+video['format'])
        else:
            print("Unknown video format {0} in URL {1}".format(video['fromat'], video['url']))

def cnwkw(url):
    '''下载给定网址上的有效视频文件 from www.cnwkw.cn    '''
    # 1. parser video list
    num, videos = web_parser(url)
    # 2. download video
    if videos:
        vido_download(num, videos)


def vdown(low=1, upper=10):  #, step=1):
    ''' 下载 心意答资源平台的微视频课程
    param low, upper: 定义了需要下载视频的序号上下限
    output： 保存视频为本地文件
    '''
    urls = ["http://www.cnwkw.cn/player?resourceId={0}".format(i) for i in range(low, upper+1)]  #, step
    #indx = low

    for url in urls:
        #print("Index: {0}, URL: {1}".format(indx, url))
        cnwkw(url)
        #indx += 1


def pool_down(low=1, upper=10, process=5):
    ''' pool_down() - Multiprocessing download, 多线程下载，可以提高下载效率。

    '''
    from multiprocessing import Pool

    urls = ["http://www.cnwkw.cn/player?resourceId={0}".format(i) for i in range(low, upper+1)]
    # 根据机器性能调整数字5，不要大于机器 CPU核数(os.cpucount()), 我的台式机是 单CPU 6核。
    with Pool(process) as pool:
        pool.map(cnwkw, urls)  # 阻塞
        #pool.apply_async(cnwkw, urls)  # 非阻塞，有问题 TODO
        #pool.map_async(cnwkw, urls)  # same as apply_async, faster than map/apply


def get_localtime():
    ctime = localtime()
    return "{0}-{1}-{2} {3}:{4}:{5}".format(ctime.tm_year, ctime.tm_mon, ctime.tm_mday, ctime.tm_hour, ctime.tm_min, ctime.tm_sec)


if __name__ == '__main__':
    if len(argv) > 2:
        if len(argv) == 3:
            process = 5
        else:
            process = (int(argv[3]) if argv[3].isnumeric else 5)

        arg1, arg2 = int(argv[1]), int(argv[2])
        lower, upper = min(arg1, arg2), max(arg1, arg2)
        print("开始 - Start at {0}".format(get_localtime()))
        if process > 0:
            pool_down(lower, upper, process)
        else:  # process==0
            vdown(lower, upper)
        print("结束 - End at {0}".format(get_localtime()))

    elif len(argv) == 2:
        lower = int(argv[1])
        print("开始 - Start at {0}".format(get_localtime()))
        vdown(lower, lower)  # one video with resourceId=lower will be downloaded
        print("结束 - End at {0}".format(get_localtime()))

    else:
        print("使用说明 - Python cnwkw.py resourceId_From [resourceId_To, process]")
 