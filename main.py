import discord
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

# Edit these!
bot = commands.Bot(command_prefix = "!", intents=intents)
channel_id = yourchannelid
guild_id = yourguildid
path = r"path/to/my/welcomeimage.png"


@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_member_join(member):
    # Saves the Profile Picture as a file for PIL to edit it.
    with requests.get(member.avatar_url) as r:
        img_data = r.content
    with open('profile.jpg', 'wb') as handler:
        handler.write(img_data)
    im1 = Image.open("background.png")
    im2 = Image.open("profile.jpg")

    # Font Stuff
    draw = ImageDraw.Draw(im1)
    font = ImageFont.truetype("BebasNeue-Regular.ttf", 32)
    # Add the Text to the result image
    guild = bot.get_guild(guild_id)
    draw.text((160, 40),f"Welcome {member.name}",(255,255,255),font=font)
    draw.text((160, 80),f"You are the {guild.member_count}th member",(255,255,255),font=font)

    size = 129

    im2 = im2.resize((size, size), resample=0)
    # Creates the mask for the profile picture
    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, size, size), fill=255)

    mask_im.save('mask_circle.png', quality=95)

    # Masks the profile picture and adds it to the background.
    back_im = im1.copy()
    back_im.paste(im2, (11, 11), mask_im)


    back_im.save('welcomeimage.png', quality=95)
    # Stuff to send the embed with a local image.
    f = discord.File(path, filename="welcomeimage.png")

    embed = discord.Embed()
    embed.set_image(url="attachment://welcomeimage.png")


    await bot.get_channel(channel_id).send(file=f, embed=embed)
    
bot.run('token')
