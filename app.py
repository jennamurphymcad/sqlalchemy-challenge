#Import Flask and Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


#index
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#Query last 12 months of precipitation data
@app.route("/api/v1.0/precipitation")
def percipitations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #set results equaly to query
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    #close session
    session.close()

    #set results into dictionary and append into a empty list
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    #return jsonify result list
    return jsonify(all_prcp)

#Query all stations into a list
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #set results equaly to query
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    #close session
    session.close()

    #return jsonify results
    return jsonify(results)


#Query last 12 months of Temp observations for station with highest observations.
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #set results equal to query 
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()

    #close session
    session.close()

    #return jsonify result
    return jsonify(results)


#Query Min, Max Avg by Start Date provided by user in search bar
@app.route("/api/v1.0/<search_date>")
def start_date(search_date):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #set result equal to query
    result = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),\
                          func.avg(Measurement.tobs)).filter(Measurement.date >= search_date).all()
    
    #close session
    session.close()

    #add results to a dictionary to make result readout a bit more clear
    result_list = []
    for date, min, max, avg in result:
        result_dict = {}
        result_dict[f">="] = search_date
        result_dict["Min Temp"] = min
        result_dict["Max Temp"] = max
        result_dict["Avg Temp"] = avg
        result_list.append(result_dict)

    #return jsonify result
    return jsonify(result_list)


#Query Min, Max, Avg by Start/End Date
@app.route("/api/v1.0/<start>/<end>")
def search_date(start=None, end=None):
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #set result equal to query
    result = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),\
                          func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <=\
                          end).all()
    
    #close session
    session.close()

    #add results to a dictionary to make result readout a bit more clear
    result_list = []
    for date, min, max, avg in result:
        result_dict = {}
        result_dict[f">="] = start
        result_dict[f"<="] = end
        result_dict["Min Temp"] = min
        result_dict["Max Temp"] = max
        result_dict["Avg Temp"] = avg
        result_list.append(result_dict)

    #return jsonify result
    return jsonify(result_list)


if __name__ == "__main__":
    app.run(debug=True)