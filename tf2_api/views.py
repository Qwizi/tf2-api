from pathlib import Path
from django.conf import settings
from django.http import HttpResponse

import polib
import vdf
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response

from maps.tasks import parse_maps
from worker.worker import TranslationFileWorker, WorkerManger, ItemsGameFileWorker


@api_view(["GET"])
def view(request):
    # # path to the items_game.txt file in static folder
    # items_game_path = Path(__file__).resolve().parent.parent / "static" / "items_game.txt"
    # tf_english_path = Path(__file__).resolve().parent.parent / "static" / "tf_english.txt"
    # items_game_vdf = vdf.load(items_game_path.open("r", encoding="utf-8"))
    # transaction_path = Path(__file__).resolve().parent.parent / "locale"/ "en" / "LC_MESSAGES" / "django.po"
    # tf_english_vdf = vdf.load(tf_english_path.open("r", encoding="utf-8"))
    # tokens = tf_english_vdf["lang"]["Tokens"]
    # maps = items_game_vdf["items_game"]["master_maps_list"]
    # print(maps)
    # parse_maps.delay(maps)

    worker = WorkerManger()
    worker.add_worker(ItemsGameFileWorker("items_game.txt"))
    # for language_code, language in settings.LANGUAGES:
    #     worker.add_worker(TranslationFileWorker(language_code, language, f"tf_{language.lower()}.txt"))
    worker.init_track_files_models()
    worker.run_workers()

    # po = polib.POFile()
    # po.metadata = {
    #     "Project-Id-Version": "1.0",
    #     "Report-Msgid-Bugs-To": "you@example.com",
    #     "POT-Creation-Date": "2007-10-18 14:00+0100",
    #     "PO-Revision-Date": "2007-10-18 14:00+0100",
    #     "Last-Translator": "you <you@example.com>",
    #     "Language-Team": "English <yourteam@example.com>",
    #     "MIME-Version": "1.0",
    #     "Content-Type": "text/plain; charset=utf-8",
    #     "Content-Transfer-Encoding": "8bit",
    # }
    # token_data = {
    #     "msgid": "",
    #     "msgstr": "",
    # }
    # for key, value in tokens.items():
    #     formated_value = value.replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "").replace("", "")
    #     formated_value = f'{formated_value.strip()}'
    #     entry = polib.POEntry(
    #         msgid=key,
    #         msgstr=formated_value,
    #         occurrences=[("welcome.py", "12"), ("anotherfile.py", "34")],
    #     )
    #     po.append(entry)
    #     print(entry)
    # print(po)
    # po.save(transaction_path)
    # test = _("English")
    # sentence = "TF_BlueTeam_Name"
    # output = _("TR_DemoRush_Sentry")
    return HttpResponse({"test": "test"})
