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
    nonce = soup.findAll('input', {'name': 'nonce'})[0]['value']
    data = {
        'password': npstPass,
        'name': 'Alvebetjent BOT',
        'nonce': nonce
    }

    s.post('https://intranett.npst.no/login', data=data)

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
    r = s.get(url='https://intranett.npst.no/api/v1/challenges/{0}/solves'.format(id))
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
    msg = message.content
    
    #no bot messages
    if message.author == client.user:
        return
    
    #only npst guild
    if message.guild.id != 652630060607733780:
        return

    #cryptobin
    if message.channel.id == 656583866600914953:
        if msg.find('cryptobin.co') != -1:
            await message.delete()
            await message.channel.send('Meldingen din ble slettet fra <#656583866600914953> fordi den ikke inneholdt en cryptobin link. Du kan diskutere løsningene i <#652630061584875532>', delete_after=5)

    #prefix
    if not msg.startswith(prefix):
        return

    #help
    if msg[1:].startswith('help'):
        embed = discord.Embed(description='Hjelp', color=0x50bdfe)
        embed.add_field(name='{0}chall <oppgavenavn>'.format(prefix), value='Printer ut de 10 første som løste en oppgave', inline=False)
        embed.add_field(name='{0}score [brukernavn]'.format(prefix), value='Printer ut enten topp 10 eller scoren til en bruker', inline=False)
        embed.set_footer(text='Etterspurt av: {0.author.name}'.format(message))
        await message.channel.send(embed=embed)

    #challenge scores
    if msg[1:].startswith('chall '):
        cname = msg[7:]
        if getID(cname) != 0:
            names = getChallScore(getID(cname))
            embed = discord.Embed(description=cname, color=0x50bdfe)
            for x in range (len(names)):
                embed.add_field(name='#{0}'.format(str(x+1)), value=names[x], inline=True)
            embed.set_footer(text='Etterspurt av: {0.author.name}'.format(message))
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Ingen challenge med dette navnet!')
        
    #scoreboard
    if msg[1:].startswith('score'):
        pname = msg[7:]
        if pname == ' ' or pname == '': 
            soup = getScoreBoard()
            scoreboard = []
            for x, tag in enumerate(soup.findAll('td')):
                if x < 23 and x > 2:
                    scoreboard.append(tag.text)
                if x > 23:
                    break
            embed = discord.Embed(description='Scoreboard', color=0x50bdfe)
            for x in range(10):
                embed.add_field(name='#{0} ({1}p)'.format(str(x+1), scoreboard[x*2+1]), value=scoreboard[x*2], inline=True)
            embed.set_footer(text='Etterspurt av: {0.author.name}'.format(message))
            await message.channel.send(embed=embed)
        else:
            soup = getScoreBoard()
            nextOne = False
            score = ''
            for tag in soup.findAll('td'):
                name = tag.text.lower().find('\t{0}\n'.format(pname.lower()))
                if nextOne:
                    score = tag.text
                    nextOne = False
                    break
                if name != -1:
                    pname = tag.text
                    nextOne = True
            if score != '':
                embed = discord.Embed(description='Points', color=0x50bdfe)
                embed.add_field(name=pname, value=score, inline=True)
                embed.set_footer(text='Etterspurt av: {0.author.name}'.format(message))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send('Ingen bruker med dette navnet!')

@client.event
async def on_ready():
    print('Logget på som {0.user}'.format(client))

startSession()
client.run(token)