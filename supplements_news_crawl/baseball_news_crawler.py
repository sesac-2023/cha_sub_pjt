"""----------------------------------------------------------------------------
        네이버 야구 - 롯데 뉴스 크롤링하고 "요청 시" 메세지 발신 
----------------------------------------------------------------------------"""
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import requests

with open('./secret', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}

token = secret['TELEGRAM_TOKEN']
chat_id = secret['CHAT_ID']


def fetch_baseball_news():
    async def lotte_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        url = 'https://sports.naver.com/kbaseball/news/list?date={}&isphoto=N&type=team&isPhoto=N&team=LT' # -> 두산 : OB, 한화 : HH 등 추후 구단별로 크롤링 가능 


        response = requests.get(url.format('20230730'))  # 오늘 날짜로 크롤링하기 -> 월요일은 야구 안함. 일요일 날짜로 테스트
        data = json.loads(response.text)  # response.text (str) -> json으로 파싱 (dict으로 구성된 list)
        # print(type(response.text))
        # print(type(data))

        # for key, item in data.items():
        #     print(key,item)
        #     break        

        result = []
        for item in data['list']:
            title = item['title']
            item_url = f"https://sports.naver.com/news?oid={item['oid']}&aid={item['aid']}" # 파라미터 엮어서 링크 만들기

            result.append({
                '제목' : title,
                '링크' : item_url
            })

        '''
        * 입력값 -> 세 가지 경우의 수로 나눠서 생각하기
        1. '롯데'
        2. '롯데 {숫자}'
        3. '롯데 {문자}'
        '''

        input = update.message.text.split()
        target = input[-1]

        # '롯데' 만 입력 시, 최근 기사 5개 발신
        if len(input) == 1: 
            content = [f"{item['제목']}\n{item['링크']}" for item in result[:5]]
            message_to_send = "\n\n".join(content) # 5개의 뉴스를 메세지 한 개에 통합해서 보내기
    
        else:
            try:  
                if 1 <= int(target) <= len(result): # '롯데 {숫자} 입력 시, 최근 첫 번째 기사부터 입력값까지의 기사를 누적해서 보여주기
                    content = [f"{item['제목']}\n{item['링크']}" for item in result[:int(target)]]
                    message_to_send = "\n\n".join(content)
                else:
                    message_to_send = "더 작은 숫자를 입력하세요" # 크롤링한 뉴스 개수보다 큰 숫자를 입력한 경우
            
            except ValueError: # '/롯데 {문자} 입력 시, 해당 키워드가 제목이나 요약에 포함될 경우
                content = [f"{item['제목']}\n{item['링크']}" for item in result if target in item['제목']]

                max_items_to_send = 10
                num_items_to_send = min(max_items_to_send, len(content)) # 기사 수를 최대 10개로 제한하고 10개 보다 적을 경우, 존재하는 만큼만 발신하기

                if content:
                    message_to_send = "\n\n".join(content[:num_items_to_send])
                else:
                    message_to_send = "No matches found." # 해당 키워드에 부합하는 기사가 없을 경우, 안내문 표시
        
        await update.message.reply_text(message_to_send, disable_web_page_preview=True)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("lotte", lotte_news))
    
    app.run_polling()
