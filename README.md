synopy
======

Python library for the Synology DiskStation APIs

Description
===========

This project aims to support all the APIs for the Synology NAS DiskStations.

Right now the only official API specification published by Synology, is for
the Download Station. And you can find it [here][1].

This is alpha software and there might be dramatic changes between releases, until
it reaches a stable state.


Usage
=====

Let's see some examples.

### DownloadStationInfo API

```python
# SYNO.DownloadStation.Info namespace
from synopy.base import Connection
from synopy.api import DownloadStationInfo

# Set up a connection
conn = Connection('http', 'dsm.localdomain', port=5000)
# Authenticate and get an 'sid' cookie
conn.authenticate('admin', 'mypasswd')

# Create an instance of the DownloadStationInfo API
dsinfo_api = DownloadStationInfo(conn, version=1)
# Make a 'getinfo' query
resp = dsinfo_api.get_info()

print(resp.payload)

{
    u'data':
        {
            u'is_manager': True,
            u'version': 2480,
            u'version_string': u'3.4-2480'
        },
    u'success': True
 }

```

### DownloadStationTask API

```python

# SYNO.DownloadStation.Task namespace
from synopy.api import DownloadStationTask

dstask_api = DownloadStationTask(conn, version=1)
# Use the 'list' query method to see the running tasks
resp = dstask_api.list()

print(resp.payload)
{
    u'data':
        {
            u'offeset': 0, # That's not my typo ;)
            u'tasks': [{u'id': u'dbid_6',
                        u'size': u'3260371830',
                        u'status': u'paused',   # <--- it's paused :(
                        u'status_extra': None,
                        u'title': u'TOTALLY.LEGAL.TORRENT.ISO',
                        u'type': u'bt',
                        u'username': u'admin'}],
            u'total': 1
        },
    u'success': True
}

# Let's put it to work!
resp = dstask_api.resume(id='dbid_6')

print(resp.payload)
{
    u'data': [{u'error': 0, u'id': u'dbid_6'}],
    u'success': True
}

# Let's check if indeed the task resumed, but ask for additional info
resp = dstask_api.list(additional='detail,file')
print(resp.payload)
{
    u'data':
        {
            u'offeset': 0,
            u'tasks':
                [{u'additional':
                    {u'detail':
                        {u'connected_leechers': 4,
                         u'connected_seeders': 41,
                         u'create_time': u'1395142482',
                         u'destination': u'DSMFiles/Downloads',
                         u'priority': u'auto',
                         u'total_peers': 0,
                         u'uri': u'magnet:?xt=really_long_magnet_link_here'},
                         u'file': [
                            {u'filename': u'Torrent Downloaded From Legal Torrents.txt',
                             u'priority': u'normal',u'size': u'353',u'size_downloaded': u'353'},
                            {u'filename': u'legaltorrent.iso',u'priority': u'normal',
                             u'size': u'3260370944',u'size_downloaded': u'1872580608'},
                            {u'filename': u'nfo.nfo',u'priority': u'normal',u'size': u'533',
                             u'size_downloaded': u'533'}]
                        },
                     u'id': u'dbid_6',
                     u'size': u'3260371830',
                     u'status': u'downloading',  # <--- yay! :)
                     u'status_extra': None,
                     u'title': u'TOTALLY.LEGAL.TORRENT.ISO',
                     u'type': u'bt',
                     u'username': u'admin'
                    }
                ],
            u'total': 1
        },
    u'success': True
}
```

### Notes
More to come!

[1]: http://ukdl.synology.com/download/other/Synology_Download_Station_Official_API_V3.pdf