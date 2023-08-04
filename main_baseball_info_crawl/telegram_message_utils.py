from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests


with open('./secret', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}

token = secret['TELEGRAM_TOKEN']
chat_id = secret['CHAT_ID']



# 업데이트가 있을 때 자동으로 텔레그램 메세지 보내기 -> 라인업, 실시간 득점 정보
def send_automated_message(message):

    url = f'https://api.telegram.org/bot{token}/sendMessage'

    try:
        res = requests.post(url, 
                            json={'chat_id': chat_id, 'text':message})
        print(res.text)
    except Exception as e:
        print(e)


# 경기 전 - 라인업 메세지 포맷
def format_lineup_message(game_time, stadium, away_name, home_name, away_lineup, home_lineup):
    away = f"\n[{away_name} 선발]\n"
    for player in away_lineup:
        away += f"{player}\n"

    home = f"\n[{home_name} 선발]\n"
    for player in home_lineup:
        home += f"{player}\n"

    detail = f"{away_name} vs {home_name}\n{game_time} {stadium}\n"
    
    message_to_send = detail + away + home
    return message_to_send


# 경기 중 - 득점 메세지 포맷
def format_score_message(away_name, home_name, away_score, home_score):
    message_to_send = f'{away_name} {away_score} - {home_score} {home_name}'
    return message_to_send




# -> 디버깅 필요
# 요청 시 텔레그램 메세지 보내기 -> 네이버 뉴스, 네이버 야구 뉴스, 라인업 정보, 득점 상황 등
# def send_message_when_requested(command_name, update.message.text, message_to_send):
#     async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#         await update.message.reply_text(message_to_send, disable_web_page_preview=True)

#     app = ApplicationBuilder().token(token).build()
#     app.add_handler(CommandHandler(command_name, execute_command))
#     app.run_polling()
