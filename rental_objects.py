from prettytable import PrettyTable

from rental_object_data import General, ObjectData, Building, Location, Appliance, Costs, Things

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД


class RentalObject:
	"""Объект недвижимости"""
	def __init__(self, rental_object_id): 


		# TODO поменять определение данных в таблице rental_objects
		# БАЗОВАЯ ИНФОРМАЦИЯ |T|> rental_objects, |T|> cities, |T|> cities_districts, |T|> ro_cities_districts, |T|> metro_stations
		self._rental_object_id = rental_object_id

		self._db = None

		self._type_id = None # тип объекта недвижимости |T| SOURCE> rental_object_types ['комната', 'квартира', 'дом']

		self._landlord_id = None # id наймодателя (собственика) - у объекта обязательно должен быть landlord 

	# ---------------------------------------------
		self._tenant_id = None # текущий наниматель, у объекта появляется tenant когда подписа договор аренды
		self._agent_id = None # агент назначенный найамодателем на этот объект
		self._rental_agreement_id = None # id текущего договора аренды  

	# ---------------------------------------------

		self._general = None # экземпляр класса General - общие данные об объекте 
		self._object_data = None # экземпляр класса ObjectData - информация об объекте
		self._building = None # экземпляр класса Building - информация об здании
		self._location = None # экземпляр класса Location - локация объекта
		self._appliance = None # экземпляр класса Appliance - информация бытовой технике
		self._costs = None # экземпляр класса Costs - расходы на содержание объекта
		self._things = None # экземпляр класса Things - список вещей внутри объекта



	#____________________________________________setters and getters____________________________________________
	# Для значений в таблице обязательно должно быть соблюдено условия NOT NULL, чтобы коректно отрабатывали условия с None
	
	@property
	def rental_object_id(self):
		return self._rental_object_id

	@property
	def db(self):
		if self._db == None:
			self._db = DataManipulation(db_config, DBcm)
		return self._db

	@property
	def type_id(self):
		if self._type_id == None:
			self._type_id = self.db.get_rental_object_type_id(self.rental_object_id)
		return self._type_id	

	@property
	def landlord_id(self):
		return self._landlord_id



	@property
	def tenant_id(self):
		if self._tenant_id == None:
			self._tenant_id= self.db.get_rental_object_tenant_id(self.rental_object_id)
		return self._tenant_id
	@tenant_id.setter


	@property
	def agent_id(self):
		if self._agent_id == None:
			self._agent_id= self.db.get_rental_object_agent_id(self.rental_object_id)
		return self._agent_id

	@property
	def rental_agreement_id(self):
		if self._rental_agreement_id== None:
			self._rental_agreement_id= self.db.get_rental_object_rental_agreement_id(self.rental_object_id)
		return self._rental_agreement_id


	@property
	def general(self):
		if self._object_data == None:
			self._object_data = General(self._rental_object_id)
		return self._object_data

	@property
	def object_data(self):
		if self._object_data == None:
			self._object_data = ObjectData(self._rental_object_id)
		return self._object_data

	@property
	def building(self):
		if self._building == None:
			self._building = Building(self._rental_object_id)
		return self._building

	@property
	def location (self):
		if self._location  == None:
			self._location  = Location(self._rental_object_id)
		return self._location 


	@property
	def appliance(self):
		if self._appliance == None:
			self._oappliance = Appliance(self._rental_object_id)
		return self._appliance

	@property
	def costs(self):
		if self._costs  == None:
			self._costs  = Costs(self._rental_object_id)
		return self._costs

	@property
	def things(self):
		if self._things  == None:
			self._things  = Things(self._rental_object_id)
		return self._things














class Room(RentalObject):
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)
		self._total_area =  None # общая площадь квартиры
		self._rooms_number = None # всего комнат в квартире

	@property
	def total_area(self):
		if self._total_area  == None:
			self._total_area = self.db.get_ro_room_total_area(self.rental_object_id)
		return self._total_area
	@total_area.setter
	def total_area(self, value):
		self.db.set_ro_room_total_area(self.rental_object_id, value)
		self._total_area = value

	@property
	def rooms_number(self):
		if self._rooms_number  == None:
			self._rooms_number = self.db.get_ro_room_rooms_number(self.rental_object_id)
		return self._rooms_number
	@rooms_number.setter
	def rooms_number(self, value):
		self.db.set_ro_room_rooms_number(self.rental_object_id, value)
		self._rooms_number = value



class Flat(RentalObject):
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)



class House(RentalObject):
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)




if __name__ == '__main__':
	rent = Room(1)
	print(rent.maintenance_costs)
	rent.maintenance_costs = [[1, 'Газ', None], [3, 'Электричество', None], [3, 'Вода', None], [4, 'Интернет', None]]




	print(rent.building.floors_number)
	rent.building.floors_number = 122
	rent.location.nearest_metro_stations = [1,2]
	print(rent.location.nearest_metro_stations)
	print(rent.building.floors_number)	
	# print(rent._name)
	# print(rent._cadastral_number)
	# print(rent._title_deed)
	# print(rent._is_rented)
	# print(rent._current_rental_agreement_id)
	# print(rent._things)
	# print(rent.name)
	# print(rent.cadastral_number)
	# print(rent.title_deed)
	# print(rent.is_rented)
	# print(rent.current_rental_agreement_id)
	# print(rent.things)
	# print(rent.total_area)
	# print(rent.rooms_number)


	# rent.name = 'Комнатушка'
	# rent.cadastral_number = '777:777'
	# rent.title_deed = 'Дог'
	# rent.is_rented = True
	# rent.current_rental_agreement_id = '1'
	# rent.things = [[1, 'комод', '1', '8000'], [2, 'стул', '2', '3000']]
	# rent.total_area = 100.7
	# rent.rooms_number = 7

	# print(rent.name)
	# print(rent.cadastral_number)
	# print(rent.title_deed)
	# print(rent.is_rented)
	# print(rent.current_rental_agreement_id)
	# print(rent.things)
	# print(rent.total_area)
	# print(rent.rooms_number)


