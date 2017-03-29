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
	abbrev = db.Column(db.String(10))
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
		backref = db.backref('launches', lazy = 'dynamic'))
	# One mission for one launch
	mission = db.relationship('Mission', uselist = False, backref = 'launch')

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
		backref = db.backref('missions', lazy = 'dynamic'))

	# One mission to one launch
	launch_id = db.Column(db.Integer, db.ForeignKey('launch.id'))
