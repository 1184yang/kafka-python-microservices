from confluent_kafka import Producer, Consumer
import json
import random

producer_config = {'bootstrap.servers': '[::1]:9092'}
consumer_config = {
    'bootstrap.servers': '[::1]:9092',
    'group.id': 'cheeses',
    'auto.offset.reset': 'earliest'
}

cheese_producer = Producer(producer_config)
sauce_consumer = Consumer(consumer_config)
sauce_consumer.subscribe(['pizza-with-sauce'])

def start_service():
    try:
        while True:
            msg = sauce_consumer.poll(0.1)
            if msg is None:
                pass
            elif msg.error():
                pass
            else:
                pizza = json.loads(msg.value())
                add_cheese(msg.key(), pizza)
    except KeyboardInterrupt:
        print('Consumer interupted: stopping\n')
    finally:
        sauce_consumer.close()

def add_cheese(order_id, pizza):
    pizza['cheese'] = calc_cheese()
    print('Add cheese: {}'.format(pizza))
    cheese_producer.poll(0)
    cheese_producer.produce('pizza-with-cheese', key=order_id, value=json.dumps(pizza))
    cheese_producer.flush()
    
def calc_cheese():
    i = random.randint(0, 6)
    cheeses = ['特加乳酪', '不加乳酪', '三倍乳酪', '山羊乳酪', 'extra', 'three cheese', 'goat cheese']
    return cheeses[i]

if __name__ == '__main__':
    start_service()
