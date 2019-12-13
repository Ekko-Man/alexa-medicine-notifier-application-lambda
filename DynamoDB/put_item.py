import boto3
import logging

dynamodb = boto3.resource('dynamodb')


def put_item(userId: str, create_time: str, deviceId: str, datetime: str, frequency_everyday: str, \
    frequency_time_perday: int, method: int):
    try:
        table = dynamodb.Table('Medicine-Notifier-reminder-record')
        table.put_item(
            Item={
                'userId': userId,
                'create_time': create_time,
                'deviceId': deviceId,
                'datetime': datetime,
                'frequency_everyday': frequency_everyday,
                'frequency_time_perday': frequency_time_perday,
                'method': method
            }
        )
    except:
        logging.info("can't put record to Dynamodb")
