"""
	Tests file for itslaunchti.me
"""

from app import app, db
import unittest
from app.models import *
import sqlalchemy

class TestModels(unittest.TestCase):
	"""
		Unit test class for testing the DB model classes
	"""

	# def setUp(self):
		# agency = Agency(name='Rocket Labs', abbrev='RL', agencyType='Government',
		# 				countryCode='USA', wikiUrl='https://www.wikipedia.org')
		# launch = Launch(name='Launch X', windowStart='March 24, 2017 20:31:00 UTC',
		# 				windowEnd='March 24, 2017 23:20:00 UTC', videoUrl='https://www.youtube.com/watch?v=wCy401hkXuk',
		# 				launchPad='Launch Complex 39', rocket='Big Rocket 7')
		# location = Location(name='Houston, Texas', countryCode='USA')
		# mission = Mission(name='Explore space', description='This is a description about this mission.',
		# 				  typeName='Astrophysics', wikiUrl='https://www.wikipedia.org')
		# 				  #agencyName='ExplorersUnited', launchName='Pegasus XL')

		# agency.id = 1
		# launch.id = 2
		# location.id = 3
		# mission.id = 4

		# agency.missions.append(mission)
		# agency.launches.append(launch)
		# launch.agency = agency
		# launch.location = location
		# launch.mission = mission
		# location.launches.append(launch)
		# mission.agencies.append(agency)
		# mission.launch = launch

		# self.agency = agency
		# self.launch = launch
		# self.location = location
		# self.mission = mission

	def test_agency_model_1(self):
		"""
		Test launch link to mission
		"""
		with app.test_request_context():
			ex1 = Agency(name='Rocket Labs', abbrev='RL', agencyType='Government',
						countryCode='USA', wikiUrl='https://www.wikipedia.org')

			# ex1 = self.agency
			db.session.add(ex1)
			db.session.commit()

			agency1 = db.session.query(Agency).filter_by(name="Rocket Labs").first()
			self.assertEqual(agency1.abbrev, "RL")
			self.assertEqual(agency1.agencyType, "Government")

			db.session.delete(ex1)
			db.session.commit()

	##################
	# DB QUERY TESTS #
	##################

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


	# def test_agency_model_link_query_1(self):
	# 	"""
	# 	Test agency link to launches
	# 	"""
	# 	with app.test_request_context():
	# 		agency1 = db.session.query(Agency).filter_by(name="Mexican Space Agency").first()
	# 		launch1 = agency1.launches;
	# 		print(launch1)

	# def test_agency_model_link_2(self):
	# 	"""
	# 	Test agency link to missions
	# 	"""
	# 	with app.test_request_context():
	# 		agency1 = db.session.query(Agency).filter_by(name="Mexican Space Agency").first()
	# 		mission1 = agency1.missions;
	# 		print(mission1)

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
		Test launch link to agency
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
			self.assertTrue(mission1 is None)

	# def test_launch_model_link_3(self):
	# 	"""
	# 	Test launch link to mission
	# 	"""
	# 	with app.test_request_context():
	# 		ex1 = self.launch
	# 		db.session.add(ex1)
	# 		db.session.commit()

	# 		launch1 = db.session.query(Launch).filter_by(name="Launch X").first()
	# 		mission1 = launch1.mission
	# 		self.assertEqual(mission1.name, "Explore space")
	# 		#self.assertEqual(mission1.agencyName, "ExplorersUnited")

	# 		db.session.delete(ex1)
	# 		db.session.commit()

	def test_location_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - location
		"""
		with app.test_request_context():
			location1 = db.session.query(Location).first()
			self.assertEqual(location1.name, "Jiuquan, People's Republic of China")

	# def test_location_model_link_1(self):
	# 	"""
	# 	Test location link to launches
	# 	"""
	# 	with app.test_request_context():
	# 		location1 = db.session.query(Location).first()
	# 		launch1 = location1.launches
	# 		print(launch1)

	def test_mission_model_query_1(self):
		"""
		Test querying the db by attribute using simple keywords - mission
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).first()
			self.assertEqual(mission1.name, "Nuclear Spectroscopic Telescope Array (NuSTAR)")

	def test_mission_model_link_query_1(self):
		"""
		Test mission link to agencies
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).first()
			agency1 = mission1.agencies
			self.assertEqual(agency1, [])

			mission2 = db.session.query(Mission).filter_by(name="WGS-4 (USA-233)").first()
			agency1 = mission2.agencies
			self.assertEqual(agency1, []) #this should not be empty, check online api


	def test_mission_model_link_query_2(self):
		"""
		Test mission link to launch
		"""
		with app.test_request_context():
			mission1 = db.session.query(Mission).filter_by(name="WGS-4 (USA-233)").first()
			launch_id1 = mission1.launch_id
			self.assertEqual(launch_id1, None) #should not be None, check online api


if __name__ == "__main__":
    unittest.main()
