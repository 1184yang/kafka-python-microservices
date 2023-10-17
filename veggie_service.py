from confluent_kafka import Producer, Consumer
import json
import random

producer_config = {'bootstrap.servers': '[::1]:9092'}
consumer_config = {
    'bootstrap.servers': '[::1]:9092',
    'group.id': 'veggies',
    'auto.offset.reset': 'earliest'
}

veggies_producer = Producer(producer_config)
meats_consumer = Consumer(consumer_config)
meats_consumer.subscribe(['pizza-with-meats'])

def start_service():
    try:
        while True:
            msg = meats_consumer.poll(0.1)
            if msg is None:
                pass
            elif msg.error():
                pass
            else:
                pizza = json.loads(msg.value())
                add_veggies(msg.key(), pizza)
    except KeyboardInterrupt:
        print('Consumer interupted: stopping\n')
    finally:
        meats_consumer.close()

def add_veggies(order_id, pizza):
    pizza['veggies'] = calc_veggies()
    print('Add veggies: {}'.format(pizza))
    veggies_producer.poll(0)
    veggies_producer.produce('pizza-with-veggies', key=order_id, value=json.dumps(pizza))
    veggies_producer.flush()

def calc_veggies():
    i = random.randint(0, 4)
    veggies = ['番茄', '橄欖', '洋蔥', '胡椒', '鳳梨', '蘑菇', 'tomato', 'olives', 'onions', 'peppers', 'pineapple', 'mushrooms']
    selection = []
    if i == 0:
        return 'none'
    else:
        for _ in range(i):
            selection.append(veggies[random.randint(0, 11)])
    return ' & '.join(set(selection))

if __name__ == '__main__':
    start_service()