import json
from pizza import Pizza, PizzaOrder
from confluent_kafka import Producer, Consumer

producer_config = {'bootstrap.servers': '[::1]:9092'}
consumer_config = {
    'bootstrap.servers': '[::1]:9092',
    'group.id': 'pizza_shop',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'true',
    'max.poll.interval.ms': '3000000'
}

pizza_producer = Producer(producer_config)

pizza_warmer = {}

def order_pizzas(count):
    order = PizzaOrder(count)
    pizza_warmer[order.id] = order
    for _ in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.poll(0)
        pizza_producer.produce('pizza', key=order.id, value=new_pizza.toJSON())
    pizza_producer.flush()
    return order.id

def get_order(order_id):
    try:
        order = pizza_warmer[order_id]
        if order == None:
            return "Order not found, perhaps it's not ready yet."
        else:
            return order.toJSON()
    except KeyError:
        return "Order not found, perhaps it's not ready yet."
    
def load_orders():
    pizza_consumer = Consumer(consumer_config)
    pizza_consumer.subscribe(['pizza-with-veggies'])
    try:
        while True:
            event = pizza_consumer.poll(1.0)
            if event is None:
                pass
            elif event.error():
                print('Bummer - {}'.format(event.error()))
            else:
                pizza = json.loads(event.value())
                add_pizza(pizza['order_id'], pizza)
    except KeyboardInterrupt:
        print('Consumer interupted: stopping\n')
    finally:
        pizza_consumer.close()

def add_pizza(order_id, pizza):
    if order_id in pizza_warmer.keys():
        order = pizza_warmer[order_id]
        order.add_pizza(pizza)