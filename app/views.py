from app import app, db
from app.models import Agency, Launch, Location, Mission
from flask import render_template, jsonify, request
import json
import os
import subprocess

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

@app.route('/about/testResults', methods=['GET'])
def getTestResults():
	#s = subprocess.check_output(['python3','./tests.py'])
	path = os.path.dirname(os.path.realpath(__file__))
	finalPath = os.path.join(path, '../tests.py')
	#p = subprocess.check_output(['python3', finalPath], stderr=subprocess.STDOUT)
	## But do not wait till netstat finish, start displaying output immediately ##
	#print(p)
	process = subprocess.Popen(['python ' + finalPath],shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	returncode = process.wait()
	print('ping returned {0}'.format(returncode))
	#print(process.stdout.read())
	process.stdout.readline()
	process.stdout.readline()
	l = [{"testResults" : str(process.stdout.read())}]#out.decode('utf-8')}]
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
@app.route('/api/<model>/<criteria>')
@app.route('/api/<model>/<criteria>/<int:page>')
@app.route('/api/<model>/<criteria>/<int:page>/<filter>')
def api_model(model, criteria=None, page=None, filter=None):
	# print("---------------------------DEBUG----------------------------------")
	# print(str(model) + " " + str(criteria) + " " + str(page) + " " + str(request.query_string))
	# print("---------------------------DEBUG----------------------------------")
	l = []

	m = ""
	if model == 'agency':
		m = Agency
	elif model == 'launch':
		m = Launch
	elif model == 'location':
		m = Location
	elif model == 'mission':
		m = Mission

	#TODO: citeria sort doesn't work if its related to another model
	#		example: criteria 'mission' does not work for Launch
	#		(for this reason these attributes are currently not in the Model attributes() lists)
	criteria = criteria if criteria in m.attributes() else None

	#TODO: pagination.. need to discuss this, paginate() method is different for query than other methods used here
	#TODO: filter: can use .filter_by or .filter method, not sure how we want to do this
	query_list = m.query.order_by(criteria).all()
	for obj in query_list:
		d = obj.dictionary()
		l.append(d)
	return jsonify(l)

	return "<h1>Model not found</h1>"

#### might use some of these later for pagination?
# @app.route('/api/<model>/<criteria>')
# def api_model_criteria(model, criteria):
# 	return model + " " + criteria

# @app.route('/api/<model>/<criteria>/<int:page>')
# def api_model_criteria_page(model, criteria, page):
# 	return model + " " + criteria + " " + str(page)

# @app.route('/api/<model>/<criteria>/<int:page>/<filter>')
# def api_model_criteria_page_filter(model, criteria, page, filter):
# 	#url: /api/agency/name/1/filter?countryCode=USA
# 	#Use request.query_string to get the parameter to filter with
#     return request.query_string
####

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





