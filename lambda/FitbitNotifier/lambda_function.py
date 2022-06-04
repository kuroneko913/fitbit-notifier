import json
from Twitter import Twitter
from Fitbit import Fitbit

OZ_UNIT = 29.565 # 1floz(アメリカ)≒29.57ml

def lambda_handler(event, context):
    fitbit = Fitbit()
    
    # activities
    battery_level = fitbit.devices()[0]['batteryLevel']
    activities = get_fitbit_activities(fitbit)
    message = build_message_for_activities(activities)
    print(message)
    
    # sleep
    sleep = fitbit.sleep()
    sleep_message = build_message_for_sleep(sleep, activities['datetime'], battery_level)
    print(sleep_message)

    # twitterへメッセージを投稿する
    twitter = Twitter()
    twitter.status_update(message)
    twitter.status_update(sleep_message)
    
    return {
        'statusCode': 200,
        'body': json.dumps(activities)
    }
    
def get_fitbit_activities(fitbit):
    results = {}
    for resource in fitbit.get_resources():
        data = fitbit.intraday_time_series(resource)
        results[list(data.keys())[0]] = list(data.values())[0][0]['value']
    results['datetime'] = list(data.values())[0][0]['dateTime']
    return results
    
def build_message_for_activities(activities):
    distances = float(activities['activities-tracker-distance']) * 1.61
    message =  f"本日({activities['datetime']})の運動 from Fitbit\n\n"
    message += f"座っていた時間: {activities['activities-tracker-minutesSedentary']}分\n"
    message += f"軽い運動の時間: {activities['activities-tracker-minutesLightlyActive']}分\n"
    message += f"アクティブな運動の時間: {activities['activities-tracker-minutesFairlyActive']}分\n"
    message += f"激しい運動の時間: {activities['activities-tracker-minutesVeryActive']}分\n\n"
    message += f"本日の歩数: {activities['activities-tracker-steps']}歩 ({distances:.3f}km)\n\n"
    message += f"消費カロリー: {activities['activities-tracker-calories']}kcal ("
    message += f"基礎代謝: {activities['activities-caloriesBMR']}kcal)\n"
    message += f"飲んだ水の量:{float(activities['foods-log-water']) * OZ_UNIT :.2f} (ml)"
    return message

def build_message_for_sleep(sleep, datetime, battery_level):
    sleep_summary = sleep['summary']
    sleep_message = f"本日({datetime})の睡眠時間 from Fitbit\n\n"
    if ('sleep' in sleep and len(sleep['sleep']) == 1):
        sleep_sleep = sleep['sleep'][0]
        sleep_message += f"睡眠時間: {sleep_summary['totalMinutesAsleep']/60 :.3f}時間\n\n"
        sleep_message += f"{sleep_sleep['startTime'].split('T')[1].split('.')[0]} ~ {sleep_sleep['endTime'].split('T')[1].split('.')[0]}\n\n"
    else:
        sleep_message += f"睡眠時間が記録されていませんでした\n\n"
    sleep_message += f"バッテリ残量:{battery_level}%\n"
    return sleep_message