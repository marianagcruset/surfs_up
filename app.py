import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask
app = Flask(__name__)
@app.route('/')
@app.route('/')
def hello_world():
    return 'Hello world'

from flask import Flask, jsonify

# access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")
# access and query our SQLite database file
Base = automap_base()
# refelect our tables
Base.prepare(engine, reflect=True)
# references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# session link from Python to our database
session = Session(engine)
# Define our Flask app. This will create a Flask application called "app."
app = Flask(__name__)
# welcome route
@app.route("/")
# add the routing information for each of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
# precipitation analysis route
@app.route("/api/v1.0/precipitation")
# routing info
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# stations route
@app.route("/api/v1.0/stations")
# routing info
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# temperature observations for the previous year route
@app.route("/api/v1.0/tobs")
# routing info
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Last route to report on the minimum, average, and maximum temperatures
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# routing info
def stats(start=2017-6-1, end=2017-6-30):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)