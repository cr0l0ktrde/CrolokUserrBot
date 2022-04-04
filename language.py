
# CrolokUserBot - Kamran Ehmedov - Emin Efendiyev

from . import LANGUAGE, LOGS, bot, PLUGIN_CHANNEL_ID
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_CHANNEL_ID)
LOGS.info("Dil faylı yüklənir...")
LANGUAGE_JSON = None

for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):
    if ((len(dil.file.name.split(".")) >= 2) and (dil.file.name.split(".")[1] == "owenjson")):
        if path.isfile(f"./userbot/language/{dil.file.name}"):
            try:
                LANGUAGE_JSON = loads(open(f"./userbot/language/{dil.file.name}", "r").read())
            except JSONDecodeError:
                dil.delete()
                remove(f"./userbot/language/{dil.file.name}")

                if path.isfile("./userbot/language/DEFAULT.owenjson"):
                    LOGS.warn("Defolt dil faylından istifadə...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.owenjson", "r").read())
                else:
                    raise Exception("Dil faylınız yanlışdır")
        else:
            try:
                DOSYA = dil.download_media(file="./userbot/language/")
                LANGUAGE_JSON = loads(open(DOSYA, "r").read())
            except JSONDecodeError:
                dil.delete()
                if path.isfile("./userbot/language/DEFAULT.owenjson"):
                    LOGS.warn("Defolt dil faylından istifadə...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.owenjson", "r").read())
                else:
                    raise Exception("Dil faylınız yanlışdır")
        break

if LANGUAGE_JSON == None:
    if path.isfile(f"./userbot/language/{LANGUAGE}.owenjson"):
        try:
            LANGUAGE_JSON = loads(open(f"./userbot/language/{LANGUAGE}.owenjson", "r").read())
        except JSONDecodeError:
            raise Exception("Yanlış json faylı")
    else:
        if path.isfile("./userbot/language/DEFAULT.owenjson"):
            LOGS.warn("Defolt dil faylından istifadə...")
            LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.owenjson", "r").read())
        else:
            raise Exception(f"Didn't find {LANGUAGE} file")

LOGS.info(f"{LANGUAGE_JSON['LANGUAGE']} dili yükləndi.")

def get_value (plugin = None, value = None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON == None:
        raise Exception("Əvvəlcə dil faylını yükləyin")
    else:
        if not plugin == None or value == None:
            Plugin = LANGUAGE_JSON.get("STRINGS").get(plugin)
            if Plugin == None:
                raise Exception("Yanlış plugin")
            else:
                String = LANGUAGE_JSON.get("STRINGS").get(plugin).get(value)
                if String == None:
                    return Plugin
                else:
                    return String
        else:
            raise Exception("Yanlış plugin və ya sətir")
