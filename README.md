
EDIT the file `main.py` and change these vars

```python
path_log = "logs.txt"
default_log_level = "INFO"
path_mkvmerge = "D:/MKVToolNix/mkvmerge.exe"
path_mkvextract = "D:/MKVToolNix/mkvextract.exe"
```


# Usage args

```bash
usage: main.py [-h] [-e] [--sub SUB] [--force] [--default] [-f FILE]
               [-d DIRECTORY] [-a] [-l LATEST] [-s] [-t TRACK_NAME] [-i ID]

Extract subtitle

optional arguments:
  -h, --help            show this help message and exit
  -e, --extract         Extract subtitle of file
  --sub SUB             Which sub you want to extract, ietf format !!
  --force               Set subtitle as forced
  --default             Set subtitle as default
  -f FILE, --file FILE  Path of file
  -d DIRECTORY, --directory DIRECTORY
                        Path of dir
  -a, --all_file        All file in the dir(s)
  -l LATEST, --latest LATEST
                        latest file(s), you can choose the number of files
  -s, --show_subs       Shows subs infos of file
  -t TRACK_NAME, --track_name TRACK_NAME
                        Export subs by track name
  -i ID, --id ID        Export subs by id
```