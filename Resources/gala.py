import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 1. import Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
me = Base.classes.measurement
stat = Base.classes.station



# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/fib<br/>"
        f"/api/v1.0/startend<br/>"
    )


@app.route("/api/v1.0/precipitation")
def get_precipitation():


    qry = session.query(me.date, me.prcp).filter(me.date >= "2016-08-23").filter(me.date <= "2017-08-23").all()
    temps = list(np.ravel(qry))
    return jsonify(temps)

@app.route("/api/v1.0/stations")
def get_station():


    hist = session.query(stat.station).all()
    paimon = list(np.ravel(hist))
    return jsonify(paimon)

@app.route("/api/v1.0/tobs")
def get_tobs():
    hist2 = session.query(me.date, me.tobs).filter(me.station == 'USC00519281').filter(me.date >= "2016-08-23").filter(me.date <= "2017-08-23").all()
    byemon = list(np.ravel(hist2))
    return jsonify(byemon)

@app.route("/api/v1.0/fib")
def start_range():
    bib = session.query(func.avg(me.tobs), func.max(me.tobs), func.min(me.tobs)).filter(me.date >= "2010-01-01").group_by(me.date).all()
    fib = list(np.ravel(bib))
    print(fib)
    return jsonify(fib)

@app.route("/api/v1.0/startend")
def startend():
    gib = session.query(func.avg(me.tobs), func.max(me.tobs), func.min(me.tobs)).filter(me.date >= "2010-01-01").filter(me.date <= "2017-08-23").group_by(me.date).all()
    lib = list(np.ravel(gib))
    return jsonify(lib)

if __name__ == '__main__':
    app.run()