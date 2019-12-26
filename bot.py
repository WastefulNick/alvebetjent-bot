'''
First real Python project :)
Discord bot that provides statistics for the (N)PST Christmas CTF 2019
Contact andreas#8860 if you have any questions
Use however you wish
'''

import os
import discord
import requests
import urllib.request
import re
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

prefix = '!'

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
npstPass = os.getenv('NPST_PASS')

client = discord.Client()

s = requests.Session()
#start session
def startSession():
    req = s.get('https://intranett.npst.no/login')
    soup = BeautifulSoup(req.text, 'html.parser')
    nonce = soup.findAll("input", {"name": "nonce"})[0]['value']
    data = {
        'password': npstPass,
        'name': 'Alvebetjent BOT',
        'nonce': nonce
    }

    loggedin = s.post('https://intranett.npst.no/login', data=data)


#chall id by name
def getID(challname): 
    r = s.get(url='https://intranett.npst.no/api/v1/challenges')
    parsed = json.loads(r.text[23:-2])

    for item in parsed:
        if item['name'].lower() == challname.lower():
            return item['id']
            break
    return 0

#scoreboard to specific chall
def getChallScore(id):
    r = s.get(url='https://intranett.npst.no/api/v1/challenges/' + str(id) + '/solves')
    parsed = json.loads(r.text[23:-2])
    names = []
    for x, item in enumerate(parsed):
        if x <= 9:
            names.append(item['name'])
        if x >= 9:
            return names
            break
    return names

#scoreboard parsed
def getScoreBoard():
    r = s.get(url='https://intranett.npst.no/scoreboard')
    return BeautifulSoup(r.text, 'html.parser')

@client.event
async def on_message(message):
    #no bot messages
    if message.author == client.user:
        return
    
    #only npst guild
    if message.guild.id != 652630060607733780:
        return

    #cryptobin
    if message.channel.id == 656583866600914953:
        cryptobin = re.search('cryptobin.co', message.content)
        if not cryptobin:
            await message.delete()
            await message.channel.send('Meldingen din ble slettet fra <#656583866600914953> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>', delete_after=5)

    #challenge scores
    if message.content.startswith(prefix + 'chall '):
        cname = message.content[7:]
        names = []
        if getID(cname) != 0:
            names = getChallScore(getID(cname))
            embed = discord.Embed(description=cname, color=0x50bdfe)
            for x in range (len(names)):
                embed.add_field(name='#' + str(x+1), value=names[x], inline=True)
            embed.set_footer(text="Etterspurt av: " + message.author.name)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Ingen challenge med dette navnet!')
        
    #scoreboard
    if message.content.startswith(prefix + 'score'):
        pname = message.content[7:]
        if pname == ' ' or pname == '': 
            soup = getScoreBoard()
            scoreboard = []
            i = 0
            for tag in soup.findAll('td'):
                if i < 23 and i > 2:
                    scoreboard.append(tag.text)
                if i > 23:
                    break
                i += 1
            embed = discord.Embed(description="Scoreboard", color=0x50bdfe)
            for x in range(0, 10):
                embed.add_field(name='#' + str(x+1) + ' (' + scoreboard[x*2+1] + 'p)', value=scoreboard[x*2], inline=True)
            embed.set_footer(text="Etterspurt av: " + message.author.name)
            await message.channel.send(embed=embed)
        else:
            myRegex = r'\t' + re.escape(pname.lower()) + r'\n'
            soup = getScoreBoard()
            nextOne = False
            score = ''
            for tag in soup.findAll('td'):
                name = re.search(myRegex, tag.text.lower())
                if nextOne:
                    score = tag.text
                    nextOne = False
                    break
                if name:
                    pname = tag.text
                    nextOne = True
            embed = discord.Embed(description="Points", color=0x50bdfe)
            embed.add_field(name=pname, value=score, inline=True)
            embed.set_footer(text="Etterspurt av: " + message.author.name)
            await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logget på som {0.user}'.format(client))

startSession()
client.run(token)