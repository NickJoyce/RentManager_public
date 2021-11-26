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