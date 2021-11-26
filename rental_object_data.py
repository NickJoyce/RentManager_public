# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД


class RentalObjectData:
	def __init__(self, rental_object_id):
		self._rental_object_id = rental_object_id # id объекта аренды
		self._db = None

	@property
	def rental_object_id(self):
		return self._rental_object_id

	@property
	def db(self):
		if self._db == None:
			self._db = DataManipulation(db_config, DBcm)
		return self._db



class Things(RentalObjectData):
	# ВЕЩИ |T| rental_objects> ro_things [[thing_number, thing_name, amount, cost], ...]
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)
		self._things = None 
	
	#____________________________________________setters and getters____________________________________________		
	@property
	def things(self):
		if self._things == None:
			self._things = self.db.get_things(self.rental_object_id)
		return self._things
	@things.setter # предполагается что при формировании словаря пользователь понимает
	def things(self, value:list):
		if isinstance(value, list):
			self.db.set_things(self.rental_object_id, value)
			self._things = value
		else:
			raise TypeError



class General(RentalObjectData):
	# ОБЩАЯ ИНФОРМАЦИЯ |T| EXTENSION rental_objects> ro_general
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)	

		self._name = None # имя объекта
		self._cadastral_number = None # TODO кадастровый номер объекта аренды # TODO
		self._title_deed = None # TODO документ подтверждающий право собственности

	#____________________________________________setters and getters____________________________________________
	@property
	def name(self):
		if self._name == None:
			self._name = self.db.get_ro_general_name(self.rental_object_id)
		return self._name
	@name.setter
	def name(self, value):
		self.db.set_ro_general_name(self.rental_object_id, value)
		self._name = value


	@property
	def cadastral_number(self):
		if self._cadastral_number == None:
			self._cadastral_number = self.db.get_ro_general_cadastral_number(self.rental_object_id)
		return self._cadastral_number	
	@cadastral_number.setter
	def cadastral_number(self, value):
		self.db.set_ro_general_cadastral_number(self.rental_object_id, value)
		self._cadastral_number = value


	@property
	def title_deed(self):
		if self._title_deed == None:
			self._title_deed = self.db.get_ro_general_title_deed(self.rental_object_id)
		return self._title_deed	
	@title_deed.setter
	def title_deed(self, value):
		self.db.set_ro_general_title_deed(self.rental_object_id, value)
		self._title_deed = value



class ObjectData(RentalObjectData):
	# ОБЩАЯ ИНФОРМАЦИЯ |T| EXTENSION rental_objects> ro_object_data
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)

		self._bathroom_type_id = None  # тип ванной комнаты (санузел) |T| SOURCE> bathroom_types ['совмещенный', 'раздельный'] 
		self._wash_place_type_id =  None # тип места для мытья |T| SOURCE> wash_place_types ['ванна', 'душевая кабина']

		self._area = None # площадь
		self._ceilings_height = None # высота потолков
		self._win_number = None # количество окон
		self._balcony = None # балкон/лоджия (количество)
		self._air_conditioner = None # кондиционер
		self._wi_fi = None # wi-fi
		self._furniture = None # мебель


		self._window_overlook = None # вид из окна |T| EXTENSION ro_general>  ro_general_window_overlooks {'на улицу': False, 'во двор': False}
		self._window_frame_type = None # тип окон |T| EXTENSION ro_general> ro_general_window_frames {'деревяные': False, 'пластиковые': False}
		self._cooking_range_type = None # тип плит |T| EXTENSION ro_general> ro_general_cooking_ranges {'электрическая': False, 'газовая': False}

	#____________________________________________setters and getters____________________________________________

	@property
	def bathroom_type_id(self):
		if self._bathroom_type_id == None:
			self._bathroom_type_id = self.db.get_ro_object_data_bathroom_type_id(self.rental_object_id)
		return self._bathroom_type_id
	@bathroom_type_id.setter
	def bathroom_type_id(self, value):
		self.db.set_ro_object_data_bathroom_type_id(self.rental_object_id, value)
		self._bathroom_type_id = value


	@property
	def wash_place_type_id(self):
		if self._wash_place_type_id == None:
			self._wash_place_type_id = self.db.get_ro_object_data_wash_place_type_id(self.rental_object_id)
		return self._wash_place_type_id
	@wash_place_type_id.setter
	def wash_place_type_id(self, value):
		self.db.set_ro_object_data_wash_place_type_id(self.rental_object_id, value)
		self._wash_place_type_id = value

	@property
	def area(self):
		if self._area == None:
			self._area = self.db.get_ro_object_data_area(self.rental_object_id)
		return self._area
	@area.setter
	def area(self, value):
		self.db.set_ro_object_data_area(self.rental_object_id, value)
		self._area = value


	@property
	def ceilings_height(self):
		if self._ceilings_height == None:
			self._ceilings_height = self.db.get_ro_object_data_ceilings_height(self.rental_object_id)
		return self._ceilings_height
	@ceilings_height.setter
	def ceilings_height(self, value):
		self.db.set_ro_object_data_ceilings_height(self.rental_object_id, value)
		self._ceilings_height = value

	@property
	def win_number(self):
		if self._win_number == None:
			self._win_number = self.db.get_ro_object_data_win_number(self.rental_object_id)
		return self._win_number
	@win_number.setter
	def win_number(self, value):
		self.db.set_ro_object_data_win_number(self.rental_object_id, value)
		self._win_number = value

	@property
	def balcony(self):
		if self._balcony == None:
			self._balcony = self.db.get_ro_object_data_balcony(self.rental_object_id)
		return self._balcony
	@balcony.setter
	def balcony(self, value):
		self.db.set_ro_object_data_balcony(self.rental_object_id, value)
		self._balcony = value


	@property
	def air_conditioner(self):
		if self._air_conditioner == None:
			self._air_conditioner = self.db.get_ro_object_data_air_conditioner(self.rental_object_id)
		return self._air_conditioner
	@air_conditioner.setter
	def air_conditioner(self, value):
		self.db.set_ro_object_data_air_conditioner(self.rental_object_id, value)
		self._air_conditioner = value


	@property
	def wi_fi(self):
		if self._wi_fi == None:
			self._wi_fi = self.db.get_ro_object_data_wi_fi(self.rental_object_id)
		return self._wi_fi
	@wi_fi.setter
	def wi_fi(self, value):
		self.db.set_ro_object_data_wi_fi(self.rental_object_id, value)
		self._wi_fi = value


	@property
	def furniture(self):
		if self._furniture == None:
			self._furniture = self.db.get_ro_object_data_furniture(self.rental_object_id)
		return self._furniture
	@furniture.setter
	def furniture(self, value):
		self.db.set_ro_object_data_furniture(self.rental_object_id, value)
		self._furniture = value


	@property
	def window_overlook(self):
		if self._window_overlook == None:
			self._window_overlook = self.db.get_ro_object_data_window_overlook(self.rental_object_id)
		return self._window_overlook
	@window_overlook.setter
	def window_overlook(self, value: dict):
		self.db.set_ro_object_data_data_window_overlook(self.rental_object_id, value)
		self._window_overlook = value


	@property
	def window_frame_type(self):
		if self._window_frame_type == None:
			self._window_frame_type = self.db.get_ro_object_data_window_frame_type(self.rental_object_id)
		return self._window_frame_type
	@window_frame_type.setter
	def window_frame_type(self, value: dict):
		self.db.set_ro_object_data_window_frame_type(self.rental_object_id, value)
		self._window_frame_type = value


	@property
	def cooking_range_type(self):
		if self._cooking_range_type == None:
			self._cooking_range_type = self.db.get_ro_object_data_cooking_range_type(self.rental_object_id)
		return self._cooking_range_type
	@cooking_range_type.setter
	def cooking_range_type(self, value: dict):
		self.db.set_ro_object_data_cooking_range_type(self.rental_object_id, value)
		self._cooking_range_type = value



class Building(RentalObjectData):
	# ЗДАНИЕ |T| EXTENSION rental_objects> ro_building
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)

		self._building_type_id = None # тип здания |T| SOURCE> building_types ['кирпичный', 'панельный'] 
		self._floors_number = None # всего этажей в доме
		self._garbage_disposal = None # мусоропровод
		self._intercom = None # домофон
		self._concierge = None # консьерж
		self._building_year = None # год постройки

		self._elevator = None # тип лифтов |T| EXTENSION ro_building> ro_building_elevators {'пассажирский': 0, 'грузовой': 0}

	#____________________________________________setters and getters____________________________________________
	@property
	def building_type_id(self):
		if self._building_type_id == None:
			self._building_type_id = self.db.get_ro_building_building_type_id(self.rental_object_id)
		return self._building_type_id
	@building_type_id.setter
	def building_type_id(self, value):
		self.db.set_ro_building_building_type_id(self.rental_object_id, value)
		self._building_type_id = value

	@property
	def floors_number(self):
		if self._floors_number == None:
			self._floors_number = self.db.get_ro_building_floors_number(self.rental_object_id)
		return self._floors_number
	@floors_number.setter
	def floors_number(self, value):
		self.db.set_ro_building_floors_number(self.rental_object_id, value)
		self._floors_number = value

	@property
	def garbage_disposal(self):
		if self._garbage_disposal == None:
			self._garbage_disposal = self.db.get_ro_building_garbage_disposal(self.rental_object_id)
		return self._garbage_disposal
	@garbage_disposal.setter
	def garbage_disposal(self, value):
		self.db.set_ro_building_garbage_disposal(self.rental_object_id, value)
		self._garbage_disposal = value

	@property
	def intercom(self):
		if self._intercom == None:
			self._intercom = self.db.get_ro_building_intercom(self.rental_object_id)
		return self._intercom
	@intercom.setter
	def intercom(self, value):
		self.db.set_ro_building_intercom(self.rental_object_id, value)
		self._intercom = value

	@property
	def concierge(self):
		if self._concierge == None:
			self._concierge = self.db.get_ro_building_concierge(self.rental_object_id)
		return self._concierge
	@concierge.setter
	def concierge(self, value):
		self.db.set_ro_building_concierge(self.rental_object_id, value)
		self._concierge = value

	@property
	def building_year(self):
		if self._building_year == None:
			self._building_year = self.db.get_ro_building_building_year(self.rental_object_id)
		return self._building_year
	@building_year.setter
	def building_year(self, value):
		self.db.set_ro_building_building_year(self.rental_object_id, value)
		self._building_year = value

	@property
	def elevator(self):
		if self._elevator == None:
			self._elevator = self.db.get_ro_building_elevator(self.rental_object_id)
		return self._elevator
	@elevator.setter
	def elevator(self, value):
		self.db.set_ro_building_elevator(self.rental_object_id, value)
		self._elevator = value



class Location(RentalObjectData):
	# ЛОКАЦИЯ |T| EXTENSION rental_objects> ro_location
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)

		self._coords = None # координаты (десятичные градусы: 41.40338, 2.17403), str
		self._country = None # страна, str
		self._region = None # субъект РФ, str
		self._city = None # город, населенный пункт, str
		self._district = None # район города, str
		self._street = None  # улица, str
		self._building_number = None # номер дома, str
		self._block_number = None # корпус, литера, строение и т.п., str
		self._appt = None # номер квартиры, str
		self._entrance_number = None # номер подъезда, str
		self._floor = None # этаж, int
		self._location_comment = None # дополнительная информация по локации, str

		# ближайшие станции метро |T| MTM metro_stations ⇄ ro_location> ro_location_metro_stations 
		self._nearest_metro_stations = None # ['Сенная', 'Гостинный двор'], list

	#____________________________________________setters and getters____________________________________________

	@property
	def coords(self):
	    if self._coords == None:
	        self._coords = self.db.get_ro_location_coords(self.rental_object_id)
	    return self._coords
	@coords.setter
	def coords(self, value):
	    self.db.set_ro_location_coords(self.rental_object_id, value)
	    self._coords = value

	@property
	def country(self):
	    if self._country == None:
	        self._country = self.db.get_ro_location_country(self.rental_object_id)
	    return self._country
	@country.setter
	def country(self, value):
	    self.db.set_ro_location_country(self.rental_object_id, value)
	    self._country = value

	@property
	def region(self):
	    if self._region == None:
	        self._region = self.db.get_ro_location_region(self.rental_object_id)
	    return self._region
	@region.setter
	def region(self, value):
	    self.db.set_ro_location_region(self.rental_object_id, value)
	    self._region = value

	@property
	def city(self):
	    if self._city == None:
	        self._city = self.db.get_ro_location_city(self.rental_object_id)
	    return self._city
	@city.setter
	def city(self, value):
	    self.db.set_ro_location_city(self.rental_object_id, value)
	    self._city = value

	@property
	def district(self):
	    if self._district == None:
	        self._district = self.db.get_ro_location_district(self.rental_object_id)
	    return self._district
	@district.setter
	def district(self, value):
	    self.db.set_ro_location_district(self.rental_object_id, value)
	    self._district = value

	@property
	def street(self):
	    if self._street == None:
	        self._street = self.db.get_ro_location_street(self.rental_object_id)
	    return self._street
	@street.setter
	def street(self, value):
	    self.db.set_ro_location_street(self.rental_object_id, value)
	    self._street = value

	@property
	def building_number(self):
	    if self._building_number == None:
	        self._building_number = self.db.get_ro_location_building_number(self.rental_object_id)
	    return self._building_number
	@building_number.setter
	def building_number(self, value):
	    self.db.set_ro_location_building_number(self.rental_object_id, value)
	    self._building_number = value

	@property
	def block_number(self):
	    if self._block_number == None:
	        self._block_number = self.db.get_ro_location_block_number(self.rental_object_id)
	    return self._block_number
	@block_number.setter
	def block_number(self, value):
	    self.db.set_ro_location_block_number(self.rental_object_id, value)
	    self._block_number = value

	@property
	def appt(self):
	    if self._appt == None:
	        self._appt = self.db.get_ro_location_appt(self.rental_object_id)
	    return self._appt
	@appt.setter
	def appt(self, value):
	    self.db.set_ro_location_appt(self.rental_object_id, value)
	    self._appt = value

	@property
	def entrance_number(self):
	    if self._entrance_number == None:
	        self._entrance_number = self.db.get_ro_location_entrance_number(self.rental_object_id)
	    return self._entrance_number
	@entrance_number.setter
	def entrance_number(self, value):
	    self.db.set_ro_location_entrance_number(self.rental_object_id, value)
	    self._entrance_number = value

	@property
	def floor(self):
	    if self._floor == None:
	        self._floor = self.db.get_ro_location_floor(self.rental_object_id)
	    return self._floor
	@floor.setter
	def floor(self, value):
	    self.db.set_ro_location_floor(self.rental_object_id, value)
	    self._floor = value

	@property
	def location_comment(self):
	    if self._location_comment == None:
	        self._location_comment = self.db.get_ro_location_location_comment(self.rental_object_id)
	    return self._location_comment
	@location_comment.setter
	def location_comment(self, value):
	    self.db.set_ro_location_location_comment(self.rental_object_id, value)
	    self._location_comment = value

	@property
	def nearest_metro_stations(self):
	    if self._nearest_metro_stations == None:
	        self._nearest_metro_stations = self.db.get_ro_location_nearest_metro_stations(self.rental_object_id)
	    return self._nearest_metro_stations
	@nearest_metro_stations.setter
	def nearest_metro_stations(self, value:list):
	    self.db.set_ro_location_nearest_metro_stations(self.rental_object_id, value)
	    self._nearest_metro_stations = self.db.get_ro_location_nearest_metro_stations(self.rental_object_id)



class Appliance(RentalObjectData):
	# БЫТОВАЯ ТЕХНИКА |T| rental_objects> ro_appliances
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)

		self._rental_object_id = rental_object_id # id объекта аренды, bool
		self._fridge = None # холодильник, bool
		self._dishwasher = None # посудомоечная машина, bool
		self._washer = None # стиральная машина, bool
		self._television = None # телевизор, bool
		self._vacuum = None # пылесос, bool
		self._teapot = None # чайник, bool
		self._iron = None # утюг, bool
		self._microwave = None  # микроволновая печь, bool

	#____________________________________________setters and getters____________________________________________


	@property
	def fridge(self):
	    if self._fridge == None:
	       self._fridge = self.db.get_ro_appliances_fridge(self.rental_object_id)
	    return self._fridge
	@fridge.setter
	def fridge(self, value):
	    self.db.set_ro_appliances_fridge(self.rental_object_id, value)
	    self._fridge = value

	@property
	def dishwasher(self):
	    if self._dishwasher == None:
	       self._dishwasher = self.db.get_ro_appliances_dishwasher(self.rental_object_id)
	    return self._dishwasher
	@dishwasher.setter
	def dishwasher(self, value):
	    self.db.set_ro_appliances_dishwasher(self.rental_object_id, value)
	    self._dishwasher = value

	@property
	def washer(self):
	    if self._washer == None:
	       self._washer = self.db.get_ro_appliances_washer(self.rental_object_id)
	    return self._washer
	@washer.setter
	def washer(self, value):
	    self.db.set_ro_appliances_washer(self.rental_object_id, value)
	    self._washer = value

	@property
	def television(self):
	    if self._television == None:
	       self._television = self.db.get_ro_appliances_television(self.rental_object_id)
	    return self._television
	@television.setter
	def television(self, value):
	    self.db.set_ro_appliances_television(self.rental_object_id, value)
	    self._television = value

	@property
	def vacuum(self):
	    if self._vacuum == None:
	       self._vacuum = self.db.get_ro_appliances_vacuum(self.rental_object_id)
	    return self._vacuum
	@vacuum.setter
	def vacuum(self, value):
	    self.db.set_ro_appliances_vacuum(self.rental_object_id, value)
	    self._vacuum = value

	@property
	def teapot(self):
	    if self._teapot == None:
	       self._teapot = self.db.get_ro_appliances_teapot(self.rental_object_id)
	    return self._teapot
	@teapot.setter
	def teapot(self, value):
	    self.db.set_ro_appliances_teapot(self.rental_object_id, value)
	    self._teapot = value

	@property
	def iron(self):
	    if self._iron == None:
	       self._iron = self.db.get_ro_appliances_iron(self.rental_object_id)
	    return self._iron
	@iron.setter
	def iron(self, value):
	    self.db.set_ro_appliances_iron(self.rental_object_id, value)
	    self._iron = value

	@property
	def microwave(self):
	    if self._microwave == None:
	       self._microwave = self.db.get_ro_appliances_microwave(self.rental_object_id)
	    return self._microwave
	@microwave.setter
	def microwave(self, value):
	    self.db.set_ro_appliances_microwave(self.rental_object_id, value)
	    self._microwave = value



class Costs(RentalObjectData):
	# РАСХОДЫ НА СОДЕРЖАНИЕ |T| rental_objects> ro_maintenance_costs [cost_number, cost_name, user_type_id]															# user_type_id - плательщик (tenant/landlord/None)
	def __init__(self, rental_object_id):
		super().__init__(rental_object_id)
		self._maintenance_costs = None 

	@property
	def maintenance_costs(self):
		if self._maintenance_costs == None:
			self._maintenance_costs = self.db.get_maintenance_costs(self.rental_object_id)
		return self._maintenance_costs
	@maintenance_costs.setter
	def maintenance_costs(self, value:list):
		if isinstance(value, list):
			self.db.set_maintenance_costs(self.rental_object_id, value)
			self._maintenance_costs = value
		else:
			raise TypeError



if __name__ == '__main__':
	x = Location(1)

	# print(x.bathroom_type_id)
	# print(x.wash_place_type_id)
	# print(x.area)
	# print(x.ceilings_height)
	# print(x.win_number)
	# print(x.balcony)
	# print(x.air_conditioner)
	# print(x.wi_fi)
	# print(x.furniture)
	# print(x.window_overlook)
	# print(x.window_frame_type)
	# print(x.cooking_range_type)

	# x.bathroom_type_id = 2
	# x.wash_place_type_id = 2
	# x.area = 16.0
	# x.ceilings_height = 3.2
	# x.win_number = 2
	# x.balcony = 1
	# x.air_conditioner = True
	# x.wi_fi = False
	# x.furniture = False
	# x.window_overlook = {'street': 1, 'yard': 2}
	# x.window_frame_type = {'wood': 1, 'plastic': 1}
	# x.cooking_range_type = {'electric': 1, 'gas': 1}

	# print(x.bathroom_type_id)
	# print(x.wash_place_type_id)
	# print(x.area)
	# print(x.ceilings_height)
	# print(x.win_number)
	# print(x.balcony)
	# print(x.air_conditioner)
	# print(x.wi_fi)
	# print(x.furniture)
	# print(x.window_overlook)
	# print(x.window_frame_type)
	# print(x.cooking_range_type)

	# print(x.building_type_id)
	# print(x.floors_number)
	# print(x.garbage_disposal)
	# print(x.intercom)
	# print(x.concierge)
	# print(x.building_year)
	# print(x.elevator)


	# x.building_type_id = 2
	# x.floors_number = 122
	# x.garbage_disposal = True
	# x.intercom = True
	# x.concierge = True
	# x.building_year = '1912'
	# x.elevator = {'passenger': 1, 'freight': 0}

	# print(x.building_type_id)
	# print(x.floors_number)
	# print(x.garbage_disposal)
	# print(x.intercom)
	# print(x.concierge)
	# print(x.building_year)
	# print(x.elevator)


	print(x.coords)
	print(x.country)
	print(x.region)
	print(x.city)
	print(x.district)
	print(x.street)
	print(x.building_number)
	print(x.block_number)	
	print(x.appt)
	print(x.entrance_number)
	print(x.floor)
	print(x.location_comment)
	print(x.nearest_metro_stations)

	x.coords = '1111 1111'
	x.country = 'РФ'
	x.region = 'Санкт-петербург'
	x.city = 'Санкт-петербург'
	x.district = 'Центральный'
	x.street = 'Мучной переулок'
	x.building_number = '3'
	x.block_number = ''
	x.appt = '11'
	x.entrance_number = '3'
	x.floor = 5
	x.location_comment = 'Вход со двора, после арки направо'
	x.nearest_metro_stations = [7,8,9]

	print(x.coords)
	print(x.country)
	print(x.region)
	print(x.city)
	print(x.district)
	print(x.street)
	print(x.building_number)
	print(x.block_number)	
	print(x.appt)
	print(x.entrance_number)
	print(x.floor)
	print(x.location_comment)
	print(x.nearest_metro_stations)


	# print(x.fridge)
	# print(x.dishwasher)
	# print(x.washer)
	# print(x.television)
	# print(x.vacuum)
	# print(x.teapot)
	# print(x.iron)
	# print(x.microwave)



	# x.fridge = False
	# x.dishwasher = True
	# x.washer = True
	# x.television = True
	# x.vacuum = True
	# x.teapot = True
	# x.iron = True
	# x.microwave = True


	# print(x.fridge)
	# print(x.dishwasher)
	# print(x.washer)
	# print(x.television)
	# print(x.vacuum)
	# print(x.teapot)
	# print(x.iron)
	# print(x.microwave)