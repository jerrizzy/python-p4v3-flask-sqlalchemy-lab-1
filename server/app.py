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
def quake_by_id(id):
   quake = Earthquake.query.filter(Earthquake.id == id).first()

   if quake is None:
       return make_response({'message': f'Earthquake {id} not found.'}, 404)
   
   return make_response(quake.to_dict(), 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def eq_by_magnitude(magnitude):
    # queried the db for Earthquake objects
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(eqs)

    # mapped each Earthquake obj to a dict
    eq_dicts = []
    for eq_obj in eqs:
        eq_dicts.append(eq_obj.to_dict())
    # can use listcomp # eq_dicts = [eq.to_dict() for eq in eqs] 

    # build our response dict
    data = {
        'count': count,
        'quakes': eq_dicts
    }

    return make_response(data, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)











if __name__ == '__main__':
    app.run(port=5555, debug=True)
