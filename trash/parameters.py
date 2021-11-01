from prettytable import PrettyTable

class Parameters:
	def __repr__(self):
		return f"{self.__class__.__name__}()"

	def __str__(self):
		table = PrettyTable()
		table.field_names = ["Параметр", "Значение"] # column name
		table._min_width = {"Параметр" : 30, "Значение": 15} # column width 
		table.align["Параметр"] = "l" # text-align: left
		table.align["Значение"] = "l" # text-align: left
		for k,v in self.__dict__.items():
			table.add_row([k, v])
		return str(table)

class Unit(Parameters):
	"""Параметры сдаваемого в аренду объекта"""
	def __init__(self):
		# ОБЩАЯ ИНФОРМАЦИЯ
		self.floor = 0.0 # этаж
		self.area = 0.0 # площадь
		self.ceilings = 0.0 # высота потолков
		self.win_number = 0 # количество окон
		self.balcony = 0 # балкон/лоджия
		self.window_overlook = {'На улицу': False, 'Во двор': False} # Вид из окон
		self.bathroom_type = {'Раздельный': 0, 'Совмещенный': 0} # тип ванной комнаты
		self.wash_place_type = {'Ванна': 0, 'Душевая кабина': 0} # тип места для мытья (ванна/душевая кабина)
		self.window_frame_type = {'Пластиковые': False, 'Деревянные': False} # тип окон
		self.air_conditioner = False # кондиционер
		self.internet = False # доступ в интернет
		self.furniture = False # мебель
		self.cooking_range_type = {'Газовая': False, 'Электрическая': False} # тип плиты

		# БЫТОВАЯ ТЕХНИКА
		self.fridge = False # холодильник
		self.dishwasher = False # посудомоечная машина
		self.washer = False # стиральная машина
		self.television = False # телевизор
		self.vacuum = False # пылесос
		self.teapot = False # чайник
		self.iron = False # утюг
		self.microwave = False # микроволновая печь


class Building(Parameters):
	"""Параметры здания"""
	def __init__(self):
		self.floors = None # всего этажей в доме
		self.elevator = {'Пассажирский': 0, 'Грузовой':0} # лифт
		self.garbage_disposal = False # мусоропровод
		self.intercom = False # домофон
		self.concierge= False # консьерж
		self.building_year = None # год постройки
		self.building_type = {'Панельный': True, 'Кирпичный': True} # тип здания


class District(Parameters):
	"""Параметры района"""
	def __init__(self):
		self.nearest_metro_stations = [] # ближайшая станция метро


if __name__ == '__main__':
	x = Building()
	print(x)

