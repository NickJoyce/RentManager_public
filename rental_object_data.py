class ObjectData:
	def __init__(self, rental_object_id, bathroom_type_id, wash_place_type_id, area, ceilings_height, win_number, balcony,
					   air_conditioner, wi_fi, furniture):
		# ОБЩАЯ ИНФОРМАЦИЯ |T| EXTENSION rental_objects> ro_object_data
		self.rental_object_id = rental_object_id # id объекта аренды
		self.bathroom_type_id = bathroom_type_id  # тип ванной комнаты (санузел) |T| SOURCE> bathroom_types ['совмещенный', 'раздельный'] 
		self.wash_place_type_id =  wash_place_type_id # тип места для мытья |T| SOURCE> wash_place_types ['ванна', 'душевая кабина']
		self.area = area# площадь
		self.ceilings_height = ceilings_height # высота потолков
		self.win_number = win_number # количество окон
		self.balcony = balcony # балкон/лоджия (количество)
		self.air_conditioner = air_conditioner # кондиционер
		self.wi_fi = wi_fi # wi-fi
		self.furniture = furniture # мебель


		self.window_overlook = None # вид из окна |T| EXTENSION ro_general>  ro_general_window_overlooks {'на улицу': False, 'во двор': False}
		self.window_frame_type = None # тип окон |T| EXTENSION ro_general> ro_general_window_frames {'деревяные': False, 'пластиковые': False}
		self.cooking_range_type = None # тип плит |T| EXTENSION ro_general> ro_general_cooking_ranges {'электрическая': False, 'газовая': False}



class Building:
	def __init__(self, rental_object_id, building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year):
		# ЗДАНИЕ |T| EXTENSION rental_objects> ro_building
		self.rental_object_id = rental_object_id # id объекта аренды
		self.building_type_id = building_type_id # тип здания |T| SOURCE> building_types ['кирпичный', 'панельный'] 
		self.floors_number = floors_number # всего этажей в доме
		self.garbage_disposal = garbage_disposal # мусоропровод
		self.intercom = intercom # домофон
		self.concierge = concierge # консьерж
		self.building_year = building_year # год постройки

		self.elevator = None # тип лифтов |T| EXTENSION ro_building> ro_building_elevators {'пассажирский': 0, 'грузовой': 0}



class Location:
	def __init__(self, rental_object_id, coords, country, region, city, district, street, building_number, block_number,
					   appt, entrance_number, floor, location_comment):
		# ЛОКАЦИЯ |T| EXTENSION rental_objects> ro_location
		self.rental_object_id = rental_object_id # id объекта аренды
		self.coords = coords # координаты (десятичные градусы: 41.40338, 2.17403)
		self.country = country # страна
		self.region = region # субъект РФ
		self.city = city # город, населенный пункт
		self.district = district # район города
		self.street = street  # улица
		self.building_number = building_number # номер дома
		self.block_number = block_number # корпус, литера, строение и т.п.
		self.appt = appt # номер квартиры
		self.entrance_number = entrance_number # номер подъезда
		self.floor = floor # этаж
		self.location_comment = location_comment # дополнительная информация по локации

		self.nearest_metro_stations = [] # ближайшие станции метро |T| MTM metro_stations ⇄ ro_location> ro_location_metro_stations ['Сенная', 'Гостинный двор']



class Appliances:
	def __init__(self, rental_object_id, fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave):
		# БЫТОВАЯ ТЕХНИКА |T| rental_objects> ro_appliances
		self.rental_object_id = rental_object_id # id объекта аренды
		self.fridge = fridge # холодильник
		self.dishwasher = dishwasher # посудомоечная машина
		self.washer = washer # стиральная машина
		self.television = television # телевизор
		self.vacuum = vacuum # пылесос
		self.teapot = teapot # чайник
		self.iron = iron # утюг
		self.microwave = microwave  # микроволновая печь



class WindowOverlook:
	def __init__(self, street, yard):
		self.street = street
		self.yard = yard


class WindowFrameType:
	def __init__(self, wood, plastic):
		self.wood = wood
		self.plastic = plastic


class CookingRangeType:
	def __init__(self, electric, gas):
		self.electric = electric
		self.gas = gas


class Elevator:
	def __init__(self, passenger, freight):
		self.passenger = passenger
		self.freight = freight