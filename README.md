# sqlalchemy-challenge

Hello!

the following repo contains files for Washington University bootcamp module 10 assignment. 
There are two ways to interact with the data and files provided. 

1. You can open the jupyter notebook file and run the cells to see analysis and plots of the precipitation data of the latest 12 months available. 
this file is located "SurfsUp->climate.ipynb"
2. You can launch the 'app.py file located "SurfsUp->app.py", This will launch a local server for an app where you can obtain the IP address and make calls locally in your browser. The available routes are as provided below:

Available Routes:
/api/v1.0/precipitation - provides a list of precipitation data for last 12 months of available data
/api/v1.0/stations - provides list of station names
/api/v1.0/tobs - provides precipitation data for the most active station
/api/v1.0/start_date - provides min, max, avg precipitation data by date range defined by start date
/api/v1.0/start_date/end_date - provides min, max, avg precipitation data by date range defined by start date and end date

This analysis and code was written by Cody Allison

References: Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml