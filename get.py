from app.models import *

import requests             # Used for http GET request
import json 				# Used for loading JSON data

# INSTRUCTIONS:
	# Create agency, then location, then launch, then mission
	# Do each part separately
# TODO: Add nicer output for empty values, such as in Mission model
# TODO: Gather more data from API, LOTS of missing values in the Mission.launch

#Global dict that stores the agency types(key: type_id, value: type_name)
agency_types = {}

#Build dict of AgencyTypes
def create_agency_types():
	agencytype_response = requests.get("https://launchlibrary.net/1.2/agencytype")
	agencytype_json = json.loads(agencytype_response.text)	
	for agency_type in agencytype_json["types"]:
		agency_types[agency_type["id"]] = agency_type["name"]

#-----------------------
#-------Agency----------
#-----------------------
def create_agency():
	print("Creating agency")
	agency_response = requests.get("https://launchlibrary.net/1.2/agency")
	agency_json = json.loads(agency_response.text)

	for agency in agency_json["agencies"]:
		inner_agency_response = requests.get("https://launchlibrary.net/1.2/agency/" + str(agency["id"]))
		inner_agency_json = json.loads(inner_agency_response.text)

		agency_info = inner_agency_json["agencies"][0]
		current_agency = Agency(name = agency_info["name"], abbrev = agency_info["abbrev"], agencyType = agency_types[agency_info["type"]], 
								countryCode = agency_info["countryCode"], wikiUrl = agency_info["wikiURL"])
		db.session.add(current_agency)
		# Relationships
			# Launches should have been added into db with Launch model
			# Missions should have been added into db with Mission model

	db.session.commit()	

#-----------------------
#-------Launch----------
#-----------------------
def create_launch():
	print("Creating launch")
	launch_response = requests.get("https://launchlibrary.net/1.2/launch")
	launch_json = json.loads(launch_response.text)

	for launch in launch_json["launches"]:
		inner_launch_response = requests.get("https://launchlibrary.net/1.2/launch/" + str(launch["id"]))
		inner_launch_json = json.loads(inner_launch_response.text)
		
		launch_info = inner_launch_json["launches"][0]

		current_videoUrl = launch_info["vidURLs"][0] if len(launch_info["vidURLs"]) > 0 else "None"
		current_launchPad = launch_info["location"]["pads"][0]["name"] if len(launch_info["location"]["pads"]) > 0 else "None"

		#Relationships

		# LOCATION
		# Get the one location associated with this launch
		current_location = launch_info["location"]["name"]
		if current_location != "":
			related_location = db.session.query(Location).filter_by(name = current_location).first()

		current_launch = Launch(name = launch_info["name"], windowStart = launch_info["windowstart"], windowEnd = launch_info["windowend"], 
								videoUrl = current_videoUrl, launchPad = current_launchPad, rocket = launch_info["rocket"]["name"],
								location_owner = related_location)

		db.session.add(current_launch)

		# MISSION
		# Note: Mission should be associated already in Mission model

		# AGENCY
		# Get the many agencies associated with this launch
		# TODO: check the agencies, a lot of them don't appear
		for agency in launch_info["location"]["pads"][0]["agencies"]:
			related_agency = db.session.query(Agency).filter_by(name = agency["name"]).first()
			if related_agency is not None:
				current_launch.agencies.append(related_agency)

	db.session.commit()

#-----------------------
#-------Location--------
#-----------------------
def create_location():
	print("Creating location")
	location_response = requests.get("https://launchlibrary.net/1.2/location")
	location_json = json.loads(location_response.text)

	for location in location_json["locations"]:

		current_location = Location(name = location["name"], countryCode = location["countrycode"])
		db.session.add(current_location)

		# Relationships

		# LAUNCH
		# Note: Location.launches should be filled in by Launch model

	db.session.commit()

# -----------------------
# -------Mission---------
# -----------------------
def create_mission():
	print("Creating mission")
	mission_response = requests.get("https://launchlibrary.net/1.2/mission")
	mission_json = json.loads(mission_response.text)

	for mission in mission_json["missions"]:
		inner_mission_response = requests.get("https://launchlibrary.net/1.2/mission/" + str(mission["id"]))
		inner_mission_json = json.loads(inner_mission_response.text)

		mission_info = inner_mission_json["missions"][0]

		# Relationships
		# LAUNCH
		# Get the one launch associated with this mission

		current_launch = mission_info["launch"]["name"] if len(mission_info["launch"]) > 0 else ""
		if current_launch != "":
			related_launch = db.session.query(Launch).filter_by(name = current_launch).first()

		current_mission = Mission(name = mission_info["name"], description = mission_info["description"],
								typeName = mission_info["typeName"], wikiUrl = mission_info["wikiURL"],
								launch = related_launch)

		# AGENCY
		# Get the many agencies associated with this mission
		# TODO: check the agencies, a lot of them don't appear
		for agency in mission_info["agencies"]:
			related_agency = db.session.query(Agency).filter_by(name = agency["name"]).first()
			if related_agency is not None:
				current_mission.agencies.append(related_agency)

		db.session.add(current_mission)

	db.session.commit()

def main():
	print("Inside main")
	create_agency_types()
	create_agency()
	create_location()
	create_launch()
	create_mission()


if __name__ == "__main__":
    main()

