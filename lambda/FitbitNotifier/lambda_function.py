import json
from Twitter import Twitter
from Fitbit import Fitbit

def lambda_handler(event, context):

    results = {}
    fitbit = Fitbit()
    for resource in fitbit.get_resources():
        data = fitbit.intraday_time_series(resource)
        print(data)
        results[list(data.keys())[0]] = list(data.values())[0][0]['value']
    results['datetime'] = list(data.values())[0][0]['dateTime']
    
    distances = float(results['activities-tracker-distance']) * 1.61

    message =  f"本日({results['datetime']})の運動 from Fitbit\n\n"
    message += f"座っていた時間: {results['activities-tracker-minutesSedentary']}分\n"
    message += f"軽い運動の時間: {results['activities-tracker-minutesLightlyActive']}分\n"
    message += f"アクティブな運動の時間: {results['activities-tracker-minutesFairlyActive']}分\n"
    message += f"激しい運動の時間: {results['activities-tracker-minutesVeryActive']}分\n\n"
    message += f"本日の歩数: {results['activities-tracker-steps']}歩 ({distances:.3f}km)\n\n"
    message += f"消費カロリー: {results['activities-tracker-calories']}kcal ("
    message += f"基礎代謝: {results['activities-caloriesBMR']}kcal)"
    
    print(message)

    # twitterへメッセージを投稿する
    twitter = Twitter()
    twitter.status_update(message)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
