import fitbit
from SecretManager import SecretManager
from datetime import datetime, timedelta, timezone

class Fitbit:
    
    # 取得対象
    RESOURCES = [
        'activities/caloriesBMR',
        'activities/tracker/calories',
        'activities/tracker/steps',
        'activities/tracker/distance',
        'activities/tracker/minutesSedentary',
        'activities/tracker/minutesLightlyActive',
        'activities/tracker/minutesFairlyActive',
        'activities/tracker/minutesVeryActive',
        'activities/tracker/activityCalories',
        'foods/log/water',
    ]
    
    def __init__(self):
        self.client = self.__get_client()
        
    def __get_client(self):
        sm = SecretManager('Fitbit')
        secret = sm.get() 
        return fitbit.Fitbit(
            secret['CLIENT_ID'], 
            secret['CLIENT_SECRET'], 
            access_token = secret['ACCESS_TOKEN'], 
            refresh_token= secret['REFRESH_TOKEN']
        )
        
    def __get_yesterday(self):
        return datetime.now(timezone(timedelta(hours=9))) - timedelta(days=1)
    
    # 前日のサマリーを取得したいので。
    def intraday_time_series(self, resource):
        yesterday = self.__get_yesterday()
        return self.client.intraday_time_series(resource, base_date = yesterday)

    def get_resources(self):
        return self.RESOURCES
        
    def sleep(self):
        return self.client.sleep()
        
    def devices(self):
        return self.client.get_devices()
