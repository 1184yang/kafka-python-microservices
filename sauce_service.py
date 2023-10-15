from confluent_kafka import Producer, Consumer
import json
import random

producer_config = {'bootstrap.servers': '[::1]:9092'}
consumer_config = {
    'bootstrap.servers': '[::1]:9092',
    'group.id': 'sauces',
    'auto.offset.reset': 'earliest'
}

sauce_producer = Producer(producer_config)
pizza_consumer = Consumer(consumer_config)
pizza_consumer.subscribe(['pizza'])

def start_service():
    try:
        while True:
            msg = pizza_consumer.poll(0.1)
            if msg is None:
                pass
            elif msg.error():
                pass
            else:
                pizza = json.loads(msg.value())
                add_sauce(msg.key(), pizza)
    except KeyboardInterrupt:
        print('Consumer interupted: stopping\n')
    finally:
        pizza_consumer.close()

def add_sauce(order_id, pizza):
    pizza['sauce'] = calc_sauce()
    print('Add sauce: {}'.format(pizza))
    sauce_producer.poll(0)
    sauce_producer.produce('pizza-with-sauce', key=order_id, value=json.dumps(pizza))
    sauce_producer.flush()

def calc_sauce():
    i = random.randint(0, 8)
    sauces = ['regular', 'light', 'extra', 'none', 'alfredo', 'regular', 'light', 'extra', 'alfredo']
    return sauces[i]

if __name__ == '__main__':
    start_service()
