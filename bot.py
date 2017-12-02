import discord
from discord.ext.commands import Bot
from discord.ext import commands
import requests as rq
from bs4 import BeautifulSoup as bs

# 디스코드 클라이언트를 생성합니다.
Client = discord.Client()
client = commands.Bot(command_prefix=None)

# 디소코드 봇 시작시 봇의 name과 id를 출력합니다.
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    if message.content.startswith('!message'):  # 디스코드에서 입력된 문자열이 !message로 시작하는지 체크합니다.
        counter = 0
        # 메세지를 입력받은 채널로 메세지를 전송합니다.
        tmp = await client.send_message(message.channel, '최근 100개의 메시지를 체크중입니다...')
        # 최근 백개의 메시지의 로그를 확인합니다.
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:    # 백개의 메시지 중에서 명령어를 입력한 유저의 메시지 개수를 셉니다.
                counter += 1
        await client.edit_message(tmp, '너의 메시지는 {}개 입니다.'.format(counter))  # 보냈던 메시지를 수정하여 메시지 개수를 전송합니다.

    elif message.content.startswith('!실시간'):    # 디스코드에서 입력된 문자열이 !실시간으로 시작하는지 체크합니다.
        # 11월 18일자 requests를 이용한 네이버 실시간 검색어 출력 코드입니다.
        content = ''
        req = rq.get("https://datalab.naver.com")
        html = req.text
        soup = bs(html, 'html.parser')

        keyword_rank = soup.find('div', {'class':'rank_inner v2'})
        date = keyword_rank.find('strong', {'class':'rank_title v2'}).text
        rank = keyword_rank.find_all('a', {'class':'list_area'})

        content += date + '\r\n'
        for l in rank:
            number = l.find('em').text
            keyword = l.find('span').text
            content += number + " " + keyword + '\r\n'
        await client.send_message(message.channel, content)

    # !야 입력시 '왜'가 나옴
    elif message.content.startswith("!야"):
        await client.send_message(message.channel, "왜")
    
    # !S stands for 입력시 'S로 시작되는 단어 나열
    elif message.content.startswith("!S stands for"):
        await client.send_message(message.channel, "Smile Sweet Sister Sadistic Suprise Service")

    # !echo --- 입력시 '---'이 출력 됌
    elif message.content.startswith("!echo"):
        try:
            content = message.content.split()
            print(content)
            await client.send_message(message.channel, content[1])
        # '---' 없을 시 'Error' 출력
        except:
            await client.send_message(message.channel, "Error")
    # !Help 입력시 명령어들 출력
    elif message.content.startswith("!help"):
        cmd_list = """[사용 할 수 있는 명령어들을 출력합니다.]
야   :   !야 입력시 '왜'를 출력합니다.
S stands for   :   !S stands for 입력시 'S로 시작되는 단어 나열합니다.
echo   :   !echo --- 입력시 '---'이 출력됩니다.
        """
        await client.send_message(message.channel, cmd_list)
    # elif message.content.startswith(""):
    #     await client.send_message(message.channel, "")



client.run('Mzg2MzM0NjE4ODkyMzY5OTMw.DQOaPg.nLRbGBItci771nEKvJ-3-FHN5Eo')
