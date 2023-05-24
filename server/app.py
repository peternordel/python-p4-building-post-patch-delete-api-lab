#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    # Define a PATCH block inside of the /bakeries/<int:id> route that updates the name of the bakery in the database and returns its data as JSON. As with the previous POST block, the request will send data in a form. The form does not need to include values for all of the bakery's attributes.
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == 'GET':
        bakery_dict = bakery.to_dict()
        response = make_response(
            bakery_dict,
            200
        )
        return response

    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )

        return response
    

# Define a POST block inside of a /baked_goods route that creates a new baked good in the database and returns its data as JSON. The request will send data in a form.
@app.route('/baked_goods', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def baked_goods():
    if request.method == 'POST':
        new_baked_good = BakedGood(
            # what attributes do we need here?
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id"),
        )

        db.session.add(new_baked_good)
        db.session.commit()

        baked_good_dict = new_baked_good.to_dict()

        response = make_response(
            baked_good_dict,
            201
        )

        return response

# Define a DELETE block inside of a /baked_goods/<int:id> route that deletes the baked good from the database and returns a JSON message confirming that the record was successfully deleted.
@app.route('/baked_goods/<int:id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def baked_goods_by_id(id):
    baked_good = BakedGood.query.filter(BakedGood.id == id).first()

    if baked_good == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            baked_good_dict = baked_good.to_dict()

            response = make_response(
                baked_good_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(baked_good, attr, request.form.get(attr))

            db.session.add(baked_good)
            db.session.commit()

            baked_good_dict = baked_good.to_dict()

            response = make_response(
                baked_good_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(baked_good)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Baked good deleted."    
            }

            response = make_response(
                response_body,
                200
            )

            return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
