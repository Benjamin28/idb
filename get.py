from app.models import *

import requests             # Used for http GET request
import json 				# Used for loading JSON data

# TODO: Add nicer output for empty values, such as in Mission model
# TODO: Clean up code such as removing d and directly creating the Agency instance
# TODO: Convert d into directly using info instead of recreating the dict

#Build dict of AgencyTypes
agencytype_response = requests.get("https://launchlibrary.net/1.2/agencytype")
agencytype_json = json.loads(agencytype_response.text)
agency_types = {}
for agency_type in agencytype_json["types"]:
	agency_types[agency_type["id"]] = agency_type["name"]

#-----------------------
#-------Agency----------
#-----------------------
agency_response = requests.get("https://launchlibrary.net/1.2/agency")
agency_json = json.loads(agency_response.text)
agencies = []

for agency in agency_json["agencies"]:
	d = {}
	inner_agency_response = requests.get("https://launchlibrary.net/1.2/agency/" + str(agency["id"]))
	inner_agency_json = json.loads(inner_agency_response.text)

	for agency_info in inner_agency_json["agencies"]:
		d["name"] = agency_info["name"]
		d["abbrev"] = agency_info["abbrev"]		
		d["agencyType"] = agency_types[agency_info["type"]]
		d["countryCode"] = agency_info["countryCode"]
		d["wikiUrl"] = agency_info["wikiURL"]

	current_agency = Agency(name = d["name"], abbrev = d["abbrev"], agencyType = d["agencyType"], 
							countryCode = d["countryCode"], wikiUrl = d["wikiUrl"])
	db.session.add(current_agency)

	#Relationships
		#Launches should have been added into db with Launch model
		#Missions should have been added into db with Mission model

	agencies.append(d)	

db.session.commit()	

#-----------------------
#-------Launch----------
#-----------------------
launch_response = requests.get("https://launchlibrary.net/1.2/launch")
launch_json = json.loads(launch_response.text)
launches = []

for launch in launch_json["launches"]:
	d = {}
	agencies = []	
	inner_launch_response = requests.get("https://launchlibrary.net/1.2/launch/" + str(launch["id"]))
	inner_launch_json = json.loads(inner_launch_response.text)
	
	for launch_info in inner_launch_json["launches"]:
		d["name"] = launch_info["name"]
		d["windowStart"] = launch_info["windowstart"]
		d["windowEnd"] = launch_info["windowend"]
		d["videoUrl"] = launch_info["vidURLs"][0] if len(launch_info["vidURLs"]) > 0 else "None"
		d["launchPad"] = launch_info["location"]["pads"][0]["name"] if len(launch_info["location"]["pads"]) > 0 else "None"
		d["rocket"] = launch_info["rocket"]["name"]

		#Relationships
		for agency in launch_info["location"]["pads"][0]["agencies"]:
			agencies.append(agency["name"])
		d["agencies"] = agencies
		d["location"] = launch_info["location"]["name"]
		d["mission"] = launch_info["missions"][0]["name"] if len(launch_info["missions"]) > 0 else "None"

	#Get the one location associated with this launch
	if d["location"] != "":
		related_location = db.session.query(Location).filter_by(name = d["location"]).first()

	current_launch = Launch(name = d["name"], windowStart = d["windowStart"], windowEnd = d["windowEnd"], 
							videoUrl = d["videoUrl"], launchPad = d["launchPad"], rocket = d["rocket"],
							location_owner = related_location)

	# Note: Mission should be associated already in Mission model
	db.session.add(current_launch)

	# Get the many agencies associated with this launch
	# TODO: check the agencies, a lot of them don't appear
	for agency in agencies:
		related_agency = db.session.query(Agency).filter_by(name = agency).first()
		if related_agency is not None:
			current_launch.agencies.append(related_agency)

	launches.append(d)	

db.session.commit()

#-----------------------
#-------Location--------
#-----------------------
location_response = requests.get("https://launchlibrary.net/1.2/location")
location_json = json.loads(location_response.text)
locations = []

for location in location_json["locations"]:
	d = {}
	d["name"] = location["name"]
	d["countryCode"] = location["countrycode"]

	current_location = Location(name = d["name"], countryCode = d["countryCode"])
	db.session.add(current_location)

	#Note: Location.launches should be filled in by Launch model

	locations.append(d)

db.session.commit()
		

# -----------------------
# -------Mission---------
# -----------------------
mission_response = requests.get("https://launchlibrary.net/1.2/mission")
mission_json = json.loads(mission_response.text)
missions = []

for mission in mission_json["missions"]:
	d = {}
	agencies = []
	inner_mission_response = requests.get("https://launchlibrary.net/1.2/mission/" + str(mission["id"]))
	inner_mission_json = json.loads(inner_mission_response.text)



	for mission_info in inner_mission_json["missions"]:
		d["name"] = mission_info["name"]
		d["description"] = mission_info["description"]
		d["typeName"] = mission_info["typeName"]
		d["wikiUrl"] = mission_info["wikiURL"]

		#Relationships
		for agency in mission_info["agencies"]:
			agencies.append(agency["name"])
		d["agencies"] = agencies
		d["launch"] = mission_info["launch"]["name"] if len(mission_info["launch"]) > 0 else ""

	#Get the one launch associated with this mission
	if d["launch"] != "":
		related_launch = db.session.query(Launch).filter_by(name = d["launch"]).first()

	current_mission = Mission(name = mission_info["name"], description = mission_info["description"],
							typeName = mission_info["typeName"], wikiUrl = mission_info["wikiURL"],
							launch = related_launch)
	#Get the many agencies associated with this mission
	# TODO: check the agencies, a lot of them don't appear
	for agency in agencies:
		related_agency = db.session.query(Agency).filter_by(name = agency).first()
		if related_agency is not None:
			current_mission.agencies.append(related_agency)

	db.session.add(current_mission)
	missions.append(d)

db.session.commit()
