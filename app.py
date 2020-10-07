import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#create engine and variables

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

#Establish Flask routes 

@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation data for 2017"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).all()

    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """List of stations"""
    results = session.query(station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Temperature observations (tobs) for 2017"""
 
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= previous_year).all()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """TMIN, TAVG, TMAX"""

    # Select statement
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(measurement.date >= start).all()
       
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run()
