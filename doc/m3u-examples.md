# HLS - HTTP Live Streaming

[HLS （HTTP Live Streaming）](draft-pantos-http-live-streaming-16.pdf), 是由 Apple 公司实现的基于 HTTP 的媒体流传输协议。`HLS`以`ts`为*传输格式*，`m3u8`为*索引文件*（文件中包含了所要用到的`ts`文件名称，时长等信息，可以用播放器播放，也可以用vscode之类的编辑器打开查看），在移动端大部分浏览器都支持，也就是说你可以用video标签直接加载一个`m3u8`文件播放视频或者直播，但是在 PC 端，除了苹果的 Safari，需要引入库来支持。
用到此方案的视频网站比如*优酷*，可以在视频播放时通过调试查看`Network`里的`XHR`请求，会发现一个`m3u8`文件，和每隔一段时间请求几个`ts`文件。


# MPEG DASH - Dynamic Adaptive Streaming over HTTP

但是除了`HLS`，还有Adobe的`HDS`，微软的`MSS`，方案一多就要有个标准点的东西，于是就有了`MPEG DASH`。
`DASH（Dynamic Adaptive Streaming over HTTP）`，是一种在互联网上传送动态码率的Video Streaming技术，类似于苹果的`HLS`，`DASH`会通过`media presentation description (MPD)`将视频内容切片成一个很短的文件片段，每个切片都有多个不同的码率，`DASH Client`可以根据网络的情况选择一个码率进行播放，支持在不同码率之间无缝切换。
`Youtube，B`站都是用的这个方案。这个方案索引文件通常是`mpd`文件（类似`HLS`的`m3u8`文件功能），传输格式推荐的是`fmp4（Fragmented MP4）`, 文件扩展名通常为`.m4s`或直接用`.mp4`。所以用调试查看b站视频播放时的网络请求，会发现每隔一段时间有几个`m4s`文件请求。


# 8.  Playlist Examples for m3u

## 8.1.  Simple Media Playlist

~~~example1
    #EXTM3U
    #EXT-X-TARGETDURATION:10
    #EXTINF:9.009,
    http://media.example.com/first.ts
    #EXTINF:9.009,
    http://media.example.com/second.ts
    #EXTINF:3.003,
    http://media.example.com/third.ts
    #EXT-X-ENDLIST
~~~

~~~from cnwkw.cn
    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-TARGETDURATION:15
    #EXT-X-MEDIA-SEQUENCE:0
    #EXTINF:14.900000,
    210082d80e31406b894b7367e55b4fe1-LD-00001.ts
    #EXTINF:6.166667,
    210082d80e31406b894b7367e55b4fe1-LD-00002.ts
    #EXTINF:13.833333,
    210082d80e31406b894b7367e55b4fe1-LD-00003.ts
    #EXTINF:9.966667,
    210082d80e31406b894b7367e55b4fe1-LD-00004.ts
    #EXTINF:9.033333,
    210082d80e31406b894b7367e55b4fe1-LD-00005.ts
    #EXTINF:10.000000,
    210082d80e31406b894b7367e55b4fe1-LD-00006.ts
    #EXTINF:8.133333,
    210082d80e31406b894b7367e55b4fe1-LD-00007.ts
    #EXTINF:10.000000,
    210082d80e31406b894b7367e55b4fe1-LD-00008.ts
    #EXTINF:9.133333,
    210082d80e31406b894b7367e55b4fe1-LD-00009.ts
    #EXTINF:8.833333,
    210082d80e31406b894b7367e55b4fe1-LD-00010.ts
    #EXTINF:10.333333,
    210082d80e31406b894b7367e55b4fe1-LD-00011.ts
    #EXTINF:9.166667,
    210082d80e31406b894b7367e55b4fe1-LD-00012.ts
    #EXTINF:1.533333,
    210082d80e31406b894b7367e55b4fe1-LD-00013.ts
    #EXT-X-ENDLIST
~~~

## 8.2.  Live Media Playlist, using HTTPS

    #EXTM3U
    #EXT-X-VERSION:3
    #EXT-X-TARGETDURATION:8
    #EXT-X-MEDIA-SEQUENCE:2680

    #EXTINF:7.975,
    https://priv.example.com/fileSequence2680.ts
    #EXTINF:7.941,
    https://priv.example.com/fileSequence2681.ts
    #EXTINF:7.975,
    https://priv.example.com/fileSequence2682.ts

## 8.3.  Playlist with encrypted Media Segments

      #EXTM3U
      #EXT-X-VERSION:3
      #EXT-X-MEDIA-SEQUENCE:7794
      #EXT-X-TARGETDURATION:15
      #EXT-X-KEY:METHOD=AES-128,URI="https://priv.example.com/key.php?r=52"
      #EXTINF:2.833,
      http://media.example.com/fileSequence52-A.ts
      #EXTINF:15.0,
      http://media.example.com/fileSequence52-B.ts
      #EXTINF:13.333,
      http://media.example.com/fileSequence52-C.ts
      #EXT-X-KEY:METHOD=AES-128,URI="https://priv.example.com/key.php?r=53"
      #EXTINF:15.0,
      http://media.example.com/fileSequence53-A.ts

## 8.4.  Master Playlist

      #EXTM3U
      #EXT-X-STREAM-INF:BANDWIDTH=1280000,AVERAGE-BANDWIDTH=1000000
      http://example.com/low.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=2560000,AVERAGE-BANDWIDTH=2000000
      http://example.com/mid.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=7680000,AVERAGE-BANDWIDTH=6000000
      http://example.com/hi.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=65000,CODECS="mp4a.40.5"
      http://example.com/audio-only.m3u8

## 8.5.  Master Playlist with I-Frames

      #EXTM3U
      #EXT-X-STREAM-INF:BANDWIDTH=1280000
      low/audio-video.m3u8
      #EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=86000,URI="low/iframe.m3u8"
      #EXT-X-STREAM-INF:BANDWIDTH=2560000
      mid/audio-video.m3u8
      #EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=150000,URI="mid/iframe.m3u8"
      #EXT-X-STREAM-INF:BANDWIDTH=7680000
      hi/audio-video.m3u8
      #EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=550000,URI="hi/iframe.m3u8"
      #EXT-X-STREAM-INF:BANDWIDTH=65000,CODECS="mp4a.40.5"
      audio-only.m3u8

## 8.6.  Master Playlist with Alternative audio

   In this example, the CODECS attributes have been condensed for space.
   A '\' is used to indicate that the tag continues on the following
   line with whitespace removed:

      #EXTM3U
      #EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aac",NAME="English", \
         DEFAULT=YES,AUTOSELECT=YES,LANGUAGE="en", \
         URI="main/english-audio.m3u8"
      #EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aac",NAME="Deutsch", \
         DEFAULT=NO,AUTOSELECT=YES,LANGUAGE="de", \
         URI="main/german-audio.m3u8"
      #EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aac",NAME="Commentary", \
         DEFAULT=NO,AUTOSELECT=NO,LANGUAGE="en", \
         URI="commentary/audio-only.m3u8"
      #EXT-X-STREAM-INF:BANDWIDTH=1280000,CODECS="...",AUDIO="aac"
      low/video-only.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=2560000,CODECS="...",AUDIO="aac"
      mid/video-only.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=7680000,CODECS="...",AUDIO="aac"
      hi/video-only.m3u8
      #EXT-X-STREAM-INF:BANDWIDTH=65000,CODECS="mp4a.40.5",AUDIO="aac"
      main/english-audio.m3u8

## 8.7.  Master Playlist with Alternative video

   This example shows 3 different video Renditions (Main, Centerfield
   and Dugout), and 3 different Variant Streams (low, mid and high).  In
   this example, clients that did not support the EXT-X-MEDIA tag and
   the VIDEO attribute of the EXT-X-STREAM-INF tag would only be able to
   play the video Rendition "Main".

   Since the EXT-X-STREAM-INF tag has no AUDIO attribute, all video
   Renditions would be required to contain the audio.

   In this example, the CODECS attributes have been condensed for space.
   A '\' is used to indicate that the tag continues on the following
   line with whitespace removed:

      #EXTM3U
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="low",NAME="Main", \
         DEFAULT=YES,URI="low/main/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="low",NAME="Centerfield", \
         DEFAULT=NO,URI="low/centerfield/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="low",NAME="Dugout", \
         DEFAULT=NO,URI="low/dugout/audio-video.m3u8"

      #EXT-X-STREAM-INF:BANDWIDTH=1280000,CODECS="...",VIDEO="low"
      low/main/audio-video.m3u8

      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="mid",NAME="Main", \
         DEFAULT=YES,URI="mid/main/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="mid",NAME="Centerfield", \
         DEFAULT=NO,URI="mid/centerfield/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="mid",NAME="Dugout", \
         DEFAULT=NO,URI="mid/dugout/audio-video.m3u8"

      #EXT-X-STREAM-INF:BANDWIDTH=2560000,CODECS="...",VIDEO="mid"
      mid/main/audio-video.m3u8

      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="hi",NAME="Main", \
         DEFAULT=YES,URI="hi/main/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="hi",NAME="Centerfield", \
         DEFAULT=NO,URI="hi/centerfield/audio-video.m3u8"
      #EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID="hi",NAME="Dugout", \
         DEFAULT=NO,URI="hi/dugout/audio-video.m3u8"

      #EXT-X-STREAM-INF:BANDWIDTH=7680000,CODECS="...",VIDEO="hi"
      hi/main/audio-video.m3u8


## 8.8.  Session Data in a Master Playlist

   In this example, only the EXT-X-SESSION-DATA is shown:

      #EXT-X-SESSION-DATA:DATA-ID="com.example.lyrics",URI="lyrics.json"

      #EXT-X-SESSION-DATA:DATA-ID="com.example.title",LANGUAGE="en", \
         VALUE="This is an example"
      #EXT-X-SESSION-DATA:DATA-ID="com.example.title",LANGUAGE="sp", \
         VALUE="Este es un ejemplo"