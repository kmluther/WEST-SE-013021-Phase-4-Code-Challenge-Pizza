#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    return make_response([restaurant.to_dict() for restaurant in Restaurant.query.all()], 200)

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if not restaurant:
        return make_response({'error': '404: Restaurant not found'}, 404)
    elif request.method == 'GET':
        return make_response(restaurant.to_dict(), 200)
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({''}, 204)

@app.route('/pizzas', methods=['GET'])
def pizzas():
    if request.method == 'GET':
        pizza_list = [p.to_dict() for p in Pizza.query.all()] 
        response = make_response(
            pizza_list,
            200
        )
        return response

@app.route('/restaurant_pizzas', methods = ['POST'])
def new_restaurant():
    data = request.get_json()
    new_restaurant_pizza = RestaurantPizza(
        price = data['price'],
        pizza_id = data['pizza_id'],
        restaurant_id = data['restaurant_id']
    )
    db.session.add(new_restaurant_pizza)
    db.session.commit()
    try:
        return make_response(new_restaurant_pizza.pizza.to_dict(), 201)
    except ValueError:
        return make_response({'error': ['Invalid input']}, 400) 

if __name__ == '__main__':
    app.run(port=5555, debug=True)
