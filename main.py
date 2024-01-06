import discord
from discord import option , guild
import json
import requests
import logging
import os
import asyncio
from datetime import datetime, timedelta



with open("config.json", "r") as config:
    configdata = json.load(config)
    print("Config Readed")

bottoken = configdata["bottoken"]
camstatus = configdata["camstatus"]
watercooldown = configdata["watercooldown"]
infocooldown = configdata["infocooldown"]
role_id= configdata["adminroleid"]



log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot.log")
logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = discord.Bot()

cooldowns = {}

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name="Sukulent'le"))
    print(f'{bot.user} olarak giriş yapıldı.')
    logging.info("--------------------------------------------------------")
    logging.info("Bot is online: %s", bot.user.name)

@bot.command(description="Sukulent'in Anlık Bilgilerini Verir.")
async def info(ctx):
    with open("config.json", "r") as config:
        configdata = json.load(config)
    camstatus = configdata["camstatus"]
    infocooldown = configdata["infocooldown"]

    user_id = str(ctx.author.id)
    if user_id in cooldowns and datetime.now() < cooldowns[user_id]:
        remaining_time = cooldowns[user_id] - datetime.now()
        embed1 = discord.Embed(
            title="Şu an Bekleme Süresindesiniz;",
            description=f"**Daha fazla işlem yapmadan önce beklemeniz gerekiyor.**\n"
                        f"Kalan Bekleme Süresi: ***{remaining_time.seconds} saniye***",
        )
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embed1.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)
        await ctx.respond(embed=embed1, ephemeral=True)
    else:
        cooldowns[user_id] = datetime.now() + timedelta(seconds=infocooldown)  

        logging.info("User %s requested the sukulent's info's.", ctx.author.name)
        nem = requests.get(url="https://flask-production-91d9.up.railway.app/nem")
        nemjson = json.loads(nem.text)
        n = nemjson["nem"]
        mesaj = ""
        if n < 10:
            mesaj = "Sukulent Çok Kuru, Neredeyse Ölecek Yardım Edin!"
        elif n < 65:
            mesaj = "Sukulent'in Daha Fazla Suya İhtiyacı Var."
        elif 65 < n < 85:
            mesaj = "Bu Sukulent İçin İyi Bir Değer"
        else:
            mesaj = "Sukulent Gereğinden Fazla Suyla Beslenmiş, Sulamayı Azaltın"

        foto = requests.get(url="https://flask-production-91d9.up.railway.app/foto")
        fotojson = json.loads(foto.text)
        f = fotojson["foto_url"]

        embed = discord.Embed(title="Sukulent'in Bilgileri",
                              colour=0x7077a1)

        embed.add_field(name="Nem Değeri",
                        value=f"*%{n}\n{mesaj}*",
                        inline=False)
        embed.add_field(name="Sukulent Kaç Gündür Yaşıyor?",
                        value="*Sukulent Tam 24 Gündür Yaşıyor!*",
                        inline=False)
        embed.add_field(name="Sukulentten Anlık Bir Foto",
                        value="↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓",
                        inline=False)

        if camstatus == 1:
            embed.set_image(url=f)

        elif camstatus == 0:
            embed.set_image(url="https://i.imgur.com/0gplz2P.png") 

        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

        embed.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)

        await ctx.respond(embed=embed)

        await asyncio.sleep(infocooldown)  
        del cooldowns[user_id]  


@bot.command(description="Sukulent'i Sular.")
async def suver(ctx):
    with open("config.json", "r") as config:
        configdata = json.load(config)
    watercooldown = configdata["watercooldown"]
    user_id = str(ctx.author.id)
    if user_id in cooldowns and datetime.now() < cooldowns[user_id]:
        remaining_time = cooldowns[user_id] - datetime.now()
        embed1 = discord.Embed(
            title="Şu an Bekleme Süresindesiniz;",
            description=f"**Daha fazla işlem yapmadan önce beklemeniz gerekiyor.**\n"
                        f"Kalan Bekleme Süresi: ***{remaining_time.seconds} saniye***",
        )
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embed1.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)
        await ctx.respond(embed=embed1, ephemeral=True)
    else:
        cooldowns[user_id] = datetime.now() + timedelta(seconds=watercooldown)  

        logging.info("User %s requested the watering sukulent", ctx.author.name)
        nem = requests.get(url="https://flask-production-91d9.up.railway.app/nem")
        nemjson = json.loads(nem.text)
        n = nemjson["nem"]
        mesaj = ""
        if n < 10:
            mesaj = "Sukulent Çok Kuru, Neredeyse Ölecek Yardım Edin!"
        elif n < 65:
            mesaj = "Sukulent'in Daha Fazla Suya İhtiyacı Var."
        elif 65 < n < 85:
            mesaj = "Bu Sukulent İçin İyi Bir Değer"
        else:
            mesaj = "Sukulent Gereğinden Fazla Suyla Beslenmiş, Sulamayı Azaltın"
        embed = discord.Embed(title="Sukulent Başarıyla Sulandı!",
                              colour=0x7077a1)

        embed.add_field(name="Nem Değeri",
                        value=f"*%{n}\n{mesaj}*",
                        inline=False)

        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

        embed.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)

        embed.set_thumbnail(url="https://media4.giphy.com/media/G0Odfjd78JTpu/200w.gif?cid=6c09b952jlkndvmg76x2u2lasnywx8v8pbg7nquc3kmryrxp&ep=v1_gifs_search&rid=200w.gif&ct=g")

        await ctx.respond(embed=embed)

        await asyncio.sleep(watercooldown)  
        del cooldowns[user_id]


@bot.command(description="Adminlerin Botun Kamera Özelliğinin Açıp Kapamasına Yarar", default_member_permissions=(discord.Permissions(administrator=True)))
@option(
    "camstatus",
    description="Kamera Özelliğinin Açıp Kapamaya Yarar",
    choices=["Açık","Kapalı"],
    required=True
)
async def cam(ctx, camstatus: str):
    user_roles = [role.id for role in ctx.author.roles]
    with open("config.json", "r") as config:
        configdata = json.load(config)
    role_id= configdata["adminroleid"]
    if int(role_id) in user_roles:
        if camstatus == "Açık" or "Kapalı":
            if camstatus == "Açık":
                camvalue = 1
                with open("config.json", "r") as config:
                    configdata = json.load(config)
                oldvalue=configdata['camstatus']
                configdata['camstatus'] = camvalue
                with open("config.json", "w") as config:
                    myJSON = json.dump(configdata, config)
                    config.close()
                embed = discord.Embed(title="Kamera Başarıyla Açılmıştır!")
                if oldvalue==camvalue:
                    embed.add_field(name="",
                    value="bi saniye zaten aynı değilmiydi :d",
                    inline=False)
                    embed.set_image(url="https://media.tenor.com/JNI46wWZhP0AAAAM/demindensimdiye.gif")
                else:
                    embed.set_thumbnail(url="https://media0.giphy.com/media/l41lUjUgLLwWrz20w/giphy.gif?cid=ecf05e47fks4yij5hoxy2zsv1y1shfddnu1sneabwc2gxwmh&ep=v1_gifs_search&rid=giphy.gif&ct=g")
                await ctx.respond(embed=embed, ephemeral=True)   
                logging.info(f"Admin {ctx.author.name} changed camera's status from {oldvalue} to {camvalue}") 
                
            elif camstatus == "Kapalı":
                camvalue = 0
                with open("config.json", "r") as config:
                    configdata = json.load(config)
                oldvalue=configdata['camstatus']
                configdata['camstatus'] = camvalue
                with open("config.json", "w") as config:
                    myJSON = json.dump(configdata, config)
                    config.close()
                embed = discord.Embed(title="Kamera Başarıyla Kapanmıştır!")
                if oldvalue==camvalue:
                    embed.add_field(name="",
                    value="bi saniye zaten aynı değilmiydi :d",
                    inline=False)
                    embed.set_image(url="https://media.tenor.com/JNI46wWZhP0AAAAM/demindensimdiye.gif")
                else:
                    embed.set_thumbnail(url="https://media0.giphy.com/media/l41lUjUgLLwWrz20w/giphy.gif?cid=ecf05e47fks4yij5hoxy2zsv1y1shfddnu1sneabwc2gxwmh&ep=v1_gifs_search&rid=giphy.gif&ct=g")
                await ctx.respond(embed=embed, ephemeral=True)
                logging.info(f"Admin {ctx.author.name} changed camera's status from {oldvalue} to {camvalue}")
        

    else:
        embedpermission = discord.Embed(title="Bu Kodu Kullanmak İçin Yeterli Rolünüz Yok",
                      description="Bu Komut <@1055151567709421578>'ın Ayarlarını Düzenlemek İçin Var,\nEğer Bir Yanlışlık Olduğu Düşünüyorsan <@&1192915655306006548>'lara Danış.")
        embedpermission.set_thumbnail(url="https://media2.giphy.com/media/nR4L10XlJcSeQ/giphy.gif?cid=ecf05e47hvsi273r8li9teshubinjszsx8nk1d9nuin71der&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embedpermission.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)
        await ctx.respond(embed=embedpermission, ephemeral=True)

@bot.command(description="Adminlerin /suver Komutunda Verilecek Olan Bekleme Süresini Ayarlamasını Sağlar.", default_member_permissions=(discord.Permissions(administrator=True)))
@option(
    "watercooldown",
    description="/suver Komutunda Verilecek Olan Bekleme Süresini Ayarlar (Saniye Şeklinde)",
    min_value=15,
    max_value=600,
    required=True
)
async def watercooldown(ctx, watercooldown: int):
    user_roles = [role.id for role in ctx.author.roles]
    with open("config.json", "r") as config:
        configdata = json.load(config)
    role_id= configdata["adminroleid"]
    if int(role_id) in user_roles:
        with open("config.json", "r") as config:
            configdata = json.load(config)
        oldvalue=configdata['watercooldown']
        configdata['watercooldown'] = watercooldown
        with open("config.json", "w") as config:
            myJSON = json.dump(configdata, config)
            config.close()
                 
        embed = discord.Embed(description=f"**/suver Komutunun Bekleme Süresi {oldvalue} Saniyeden {watercooldown} Saniyeye Değişmiştir.**")
        if {oldvalue}=={watercooldown}:
            embed.add_field(name="",
                    value="bi saniye zaten aynı değilmiydi :d",
                    inline=False)
            embed.set_image(url="https://media.tenor.com/JNI46wWZhP0AAAAM/demindensimdiye.gif")
        else:
            embed.set_thumbnail(url="https://media0.giphy.com/media/l41lUjUgLLwWrz20w/giphy.gif?cid=ecf05e47fks4yij5hoxy2zsv1y1shfddnu1sneabwc2gxwmh&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        await ctx.respond(embed=embed, ephemeral=True)
        logging.info(f"Admin {ctx.author.name} change water commands cooldown from {oldvalue} to {watercooldown}")
        

    else:
        embedpermission = discord.Embed(title="Bu Kodu Kullanmak İçin Yeterli Rolünüz Yok",
                      description="Bu Komut <@1055151567709421578>'ın Ayarlarını Düzenlemek İçin Var,\nEğer Bir Yanlışlık Olduğu Düşünüyorsan <@&1192915655306006548>'lara Danış.")
        embedpermission.set_thumbnail(url="https://media2.giphy.com/media/nR4L10XlJcSeQ/giphy.gif?cid=ecf05e47hvsi273r8li9teshubinjszsx8nk1d9nuin71der&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embedpermission.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)
        await ctx.respond(embed=embedpermission, ephemeral=True)

@bot.command(description="Adminlerin /info Komutunda Verilecek Olan Bekleme Süresini Ayarlamasını Sağlar.", default_member_permissions=(discord.Permissions(administrator=True)))
@option(
    "infocooldown",
    description="/info Komutunda Verilecek Olan Bekleme Süresini Ayarlar (Saniye Şeklinde)",
    min_value=15,
    max_value=600,
    required=True
)
async def infocooldown(ctx, infocooldown: int):
    user_roles = [role.id for role in ctx.author.roles]
    with open("config.json", "r") as config:
        configdata = json.load(config)
    role_id= configdata["adminroleid"]
    if int(role_id) in user_roles:
        with open("config.json", "r") as config:
            configdata = json.load(config)
        oldvalue=configdata['infocooldown']
        configdata['infocooldown'] = infocooldown
        with open("config.json", "w") as config:
            myJSON = json.dump(configdata, config)
            config.close()
        embed = discord.Embed(description=f"**/info Komutunun Bekleme Süresi {oldvalue} Saniyeden {infocooldown} Saniyeye Değişmiştir.**")
        if {oldvalue}=={infocooldown}:
            embed.add_field(name="",
                    value="bi saniye zaten aynı değilmiydi :d",
                    inline=False)
            embed.set_image(url="https://media.tenor.com/JNI46wWZhP0AAAAM/demindensimdiye.gif")
        else:
            embed.set_thumbnail(url="https://media0.giphy.com/media/l41lUjUgLLwWrz20w/giphy.gif?cid=ecf05e47fks4yij5hoxy2zsv1y1shfddnu1sneabwc2gxwmh&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        await ctx.respond(embed=embed, ephemeral=True)
        logging.info(f"Admin {ctx.author.name} change water commands cooldown from {oldvalue} to {infocooldown}")
        

    else:
        embedpermission = discord.Embed(title="Bu Kodu Kullanmak İçin Yeterli Rolünüz Yok",
                      description="Bu Komut <@1055151567709421578>'ın Ayarlarını Düzenlemek İçin Var,\nEğer Bir Yanlışlık Olduğu Düşünüyorsan <@&1192915655306006548>'lara Danış.")
        embedpermission.set_thumbnail(url="https://media2.giphy.com/media/nR4L10XlJcSeQ/giphy.gif?cid=ecf05e47hvsi273r8li9teshubinjszsx8nk1d9nuin71der&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        embedpermission.set_footer(text=f'requested by: {ctx.author}', icon_url=avatar_url)
        await ctx.respond(embed=embedpermission, ephemeral=True)
    

bot.run(bottoken)
