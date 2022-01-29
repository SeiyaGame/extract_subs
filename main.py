# -*- coding: utf-8 -*-
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logger import setup_logger, get_logger
from extractmkv import ExtractMkv, allow_codec
import os

path_log = "logs.txt"
default_log_level = "INFO"
path_mkvmerge = "D:/MKVToolNix/mkvmerge.exe"
path_mkvextract = "D:/MKVToolNix/mkvextract.exe"

log = get_logger()


def parse_command_line():
    """
    parse command line arguments
    Returns
    -------
    ArgumentParser object: with parsed command line arguments
    """

    parser = ArgumentParser(
        description="Extract subtitle",
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("-e", "--extract", action="store_true",
                        help="Extract subtitle of file")

    parser.add_argument("--sub", default="FR", help="Which sub you want to extract, ietf format !!")
    parser.add_argument("--force", action="store_true", help="Set subtitle as forced")
    parser.add_argument("--default", action="store_true", help="Set subtitle as default")
    parser.add_argument("-f", "--file", help="Path of file")
    parser.add_argument("-d", "--directory", help="Path of dir")
    parser.add_argument("-a", "--all_file", action="store_true", help="All file in the dir(s)")
    parser.add_argument("-l", "--latest", default=1, help="latest file(s), you can choose the number of files")
    parser.add_argument("-s", "--show_subs", action="store_true", help="Shows subs infos of file")
    parser.add_argument("-t", "--track_name", help="Export subs by track name")
    parser.add_argument("-i", "--id", help="Export subs by id", type=int)

    args = parser.parse_args()

    print(args)

    return args


def newest(list_files, number_of_file):
    files = sorted(list_files, key=os.path.getctime, reverse=True)
    return files[:number_of_file]


def get_list_of_files(main_dir):
    list_files = list()
    for (dirpath, dirnames, filenames) in os.walk(main_dir):
        list_files += [os.path.join(dirpath, file) for file in filenames if not allow_codec(file)]

    return list_files


def path_exist(path):
    if not os.path.exists(path):
        log.info("Le chemin de destination n'existe pas !")
        exit(1)


def main():
    # parse command line
    args = parse_command_line()

    # setup logging
    setup_logger(default_log_level, path_log)
    extractmkv = ExtractMkv(path_mkvextract, path_mkvmerge)

    if args.extract:

        if args.file is not None:
            path_exist(args.file)
            if os.path.isfile(args.file):

                if args.show_subs:
                    subs = extractmkv.get_subs(args.file)
                    log.info(subs)
                else:
                    extractmkv.extract_subs(args.file, args.sub, args.default, args.force, args.track_name, args.id)
            else:
                log.info("Le chemin n'est pas un fichier !")

        if args.directory is not None:
            path_exist(args.directory)

            if args.all_file:
                for file in get_list_of_files(args.directory):

                    if args.show_subs:
                        subs = extractmkv.get_subs(file)
                        log.info(subs)
                    else:
                        extractmkv.extract_subs(file, args.sub, args.default, args.force, args.track_name, args.id)

            elif int(args.latest) > 0:
                list_newest_files = newest(get_list_of_files(args.directory), int(args.latest))

                log.info(f"Vérification des {args.latest} derniers fichiers")

                for file in list_newest_files:

                    if args.show_subs:
                        subs = extractmkv.get_subs(file)
                        log.info(subs)
                    else:
                        extractmkv.extract_subs(file, args.sub, args.default, args.force, args.track_name, args.id)


if __name__ == '__main__':
    main()
