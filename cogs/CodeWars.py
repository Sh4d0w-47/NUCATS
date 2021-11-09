import random
import requests
from discord.ext import commands
from replit import db
import tools


class CodeWars(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, arg1):
        # checks if person exists
        await ctx.message.delete()
        response = requests.get("https://www.codewars.com/api/v1/users/" + arg1)
        if (response.status_code == 200):
            db[str(ctx.author)] = [arg1]
            # if exist add to array end and store in db
            await tools.log(self.client, "CODEWARS User {" + arg1 + "} added for " + str(ctx.author))
            await ctx.channel.send("CODEWARS User {" + arg1 + "} added for " + str(ctx.author), delete_after=30)
        else:
            # if don't exist error
            await tools.log(self.client, "api response error : " + str(response))
            await ctx.channel.send("api response error : " + str(response), delete_after=30)

    @commands.command()
    async def list(self, ctx):
        response = db.keys()
        await tools.log(self.client, response)


    @commands.command()
    async def val(self, ctx, arg1):
        response = db[arg1]
        await tools.log(self.client, response)


    @commands.command()
    async def draw(self, ctx, id):
        response = db.keys()
        winner = random.sample(response, 1)
        winnerUsername = db[winner[0]]
        await tools.log(self.client, f'Drawn is {winner} {winnerUsername[0]}')
        await ctx.channel.send(f'Drawn is {winner} {winnerUsername[0]}')
        response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
        resObject = response.json()
        for obj in resObject["data"]:
            if (obj["id"] == id):
                await tools.log(self.client, f'{winner} has  completed the challenge soo wins £5 pounds!!!')
                await ctx.channel.send(f'{winner} has  completed the challenge soo wins £5 pounds!!!')
                return 0
        await ctx.channel.send(f'{winner} has not completed the challenge soo we draw again')
        await tools.log(self.client, f'{winner} has not completed the challenge soo we draw again')
        return 0

    @commands.command()
    async def challenge(self, ctx, arg1):
        del db["code"]
        db["code"] = [arg1]


    @commands.command()
    async def complete(self, ctx):
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


    @commands.command()
    async def complete2(self, ctx, arg1):
        winner = arg1
        winnerUsername = db[winner]
        response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
        resObject = response.json()
        for obj in resObject["data"]:
            if (obj["id"] == db["code"][0]):
                await tools.log(self.client, f'{winner} has completed the challenge')
                await ctx.channel.send(f'{winner} has completed the challenge')
                return 0
        await ctx.channel.send(f'{winner} has not completed the challenge')
        return 0


    @commands.command()
    async def listComplete(self, ctx):
        response = db.keys()
        for k in response:
            out = False
            winner = str(k)
            winnerUsername = db[winner]
            response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
            resObject = response.json()
            try:
                for obj in resObject["data"]:
                    if (str(obj["id"]) == str(db["code"][0])):
                        await ctx.channel.send(f'{winner} has completed the challenge ')
                        out = True
                if not out:
                    await ctx.channel.send(f'{winner} has not completed the challenge')
            except Exception:
                await ctx.channel.send(f'{winner} has not completed the challenge')


    @commands.command()
    async def listStat(self, ctx):
        response = db.keys()
        complete = 0;
        total = 0;
        for k in response:
            total = total + 1
            out = False
            winner = str(k)
            winnerUsername = db[winner]
            response = requests.get(f'https://www.codewars.com/api/v1/users/{winnerUsername[0]}/code-challenges/completed')
            resObject = response.json()
            try:
                for obj in resObject["data"]:
                    if (str(obj["id"]) == str(db["code"][0])):
                        complete = complete + 1
            except Exception:
                total = total - 1
        await ctx.channel.send(
            f'{complete} / {total} or {int(100 * (complete / total))}% have completed the challenge so far!!')

    @commands.command()
    async def remove(self, ctx, arg1):
        del db[arg1]


def setup(client):
    client.add_cog(CodeWars(client))
