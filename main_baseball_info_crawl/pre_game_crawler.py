
import requests
import json
from url_extractor import get_today_pre_game_url


def get_today_pre_game_info():
    url = get_today_pre_game_url()

    # 데이터 가져오기
    response = requests.get(url)
    data = json.loads(response.text)

    # 중첩 딕셔너리로 구성되어 있음. 
    # 라인업 외 추가할 서비스가 있을 경우, 확인 바람 (선수 정보 상세 등)
    info = data['result']['previewData']
    game_info = info['gameInfo']
    home_info = info['homeTeamLineUp']['fullLineUp']
    away_info = info['awayTeamLineUp']['fullLineUp']


    # 필요한 정보만 추출 -> 구장명, 홈팀 이름, 홈팀 라인업, 원정팀 이름, 원정팀 라인업
    game_date = game_info['gdate']
    game_time = game_info['gtime']
    stadium = game_info['stadium']
    home_name = game_info['hName']
    home_lineup = [player['playerName'] for player in home_info]
    away_name = game_info['aName']
    away_lineup = [player['playerName'] for player in away_info]

    info_to_notify = {
        '경기 날짜' : game_date,
        '경기 시간' : game_time,
        '구장명' : stadium, 
        '홈팀 이름' : home_name, 
        '홈팀 라인업' : home_lineup, 
        '원정팀 이름' : away_name, 
        '원정팀 라인업' : away_lineup
    }

    print('get_today_pre_game_info 불러오기 완료')
    return info_to_notify
    # return game_date, game_time, stadium, away_name, home_name, away_lineup, home_lineup