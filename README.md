# iTunes2RockboxPlaylist
Utility to convert iTunes m3u8 playlists for use on Rockbox devices

```
usage: itunes2rockbox.py [-h] [-l ROCKBOX_LIBRARY] [-r ROCKBOX_ROOT] [-c] [-e] [-m] in_file out_file rockbox_device

Converts m3u files exported from iTunes to Rockbox-compatible playlists

positional arguments:
  in_file               iTunes exported m3u
  out_file              Destination m3u file
  rockbox_device        Rockbox Device Path (Mountpoint)

optional arguments:
  -h, --help            show this help message and exit
  -l ROCKBOX_LIBRARY, --rockbox-library ROCKBOX_LIBRARY
                        If we only want to search a subdirectory of the Rockbox device, pass the library path here
  -r ROCKBOX_ROOT, --rockbox-root ROCKBOX_ROOT
                        If your Rockbox Music library is stored on an SD card, specify the prefix
                                (e.g. Clip+ microSD is mounted at <microSD1>)
  -c, --case-sensitive  Enforce case sensitivity in filenames
  -e, --ignore-extensions
                        Ignore file extensions when searching for target files
  -m, --ignore-missing  Do not leave blank lines for missing files

Usage examples:
    python .\itunes2rockbox.py -l E:\Music my_best_playlist.m3u my_converted_playlist.m3u E:\
        Search only E:\Music for music files
    python .\itunes2rockbox.py -m my_best_playlist.m3u my_converted_playlist.m3u /media/rockbox/
        Search the entirety of /media/rockbox for music, but do not put empty lines for missing files
```
