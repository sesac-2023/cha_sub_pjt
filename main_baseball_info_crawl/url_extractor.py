"""----------------------------------------------------------------------------
    url extractor  
    
    함수 이름)
    1. get_month_table_url()
    2. get_monthly_pre_game_urls()
    3. get_today_pre_game_url()
    4. get_monthly_live_update_urls()
    5. get_today_live_update_url()     
    
    함수 설명)
    1. my_team의 월간 경기 정보가 있는 url
    2. 라인업 전송에 필요한 pre_game_url -> 월간 (경기 없는 날 제외)
    3. 라인업 전송에 필요한 pre_game_url -> 오늘 날짜 (경기 없을 경우 none)
    4. 득점 실시간 전송에 필요한 live_update_url -> 월간 (경기 없는 날 제외)
    5. 득점 실시간 전송에 필요한 live_update_url -> 오늘 날짜 (경기 없을 경우 none)

     ** 경기 취소 건 업데이트 어떻게 할지 생각하기
----------------------------------------------------------------------------"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
today = datetime.today().strftime('%Y%m%d')
this_month = datetime.today().strftime('%m')
this_year = datetime.today().strftime('%Y')
my_team = 'LT'

url = f'https://sports.news.naver.com/kbaseball/schedule/index?date={today}&month={this_month}&year={this_year}&teamCode={my_team}'
# url = f'https://sports.news.naver.com/kbaseball/schedule/index?date=20230730&month=07&year={this_year}&teamCode={my_team}' 경기 없는 날 테스트용 url

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
btn = soup.select('.td_btn')



# my_team의 월간 경기 정보가 있는 url 가져오기
def get_month_table_url():
    return url

# 월간 pre_game_urls 가져오기
def get_monthly_pre_game_urls():
    pre_game_urls = []
    for _ in btn:
        url_info = _.select_one('a')['href'].split('/')[2:3]
        part_of_url = url_info[0]
        for date in url_info:
            pre_game_urls.append({
                '경기 날짜' : date[:8],
                'url' : f'https://api-gw.sports.naver.com/schedule/games/{part_of_url}/preview' # https://m.sports.naver.com/game/20230730LTHT02023/lineup -> beautifulsoup 불가능
                })
        
    # print('pre_game_urls 불러오기 완료')
    return pre_game_urls


# 오늘의 pre_game_url 가져오기
def get_today_pre_game_url():
    today_pre_game_url = next((item['url'] for item in get_monthly_pre_game_urls() if item['경기 날짜'] == today), None)
    return today_pre_game_url



# 월간 live_update_urls 가져오기
def get_monthly_live_update_urls():
    live_update_urls = []
    for _ in btn:
        url_info = _.select_one('a')['href'].split('/')[2:3]
        part_of_url = url_info[0]
        for date in url_info:
            live_update_urls.append({
                '경기 날짜' : date[:8],
                'url' : f'https://api-gw.sports.naver.com/schedule/games/{part_of_url}' # https://m.sports.naver.com/game/20230730LTHT02023/lineup -> beautifulsoup 불가능
                })
        
    # print('live_update_urls 불러오기 완료')
    return live_update_urls


# 오늘의 live_update_url 가져오기
def get_today_live_update_url():
    today_live_update_url = next((item['url'] for item in get_monthly_live_update_urls() if item['경기 날짜'] == today), None)
    # today_update_url = None
    # for item in get_monthly_live_update_urls():
    #     # print(each_day)
    #     if item['경기 날짜'] == today:
    #         today_update_url = item['url']
        
    # print('today_update_url 불러오기 완료')
    return today_live_update_url

