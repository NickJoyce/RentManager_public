class Building:
	def __init__(self):
		# ЗДАНИЕ |T| EXTENSION rental_objects> ro_building_data
		self.floors_number = None # всего этажей в доме
		self.garbage_disposal = False # мусоропровод
		self.intercom = False # домофон
		self.concierge= False # консьерж
		self.building_year = None # год постройки
		self.building_type = '' # тип здания |T| SOURCE> building_types ['кирпичный', 'панельный'] 

		self.elevator = {} # тип лифтов |T| EXTENSION ro_building> ro_building_elevators {'пассажирский': 0, 'грузовой': 0}