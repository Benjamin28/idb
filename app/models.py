from app import db
#check string size for all of the columns!!

class Agency(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	abbrev = db.Column(db.String(10), unique = True)
	agencyType = db.Column(db.String(120))
	countryCode = db.Column(db.String(10))
	wikiUrl = db.Column(db.String(120))

class Launch(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	windowStart = db.Column(db.String(120))
	windowEnd = db.Column(db.String(120))
	videoUrl = db.Column(db.String(120))
	launchPad = db.Column(db.String(120))
	rocket = db.Column(db.String(120))

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)	
	name = db.Column(db.String(120), unique = True)
	countryCode = db.Column(db.String(10))

class Mission(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120), unique = True)
	description = db.Column(db.String(400))
	typeName = db.Column(db.String(120))
	wikiUrl = db.Column(db.String(120))
	agencyName = db.Column(db.String(120))
	launchName = db.Column(db.String(120))


# define relationships later