import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

from pyrogram.types.messages_and_media import Message
from pyrogram import Client, filters
import time


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

app = Client("GUNC",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token
             )

anlik_calisan = []

ozel_list = [1193186807,1724329185,5159148002,1995417444]
anlik_calisan = []
grup_sayi = []
etiketuye = []
rxyzdev_tagTot = {}
rxyzdev_initT = {}

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)
  
  if event.chat_id in rxyzdev_tagTot:await event.respond(f"❌ Etiket işlemi durduruldu.\n\n Etiketlerin Sayı: {rxyzdev_tagTot[event.chat_id]} \n\n@LoseOnlineRobot")


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Merhaba 👋 Ben @LoseOnlineRobot\n\nBen Grubunuzdaki Üyeleri Etiketlemek İçin Python ile Yazılmış Bir Botum\nBeni Grubunuza Alıp Üyeleri Etiketleye Bilirsiz\nLütfen Çalışmam İçin Boş Yetki Verin👀\n\n Komutlar için /help yazın**",
                    buttons=(
                      [
                       Button.url('➕ Beni Bir Gruba Ekle ', 'https://t.me/LoseOnlineRobot?startgroup=a')
                      ],
                      [
                       Button.url('👨‍💻 Sahibim', 'https://t.me/loseonline')
                      ],
                      [
                       Button.url('📣 Reklam Vermek İçin', 'https://t.me/loseonline')
                      ],
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Komutlar:\n\n/utag - Kullanıcıları Etiketlerim.\n/atag - Yöneticileri Etiketlerim.\n/tektag - Tek tek etiketlerim.\n/cancel - Etiket İşlemini İptal Ederim .\n❕ Yalnızca Yöneticiler Bu Komutları Kullanabilir**"
  await event.reply(helptext)

@client.on(events.NewMessage())
async def mentionalladmin(event):
  global etiketuye
  if event.is_group:
    if event.chat_id in etiketuye:
      pass
    else:
      etiketuye.append(event.chat_id)

@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  rxyzdev_tagTot[event.chat_id] = 0
  if event.is_private:
    return await event.respond("__Bu Komut Sadace Grublarda ve Kanallarda Kullanabilirsin!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca Gurup Yöneticiler Etiket işlemini Yapabilir!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski Mesajlar için Üyelerden Bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana Bir Metin Ver!__")
  else:
    return await event.respond("__Bir Mesajı Yanıtlayın veya Başkalarından Bahsetmem için Bana Bir Betin Verin!!__")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond("**Etiket İşlemi Başladı ✅**")
        
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
      rxyzdev_tagTot[event.chat_id] += 1
      usrnum += 1
      usrtxt += f"\n👤 - [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n{usrtxt}")
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
        
    sender = await event.get_sender()
    rxyzdev_initT = f"\n👤 - [{sender.first_name}](tg://user?id={sender.id})"
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"✅ **Etiket İşlemi Başarıyla Tamamlandı !**\n\n👥 **Etiketlerin Sayları**: {rxyzdev_tagTot[event.chat_id]}\n\n🗣 **Etiket İşlemini Başlatan**: {rxyzdev_initT}")
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
      rxyzdev_tagTot[event.chat_id] += 1
      usrnum += 1
      usrtxt += f"👤 - [{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
     
    sender = await event.get_sender()
    rxyzdev_initT = f"[{sender.first_name}](tg://user?id={sender.id})"      
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"✅ **Etiket İşlemi Başarıyla Tamamlandı !**\n\n👥 **Etiketlerin Sayıları**: {rxyzdev_tagTot[event.chat_id]}\n\n🗣 **Etiket İşlemini Başlatan**: {rxyzdev_initT}")

@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mentionalladmin(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu Komut Yalnızca Grublarda Ve Kanallarda Kullanıma Bilir!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnızca Yöneticiler Etiket İşlemini Yapabilir__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski Mesajlar için Üyelerden Bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana Bir Metin Ver!__")
  else:
    return await event.respond("__Bir Mesajı Yanıtlayın veya Başkalarından Bahsetmem için Bana Bir Betin Verin!__")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond("**Etiket İşlemi Başladı ✅**")
  
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Etiket İşlemi Başarılı Bir Şekilde Bitti✅ ")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id,filter=ChannelParticipantsAdmins):
      usrnum += 1
      usrtxt += f"\n[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("İşlem Durduruldu ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(3)
        usrnum = 0
        usrtxt = ""

    sender = await event.get_sender()
    rxyzdev_initT = f"[{sender.first_name}](tg://user?id={sender.id})"
    if event.chat_id in rxyzdev_tagTot:await event.respond(f"✅ Etiket İşlemi Başarıyla Tamamlandı !.\n\n👥 Etiketlerin Sayları: {rxyzdev_tagTot[event.chat_id]}\n🗣 Etiket İşlemini Başlatan: {rxyzdev_initT}")



@app.on_message(filters.command(["tektag", "mentiona"], ["@", "/"]) & ~filters.private)
def tag(_, message: Message):

    kısa = False

    try:
        message.text.split()[1]
    except IndexError:

        kısa = True

    if kısa == False:

        if message.text.split()[1].isnumeric() == True:
            uye_sayi = int(app.get_chat_members_count(message.chat.id))
            metin = ""
            sayi = int(message.text.split()[1])
            sayac = 0
            kisiler = app.get_chat_members(message.chat.id)

            if uye_sayi < sayi:
                message.reply(
                        "__🇹🇷 Girdiğiniz Sayı Grup Üye Sayısından Fazla !!\n\nEtiketleme İşlemi Yapılmıyor...")

            else:
                for i in message.text.split()[2:]:
                    metin += i + " "

                chat_id = message.chat.id

                message.reply(
                    f"🇹🇷 {sayi} ** Kişi Etiketleniyor**...\n\n**Sebep** :  __{metin}__")

                for kisi in kisiler:

                    if kisi.user.is_bot == False:

                        isim = kisi.user.first_name
                        try:
                                app.send_message(chat_id, f"\n·{isim}\n\n[{metin}](tg://user?id={kisi.user.id}) ")
                        except:
                            pass
                        time.sleep(3)

                        sayac += 1
                        if sayac == sayi:
                            app.send_message(chat_id,
                                                 f"🇹🇷 {sayi} **Kişi Etiketlendi...**")
                            break
        elif message.text.split()[1].isnumeric() == False:


            metin = ""
            sayi = 50
            sayac = 0
            kisiler = app.get_chat_members(message.chat.id)


            for i in message.text.split()[1:]:
                metin += i + " "

            print(metin)
            message.reply(f"🇹🇷 ** Üyeler Etiketleniyor**...\n**Sebep** :  __{metin}__\n\n🇹🇷**KULLANICILARI ETİKETLİYORUM...")

            for kisi in kisiler:
                if kisi.user.is_bot == False:
                    isim = kisi.user.first_name
                    try:
                        app.send_message(message.chat.id, f"\n·{metin} [{isim}](tg://user?id={kisi.user.id}) ")
                    except:
                        pass
                    time.sleep(3)

                    sayac += 1

                    if sayac == sayi:
                        app.send_message(message.chat.id,
                                         "🇹🇷 **Etiketleme bitti...**")
                        break


    elif kısa == True:

        metin = ""
        sayi = 50
        sayac = 0
        kisiler = app.get_chat_members(message.chat.id)

        message.reply(f"🇹🇷 ** Üyeler Etiketleniyor**...\n**Sebep** :  __{metin}__")

        for kisi in kisiler:
            if kisi.user.is_bot == False:
                isim = kisi.user.first_name
                try:
                    app.send_message(message.chat.id, f"\n·{metin} [{isim}](tg://user?id={kisi.user.id}) ")
                except:
                    pass
                time.sleep(3)

                sayac += 1
                if sayac == sayi:
                    app.send_message(message.chat.id, "🇹🇷 **Etiketleme bitti...**")
                    break





@client.on(events.NewMessage())
async def mentionalladmin(event):
  global grup_sayi
  if event.is_group:
    if event.chat_id in grup_sayi:
      pass
    else:
      grup_sayi.append(event.chat_id)

@client.on(events.NewMessage(pattern='^/stats ?(.*)'))
async def son_durum(event):
    global anlik_calisan,grup_sayi,ozel_list
    sender = await event.get_sender()
    if sender.id not in ozel_list:
      return
    await event.respond(f"**@LoseOnlineRobot İstatistikleri 🤖**\n\nToplam Grup: `{len(grup_sayi)}`\nAnlık Çalışan Grup: `{len(anlik_calisan)}`")


@client.on(events.NewMessage(pattern='^/reklam ?(.*)'))
async def duyuru(event):
 
  global grup_sayi,ozel_list
  sender = await event.get_sender()
  if sender.id not in ozel_list:
    return
  reply = await event.get_reply_message()
  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a mesaj gönderiliyor...")
  for x in grup_sayi:
    try:
      await client.send_message(x,f"**⭐ Sponsor**\n\n{reply.message}")
    except:
      pass
  await event.respond(f"Gönderildi.")

@client.on(events.NewMessage(pattern='^/duyuru ?(.*)'))
async def duyuru(event):
 
  global grup_sayi,ozel_list
  sender = await event.get_sender()
  if sender.id not in ozel_list:
    return
  reply = await event.get_reply_message()
  await event.respond(f"Toplam {len(grup_sayi)} Gruba'a mesaj gönderiliyor...")
  for x in grup_sayi:
    try:
      await client.send_message(x,f"**📣 Duyuru**\n\n{reply.message}")
    except:
      pass
  await event.respond(f"Gönderildi.")

@client.on(events.NewMessage(pattern='^/dlive'))
async def event(ups):
  if ups.sender_id == 1193186807:
   await ups.reply("** Sevgili Bot Ustam Şuan Çalışmaktayım🇹🇷🤍**")
  elif ups.sender_id == 1724329185:
    await ups.reply("**Sayın CEO'm Şuan Çalışmaktayım 🇹🇷🤍**")
  elif ups.sender_id == 5159148002:
    await ups.reply("** Sayın @Ber4tbey Şuan Çalışmaktayım 🇹🇷🤍**")
  elif ups.sender_id == 1995417444:
    await ups.reply("__Hüsocum Şuan Çalışıyorum Merak Etme🥺👉👈__")
  else:
    await ups.reply("**Sen benim sahibim değilsin! **")


app.run()
print(">> Bot çalışıyor <<")
client.run_until_disconnected()
