# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    #list of available routes
    return (f"Welcome to the Hawaii Climate API homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    #query measurement table for date and precipitation data for last 12 available month
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=year_ago).\
    filter(Measurement.date <='2017-08-23').all()
    
    session.close()
    
    #add results to dictionary
    precipitation_data={}
    for row in results:
        precipitation_data[row.date] = row.prcp
    
    #return dict in JSON
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    
    #query station table for station names
    results = session.query(Station.name).all()
    
    session.close()
    
    #convert into normal list
    all_stations = list(np.ravel(results))
    
    #return station names in JSON
    return jsonify(all_stations)
        

@app.route("/api/v1.0/tobs")
def tobs():
    
    #determine most active station by count of measurements
    most_active = session.query(Measurement.station).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first()
    
    #query most active station for last 12 available months
    results = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.station == most_active.station).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.date <='2017-08-23').all()
    
    session.close()
    
    #create list of dictionaries containing most active station precipitation data
    results_data = []
    for row in results:
        data_dict = {row.date:row.tobs}
        results_data.append(data_dict)
    
    #return list  of measurements in JSON
    return jsonify(results_data)
        
        
    
        
@app.route("/api/v1.0/<start>")
def start(start):
    
    #create list of data needed for date analysis: Date, Min temp, Max temp, avg temp
    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    #query measurement table with SEL data with start date as query parameter
    results = session.query(*sel).\
    filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    #create list of dictionaries. SEL data for each day
    temp_data = []
    for row in results:
        temp_dict = {}
        temp_dict["Date"] = row[0]
        temp_dict["Min"] = row[1]
        temp_dict["Max"] = row[2]
        temp_dict["AVG"] = row[3]
        temp_data.append(temp_dict)
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    #create list of data needed for date analysis: Date, Min temp, Max temp, avg temp
    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    #query measurement table with SEL data with start date and end date as query parameters
    results = session.query(*sel).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    
    #create list of dictionaries. SEL data for each day
    temp_data = []
    for row in results:
        temp_dict = {}
        temp_dict["Date"] = row[0]
        temp_dict["Min"] = row[1]
        temp_dict["Max"] = row[2]
        temp_dict["AVG"] = row[3]
        temp_data.append(temp_dict)
    return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug=True)
