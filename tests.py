"""
	Tests file for itslaunchti.me
"""

from app import app, db
import unittest
from app.models import *
import sqlalchemy

class TestModels(unittest.TestCase):
	"""
		Unit test class for testing the DB model classes and db queries
	"""

	def setUp(self):
		agency = Agency(name='testAgency3', abbrev='testAbb', agencyType='testType',
						countryCode='testCC', wikiUrl='https://www.wikipedia.org')
		launch = Launch(name='testnameLaunch', windowStart='March 24, 2017 20:31:00 UTC',
						windowEnd='March 24, 2017 23:20:00 UTC', videoUrl='https://www.youtube.com/watch?v=wCy401hkXuk',
						launchPad='testLP', rocket='testRocket', rocketLink = 'https://s3.amazonaws.com/launchlibrary/RocketImages/Ariane+5+ECA_1920.jpg',
						status = 'SUCCESS')
		location = Location(name='testLoc', countryCode='testCC2')
		mission = Mission(name='testMissionN', description='This is a description about this mission.',
						  typeName='testType2', wikiUrl='https://www.wikipedia2.org')

		self.agency = agency
		self.launch = launch
		self.location = location
		self.mission = mission

	###############
	# MODEL TESTS #
	###############

	def test_agency_model_1(self):
		"""
		Test Agency model
		"""
		with app.test_request_context():
			ex1 = self.agency
			db.session.add(ex1)
			db.session.commit()

			agency1 = db.session.query(Agency).filter_by(name="testAgency3").first()
			self.assertEqual(agency1.abbrev, "testAbb")
			self.assertEqual(agency1.agencyType, "testType")

			db.session.delete(ex1)
			db.session.commit()

	def test_launch_model_1(self):
		"""
		Test Launch model
		"""
		with app.test_request_context():
			ex1 = self.launch
			db.session.add(ex1)
			db.session.commit()

			launch1 = db.session.query(Launch).filter_by(name="testnameLaunch").first()
			self.assertEqual(launch1.launchPad, "testLP")
			self.assertEqual(launch1.rocket, "testRocket")

			db.session.delete(ex1)
			db.session.commit()

	def test_location_model_1(self):
		"""
		Test Location model
		"""
		with app.test_request_context():
			ex1 = self.location
			db.session.add(ex1)
			db.session.commit()

			location1 = db.session.query(Location).filter_by(name="testLoc").first()
			self.assertEqual(location1.countryCode, "testCC2")

			db.session.delete(ex1)
			db.session.commit()

	def test_mission_model_1(self):
		"""
		Test Mission model
		"""
		with app.test_request_context():
			ex1 = self.mission
			db.session.add(ex1)
			db.session.commit()

			mission1 = db.session.query(Mission).filter_by(name="testMissionN").first()
			self.assertEqual(mission1.wikiUrl, 'https://www.wikipedia2.org')

			db.session.delete(ex1)
			db.session.commit()

	######################################
	# DB QUERY TESTS, MODEL TESTS VIA DB #
	######################################

	def test_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - no entries
		"""
		with app.test_request_context():
			agency_none = db.session.query(Agency).filter_by(name="not here").first()
			self.assertTrue(agency_none is None)

	def test_agency_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - agency
		"""
		with app.test_request_context():
			agency1 = db.session.query(Agency).filter_by(name="Mexican Space Agency").first()
			self.assertEqual(agency1.abbrev, "AEM")
			self.assertEqual(agency1.countryCode, "MEX")


	def test_agency_model_link_query_1(self):
		"""
		Test agency link to launches via db
		"""
		with app.test_request_context():
			agency1 = db.session.query(Agency).filter_by(name="SpaceX").first()
			launch1 = agency1.launches[0]
			self.assertEqual(launch1.rocket, "Saturn V")

	def test_agency_model_link_2(self):
		"""
		Test agency link to missions via db
		"""
		with app.test_request_context():
			agency1 = db.session.query(Agency).filter_by(name="Mexican Space Agency").first()
			mission1 = agency1.missions[0];
			self.assertEqual(mission1.name, "ISS 44")

	def test_launch_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - launch
		"""
		with app.test_request_context():
			launch1 = db.session.query(Launch).filter_by(name="Long March 3B | Shijian-13").first()
			self.assertEqual(launch1.name, "Long March 3B | Shijian-13")
			self.assertEqual(launch1.rocket, "Long March 3B")


	def test_launch_model_link_query_1(self):
		"""
		Test launch link to agencies via db
		"""
		with app.test_request_context():
			launch1 = db.session.query(Launch).filter_by(name="Long March 3B | Shijian-13").first()
			agency1 = launch1.agencies[0]
			self.assertEqual(agency1.countryCode, "CHN")

	def test_launch_model_link_query_2(self):
		"""
		Test launch link to mission
		"""
		with app.test_request_context():
			launch1 = db.session.query(Launch).first()
			mission1 = launch1.mission
			self.assertEqual(mission1.name, "Vostok 1")

	def test_location_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - location
		"""
		with app.test_request_context():
			location1 = db.session.query(Location).first()
			self.assertEqual(location1.name, "Jiuquan, People's Republic of China")

	def test_location_model_link_1(self):
		"""
		Test location link to launches via db
		"""
		with app.test_request_context():
			location1 = db.session.query(Location).first()
			launch1 = location1.launches[0]
			self.assertEqual(launch1.rocket, "Long March 2F")

	def test_mission_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - mission
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).first()
			self.assertEqual(mission1.name, "Nuclear Spectroscopic Telescope Array (NuSTAR)")

	def test_mission_model_link_query_1(self):
		"""
		Test mission link to agencies via db
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).first()
			agency1 = mission1.agencies[0]
			self.assertEqual(agency1.name, "National Aeronautics and Space Administration")


	def test_mission_model_link_query_2(self):
		"""
		Test mission link to launch_id via db
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).filter_by(name="WGS-4 (USA-233)").first()
			launch_id1 = mission1.launch_id
			self.assertEqual(launch_id1, 485)


if __name__ == "__main__":
    unittest.main()
