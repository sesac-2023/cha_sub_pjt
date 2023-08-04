#===============================================================================
#          연습 - 네이버 뉴스(연합뉴스) 크롤링하고 "요청 시" 메세지 발신
#=============================================================================== 

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


with open('./secret', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}

token = secret['TELEGRAM_TOKEN']
chat_id = secret['CHAT_ID']

headers = {'User-Agent' :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
today = datetime.now().strftime('%Y%m%d')


def fetch_naver_news():
    async def naver_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date={}&page={}'  #연합뉴스 : 001, 한국경제 : 015 등등 -> 추후 언론사별로 크롤링할 수 있을 듯 (뉴스-연합 맨시티)
        
        result = []
        for page_number in range(1, 6):  # 5페이지까지 크롤링
            response = requests.get(url.format(today, page_number), headers=headers) # 오늘 날짜로 크롤링
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('ul[class^="type06"] li')

            for news in news_items:
                title = news.select('dt')[-1].text.strip()
                item_url = news.select_one('a')['href']
                content = news.select_one('.lede').text.strip()

                result.append({
                    '제목': title,
                    '요약': content,
                    '링크': item_url
                })    
        
        '''
        * 입력값 -> 세 가지 경우의 수로 나눠서 생각하기
        1. '뉴스'
        2. '뉴스 {숫자}'
        3. '뉴스 {문자}'
        '''
    
        input = update.message.text.split()
        target = input[-1]

        # '뉴스' 만 입력 시, 최근 기사 5개 발신
        if len(input) == 1: # and input[0] == 'news' 불필요함 
            content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result[:5]]
            message_to_send = "\n\n".join(content) # 5개의 뉴스를 메세지 한 개에 통합해서 보내기

        else: 
            try:                   
                if 1 <= int(target) <= len(result): # '뉴스 {숫자}' 입력 시, 최근 첫 번째 기사부터 입력값까지의 기사를 누적해서 보여주기
                    content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result[:int(target)]] #'뉴스 0'이라고 입력 시, 출력되는 결과값 없음.
                    message_to_send = "\n\n".join(content)
                else:
                    message_to_send = '더 작은 숫자를 입력하세요'  # 크롤링한 뉴스 개수보다 큰 숫자를 입력한 경우
                
            except ValueError: # '뉴스 {문자}' 입력 시, 해당 키워드가 제목이나 요약에 포함될 경우
                content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result if target in item['제목'] or target in item['요약']]

                if content:
                    max_items_to_send = 10
                    num_items_to_send = min(max_items_to_send, len(content)) # 기사 수를 최대 10개로 제한하고 10개 보다 적을 경우, 존재하는 만큼만 발신하기 

                    message_to_send = "\n\n".join(content[:num_items_to_send])
                else:
                    message_to_send = "No matches found." # 해당 키워드에 부합하는 기사가 존재하지 않을 경우, 안내문 표시
        
        await update.message.reply_text(message_to_send, disable_web_page_preview=True)


    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("news", naver_news))

    app.run_polling()


        