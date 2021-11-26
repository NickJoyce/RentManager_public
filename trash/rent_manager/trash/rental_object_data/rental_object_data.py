class ObjectData:
	def __init__(self):
		# ОБЩАЯ ИНФОРМАЦИЯ |T| EXTENSION rental_objects> ro_object_data
		self.area = 0.0 # площадь
		self.ceilings_height = 0.0 # высота потолков
		self.win_number = 0 # количество окон
		self.balcony = 0 # балкон/лоджия (количество)
		self.air_conditioner = False # кондиционер
		self.wi_fi = False # wi-fi
		self.furniture = False # мебель
		self.bathroom_type = ''  # тип ванной комнаты (санузел) |T| SOURCE> bathroom_types ['совмещенный', 'раздельный'] 
		self.wash_place_type = '' # тип места для мытья |T| SOURCE> wash_place_types ['ванна', 'душевая кабина']

		self.window_overlook = {} # вид из окна |T| EXTENSION ro_general>  ro_general_window_overlooks {'на улицу': False, 'во двор': False}
		self.window_frame_type = {} # тип окон |T| EXTENSION ro_general> ro_general_window_frames {'деревяные': False, 'пластиковые': False}
		self.cooking_range_type = {} # тип плит |T| EXTENSION ro_general> ro_general_cooking_ranges {'электрическая': False, 'газовая': False}



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



class Location:
	def __init__(self):
		# ЛОКАЦИЯ |T| EXTENSION rental_objects> ro_location
		self.coords = '' # координаты (десятичные градусы: 41.40338, 2.17403)
		self.country = 'Россия' # страна
		self.region = '' # субъект РФ
		self.city = '' # город, населенный пункт
		self.district = '' # район города
		self.street = '' # улица
		self.building_number = '' # номер дома
		self.block_number = '' # корпус, литера, строение и т.п.
		self.appt = '' # номер квартиры
		self.entrance_number = 0 # номер подъезда
		self.floor = 0 # этаж
		self.location_comment = '' # дополнительная информация по локации

		self.nearest_metro_stations = [] # ближайшие станции метро |T| MTM metro ⇄ ro_district> ro_district_metro_stations ['Сенная', 'Гостинный двор']



class Appliances:
	def __init__(self):
		# БЫТОВАЯ ТЕХНИКА |T| rental_objects> ro_appliances
		self.fridge = False # холодильник
		self.dishwasher = False # посудомоечная машина
		self.washer = False # стиральная машина
		self.television = False # телевизор
		self.vacuum = False # пылесос
		self.teapot = False # чайник
		self.iron = False # утюг
		self.microwave = False # микроволновая печь