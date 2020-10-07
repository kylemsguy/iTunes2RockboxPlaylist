import os
import sys
import argparse

# If you wish to support more files (e.g. mp4, files iTunes doesn't support)
# simply add it to the following tuple
SUPPORTED_MUSIC_FILES = ("mp3", "m4a", "wav", "aif", "aiff")


parser = argparse.ArgumentParser(
    description="Converts m3u files exported from iTunes to Rockbox-compatible playlists",
    epilog=f"""Usage examples:
    python {sys.argv[0]} -l E:\\Music my_best_playlist.m3u my_converted_playlist.m3u E:\\
        Search only E:\\Music for music files
    python {sys.argv[0]} -m my_best_playlist.m3u my_converted_playlist.m3u /media/rockbox/
        Search the entirety of /media/rockbox for music, but do not put empty lines for missing files
    """,
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    "in_file",
    help="iTunes exported m3u",
)
parser.add_argument(
    "out_file",
    help="Destination m3u file",
)
parser.add_argument(
    "rockbox_device",
    help="Rockbox Device Path (Mountpoint)",
)
parser.add_argument(
    "-l", "--rockbox-library",
    help="If we only want to search a subdirectory of the Rockbox device, pass the library path here",
)
parser.add_argument(
    "-r", "--rockbox-root",
    help="If your Rockbox Music library is stored on an SD card, specify the prefix\n\t(e.g. Clip+ microSD is mounted at <microSD1>)",
)
parser.add_argument(
    "-c", "--case-sensitive",
    help="Enforce case sensitivity in filenames",
    action="store_true",
)
parser.add_argument(
    "-e", "--ignore-extensions",
    help="Ignore file extensions when searching for target files",
    action="store_true",
)
parser.add_argument(
    "-m", "--ignore-missing",
    help="Do not leave blank lines for missing files",
    action="store_true",
)
args = parser.parse_args()

print("Indexing Rockbox Library... Please wait...")
# If there are duplicate files, the first file encountered
# is the one that will be selected for the output
# By default, this is the file highest in the file tree
file_index = {}
if args.rockbox_library:
    rockbox_library = args.rockbox_library
else:
    rockbox_library = args.rockbox_device
for root, dirs, files in os.walk(rockbox_library):
    for name in files:
        ext = name.split('.')[-1]
        if ext in SUPPORTED_MUSIC_FILES and not name in file_index:
            key = name if args.case_sensitive else name.lower()
            if args.ignore_extensions:
                key = '.'.join(key.split('.')[:-1])
            file_index[key] = os.path.join(root, name)
            

print("Indexing complete")
print(f"Now processing {args.in_file}")
if not args.ignore_missing:
    print(f"NOTE: A blank line will be placed to mark any missing tracks. Pass -m to suppress.")

with open(args.in_file, 'r', encoding='utf-8') as infile:
    src_playlist = infile.readlines()

output_lines = []
i = 1
for line in src_playlist:
    # Skip all #EXTM3U and #EXTINF lines
    if line.startswith("#"):
        continue
    
    # Clean up line
    line = line.strip()
    track_name = os.path.basename(line)
    key = track_name if args.case_sensitive else track_name.lower()
    if args.ignore_extensions:
        key = '.'.join(key.split('.')[:-1])
    if key in file_index:
        output_lines.append(file_index[key])
    else:
        print(f"WARNING: File with name {track_name} (position {i}) not found in Rockbox library", file=sys.stderr)
        if not args.ignore_missing:
            output_lines.append("")
    i += 1
        
print(f"Done! Writing to output file {args.out_file}...")
with open(args.out_file, 'w', encoding='utf-8') as outfile:
    for line in output_lines:
        if not line:
            print(file=outfile)
            continue
        rockbox_mountpoint = args.rockbox_device
        path = os.path.relpath(line, rockbox_mountpoint)
        if os.name == 'nt':
            split_path = [x for x in path.split('\\') if x]
        else:
            split_path = [x for x in path.split('/') if x]

        if args.rockbox_root:
            split_path.insert(0, args.rockbox_root)
        path = f"/{'/'.join(split_path)}"
        print(path, file=outfile)
        
print(f"Done! Playlist written to {args.out_file}")
        
