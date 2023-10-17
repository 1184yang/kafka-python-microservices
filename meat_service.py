from confluent_kafka import Producer, Consumer
import json
import random

producer_config = {'bootstrap.servers': '[::1]:9092'}
consumer_config = {
    'bootstrap.servers': '[::1]:9092',
    'group.id': 'meats',
    'auto.offset.reset': 'earliest'
}

meats_producer = Producer(producer_config)
cheese_consumer = Consumer(consumer_config)
cheese_consumer.subscribe(['pizza-with-cheese'])

def start_service():
    try:
        while True:
            msg = cheese_consumer.poll(0.1)
            if msg is None:
                pass
            elif msg.error():
                pass
            else:
                pizza = json.loads(msg.value())
                add_meats(msg.key(), pizza)
    except KeyboardInterrupt:
        print('Consumer interupted: stopping\n')
    finally:
        cheese_consumer.close()

def add_meats(order_id, pizza):
    pizza['meats'] = calc_meats()
    print('Add meats: {}'.format(pizza))
    meats_producer.poll(0)
    meats_producer.produce('pizza-with-meats', key=order_id, value=json.dumps(pizza))
    meats_producer.flush() 
    
def calc_meats():
    i = random.randint(0, 4)
    meats = ['義大利辣香腸', '香腸', '火腿', '鳀魚', '薩拉米', '培根', 'pepperoni', 'sausage', 'ham', 'anchovies', 'salami', 'bacon']
    selection = []
    if i == 0:
        return 'none'
    else:
        for _ in range(i):
            selection.append(meats[random.randint(0, 11)])
    return ' & '.join(set(selection))

if __name__ == '__main__':
    start_service()