# lrcdl

lrcdl is a command-line tool for fetching lyrics from audio files using https://lrclib.net.

## Installation

```
pip install lrcdl
```

## Basic Usage

Download lyrics (.lrc) from a track:

```
lrcdl song.mp3
```

By default, lrcdl will only download __timed__ lyrics if they're found. To include plain, non-timed lyrics, use the `--include-plain` flag:

```
lrcdl song.mp3 --include-plain
```

Which will download plain lyrics only if timed ones were not found.

### Supplying metadata

lrcdl relies on the metadata inside the audio track to find lyrics. In cases where the audio file does not have enough metadata, you can manually fill them in using the following parameters: `--title`, `--album`, `--artist`

Example:
```
lrcdl "Ghost Division.flac" --title "Ghost Division" --album "The Art of War" --artist Sabaton
```

### Downloading lyrics for entire music library

If you have a music library and you want to download lyrics for all tracks, you can use the `-r`/`--recursive` option while specifying a directory as the path:

```
lrcdl /PATH/TO/MUSIC -r
```

Note that lrcdl will skip files that already have an LRC file and will not overwrite them.

This command can be safely setup as a scheduled task or a cron job to download lyrics on a nightly basis, however if you have a lot of tracks in your library which lrcdl cannot find lyrics for, then lrcdl will continue to try and download lyrics for them on every run.

To improve performance and avoid unnecessary strain on lrclib's servers, you're highly advised to specify a cache file to skip already-checked files on the next run:

```
lrcdl /PATH/TO/MUSIC/ -r --cache /PATH/TO/CACHE/cache.txt
```

### Python API

To use within Python:

```py
from lrcdl import Track, Options


track = Track("/path/to/song.mp3")

options = Options()
# or specify a path
options = Options(download_path="/path/file.lrc")

track.download_lyrics(options)
```