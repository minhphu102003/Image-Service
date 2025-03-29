import os
from dotenv import load_dotenv
from confluent_kafka import Producer
from confluent_kafka import Consumer

def load_kafka_config():
    load_dotenv()
    return {
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'), 
        'security.protocol': 'SASL_SSL',                   
        'sasl.mechanism': 'PLAIN',                         
        'sasl.username': os.getenv('SASL_USERNAME'),       
        'sasl.password': os.getenv('SASL_PASSWORD'),      
        'client.id': 'image-producer'    
    }

def create_kafka_producer():
    config = load_kafka_config()
    return Producer(config)

def create_kafka_consumer(topic, group_id):
    config = load_kafka_config()
    config.update({
        'group.id': group_id,
        'auto.offset.reset': 'earliest' 
    })
    consumer = Consumer(config)
    consumer.subscribe([topic])
    return consumer