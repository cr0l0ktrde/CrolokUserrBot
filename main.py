# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Owen UserBot - ErdewBey - ByMisakiMey

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, OWEN_VERSION, PATTERNS, DEFAULT_NAME, BOT_TOKEN
from .modules import ALL_MODULES
from .asisstant.modules import ALL_MODULE
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions
from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp
import glob

ALIVE_MSG = [
    "` 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊` **{owensahip}**  \n  {owen} ",
    " ` 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊` **{owensahip}**, `` \n  {owen} ",
    "` 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊`, **{owensahip}** \n  {owen} ",
    " 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊` \n Bot Versiyonu: {owen} ",
    "` 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊` **{owensahip}**. \n  {owen} ",
    "` 🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊` \n Bot Versiyonu: {owen} "
]

DIZCILIK_STR = [
    "stiker üçün darıxıram...",
    "Oğurladım getdi tez sağal 🤭",
    "Yaşasın diz çökək...",
    "Bu stikeri öz paketimə dəvət edirəm...",
    "Bunu oğurlamalıyam...",
    "Hey, bu gözəl stikerdir!\nMən dərhal bunu oğurladım..",
    "Stikerinizə oğurlayıram\nhahaha.",
    "Hey ora bax. (☉｡☉)!→\nMən buna oğurlayarkən...",
    "Qızılgüllər qırmızı bənövşələr mavidir, bu stikeri paketimə oğurlasam cool olacam..",
    "Stiker həbsdədir...",
    "By Oğru bu stikəri oğurladı",
    "Niyə bu gözəl stiker paketimdə olmasın 🤭",
]

AFKSTR = [
    "Hazırda tələsirəm, sonra mənə yaza bilərsən? Onsuz da qayıdacağam."
    "Zəng etdiyiniz şəxs hazırda telefona cavab verə bilmir. Tondan sonra mesajınızı öz tarifinizdə qoya bilərsiniz. Mesajın qiyməti 49 qəpikdir. \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Bir neçə dəqiqəyə qayıdacağam. Amma etməsəm... bir az daha gözləyin."
    "Hazırda burada deyiləm, amma yəqin ki, başqa yerdəyəm."
    "Qızılgüllər qırmızıdır\nBənövşələr mavidir\nMənə mesaj buraxın\nMən sizə qayıdacağam.",
    "Bəzən həyatda ən yaxşı şeylər gözləməyə dəyər...\nMən tezliklə qayıdacağam."
    "Mən tezliklə qayıdacağam, amma qayıtmasam, daha sonra qayıdacağam."
    "Hələ başa düşmürsənsə,\nMən burada deyiləm."
    "Salam, uzaq mesajıma xoş gəldin, bu gün səni necə görməməzliyə vura bilərəm?"
    "Hazırda klaviaturadan uzaqdayam, amma ekranınızda kifayət qədər yüksək səslə qışqırırsınızsa, sizi eşidirəm."
    "Mən bu istiqamətdə gedirəm\n---->",
    "Mən bu istiqamətdə gedirəm\n<----",
    "Lütfən, bir mesaj buraxın və məni artıq olduğumdan daha vacib hiss etdirin."
    "Sahibim burada deyil, mənə mesaj yazmağı dayandırın."
    "Burada olsaydım\nSənə harda olduğumu deyərdim.\n\nAmma mən deyiləm,\ngeri qayıdanda soruş...",
    "Mən uzaqdayam!\nBilmirəm nə vaxt qayıdacağam!\nİnşallah bir neçə dəqiqəyə!",
    "Sahibim hazırda müsait deyil. Adınızı, nömrənizi və ünvanınızı bildirsəniz, mən onu ona verə bilərəm ki, qayıdanda."
    "Bağışlayın, ustadım burada deyil.\nO gələnə qədər mənimlə danışa bilərsiniz.\nAğam daha sonra sizinlə əlaqə saxlayacaq."
    "Məhz edirəm ki, bir mesaj gözləyirdin!",
    "Həyat çox qısadır, görüləsi çox şey var...\nMən onlardan birini edirəm...",
    "Hal-hazırda burada deyiləm....\n amma olsam ...\n\nbu əla olmazdımı?",
    "Məni xatırlamağınıza şadam, amma hazırda klaviatura mənim üçün çox uzaqdır",
    "Bəlkə mən yaxşıyam, bəlkə də pisəm, bilmirsən, amma AFK olduğumu görə bilərsən"
]

KICKME_MSG = [
    "Əlvida mən gedirəm 👋🏻",
    "Mən sakitcə gedirəm   ",
    "Sən bilmədən getsəm, bir gün qrupda olmadığımı anlayacaqsan.. Ona görə bu mesajı tərk edirəm🚪",
    "Mən bu yeri dərhal tərk etməliyəm🤭"
]

CV_MSG = [
"**{DEFAULT_NAME}** `O, çox məlumat vermədi, amma bilirəm ki, O, çox zövqlüdür, çünki Owen Userbot-dan istifadə edir.` 😁",
    "'Bağışlayın, sizə verəcək heç bir məlumatım yoxdur.'"
]


UNAPPROVED_MSG = ("`Hey, olduğun yerdə qal!👨‍💻 Mən Owenəm. Narahat olma!\n\n`"
                  "`Sahibim mənə mesaj yazmağa icazə vermədi, ona görə də sahibim sizi təsdiq edənə qədər bu mesajı alacaqsınız.. `"
                  "`Sahibimin aktiv olmasını gözləyin, o, adətən PM-ləri təsdiqləyir.\n\n`"
                  "`Bildiyim qədər, o, baş nazirlərin çılğın insanlara getməsinə icazə vermir.")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()



INVALID_PH = '\nXƏTA: Daxil edilmiş telefon nömrəsi yanlışdır' \
             '\n İpucu: Ölkə kodunuzdan istifadə edərək nömrənizi daxil edin' \
             '\n Telefon nömrənizi yenidən yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()
BRAIN_CHECKER = BRAIN_CHECKER[0]


def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # OWENPY
            Owenpy = re.search('\"\"\"OWENPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Owenpy == None:
                Owenpy = Owenpy.group(0)
                for Satir in Owenpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu plagin xaricdən yüklənib. Heç bir izahat müəyyən edilməmişdir.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    owenbl = requests.get('https://raw.githubusercontent.com/erdewbey/datas/master/blacklist.json').json()
    if idim in owenbl:
        bot.send_message("mən", f"`❌ Crolok adminləri sizə botdan qadağa qoydular! Bot bağlanır...`")
        LOGS.error("Crolok adminləri sizi botdan qadağan etdi! Bot bağlanır...")
        bot.disconnect()
    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": f"{str(choice(ALIVE_MSG))}", "afk": f"`{str(choice(AFKSTR))}`", "kickme": f"`{str(choice(KICKME_MSG))}`", "pm": str(UNAPPROVED_MSG), "dızcı": str(choice(DIZCILIK_STR)), "cv": str(choice(CV_MSG)), "ban": "🌀 {mention}`, Banlandı!!`", "mute": "🌀 {mention}`, səssize alındı!`", "approve": "`Salam` {mention}`, İndi mənə mesaj göndərə bilərsiniz!`", "disapprove": "{mention}`, İndi mənə mesaj göndərə bilərsiniz!`", "block": "{mention}`, Məni buna məcbur etdin! Mən səni blokladım!`"}


    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "cv", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("🔄 Pluginlər Yüklənir..")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin Onsuz Yüklənib " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`[×] Yükləmə alınmadı! Plugin Səhv!!\n\nXəta: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("mən", f"`Lütfən, plaginləri daimi etmək üçün PLUGIN_CHANNEL_ID təyin edin.`")


   
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

    
for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)
if BOT_TOKEN:
 for module_name in ALL_MODULE:
    imported_module = import_module("userbot.asisstant.modules." + module_name)    

os.system("clear")

LOGS.info("+===========================================================+")
LOGS.info("|             🐊  𝐂  𝐑  Ꮻ  𝐋  Ꮻ  𝐊   🐊                   |")
LOGS.info("+==============+==============+==============+==============+")
LOGS.info("|                                                            |")
LOGS.info("Botunuz işləyir! İstənilən söhbətdə .alive yazaraq onu sınayın."
          " Əgər köməyə ehtiyacınız varsa, Dəstək qrupumuza gəlin t.me/CrolokSup")
LOGS.info(f"Sizin bot versiyanız: Crolok ==> {OWEN_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
