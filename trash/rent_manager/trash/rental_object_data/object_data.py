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