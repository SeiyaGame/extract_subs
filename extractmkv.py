# * coding=utf8 *

import subprocess
import os
import json
from logger import get_logger

log = get_logger()


def allow_codec(file):
    allow_codec_sub = [".ass", ".srt", ".vtt"]

    for codec_sub in allow_codec_sub:
        if codec_sub in file:
            return True
    return False


def execute_commande_shell(cmd):
    """Fonction qui renvoie l'erreur, l'output et le code de la commande"""

    # On execute la commande
    execute_commande = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # On recupere la sorti et les erreurs si il en a
    (output, err) = execute_commande.communicate()

    return output.decode('UTF-8'), err.decode('UTF-8'), execute_commande.returncode


class ExtractMkv:

    def __init__(self, mkvextract, mkvmerge):
        self._mkvextract_path = mkvextract
        self._mkvmerge_path = mkvmerge

        self._allow_codec_sub_full = ["SubStationAlpha", "SubRip/SRT", "WebVTT"]

    def get_info_file(self, path_file):
        """
        Permet de recuperer les infos d'un fichier mkv
        :param path_file: chemin du fichier
        :return: renvoie un dictionnaire avec les infos du fichier
        """

        cmd = f"{self._mkvmerge_path} -J \"{path_file}\""
        output, err, return_code = execute_commande_shell(cmd)

        data = json.loads(output)
        return return_code, data

    def get_subs(self, path_file):

        return_code, data = self.get_info_file(path_file)
        subs_list = list()

        if return_code == 0:

            for track in data['tracks']:
                if track['type'] == "subtitles":
                    subs_list.append(track)

        else:
            log.info(data["errors"])

        return subs_list

    def extract_subs(self, path_file, language_wanted, default_sub, forced_sub, track_name, id):
        subs = self.get_subs(path_file)

        log.info(f"nom du fichier: {os.path.basename(path_file)}")
        if len(subs) == 0:
            log.info("Aucun sous-titre à extraire !")

        for sub in subs:

            if not sub['codec'] in self._allow_codec_sub_full:
                log.info("Codec non répertorier")
                continue

            extension_file = None
            if sub['codec'] == "SubStationAlpha":
                extension_file = ".ass"
            elif sub['codec'] == "SubRip/SRT":
                extension_file = ".srt"
            elif sub['codec'] == "WebVTT":
                extension_file = ".vtt"

            language = None
            try:
                language = sub['properties']['language_ietf']
            except KeyError:
                language = sub['properties']['language']

            if language_wanted.lower() not in language.lower():
                if len(subs) > 1:
                    continue
                elif language.lower() == "und":
                    language = language_wanted.lower()

            if id:
                if sub['id'] != id:
                    continue

            elif track_name:
                if not sub['properties']['track_name'] == track_name:
                    continue
            # else:
            #     if len(subs) > 1:
            #         if not sub['properties']['default_track']:
            #             continue

            # if default_sub and forced_sub:
            #     log.info("Vous ne pouvez pas mettre un sous-titre par defaut et forcé en même temps !")
            #     exit(1)

            file_path_without_ext_file = os.path.splitext(path_file)[0]
            output_file = f"{file_path_without_ext_file}.{language}{extension_file}"

            if default_sub and forced_sub:
                output_file = f"{file_path_without_ext_file}.{language}.forced.default{extension_file}"
            elif default_sub:
                output_file = f"{file_path_without_ext_file}.{language}.default{extension_file}"
            elif forced_sub:
                output_file = f"{file_path_without_ext_file}.{language}.forced{extension_file}"

            if os.path.exists(output_file):
                log.info(f"Le fichier {output_file} existe déjâ !")
                break

            cmd = f"{self._mkvextract_path} tracks \"{path_file}\" {sub['id']}:\"{output_file}\""

            log.info(f"Extraction des sous-titre en cours de {os.path.basename(path_file)} ...")
            output, err, return_code = execute_commande_shell(cmd)

            if return_code == 0:
                log.info(f"Extraction des sous-titre réussi pour: {path_file}")
            else:
                log.info(f"Une erreur est survenu lors de l'extraction des sous-titre: {err}")
