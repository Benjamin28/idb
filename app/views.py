from app import app, db
from app.models import Agency, Launch, Location, Mission
from flask import render_template, jsonify, request
import json
import os
import subprocess
import urllib

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
	#s = subprocess.check_output(['python3','./tests.py'])
	path = os.path.dirname(os.path.realpath(__file__))
	finalPath = os.path.join(path, '../tests.py')
	process = subprocess.check_output(['python3', finalPath], stderr=subprocess.STDOUT)
	## But do not wait till netstat finish, start displaying output immediately ##
	#print(p)
	#process = subprocess.Popen(['python ' + finalPath],shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#print(process.stdout.read())
	#process.readline()
	#process.readline()
	l = [{"testResults" : str(process)}]#out.decode('utf-8')}]
	# i = 1
	# p.stdout.readline()
	# p.stdout.readline()
	# while True and i > 0:
	# 	out = p.stdout.read()
	# 	if out == '' and p.poll() != None:
	# 		break
	# 	if out != '':
	# 		print(out)
	# 	i-=1
	# print(out)

	return jsonify(l)


#API
@app.route('/api/<model>')
def api_model(model):
	# print("---------------------------DEBUG----------------------------------")
	# print(urllib.parse.unquote(str(request.query_string)))
	# print("---------------------------DEBUG----------------------------------")
	NUM_PER_PAGE = 12
	l = []
	m = getModel(model)[0]

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
		if model == 'agency':
			str_dict['agencyType'] = None
		elif model == 'launch':
			str_dict['status'] = None
		elif model == 'location':
			str_dict['countryCode'] = None
		elif model == 'mission':
			str_dict['typeName'] = None

		for pair in split_req_str:
			split_eq = pair.split("=")
			str_dict[split_eq[0]] = split_eq[1]

		criteria = str_dict['orderBy'] if str_dict['orderBy'] in m.attributes() else None
		page_num = int(str_dict['page'])
		page_num = page_num if page_num >= 1 else 1

		query_list = m.query

		if model == 'agency' and str_dict['agencyType'] != None:
			query_list = query_list.filter_by(agencyType=str_dict['agencyType']) 
		elif model == 'launch' and str_dict['status'] != None:
			query_list = query_list.filter_by(status=str_dict['status'])
		elif model == 'location' and str_dict['countryCode'] != None:
			query_list = query_list.filter_by(countryCode=str_dict['countryCode'])
		elif model == 'mission' and str_dict['typeName'] != None:
			query_list = query_list.filter_by(typeName=str_dict['typeName'])

		if(str_dict['order'] == 'desc'):
			query_list = query_list.order_by(desc(criteria)).paginate(page_num, str_dict['limit'], False).items
		else:
			query_list = query_list.order_by(criteria).paginate(page_num, str_dict['limit'], False).items
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
		return "<h1>Model not found</h1>"
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


