import requests

def get_usd_rate():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    usd_rate = data['Valute']['USD']['Value']
    return usd_rate
