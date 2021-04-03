import fitbit
from SecretManager import SecretManager
from datetime import datetime

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
    
    def intraday_time_series(self, resource):
        return self.client.intraday_time_series(resource)

    def get_resources(self):
        return self.RESOURCES
