# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def locate_id(id):
    locate = Earthquake.query.filter_by(id=id).first()

    if locate:
        body = locate.to_dict()
        status = 200

    else:
        body = {'message':f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    matching_quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    count = len(matching_quakes)
    quakes_data = []

    for quake in matching_quakes:
        quakes_data.append({
            'id': quake.id,
            'location': quake.location,
            'magnitude': quake.magnitude,
            'year': quake.year
        })

    response_body = {
        'count': count,
        'quakes': quakes_data
    }

    return make_response(response_body, 200)
 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
