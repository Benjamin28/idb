"""
	Tests file for itslaunchti.me
"""

from app import app, db
import unittest
from models import Agency, Launch, Location, Mission
import sqlalchemy

class TestModels(unittest.TestCase):
	"""
		Unit test class for testing the DB model classes
	"""

	def setUp(self):
		agency = Agency(name='Rocket Labs', abbrev='RL', agencyType='Government',
						countryCode='USA', wikiUrl='https://www.wikipedia.org')
		launch = Launch(name='Launch X', windowStart='March 24, 2017 20:31:00 UTC',
						windowEnd='March 24, 2017 23:20:00 UTC', videoUrl='https://www.youtube.com/watch?v=wCy401hkXuk',
						launchPad='Launch Complex 39', rocket='Big Rocket 7')
		location = Location(name='Houston, Texas', countryCode='USA')
		mission = Mission(name='Explore space', description='This is a description about this mission.',
						  typeName='Astrophysics', wikiUrl='https://www.wikipedia.org',
						  agencyName='ExplorersUnited', launchName='Pegasus XL')
		agency.id = 1
		launch.id = 2
		location.id = 3
		mission.id = 4
		#relationship lines go here

		self.agency = agency
		self.launch = launch
		self.location = location
		self.mission = mission

	def test_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - no entries
		"""
		with app.test_request_context():
			ex1 = self.agency
			db.session.add(ex1)
			db.session.commit()

			agency_none = db.session.query(Agency).filter_by(name="not here").first()
			self.assertTrue(agency_none is None)

			db.session.delete(ex1)
			db.session.commit()

	def test_agency_model_1(self):
		"""
		Test querying the db by attribute using simple keywords - agency
		"""
		with app.test_request_context():
			ex1 = self.agency
			db.session.add(ex1)
			db.session.commit()

			agency1 = db.session.query(Agency).filter_by(name="Rocket Labs").first()
			self.assertEqual(agency1.abbrev, "RL")
			self.assertEqual(agency1.countryCode, "USA")

			db.session.delete(ex1)
			db.session.commit()

	def test_launch_model_1(self):
		"""
		Test querying the db by attribute using simple keywords - launch
		"""
		with app.test_request_context():
			ex1 = self.launch
			db.session.add(ex1)
			db.session.commit()

			launch1 = db.session.query(Launch).filter_by(name="Launch X").first()
			self.assertEqual(launch1.rocket, "Big Rocket 7")
			self.assertTrue(launch1.id == 2)

			db.session.delete(ex1)
			db.session.commit()

	def test_location_model_1(self):
		"""
		Test querying the db by attribute using simple keywords - location
		"""
		with app.test_request_context():
			ex1 = self.location
			db.session.add(ex1)
			db.session.commit()

			location1 = db.session.query(Location).filter_by(countryCode="USA").first()
			self.assertEqual(location1.name, "Houston, Texas")

			db.session.delete(ex1)
			db.session.commit()

	def test_mission_model_1(self):
		"""
		Test querying the db by attribute using simple keywords - mission
		"""
		with app.test_request_context():
			ex1 = self.mission
			db.session.add(ex1)
			db.session.commit()

			mission1 = db.session.query(Mission).filter_by(typeName="Astrophysics").first()
			self.assertEqual(mission1.name, "Explore space")
			self.assertEqual(mission1.agencyName, "ExplorersUnited")

			db.session.delete(ex1)
			db.session.commit()


if __name__ == "__main__":
    unittest.main()
    