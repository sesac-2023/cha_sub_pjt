import time
from datetime import datetime, timedelta
from my_team_schedule import has_my_team_game_today
from pre_game_crawler import get_today_pre_game_info
from live_update_crawler import get_today_live_update_score, get_today_team_name, get_game_status, get_current_inning
from telegram_message_utils import format_lineup_message, format_score_message, send_automated_message


# 라인업 전송
def send_today_game_info():
    data = get_today_pre_game_info()
    game_date, game_time, stadium, away_name, home_name = data['경기 날짜'], data['경기 시간'], data['구장명'], data['원정팀 이름'], data['홈팀 이름'] 
    away_lineup = data['원정팀 라인업'] # list
    home_lineup = data['홈팀 라인업'] # list
    message_to_send = format_lineup_message(game_time, stadium, away_name, home_name, away_lineup, home_lineup)
    print('라인업 전송 완료')
    return send_automated_message(message=message_to_send)
    



def send_score_real_time():
    global score
    away_name, home_name = get_today_team_name()
    current_score = get_today_live_update_score()
    away_score, home_score = current_score[away_name], current_score[home_name]
    print('득점 정보 확인 중')
    if score != current_score:
        # message_to_send = format_score_message(away_name, home_name, away_score, home_score)
        message_to_send = f'{get_current_inning()}\n{format_score_message(away_name, home_name, away_score, home_score)}'
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
    period = 400
    on_game = False
    
    while True:
        if has_my_team_game_today():
            print('금일 경기 진행')
            if on_game == False:
                period = 400
                if not lineup_sent_60m and is_to_fetch_lineup(60):
                    send_today_game_info()
                    lineup_sent_60m = True
                
                if not lineup_sent_30m and is_to_fetch_lineup(30):
                    send_today_game_info()
                    lineup_sent_30m = True

                if is_to_fectch_score():
                    print('경기 중')
                    on_game = True
                
            else:
                period = 10
                print('득점 확인 중')
                send_score_real_time()

                if get_game_status() == 'RESULT': # 'BEFORE', 'STARTED', 'RESULT'
                    send_automated_message(message='경기 종료')
                    print('경기 종료')
                    lineup_sent_60m = False
                    lineup_sent_30m = False
                    score = None
                    period = 400
                    on_game = False

        else:
            period = 43200 + 60

        time.sleep(period)
