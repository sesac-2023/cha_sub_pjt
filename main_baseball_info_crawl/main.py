import time
from datetime import datetime, timedelta
from my_team_schedule import has_my_team_game_today
from pre_game_crawler import get_today_pre_game_info
from live_update_crawler import get_today_live_update_score, get_today_team_name
from telegram_message_utils import format_lineup_message, format_score_message, send_automated_message


# 라인업 전송
def send_today_game_info():
    data = get_today_pre_game_info()
    game_date, game_time, stadium, away_name, home_name = data['경기 날짜'], data['경기 시간'], data['구장명'], data['원정팀 이름'], data['홈팀 이름'] 
    away_lineup = data['원정팀 라인업'] # list
    home_lineup = data['홈팀 라인업'] # list
    message_to_send = format_lineup_message(game_time, stadium, away_name, home_name, away_lineup, home_lineup)
    print('라인업 전송 완료')
    return send_automated_message(message=message_to_send, disable_web_page_preview=True)
    


def send_score_real_time():
    global score
    away_name, home_name = get_today_team_name()
    current_score = get_today_live_update_score()
    away_score, home_score = current_score[away_name], current_score[home_name]
    print('득점 정보 확인 중')
    if score != current_score:
        message_to_send = format_score_message(away_name, home_name, away_score, home_score)
        send_automated_message(message=message_to_send)
        print('득점 정보 전송 완료')
        score = current_score  




# 경기 시간과 현재 시간 비교
def is_to_fectch_score():
    now = datetime.now()
    data = get_today_pre_game_info()
    game_begins = datetime.strptime(str(data['경기 날짜'])+data['경기 시간'], '%Y%m%d%H:%M')
    if game_begins <= now < game_begins + timedelta(hours=4):
        return True
    return False


def is_to_fetch_lineup_60m():
    now = datetime.now()
    data = get_today_pre_game_info()
    game_begins = datetime.strptime(str(data['경기 날짜'])+data['경기 시간'], '%Y%m%d%H:%M')
    if game_begins - timedelta(hours=1) <= now <= game_begins - timedelta(minutes=50):
        return True
    return False


def is_to_fetch_lineup(minutes_before_game):
    now = datetime.now()
    data = get_today_pre_game_info()
    game_begins = datetime.strptime(str(data['경기 날짜']) + data['경기 시간'], '%Y%m%d%H:%M')
    return game_begins - timedelta(minutes=minutes_before_game) <= now <= game_begins - timedelta(minutes=minutes_before_game - 10)



if __name__ == "__main__":
    lineup_sent_60m = False
    lineup_sent_30m = False
    score = None
    
    if has_my_team_game_today():
        while True:
            if not lineup_sent_60m and is_to_fetch_lineup(60):
                send_today_game_info()
                lineup_sent_60m = True
            period = 400
            
            if not lineup_sent_30m and is_to_fetch_lineup(30):
                send_today_game_info()
                lineup_sent_30m = True
            period = 400                            

            if is_to_fectch_score():
                send_score_real_time()
            period = 10

            time.sleep(period)






#         # 현재 날짜, 시간 -> 변수에 할당 10분마다 업데이트 time.sleep(600)
        

#         # 1. 오늘날짜 경기가 시작 전인지 체크
#         # 경기시작 시간 datetime으로 변환 - 현재 시간과 비교 -> 한 시간 이내, 30분 이내
#         # 발송했는지 체크 boolean 변수 필요 (1시간, 30분 각각) 
#         # 현재 시간 > 경기 시간 지나면 boolean변수 초기화 False
#         # period = 10


#         # 2. 오늘날짜 경기가 있다면, 현재 시간이 경기시작 한 시간 전인지
#         #  - 1시간 전이면 라인업 발송 (30분 전)



#             # 3. 경기 시작했으면, (10초마다)
#             #   - 스코어 확인 후 변경사항이 있으면 텔레그램 발송
#             # time.sleep(10) 변경 -> 변수로 바꾸기 
#             # 이전 점수 - 현재 점수 비교 후 텔레그램 메세지


        

