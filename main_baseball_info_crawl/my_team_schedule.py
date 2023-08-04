'''---------------------------------------------------------------------
    my_team_schedule
    
    함수 이름)
    1. get_my_team_month_table()
    2. has_my_team_game_today()

    함수 설명)
    1. my_team의 월간 경기 정보 불러오기  -> list of dictionaries
    2. 오늘 날짜에 my_team 경기 확인 -> boolean
---------------------------------------------------------------------'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from url_extractor import get_month_table_url

def get_my_team_month_table():
    url = get_month_table_url()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    month_table = []
    month_info = soup.select('#calendarWrap')
    for day in month_info:
        day_info = day.select('div[class^="sch_tb"]')

        for item in day_info:
            try:
                date = item.select_one('.td_date').text.split()[0]
                time = item.select_one('.td_hour').text
                away_team = item.select_one('.team_lft').text
                home_team = item.select_one('.team_rgt').text

                month_table.append({
                    '날짜' : date,
                    '시간' : time,
                    '원정팀' : away_team,
                    '홈팀' : home_team,
                })
            
            except AttributeError:
                pass
    
    print('월 단위 경기 정보 불러오기 완료')
    # print(month_table)
    return month_table


current_month = datetime.today().month
current_day = datetime.today().day
today = f'{current_month}.{current_day}'


def has_my_team_game_today():
    month_table = get_my_team_month_table()
    for dictionary in month_table:
        if dictionary['날짜'] == today:
            print('오늘 경기 진행')
            return True   
    return False