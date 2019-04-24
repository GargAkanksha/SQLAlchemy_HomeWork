import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#####################################
app = Flask(__name__)
last_year="2016-08-23"
@app.route("/")
def welcome():
    return(
        f"Welcome to Hawaii Weather API:<br/>"
        f"/api/v1.0/Precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/Temperature Obersevations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end_date<br/>"
    )

#/api/v1.0/Precipitation<br/>
@app.route("/api/v1.0/Precipitation")
def Precipitation():
    Precipitations = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date.between("2016-08-23","2017-08-23")).\
    order_by(Measurement.date).all()
    return jsonify(Precipitations)

#/api/v1.0/stations<br/>
@app.route("/api/v1.0/stations")
def stations():
    stations= session.query(Station.station, Station.name).all()
    return jsonify(stations)

#/api/v1.0/Temperature Obersevations
@app.route("/api/v1.0/Temperature Obersevations")
def tobs():
    temp = session.query( Measurement.date,Measurement.station,Measurement.tobs).\
    filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()
    return jsonify(temp)

#/api/v1.0/Start
@app.route("/api/v1.0/<date>")
def start(date):
    tem = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
    func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(tem)

#/api/v1.0/start/end_date
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    Tem_Result_Period = session.query(func.min(Measurement.tobs),\
    func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(Tem_Result_Period)

if __name__ == "__main__":
    app.run(debug=True)