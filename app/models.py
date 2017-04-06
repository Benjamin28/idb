from app import db

am_associationTable = db.Table('am_association',
	db.Column('agency_id', db.Integer, db.ForeignKey('agency.id')),
	db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'))
)

al_associationTable = db.Table('al_association',
	db.Column('agency_id', db.Integer, db.ForeignKey('agency.id')),
	db.Column('launch_id', db.Integer, db.ForeignKey('launch.id'))
)

class Agency(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True)
	abbrev = db.Column(db.String())
	agencyType = db.Column(db.String())
	countryCode = db.Column(db.String())
	wikiUrl = db.Column(db.String())

	# launches attr appears to be here with the backref in the Launch model
	# Can call Agency.launches to get the list of launches

	# missions attr appears to be here with the backref in the Mission model
	# Can call Agency.missions to get the list of missions

	def dictionary(self):
		d = {"id" : self.id, "name" : self.name, "abbrev" : self.abbrev, "agencyType" : self.agencyType,
							"countryCode" : self.countryCode, "wikiUrl" : self.wikiUrl}
		d["launches"] = {launch.id: launch.name for launch in self.launches}
		d["missions"] = {mission.id: mission.name for mission in self.missions}
		return d

	def attributes():
		return ['id','name','abbrev','agencyType','countryCode','wikiUrl']

class Launch(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True)
	windowStart = db.Column(db.String())
	windowEnd = db.Column(db.String())
	videoUrl = db.Column(db.String())
	launchPad = db.Column(db.String())
	rocket = db.Column(db.String())
	rocketLink = db.Column(db.String())
	status = db.Column(db.Integer)

	#id used to identify the launches associated with the location
	location_id = db.Column(db.Integer, db.ForeignKey('location.id')) # Use location_owner = "ex_location" to assign
	# Many agencies to many launches
	agencies = db.relationship('Agency', secondary = al_associationTable, 
		backref = db.backref('launches', lazy = 'dynamic'))
	# One mission for one launch
	mission = db.relationship('Mission', uselist = False, backref = 'launch')

	def dictionary(self):
		d = {"id" : self.id, "name" : self.name, "windowStart" : self.windowStart, 
				"windowEnd" : self.windowEnd,"videoUrl" : self.videoUrl,
				"launchPad": self.launchPad, "rocket" : self.rocket,
				"rocketLink" : self.rocketLink, "status" : self.status}
		d["location"] = Location.query.get(self.location_id).name
		d["agencies"] = {agency.id: agency.name for agency in self.agencies}
		d["mission"] = self.mission.name if self.mission is not None else "None"
		return d

	def attributes():
		return ['id','name','windowStart','windowEnd','videoUrl','launchPad','rocket', 'rocketLink', 'status', 'location_id']

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	name = db.Column(db.String(), unique = True)
	countryCode = db.Column(db.String())

	# Many launches to one location
	launches = db.relationship('Launch', backref = 'location_owner', lazy = 'dynamic')

	def dictionary(self):
		d = {"id" : self.id, "name" : self.name, "countryCode" : self.countryCode}
		d["launches"] = {launch.id: launch.name for launch in self.launches}
		return d

	def attributes():
		return ['id','name','countryCode']

class Mission(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(), unique = True)
	description = db.Column(db.String())
	typeName = db.Column(db.String())
	wikiUrl = db.Column(db.String())

	# Many agencies to many missions
	agencies = db.relationship('Agency', secondary = am_associationTable, 
		backref = db.backref('missions', lazy = 'dynamic'))

	# One mission to one launch
	launch_id = db.Column(db.Integer, db.ForeignKey('launch.id'))

	def dictionary(self):
		d = {"id" : self.id, "name" : self.name, "description" : self.description, "typeName" : self.typeName,
						"wikiUrl" : self.wikiUrl}
		d["agencies"] = {agency.id: agency.name for agency in self.agencies}
		d["launch"] = Launch.query.get(self.launch_id).name if self.launch is not None else "None"
		return d

	def attributes():
		return ['id','name','description','typeName','wikiUrl','launch_id']
