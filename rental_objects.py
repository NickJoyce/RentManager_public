from prettytable import PrettyTable

class RentalObject:
	"""Объект недвижимости"""
	def __init__(self, rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id): 


		# TODO поменять определение данных в таблице rental_objects
		# БАЗОВАЯ ИНФОРМАЦИЯ |T|> rental_objects, |T|> cities, |T|> cities_districts, |T|> ro_cities_districts, |T|> metro_stations
		self.rental_object_id = rental_object_id
		self.type_id = type_id # тип объекта недвижимости |T| SOURCE> rental_object_types ['комната', 'квартира', 'дом']
		self.name = name # имя объекта
		self.cadastral_number = cadastral_number # TODO кадастровый номер объекта аренды # TODO
		self.title_deed = title_deed # TODO документ подтверждающий право собственности
		self.is_rented = is_rented # объект сдан?
		self.current_rental_agreement_id = current_rental_agreement_id # номер договора аренды

		self.location = None # экземпляр класса Location - локация объекта
		self.object_data = None # экземпляр класса ObjectData - информация об объекте
		self.building_data = None # экземпляр класса ObjectData - информация об здании
		self.appliances = None # экземпляр класса ObjectData - информация бытовой технике

		# ВЕЩИ |T| rental_objects> ro_things 
		self.things = {} #  вещи в объекте {'table':[1, 3000], ..., n}


		


	def __repr__(self):
		return f"{self.__class__.__name__}({self.rental_object_id}, {self.type_id}, {self.name})"

	def __str__(self):
		table = PrettyTable()
		table.field_names = ["rental_object_id", 'type_id', "name"] # column name
		table._min_width = {"rental_object_id" : 20, "type_id" : 20, "name" : 20} # column width 
		table.add_row([self.rental_object_id, self.type_id, self.name])	
		return str(table)


class Room(RentalObject):
	def __init__(self, rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id, 
					   room_id, total_area, rooms_number):
		super().__init__(rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id)
		self.room_id = room_id
		self.total_area =  total_area # общая площадь квартиры
		self.rooms_number = rooms_number # всего комнат в квартире

	def __str__(self):
		super().__str__()
		table = PrettyTable()
		table.field_names = ["room_id"] # column name
		table._min_width = {"room_id" : 20} # column width 
		table.add_row([self.room_id])	
		return f'{super().__str__()}\n{str(table)}'


class Flat(RentalObject):
	def __init__(self, rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id, 
					   flat_id):
		super().__init__(rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id)
		self.flat_id =  flat_id

	def __str__(self):
		super().__str__()
		table = PrettyTable()
		table.field_names = ["flat_id"] # column name
		table._min_width = {"flat_id" : 20} # column width 
		table.add_row([self.flat_id])	
		return f'{super().__str__()}\n{str(table)}'


class House(RentalObject):
	def __init__(self, rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id, 
					   house_id):
		super().__init__(rental_object_id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id)
		self.house_id =  house_id

	def __str__(self):
		super().__str__()
		table = PrettyTable()
		table.field_names = ["house_id"] # column name
		table._min_width = {"house_id" : 20} # column width 
		table.add_row([self.house_id])	
		return f'{super().__str__()}\n{str(table)}'




if __name__ == '__main__':
	x = Room(1)
	print(x.area)
	print(x.ceilings_height)
	print(x.win_number)
	print(x.balcony)

	x.area = 15.5
	x.ceilings = 3.4
	x.win_number = 1
	x.balcony = None
	x.window_overlook['street'] = False



	print(x.area)
	print(x.ceilings)
	print(x.win_number)
	print(x.balcony)
	print(x.window_overlook['street'])
	print(x.BUILDING_TYPES)
