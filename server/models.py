from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'Name: {self.name} | Ingredients: {self.ingredients}'
    
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    serialize_rules = ('-created_at', '-updated_at', '-restaurants', '-restaurant_pizzas')

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError({'error': 'Price must be between 1 and 30'})
        return price

    def __repr__(self):
        return f'Price: {self.price} | pizza_id: {self.pizza_id} | restaurant_id: {self.restaurant_id}'
    
    serialize_rules = ('-created_at', '-updated_at', '-pizza_id', '-restaurant_id')
    
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def __repr__(self):
        return f'Name: {self.name} | Address: {self.address}'
    
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    serialize_rules = ('-restaurant_pizzas', '-pizzas')