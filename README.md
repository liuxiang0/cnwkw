# cnwkw

crawl the video (MP4 or m3u8) which is given resourceID

## 1 - Usage

python cnwkw.py id1 [id2, process_count]

will download all videos whose resourceID is between id1 and id2.

where 
- id1 and id2 are the resourceID
- process_count <= os.cpu_count()

## 2 - How to get resourceID

You can browse http://www.cnwkw.cn

http://www.cnwkw.cn/player/?resourceId=89900

keep the last number

## 3 - Configuration

you should modify the conf.py, tell python where to save videos

## 4 - M3U8 class

Ref [globocom/m3u8](https://github.com/globocom/m3u8)

## 5 - Contact

Emailto liuxiangxyd@163.com
