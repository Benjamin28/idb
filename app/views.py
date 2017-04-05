from app import app, db
from app.models import Agency, Launch, Location, Mission
from flask import render_template, jsonify, request
import json

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/agencies')
def agencies():
	return render_template("agencies.html")

@app.route('/launches')
def launches():
	return render_template("launches.html")

@app.route('/locations')
def locations():
	return render_template("locations.html")

@app.route('/missions')
def missions():
	return render_template("missions.html")

@app.route('/about')
def about():
	return render_template("about.html")

#API
@app.route('/api/<model>')
def api_model(model):
	l = []
	if model == 'agency':
		agency_list = Agency.query.all()
		for agency in agency_list:
			d = {"id" : agency.id, "name" : agency.name, "abbrev" : agency.abbrev, "agencyType" : agency.agencyType,
							"countryCode" : agency.countryCode, "wikiUrl" : agency.wikiUrl}
			#RELATIONSHIPS
			launch_d = {launch.id: launch.name for launch in agency.launches}
			mission_d = {mission.id: mission.name for mission in agency.missions}
			d["launches"] = launch_d
			d["missions"] = mission_d
			l.append(d)
		return jsonify(agencies = l)

	elif model == 'launch':
		launch_list = Launch.query.all()
		for launch in launch_list:
			d = {"id" : launch.id, "name" : launch.name, "windowStart" : launch.windowStart, "windowEnd" : launch.windowEnd,
					"videoUrl" : launch.videoUrl, "launchPad" : launch.launchPad, "rocket" : launch.rocket, 
					"location_id" : launch.location_id}
			#RELATIONSHIPS
			agency_d = {agency.id: agency.name for agency in launch.agencies}
			d["agencies"] = agency_d
			d["mission"] = launch.mission.name if launch.mission is not None else "None" 
			l.append(d)
		return jsonify(launches = l)

	elif model == 'location':
		location_list = Location.query.all()
		for location in location_list:
			d = {"id" : location.id, "name" : location.name, "countryCode" : location.countryCode}
			#RELATIONSHIPS
			launch_d = {launch.id: launch.name for launch in location.launches}
			d["launches"] = launch_d
			l.append(d)
		return jsonify(locations = l)

	elif model == 'mission':
		mission_list = Mission.query.all()
		for mission in mission_list:
			d = {"id" : mission.id, "name" : mission.name, "description" : mission.description, "typeName" : mission.typeName,
						"wikiUrl" : mission.wikiUrl, "launch_id" : mission.launch_id}
			#RELATIONSHIPS
			agency_d = {agency.id: agency.name for agency in mission.agencies}
			# launch_id = 
			d["agencies"] = agency_d
			l.append(d)
			#TODO: GET AGENCIES AND LAUNCH ID
		return jsonify(missions = l)
	return "<h1>Model not found</h1>"

@app.route('/api/<model>/<criteria>')
def api_model_criteria(model, criteria):
	return model + " " + criteria

@app.route('/api/<model>/<criteria>/<int:page>')
def api_model_criteria_page(model, criteria, page):
	return model + " " + criteria + " " + str(page)

@app.route('/api/<model>/<criteria>/<int:page>/<filter>')
def api_model_criteria_page_filter(model, criteria, page, filter):
	#url: /api/agency/name/1/filter?countryCode=USA
	#Use request.query_string to get the parameter to filter with
    return request.query_string

# temperal route to dummy pages 
# Should be removed later!!!!!
@app.route('/agencies?id=1')
def agency_1():
	return render_template("temp/agency_1.html");

@app.route('/agencies?id=2')
def agency_2():
	return render_template("temp/agency_2.html");

@app.route('/agencies?id=3')
def agency_3():
	return render_template("temp/agency_3.html");

@app.route('/launches?id=1')
def launches_1():
	return render_template("temp/launches_1.html");

@app.route('/launches?id=2')
def launches_2():
	return render_template("temp/launches_2.html");

@app.route('/launches?id=3')
def launches_3():
	return render_template("temp/launches_3.html");

@app.route('/locations?id=1')
def location_1():
	return render_template("temp/location_1.html");

@app.route('/locations?id=2')
def location_2():
	return render_template("temp/location_2.html");

@app.route('/locations?id=3')
def location_3():
	return render_template("temp/location_3.html");

@app.route('/missions?id=1')
def mission_1():
	return render_template("temp/mission_1.html");

@app.route('/missions?id=2')
def mission_2():
	return render_template("temp/mission_2.html");

@app.route('/missions?id=3')
def mission_3():
	return render_template("temp/mission_3.html");





