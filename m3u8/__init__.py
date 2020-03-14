# coding: utf-8

import sys
import ssl
import os
from posixpath import normpath

try:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.parse import urlparse, urljoin
except ImportError:  # Python 2.x
    from urllib2 import urlopen, Request, HTTPError
    from urlparse import urlparse, urljoin

from m3u8.model import (M3U8, Segment, SegmentList, PartialSegment,
                        PartialSegmentList, Key, Playlist, IFramePlaylist,
                        Media, MediaList, PlaylistList, Start,
                        RenditionReport, RenditionReportList, ServerControl,
                        Skip, PartInformation, PreloadHint)
from m3u8.parser import parse, ParseError
from m3u8.mixins import is_url

PYTHON_MAJOR_VERSION = sys.version_info

__all__ = ('M3U8', 'Segment', 'SegmentList', 'PartialSegment',
            'PartialSegmentList', 'Key', 'Playlist', 'IFramePlaylist',
            'Media', 'MediaList', 'PlaylistList', 'Start', 'RenditionReport',
            'RenditionReportList', 'ServerControl', 'Skip', 'PartInformation',
            'PreloadHint', 'loads', 'load', 'parse', 'ParseError')

def loads(content, uri=None, custom_tags_parser=None):
    '''
    Given a string with a m3u8 content, returns a M3U8 object.
    Optionally parses a uri to set a correct base_uri on the M3U8 object.
    Raises ValueError if invalid content
    '''

    if uri is None:
        return M3U8(content, custom_tags_parser=custom_tags_parser)
    else:
        base_uri = _parsed_url(uri)
        return M3U8(content, base_uri=base_uri, custom_tags_parser=custom_tags_parser)


def load(uri, timeout=None, headers={}, custom_tags_parser=None, verify_ssl=True):
    '''
    Retrieves the content from a given URI and returns a M3U8 object.
    Raises ValueError if invalid content or IOError if request fails.
    Raises socket.timeout(python 2.7+) or urllib2.URLError(python 2.6) if
    timeout happens when loading from uri
    '''
    if is_url(uri):
        return _load_from_uri(uri, timeout, headers, custom_tags_parser, verify_ssl)
    else:
        return _load_from_file(uri, custom_tags_parser)


def _load_from_uri(uri, timeout=None, headers={}, custom_tags_parser=None, verify_ssl=True):
    request = Request(uri, headers=headers)
    context = None
    if not verify_ssl:
        context = ssl._create_unverified_context()
    resource = urlopen(request, timeout=timeout, context=context)
    base_uri = _parsed_url(resource.geturl())
    if PYTHON_MAJOR_VERSION < (3,):
        content = _read_python2x(resource)
    else:
        content = _read_python3x(resource)
    return M3U8(content, base_uri=base_uri, custom_tags_parser=custom_tags_parser)


def _parsed_url(url):
    parsed_url = urlparse(url)
    prefix = parsed_url.scheme + '://' + parsed_url.netloc
    base_path = normpath(parsed_url.path + '/..')  # from posixpath module
    return urljoin(prefix, base_path)


def _read_python2x(resource):
    return resource.read().strip()


def _read_python3x(resource):
    return resource.read().decode(
        resource.headers.get_content_charset(failobj="utf-8")
    )


def _load_from_file(uri, custom_tags_parser=None):
    with open(uri) as fileobj:
        raw_content = fileobj.read().strip()
    base_uri = os.path.dirname(uri)
    return M3U8(raw_content, base_uri=base_uri, custom_tags_parser=custom_tags_parser)
