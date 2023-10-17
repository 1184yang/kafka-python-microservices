from flask import Flask
from threading import Thread
import json
import pizza_service

app = Flask(__name__)
app.json.ensure_ascii = False
app.json_encoder

@app.route('/')
def hello():
    return "Hello Tainan, 台南!"

# 送出訂單: curl -X POST http://localhost:5000/order/5
#      or: curl -H "Content-Type: application/json" --request POST -d '{"count":5}' http://localhost:5000/order/count
@app.route('/order/<count>', methods=['POST'])
def order_pizzas(count):
   order_id = pizza_service.order_pizzas(int(count))
   return json.dumps({"order_id": order_id})

# 取得訂單資料: curl http://localhost:5000/order/{{pizza-order-UUID}}
@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
   print('order: {}'.format(pizza_service.get_order(order_id)))
   return pizza_service.get_order(order_id)

# @app.before_request
def launch_consumer():
    print('Startup Pizza Service Consumer')
    t = Thread(target=pizza_service.load_orders)
    t.start()

if __name__ == '__main__':
    launch_consumer()
    app.run()