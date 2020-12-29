from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('order_index.html')


@app.route('/order', methods=['POST'])
def new_order():
    name_recieve = request.form['name_give']
    address_recieve = request.form['address_give']
    number_recieve = request.form['number_give']
    phonenumber_recieve = request.form['phonenumber_give']

    order_data = {
        'name' : name_recieve,
        'address' : address_recieve,
        'number' : number_recieve,
        'phonenumber' : phonenumber_recieve
    }
    db.order.insert_one(order_data)
    return jsonify({'result': 'success', 'msg': '주문이 완료되었습니다!'})

@app.route('/order', methods=['GET'])
def read_order() :
    orders = list(db.order.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



