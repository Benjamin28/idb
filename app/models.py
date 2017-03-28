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
	name = db.Column(db.String(120), unique = True)
	abbrev = db.Column(db.String(10), unique = True)
	agencyType = db.Column(db.String(120))
	countryCode = db.Column(db.String(10))
	wikiUrl = db.Column(db.String(120))

	# launches attr appears to be here with the backref in the Launch model
	# Can call Agency.launches to get the list of launches

	# missions attr appears to be here with the backref in the Mission model
	# Can call Agency.missions to get the list of missions

class Launch(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	windowStart = db.Column(db.String(120))
	windowEnd = db.Column(db.String(120))
	videoUrl = db.Column(db.String(120))
	launchPad = db.Column(db.String(120))
	rocket = db.Column(db.String(120))

	#id used to identify the launches associated with the location
	location_id = db.Column(db.Integer, db.ForeignKey('location.id')) # Use location_owner = "ex_location" to assign
	# Many agencies to many launches
	agencies = db.relationship('Agency', secondary = al_associationTable, 
		backref = db.backref('launches'), lazy = 'dynamic')
	# One mission for one launch
	mission = db.relationship('Mission', uselist = False, back_populates = 'launch')

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	name = db.Column(db.String(120), unique = True)
	countryCode = db.Column(db.String(10))

	# Many launches to one location
	launches = db.relationship('Launch', backref = 'location_owner', lazy = 'dynamic')

class Mission(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	description = db.Column(db.String(400))
	typeName = db.Column(db.String(120))
	wikiUrl = db.Column(db.String(120))

	# Many agencies to many missions
	agencies = db.relationship('Agency', secondary = am_associationTable, 
		backref = db.backref('missions'), lazy = 'dynamic')

	# One mission to one launch
	launch = db.relationship('Launch', back_populates = 'mission')
	
	


# from app import db
# #check string size for all of the columns!!
# # Relational Table for many to many relationship for agency and mission
# associationTable = db.Table('association',
# 	db.Column('agency_id', db.Integer, db.ForeignKey('agency.id')),
# 	db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'))
# )

# class Agency(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	name = db.Column(db.String(120), unique = True)
# 	abbrev = db.Column(db.String(10), unique = True)
# 	agencyType = db.Column(db.String(120))
# 	countryCode = db.Column(db.String(10))
# 	wikiUrl = db.Column(db.String(120))
# 	# Many to one for Launch (many launches for an agency)
# 	launches = db.relationship('Launch', backref = 'agency', lazy = 'dynamic')
# 	# Many to many for Missions (many agencies for many missions)
# 	missions = db.relationship('Mission', secondary = associationTable, back_populates='agencies')
	
# 	# def __repr__(self):
# 	# 	return "<Agency(name='%s', abbrev='%s', countryCode='%s')>" % (self.name, self.abbrev, self.countryCode)

# 	# def getJson(self):
# 	# 	return json information about an instance

# #>>>>>>> 66fc8a6e1744d34b767d22a4b81c9ee92bce084e

# class Launch(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	name = db.Column(db.String(120), unique = True)
# 	windowStart = db.Column(db.String(120))
# 	windowEnd = db.Column(db.String(120))
# 	videoUrl = db.Column(db.String(120))
# 	launchPad = db.Column(db.String(120))
# 	rocket = db.Column(db.String(120))
# 	# One to many for Agency (one agency for a launch)
# 	agency = db.Column(db.Integer, db.ForeignKey('agency.id'))
# 	# One to many for launch (one location for a launch)
# 	location = db.Column(db.Integer, db.ForeignKey('location.id'))
# 	# One to one for Mission (one mission for a launch)
# #	mission = db.relationship('Mission', back_populates = 'launch')

# 	# def __repr__(self):
# 		# return "<Launch(name='%s')>" % (self.name)

# 	# def getJson(self):
# 	# 	return json information about an instance	

# class Location(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)	
# 	name = db.Column(db.String(120), unique = True)
# 	countryCode = db.Column(db.String(10))
# 	# Many to one for Launch (many launches for a location)
# #	launches = db.relationship('Launch', backref = 'location', lazy = 'dynamic')

# 	# def __repr__(self):
# 		# return "<Location(name='%s')>" % (self.name)

# 	# def getJson(self):
# 	# 	return json information about an instance

# 	# def getLaunches(self):
# 		# return all launches associated with a location		

# class Mission(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	name = db.Column(db.String(120), unique = True)
# 	description = db.Column(db.String(400))
# 	typeName = db.Column(db.String(120))
# 	wikiUrl = db.Column(db.String(120))
# 	# Many to many for Agencies (many agencies for many missions)
# #	agencies = db.relationship('Agency', secondary = associationTable, back_populates = 'missions')
# 	# One to one for Launch (one launch for a mission)
# #	launch = db.relationship('Launch', uselist = False, back_populates = 'mission')

# 	# def __repr__(self):
# 		# return "<Mission(name='%s')>" % (self.name)

# 	# def getJson(self):
# 	# 	return json information about an instance

# 	# def getLaunch(self):
# 		# return json information about the launch associated with a mission		

# 	# agencyName = db.Column(db.String(120))
# 	# launchName = db.Column(db.String(120))
