import requests
import json
from url_extractor import get_today_live_update_url


def get_today_live_update_score():

    """
    Return:
    홈팀, 원정팀 실시간 득점 -> 딕셔너리
    
    Example: {'롯데': 2, '두산': 1}
    """

    url = get_today_live_update_url()

    response = requests.get(url)
    data = json.loads(response.text)

    info = data['result']['game']
    away_name = info['awayTeamName']
    home_name = info['homeTeamName']
    away_score = info['awayTeamScore']
    home_score = info['homeTeamScore']

    current_score = {
        away_name : away_score,
        home_name : home_score
    }
    
    # print('get_today_live_update_score 불러오기 완료')
    return current_score


def get_today_team_name():
    url = get_today_live_update_url()

    response = requests.get(url)
    data = json.loads(response.text)

    info = data['result']['game']
    away_name = info['awayTeamName']
    home_name = info['homeTeamName']
    away_score = info['awayTeamScore']
    home_score = info['homeTeamScore']

    return away_name, home_name


def get_game_status():
    url = get_today_live_update_url()

    response = requests.get(url)
    data = json.loads(response.text)
    
    game_status = data['result']['game']['statusCode']
    return game_status


def get_current_inning():
    url = get_today_live_update_url()

    response = requests.get(url)
    data = json.loads(response.text)
    
    current_inning = data['result']['game']['statusInfo']
    return current_inning