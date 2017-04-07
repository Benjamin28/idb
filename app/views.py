from app import app, db
from app.models import Agency, Launch, Location, Mission
from flask import render_template, jsonify, request
from sqlalchemy import desc
import json
import os, sys
import subprocess
import urllib
import operator

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/agency/agency-instance')
def agency_instance():
	return render_template("agency-instance.html")

@app.route('/launch/launch-instance')
def launch_instance():
	return render_template("launch-instance.html")

@app.route('/location/location-instance')
def location_instance():
	return render_template("location-instance.html")

@app.route('/mission/mission-instance')
def mission_instance():
	return render_template("mission-instance.html")

@app.route('/about/testResults', methods=['GET'])
def getTestResults():
	path = os.path.dirname(os.path.realpath(__file__))
	finalPath = os.path.join(path, '../tests.py')
	env = os.environ.copy()
	env['PYTHONPATH'] = ":".join(sys.path)

	f = open(os.path.join(path, "../coverage.txt"), "r")
	s = f.read()
	s += "\n"
	print(s)
	print(finalPath)
	process = subprocess.Popen(
		["python3", finalPath],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		env = env
	)
	(stdout, stderr) = process.communicate()
	percentage = stderr.decode('utf-8')
	percentage = percentage.split("\n", 2)[2]
	s += "\n"
	s += percentage
	l = [{"testResults" : s}]
	return jsonify(l)

#API
@app.route('/api/<model>')
def api_model(model):
	NUM_PER_PAGE = 12
	l = []
	m = getModel(model)[0]
	if m == -1:
		return "<h1>Error 404: Page not found</h1>"	

	req_str = urllib.parse.unquote(str(request.query_string)[2:-1])
	if len(req_str) == 0:
		query_list = m.query.all()
	elif len(req_str.split("&")) == 1 and "id" in req_str:
		query_list = m.query.filter_by(id=req_str.replace("id=", ""))
	else:

		split_req_str = req_str.split("&")
		str_dict = {'orderBy':None,'order':'asc','page':1,'limit':NUM_PER_PAGE}

		#Check which model (agency, launch, location, mission)
		#and change str_dict accordingly with default None values
		if model == 'agencies':
			str_dict['agencyType'] = None
		elif model == 'launches':
			str_dict['status'] = None
		elif model == 'locations':
			str_dict['countryCode'] = None
		elif model == 'missions':
			str_dict['typeName'] = None

		for pair in split_req_str:
			split_eq = pair.split("=")
			split_plus = split_eq[1].split("+")
			if len(split_plus) > 1:
				str_dict[split_eq[0]] = split_plus
			else:
				str_dict[split_eq[0]] = split_eq[1]

		criteria = str_dict['orderBy'] if str_dict['orderBy'] in m.attributes() else 'id'
		page_num = int(str_dict['page'])
		page_num = page_num if page_num >= 1 else 1

		query_list = m.query

		if model == 'agencies' and str_dict['agencyType'] != None:
			if type(str_dict['agencyType']) is list:
				my_list = str_dict['agencyType']
				query_list = query_list.filter(Agency.agencyType.in_(my_list)) 
			else:
				query_list = query_list.filter_by(agencyType=str_dict['agencyType']) 
		elif model == 'launches' and str_dict['status'] != None:
			if type(str_dict['status']) is list:
				my_list = str_dict['status']
				query_list = query_list.filter(Launch.status.in_(my_list)) 
			else:
				query_list = query_list.filter_by(status=str_dict['status'])
		elif model == 'locations' and str_dict['countryCode'] != None:
			if type(str_dict['countryCode']) is list:
				my_list = str_dict['countryCode']
				query_list = query_list.filter(Location.countryCode.in_(my_list)) 
			else:
				query_list = query_list.filter_by(countryCode=str_dict['countryCode'])
		elif model == 'missions' and str_dict['typeName'] != None:
			if type(str_dict['typeName']) is list:
				my_list = str_dict['typeName']
				query_list = query_list.filter(Mission.typeName.in_(my_list)) 
			else:
				query_list = query_list.filter_by(typeName=str_dict['typeName'])

		if(str_dict['order'] == 'desc'):
			query_list = query_list.order_by(desc(criteria)).paginate(page_num, int(str_dict['limit']), False).items
		else:
			query_list = query_list.order_by(criteria).paginate(page_num, int(str_dict['limit']), False).items
		if query_list == []:
			return "<h1>Page "+str(str_dict['page'])+" does not contain any "+model+".</h1>"

	for obj in query_list:
		d = obj.dictionary()
		l.append(d)
	return jsonify(l)

@app.route('/<model>')
def models(model):
	info = getModel(model)
	m = info[0]
	if m == -1:
		return "<h1>Error 404: Page not found</h1>"
	req_str = urllib.parse.unquote(str(request.query_string)[2:-1])

	if "id" in req_str:
		id = req_str.replace("id=", "")
		if info[1] == "agencies":
			return render_template('agency-instance.html')
		elif info[1] == "launches":
			return render_template('launch-instance.html')
		elif info[1] == "locations":
			return render_template('location-instance.html')
		elif info[1] == "missions":
			return render_template('mission-instance.html')

	return render_template(info[1] + ".html")

# @app.route('/<model>')
# @app.route('/<model>/<int:page>')
# def models(model, page=1):
# 	NUM_PER_PAGE = 12
# 	l = []
# 	info = getModel(model)
# 	m = info[0]
# 	if m == -1:
# 		return "<h1>Model not found</h1>"

# 	# print("---------------------------DEBUG----------------------------------")
# 	# # print(request.query_string)
# 	# print(urllib.parse.unquote(str(request.query_string)))
# 	# print("---------------------------DEBUG----------------------------------")

# 	#filtwerin still not working
# 	query_list = m.query.filter_by().paginate(page, NUM_PER_PAGE, False).items
# 	if query_list == []:
# 		return "<h1>Page "+str(page)+" does not contain any "+model+".</h1>"
# 	for obj in query_list:
# 		d = obj.dictionary()
# 		l.append(d)
# 	# return jsonify(l)
# 	return render_template(info[1]+".html",models=l)

# @app.route('/api/<model>/<criteria>/<int:page>/<filter>')
# def api_model_criteria_page_filter(model, criteria, page, filter):
# 	#url: /api/agency/name/1/filter?countryCode=USA
# 	#Use request.query_string to get the parameter to filter with
#     return request.query_string
####

#UTILITY METHODS
def getModel(model):
	if model == 'agencies':
		return (Agency, "agencies")
	elif model == 'launches':
		return (Launch, "launches")
	elif model == 'locations':
		return (Location, "locations")
	elif model == 'missions':
		return (Mission, "missions")
	else:
		return (-1, "Model not found")


