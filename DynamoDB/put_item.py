import boto3
import logging

dynamodb = boto3.resource('dynamodb')


def put_item(userId: str, create_time: str, deviceId: str, date: str, time: str, repaet: str, method: int):
    try:
        table = dynamodb.Table('Medicine-Notifier-reminder-record')
        table.put_item(
            Item={
                'userId': userId,
                'create_time': create_time,
                'deviceId': deviceId,
                'date': date,
                'time': time,
                'repeat': repaet,
                'method': method
            }
        )
    except:
        logging.info("can't put record to Dynamodb")
