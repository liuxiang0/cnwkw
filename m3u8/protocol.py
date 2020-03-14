# coding: utf-8
# Ref [m3u playlist tags](https://tools.ietf.org/html/draft-pantos-http-live-streaming-16#section-4.3)

# Basic tags
extm3u = '#EXTM3U'
ext_x_version = '#EXT-X-VERSION'

# Media segment tags
extinf = '#EXTINF'  #EXTINF:<duration>[,<title>]
ext_x_byterange = '#EXT-X-BYTERANGE'  #EXT-X-BYTERANGE:<n>[@<o>]
ext_x_discontinuity = '#EXT-X-DISCONTINUITY'
ext_x_key = '#EXT-X-KEY'   #EXT-X-KEY:<attribute-list>
ext_x_map = '#EXT-X-MAP'   #EXT-X-MAP:<attribute-list>
ext_x_program_date_time = '#EXT-X-PROGRAM-DATE-TIME'   #EXT-X-PROGRAM-DATE-TIME:<YYYY-MM-DDThh:mm:ssZ>

# Media playlist tags
ext_x_targetduration = '#EXT-X-TARGETDURATION'   #EXT-X-TARGETDURATION:<s>
ext_x_media_sequence = '#EXT-X-MEDIA-SEQUENCE'   #EXT-X-MEDIA-SEQUENCE:<number>
ext_x_discontinuity_sequence = '#EXT-X-DISCONTINUITY-SEQUENCE'   #EXT-X-DISCONTINUITY-SEQUENCE:<number>
ext_x_endlist = '#EXT-X-ENDLIST'
ext_x_playlist_type = '#EXT-X-PLAYLIST-TYPE'   #EXT-X-PLAYLIST-TYPE:<EVENT|VOD>
ext_i_frames_only = '#EXT-X-I-FRAMES-ONLY'

# Master playlist tags
ext_x_media = '#EXT-X-MEDIA'   #EXT-X-MEDIA:<attribute-list>
ext_x_stream_inf = '#EXT-X-STREAM-INF'   #EXT-X-STREAM-INF:<attribute-list>
ext_x_i_frame_stream_inf = '#EXT-X-I-FRAME-STREAM-INF'   #EXT-X-I-FRAME-STREAM-INF:<attribute-list>
ext_x_session_data = '#EXT-X-SESSION-DATA'   #EXT-X-SESSION-DATA:<attribute list>

# Media or master playlist tags
ext_is_independent_segments = '#EXT-X-INDEPENDENT-SEGMENTS'
ext_x_start = '#EXT-X-START'   #EXT-X-START:<attribute list>

# **KEY Files**
# **Encrypting media segments**
# **Client/Server Responsibilities**

# Other tags
ext_x_allow_cache = '#EXT-X-ALLOW-CACHE'
ext_x_cue_out = '#EXT-X-CUE-OUT'
ext_x_cue_out_cont = '#EXT-X-CUE-OUT-CONT'
ext_x_cue_in = '#EXT-X-CUE-IN'
ext_x_cue_span = '#EXT-X-CUE-SPAN'
ext_x_scte35 = '#EXT-OATCLS-SCTE35'
ext_x_server_control = '#EXT-X-SERVER-CONTROL'
ext_x_part_inf = '#EXT-X-PART-INF'
ext_x_part = '#EXT-X-PART'
ext_x_rendition_report = '#EXT-X-RENDITION-REPORT'
ext_x_skip = '#EXT-X-SKIP'
ext_x_session_key = '#EXT-X-SESSION-KEY'
ext_x_preload_hint = '#EXT-X-PRELOAD-HINT'
