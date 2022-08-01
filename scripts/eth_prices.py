from random import randrange, random
from datetime import datetime, timedelta
from time import sleep
import requests
from kafka import KafkaProducer
import json
import sys

    
while True:
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd').json()
    a=str(datetime.now().isoformat())
    crypto_data={}
    crypto_data['date']=a
    crypto_data['price']=response['ethereum']['usd']
    crypto_data['currency']='usd'
    topic='crypto'
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(topic, crypto_data)
    print(crypto_data)
    sleep(30)
