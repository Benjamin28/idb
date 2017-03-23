from app import db
#check string size for all of the columns!!

class Agency(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	abbrev = db.Column(db.String(10), unique = True)
	agencyType = db.Column(db.String(120))
	countryCode = db.Column(db.String(10))
	wikiUrl = db.Column(db.String(120))
	# Many to one for Launch (many launches for an agency)
	launches = db.relationship('launches', backref = 'agency', lazy = 'dynamic')
	# Many to many for Missions (many agencies for many missions)
	missions = db.relationship('missions', secondary = associationTable, back_populates='agencies')

class Launch(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	windowStart = db.Column(db.String(120))
	windowEnd = db.Column(db.String(120))
	videoUrl = db.Column(db.String(120))
	launchPad = db.Column(db.String(120))
	rocket = db.Column(db.String(120))
	# One to many for Agency (one agency for a launch)
	agency = db.Column(db.Integer, db.ForeignKey('agency.id'))
	# One to many for launch (one location for a launch)
	location = db.Column(db.Integer, db.ForeignKey('location.id'))
	# One to one for Mission (one mission for a launch)
	mission = db.relationship('mission', back_populates = 'launch')

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	name = db.Column(db.String(120), unique = True)
	countryCode = db.Column(db.String(10))
	# Many to one for Launch (many launches for a location)
	launches = db.relationship('launches', backref='location', lazy='dynamic')

class Mission(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	description = db.Column(db.String(400))
	typeName = db.Column(db.String(120))
	wikiUrl = db.Column(db.String(120))
	# Many to many for Agencies (many agencies for many missions)
	agencies = db.relationship('agencies', secondary = associationTable, back_populates = 'missions')
	# One to one for Launch (one launch for a mission)
	launch = db.relationship('launch', uselist = False, back_populates = 'mission')

	# agencyName = db.Column(db.String(120))
	# launchName = db.Column(db.String(120))

# Relational Table for many to many relationship for agency and mission
associationTable = db.Table('association',
	db.Column('agency_id', db.Integer, db.ForeignKey('agency.id'))
	db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'))
)

