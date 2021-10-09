from user import Landlord, Tenant # Найиодатель, Наниматель
from conditions import Conditions # Условия сдачи в аренду
from payments import Payments # дополнительные платежи

class RealEstateObject:
	"""Объекты недвижимости"""
	def __init__(self, address: str, floor: int, area: float, photo: list, type_ = 'Real Estate Object', landlord = None, Tenant = None,
					   conditions = None, payments = None):
		self.address = address # адрес
		self.floor = floor # этаж
		self.area = area # площадь
		self.photo = photo # список наименований файлов
		self.type = type_ # тип объекта недвижимости
		# TODO определить все базовые атрибуты для коневого класса

		# НАЙМОДАТЕЛЬ
		self.landlord = landlord # экземпляр класса Landlord

		# НАНИМАТЕЛЬ
		self.tenant = tenant # экземпляр класса Tenant

		# УСЛОВИЯ АРЕНДЫ
		self.conditions = conditions # экземпляр класса Conditions

		# ДОПОЛНИТЕЛЬНЫЕ ПЛАТЕЖИ
		self.payments = payments # экземпляр класса Payments

		# ВЕЩИ
		# TODO



class Flat(RealEstateObject):
	def __init__(self, address: str, floor: int, area: float, photo: list, type_ = 'flat', landlord = None, Tenant = None,
					   conditions = None, payments = None):
		super().__init__(address, floor, area, photo, type_, landlord, Tenant, conditions)


class Room(RealEstateObject):
	def __init__(self, address: str, floor: int, area: float, photo: list, total_area: float, rooms_nuber: int,
					   type_ = 'room', landlord = None, Tenant = None, conditions = None, payments = None):
		super().__init__(address, floor, area, photo, type_, landlord, Tenant, conditions)
		self.total_area = total_area # общая площадь квартиры
		self.rooms_nuber = rooms_nuber # всего комнат в квартире


class House(RealEstateObject):
	def __init__(self, address: str, floor: int, area: float, photo: list, total_area: float, rooms_nuber: int,
					   type_ = 'room', landlord = None, Tenant = None, conditions = None, payments = None):
		super().__init__(address, floor, area, photo, type_, landlord, Tenant, conditions)
