import os
import random
import re
import smtplib
import string
from random import randint

import aiohttp
import discord
import requests
from discord.ext import commands
from replit import db

intents = discord.Intents().all()
client = discord.Client()
client = commands.Bot(command_prefix='!', intents=intents)


# WIP AREA START


@client.event
async def on_ready():
    await log('NUCATS BOT Online')


@client.event
async def on_member_join(member):
    await member.create_dm()
    try:
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to NUCATS Discord server!'
        )
        await member.dm_channel.send(
            f'To gain access type ``!auth`` here or in the welcome channel'
        )
    except Exception as e:
        await log(member.name + " Privacy Setting Issue")
    await log(member.name + " joined the server")


# @client.command()
# async def scan(ctx):
# allows ppl to join the weekly code war list


@client.command()
async def join(ctx, arg1):
    # checks if person exists
    await ctx.message.delete()
    response = requests.get("https://www.codewars.com/api/v1/users/" + arg1)
    if (response.status_code == 200):
        db[str(ctx.author)] = [arg1]
        # if exist add to array end and store in db
        await log("CODEWARS User {" + arg1 + "} added for " + str(ctx.author))
        await ctx.channel.send("CODEWARS User {" + arg1 + "} added for " + str(ctx.author), delete_after=30)
    else:
        # if don't exist error
        await log("api response error : " + str(response))
        await ctx.channel.send("api response error : " + str(response), delete_after=30)


@client.command()
async def list(ctx):
    response = db.keys()
    await log(response)


@client.command()
async def val(ctx, arg1):
    response = db[arg1]
    await log(response)


@client.command()
async def draw(ctx, id):
    response = db.keys()
    winner = random.sample(response, 1)
    winnerUsername = db[winner[0]]
    await log(f'Drawn is {winner} {winnerUsername[0]}')
    await ctx.channel.send(f'Drawn is {winner} {winnerUsername[0]}')
    response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
    resObject = response.json()
    for obj in resObject["data"]:
        if (obj["id"] == id):
            await log(f'{winner} has  completed the challenge soo wins £5 pounds!!!')
            await ctx.channel.send(f'{winner} has  completed the challenge soo wins £5 pounds!!!')
            return 0
    await ctx.channel.send(f'{winner} has not completed the challenge soo we draw again')
    await log(f'{winner} has not completed the challenge soo we draw again')
    await draw(ctx, id)
    return 0


@client.command()
async def challenge(ctx, arg1):
    del db["code"]
    db["code"] = [arg1]


@client.command()
async def complete(ctx):
    await ctx.message.delete()
    winner = str(ctx.author)
    winnerUsername = db[winner]
    response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
    resObject = response.json()
    for obj in resObject["data"]:
        if (str(obj["id"]) == str(db["code"][0])):
            await ctx.channel.send(f'{winner} has completed the challenge ', delete_after=30)
            return 0
    await ctx.channel.send(f'{winner} has not completed the challenge', delete_after=30)
    return 0


@client.command()
async def complete2(ctx, arg1):
    winner = arg1
    winnerUsername = db[winner]
    response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
    resObject = response.json()
    for obj in resObject["data"]:
        if (obj["id"] == db["code"][0]):
            await log(f'{winner} has completed the challenge')
            await ctx.channel.send(f'{winner} has completed the challenge')
            return 0
    await ctx.channel.send(f'{winner} has not completed the challenge')
    return 0


@client.command()
async def listComplete(ctx):
    response = db.keys()
    for k in response:
        out = False
        winner = str(k)
        winner_username = db[winner]
        response = requests.get(f'https://www.codewars.com/api/v1/users/{winner_username[0]}/code-challenges/completed')
        res_object = response.json()
        try:
            for obj in res_object["data"]:
                if str(obj["id"]) == str(db["code"][0]):
                    await ctx.channel.send(f'{winner} has completed the challenge ')
                    out = True
            if not out:
                await ctx.channel.send(f'{winner} has not completed the challenge')
        except Exception:
            await ctx.channel.send(f'{winner} has not completed the challenge')


@client.command()
async def listStat(ctx):
    response = db.keys()
    complete = 0
    total = 0
    for k in response:
        total = total + 1
        out = False
        winner = str(k)
        winner_username = db[winner]
        response = requests.get(f'https://www.codewars.com/api/v1/users/{winner_username[0]}/code-challenges/completed')
        res_object = response.json()
        try:
            for obj in res_object["data"]:
                if str(obj["id"]) == str(db["code"][0]):
                    complete = complete + 1
        except Exception:
            total = total - 1
    await ctx.channel.send(
        f'{complete} / {total} or {int(100 * (complete / total))}% have completed the challenge so far!!')


@client.command()
async def remove(ctx, arg1):
    del db[arg1]


@client.command()
async def ran(ctx, arg1, arg2):
    await ctx.channel.send("Your random number is : " + str(randint(int(arg1) - 1, int(arg2))))


@client.command()
async def flip(ctx):
    await ctx.channel.send(f"{ctx.message.author.mention}🪙 throws a coin in the a air and it lands on....")
    if randint(0, 2) == 1:
        await ctx.channel.send("HEADS")
    else:
        await ctx.channel.send("TAILS")


@client.command()
async def auth(ctx):
    # intro message
    await ctx.message.delete()
    await log(str(ctx.author) + " has begun auth process")
    await log(str(ctx.author) + " Auth Step - Username input (1/7)")
    try:
        await ctx.author.send(
            'Thank You for starting the NUCATS authentication Process\nWe cant wait for you to join us on the '
            'server!!!! :)')
        await ctx.author.send(
            '\nStep 1/6 Please enter your uni username you use to log in with I.E. B8028969 or C1023937')
    except Exception as e:
        try:
            c = client.get_channel(752536544765542431)
            await c.send(
                f"{ctx.message.author.mention}  your privacy settings are preventing the bot messaging you \n Error "
                f"please contact a Server admin")
            c = client.get_channel(878233107956924426)
            await c.send(
                f"{ctx.message.author.mention}  your privacy settings are preventing the bot messaging you \n Error "
                f"please contact a Server admin")
        except Exception as f:
            await log(str(ctx.author) + " has Privacy setting issue")
    await log(str(ctx.author) + " has begun auth process")

    # Step 1 - validate username
    # Regex check
    async def check(m):
        if len(m) != 8:
            print(m)
            await log(str(ctx.author) + " Auth Step - Username Regex check (2/7)")
            await log(str(ctx.author) + " Auth Step - Fail Username does not match len")
            return False
        regex = '^([A-C|a-c])\d{7}$'
        if re.match(regex, m):
            await log(str(ctx.author) + " Auth Step - Success Valid Username")
            return True
        else:
            await log(str(ctx.author) + " Auth Step - Fail Regex did not match")
            return False

    # loops till valid username given
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if await check(msg.content):
                break
            else:
                await ctx.author.send('Invalid Username please check it is correct')
    # Step 2 - Send validation code
    await log(str(ctx.author) + " Auth Step - Verification code sent to email (3/7)")
    # generate code
    authCode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    await ctx.author.send(
        'Step 2/6 We have emailed you a verification code!!\nplease copy and paste it below\nThis email may be in your '
        'junk mail')
    # sends email
    sent_from = "nucats.auth.no.reply@gmail.com"
    to = [msg.content + '@ncl.ac.uk']
    body = 'Hi ' + str(
        ctx.author) + ' please copy and paste the following code into the discord private chat\n\n' + authCode
    subject = "Verification Code"
    email_text = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('nucats.auth.no.reply@gmail.com', os.environ['AuthPW'])
        server.sendmail('nucats.auth.no.reply@gmail.com', to, email_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        await log(str(ctx.author) + " Auth Step - ERROR with mail server")
        await log(e)
        print(e)
        try:
            sent_from = "nucats.auth.no.reply@gmail.com"
            to = [msg.content + '@ncl.ac.uk']
            body = 'Hi please copy and paste the following code into the discord private chat\n\n' + authCode
            subject = "Verification Code"
            email_text = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

        %s
        """ % (sent_from, ", ".join(to), subject, body)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login('nucats.auth.no.reply@gmail.com', os.environ['AuthPW'])
            server.sendmail('nucats.auth.no.reply@gmail.com', to, email_text)
            server.close()
            print('Email sent!')
        except Exception as e:
            await log(str(ctx.author) + " Auth Step - ERROR with mail server")
            await log(e)
            print(e)
    # step 3 check auth code
    await log(str(ctx.author) + " Auth Step - await valid code (4/7)")
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content == authCode:
                break
            else:
                await ctx.author.send('Invalid Verification Code')
    # step 4 agree with rules
    await log(str(ctx.author) + " Auth Step - Rules (5/7)")
    await ctx.author.send("""Step 3/6 Please read our rules and type agree to agree to them

1. Be respectful
You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.

2. No Inappropriate Language and Material
The use of profanity should be kept to a minimum. However, any derogatory language towards any user is prohibited.

3. No spamming
Don't send a lot of small messages right after each other. Do not disrupt chat by spamming.

4. No pornographic/adult/other NSFW material
This is a community server and not meant to share this kind of material.

5. No offensive names and profile pictures You will be asked to change your name or picture if the staff deems them 
inappropriate. Your name should be the name you go by hence (hopefully) should no be offensive. 

8. Direct & Indirect Threats
Threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed.

9. Follow the NCL student Charter
You can find it here: https://www.ncl.ac.uk/student-progress/policies/student-charter/

10. No Collusion on Uni Work

The Committee will Mute/Kick/Ban per discretion. If you feel mistreated dm an Admin and we will resolve the issue.

All Channels will have pinned messages explaining what they are there for and how everything works. If you don't 
understand something, feel free to ask!""")
    await ctx.author.send('**Please read the rule and type agree to agree with them**')
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content.lower() == 'agree':
                break
            else:
                await ctx.author.send('Please read the rule and type agree to agree with them')
    # step 5 Nickname
    await log(str(ctx.author) + " Auth Step - Name and Pronoun (6/7)")
    await ctx.author.send(
        '**Step 4/6 As part of the rules of the Nucats server we require everyone Discord name to be their actual '
        'name**')
    await ctx.author.send(
        'Please enter your preferred name below. Please note giving a bad name will result in being force to go back '
        'through auth soz')
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            guild = client.get_guild(752532623678505011)
            print(guild)
            member = guild.get_member(msg.author.id)
            print(member)
            if len(msg.content) > 14:
                await ctx.author.send('Nickname too long')
            else:
                await member.edit(nick=msg.content)
                break
    await log(str(ctx.author) + " Changed Nickname to " + msg.content)
    # step 6 Pronoun
    await ctx.author.send('''Step 5/6 Please select your preferred pronoun by entering the corresponding number
      1 - he/him
      2 - she/her
      3 - they/them
    IF your Pronoun is not here please message the committee and we will sort it :)''')
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content == '1':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="He/Him")
                await member.add_roles(var)
                break
            elif msg.content == '2':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="She/Her")
                await member.add_roles(var)
                break
            elif msg.content == '3':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="They/Them")
                await member.add_roles(var)
                break
    # step 7 stage
    await ctx.author.send('''Step 6/6 Please select which stage you are in by entering the corresponding number')
      1 - first
      2 - second
      3 - third
      4 - fourth
      5 - placement
      6 - post grad
      7 - alumni''')
    while True:
        msg = await client.wait_for('message')
        if ctx.author == msg.author and isinstance(msg.channel, discord.channel.DMChannel):
            if msg.content == '1':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Stage 1")
                await member.add_roles(var)
                break
            elif msg.content == '2':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Stage 2")
                await member.add_roles(var)
                break
            elif msg.content == '3':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Stage 3")
                await member.add_roles(var)
                break
            elif msg.content == '4':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Stage 4")
                await member.add_roles(var)
                break
            elif msg.content == '5':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Placement")
                await member.add_roles(var)
                break
            elif msg.content == '6':
                guild = client.get_guild(752532623678505011)
                member = guild.get_member(ctx.author.id)
                var = discord.utils.get(member.guild.roles, name="Post Grad")
                await member.add_roles(var)
                break
            elif msg.content == '7':
                await ctx.author.send('Sorry only ppl at the uni are allowed full access to the server')
                await log(str(ctx.author) + " Hit Alumni Trap lol")

    # auth final steps
    await log(str(ctx.author) + " Auth Step - Stage (7/7)")
    guild = client.get_guild(752532623678505011)
    member = guild.get_member(ctx.author.id)
    var = discord.utils.get(member.guild.roles, name="Verified")
    await member.add_roles(var)
    var = discord.utils.get(member.guild.roles, name="Alumni")
    await member.remove_roles(var)
    await log(str(ctx.author) + " Auth Complete")
    await ctx.author.send('Great!!! You are now authed and have full access to the server :D')
    await ctx.author.send(
        'Cant wait to speak to you soon!!! and hopefully see you at some of our events!!!\n Cheers Jonno')
    c = client.get_channel(752547001794822255)
    if ctx.message.channel == 757937625280806923:
        await c.send(
            f"{ctx.message.author.mention}👋 Welcome to the NUCATS Server!!! \nCheck the updates channel for the "
            f"latest news on our even\nAny questions feel free to reach out to committee")


@client.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    await ctx.send(embed=embed)


@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="OMG something even better! a Doggo!!!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    await ctx.send(embed=embed)


@client.command()
async def nucat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="OMG something even better! a Doggo!!!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    await ctx.send(embed=embed)


@client.command()
async def nudog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')
        dogjson = await request.json()
    embed = discord.Embed(title="I was made to code this in...", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    await ctx.send(embed=embed)


@client.command()
async def nucats(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="OMG something even better! a Doggo!!!", color=discord.Color.purple())
    embed.set_image(url=dogjson['link'])
    await ctx.send(embed=embed)


@client.command()
async def roll(ctx):
    """Rolls a dice in NdN format."""
    result = ', '.join(str(random.randint(1, 6)) for r in range(6))
    await ctx.send(result)


async def log(value):
    l = client.get_channel(872913487247052890)
    print(value)
    await l.send(str(value))


client.run(os.environ['DiscordToken'])
