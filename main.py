from datetime import date

from rental_agreement import RentalAgreement # договор аренды

from users import Admin, Agent, Landlord, Tenant # пользователи
from passport import Passport # паспортные данные пользователей
from register import Register # регистрационные данные пользоватлей

from rental_objects import Room, Flat, House # объекты аренды

from conditions import Conditions, AdditionalPayments # условия аренды, дополнительны платежи

from rental_object_data import ObjectData, Building, Location, Appliances
from rental_object_data import WindowOverlook, WindowFrameType, CookingRangeType, Elevator

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataDefinition # класс для определения и модификации объектов(таблиц, базданных)
from database.use_db import DataManipulation # класс для манипулирования данными в БД



db_def = DataDefinition(db_config, DBcm)
db = DataManipulation(db_config, DBcm) # экземпляр класса для взаимодействия с БД


	
# СОЗДАНИЕ ЭКЗЕМПЛЯРОВ КЛАССОВ С ПРИСВОЕНИЕМ АТРИБУТАМ ЗНАЧЕНИЙ ИЗ БД
def create_user_instance_by_id(user_id):
	"""Создает экземпляр одного из классов (Admin, Agent, Landlord или Tenant)
	   в зависимости от типа пользователя, присваивает значения подгруженные из БД 
	   соответствующим арибутам
	"""
	user_data = db.get_user_data(user_id)
	user_type = db.get_user_type_by_id(user_id)
	if user_type == 'администратор':
		user = Admin(*user_data, *db.get_admin_user_data(user_id))
	elif user_type == 'агент':
		user = Agent(*user_data, *db.get_agent_user_data(user_id))
	elif user_type == 'наймодатель':
		user = Landlord(*user_data, *db.get_landlord_user_data(user_id))
	elif user_type == 'наниматель':
		user = Tenant(*user_data, *db.get_tenant_user_data(user_id))
	user.passport = Passport(*db.get_passport_data(user_id))
	user.register = Register(*db.get_register_data(user_id))
	return user


def create_rental_object_instance_by_id(rental_object_id):
	"""Создает экземпляр одного из классов (Room, Flat или House)
	   в зависимости от типа пользователя, присваивает значения подгруженные из БД 
	   соответствующим арибутам
	"""
	rental_object = db.get_rental_object_data(rental_object_id)
	rental_object_type = db.get_rental_object_type_by_id(rental_object_id)

	if rental_object_type == 'комната':
		rental_object = Room(*rental_object, *db.get_room_rental_object_data(rental_object_id))
	elif rental_object_type == 'квартира':
		rental_object = Flat(*rental_object, *db.get_flat_rental_object_data(rental_object_id))
	elif rental_object_type == 'дом':
		rental_object = House(*rental_object, *db.get_house_rental_object_data(rental_object_id))

	rental_object.location = Location(*db.get_location_data(rental_object_id))
	rental_object.location.nearest_metro_stations = db.get_location_nearest_metro_stations_data(rental_object_id)

	rental_object.object_data = ObjectData(*db.get_object_data(rental_object_id))
	rental_object.object_data.window_overlook = WindowOverlook(*db.get_object_window_overlook_data(rental_object_id))
	rental_object.object_data.window_frame_type = WindowFrameType(*db.get_object_window_frame_type_data(rental_object_id))
	rental_object.object_data.cooking_range_type = CookingRangeType(*db.get_object_cooking_range_type_data(rental_object_id))

	rental_object.building = Building(*db.get_building_data(rental_object_id))
	rental_object.building.elevator = Elevator(*db.get_building_elevator_data(rental_object_id))

	rental_object.appliances = Appliances(*db.get_appliances_data(rental_object_id))

	rental_object.things = db.get_things_data(rental_object_id)

	return rental_object






# ОБНОВЛЕНИЕ ЗНАЧЕНИЙ В ПОЛЯХ БД СООТВЕТСТВУЮЩИХ АТРИБУТАМ ЭКЗКМПЛЯРА
def save_user(inst):
	"""Обновляет данные в БД соответствующие атрибутам принятого экземпляра"""
	user_id = inst.user_id
	db.update_user_data(user_id, inst.name, 
								 inst.phone, 
								 inst.email) # таблица users
	
	if isinstance(inst, Landlord):
		db.update_landlord_user_data(user_id, inst.inn) # таблица users_landlords
	elif isinstance(inst, Tenant):
		db.update_tenant_user_data(user_id) # таблица users_tenants
	elif isinstance(inst, Admin):
		db.update_admin_user_data(user_id) # таблица users_admins
	elif isinstance(inst, Agent):
		db.update_agent_user_data(user_id) # таблица users_agents
	else:
		raise TypeError

	db.update_passport_data(user_id, inst.passport.first_name, 
									 inst.passport.patronymic, 
									 inst.passport.last_name, 
					    			 inst.passport.serie, 
					    			 inst.passport.number, 
					   				 inst.passport.authority, 
					    			 inst.passport.department_code,
		                			 inst.passport.date_of_issue, 
		                			 inst.passport.date_of_birth, 
		                			 inst.passport.place_of_birth, 
		                			 inst.passport.registration) # таблица passport

	db.update_register_data(user_id, inst.register.login, 
				       				 inst.register.password) # таблица register




def save_rental_object(inst):
	rental_object_id = inst.rental_object_id
	db.update_rental_object_data(rental_object_id, inst.name,
												   inst.cadastral_number,
												   inst.title_deed,
												   inst.is_rented,
												   inst.current_rental_agreement_id) # таблица rental_objects
	if isinstance(inst, Room):
		db.update_room_rental_object_data(rental_object_id, inst.total_area,
														    inst.rooms_number)
	elif isinstance(inst, Flat):
		db.update_flat_rental_object_data(rental_object_id)
	elif isinstance(inst, House):
		db.update_house_rental_object_data(rental_object_id)
	else:
		raise TypeError

	db.update_location_data(rental_object_id, inst.location.coords, 
											  inst.location.country, 
											  inst.location.region, 
											  inst.location.city, 
											  inst.location.district, 
											  inst.location.street, 
											  inst.location.building_number, 
											  inst.location.block_number, 
											  inst.location.appt, 
											  inst.location.entrance_number, 
											  inst.location.floor, 
											  inst.location.location_comment)

	db.update_location_nearest_metro_stations_data(rental_object_id, inst.location.nearest_metro_stations)



	db.update_object_data(rental_object_id, inst.object_data.bathroom_type_id, 
									        inst.object_data.wash_place_type_id, 
									        inst.object_data.area, 
									        inst.object_data.ceilings_height, 
									        inst.object_data.win_number, 
									        inst.object_data.balcony, 
									        inst.object_data.air_conditioner, 
									        inst.object_data.wi_fi, 
									        inst.object_data.furniture)

	db.update_object_data_window_overlook(rental_object_id, inst.object_data.window_overlook.street,
														    inst.object_data.window_overlook.yard)


	db.update_object_data_window_frame_type(rental_object_id, inst.object_data.window_frame_type.wood ,
														      inst.object_data.window_frame_type.plastic)

	db.update_object_data_cooking_range_type(rental_object_id, inst.object_data.cooking_range_type.electric,
														       inst.object_data.cooking_range_type.gas)


	db.update_building_data(rental_object_id, inst.building.building_type_id,
											  inst.building.floors_number, 
											  inst.building.garbage_disposal, 
											  inst.building.intercom, 
											  inst.building.concierge, 
											  inst.building.building_year)


	db.update_appliances_data(rental_object_id, inst.appliances.fridge, 
												inst.appliances.dishwasher, 
												inst.appliances.washer, 
												inst.appliances.television, 
												inst.appliances.vacuum, 
												inst.appliances.teapot, 
												inst.appliances.iron, 
												inst.appliances.microwave)

	db.update_things_data(rental_object_id, inst.things)





if __name__ == '__main__':
	# db_def.reload_all_tables()
	# rental_object_types = ['комната', 'квартира', 'дом']
	# for type_ in rental_object_types:
	# 	db.insert_rental_object_type(type_)

	# bathroom_types = ['совмещенный', 'раздельный'] 
	# for type_ in bathroom_types:
	# 	db.add_bathroom_type(type_)

	# wash_place_type = ['ванна', 'душевая кабина']
	# for type_ in wash_place_type:
	# 	db.add_wash_place_type(type_)

	# building_types = ['кирпичный', 'панельный'] 
	# for type_ in building_types:
	# 	db.add_building_type(type_)

	# db.add_thing(4, 'Стул', 2, 2500)
	# db.add_thing(4, 'Стол', 1, 8500)
	# db.add_thing(4, 'Кровать', 1, 1500)







	# db.create_rental_object('комната', 'Мучной (Комната 1)')
	# db.create_rental_object('квартира', 'Вася')
	# db.create_rental_object('комната', 'Мучной (Комната 2)')
	# db.create_rental_object('дом', 'Зеленогорск')

	room1 = create_rental_object_instance_by_id(1)
	room2 = create_rental_object_instance_by_id(3)

	flat = create_rental_object_instance_by_id(2)
	house = create_rental_object_instance_by_id(4)

	house.name = 'Васильевкий остров'
	house.cadastral_number = '123:223232:232:3434232'
	house.title_deed = 'Договор купли продажи АБ 128ывыв6'
	house.is_rented = 1
	house.current_rental_agreement_id = 3


	house.location.coords = '60.23278035702726, 29.70443221234928'
	house.location.country = 'Россия'
	house.location.region = 'Ленинградская область'
	house.location.city = 'Зеленогорск'
	house.location.district = 'Центральный'
	house.location.street = 'ул. Ленина' 
	house.location.building_number = '12'
	house.location.block_number = ''
	house.location.appt = '39'
	house.location.entrance_number = '3' 
	house.location.floor = 5
	house.location.location_comment = 'Отличный дом в Зеленогорске'

	house.object_data.bathroom_type_id = 1
	house.object_data.wash_place_type_id = 2
	house.object_data.area = 35
	house.object_data.ceilings_height = 3.5 
	house.object_data.win_number = 2 
	house.object_data.balcony = 0
	house.object_data.air_conditioner = 0
	house.object_data.wi_fi = 0
	house.object_data.furniture = 1

	house.building.building_type_id = 1
	house.building.floors_number = 15
	house.building.garbage_disposal = 0 
	house.building.intercom = 1
	house.building.concierge = 1
	house.building.building_year = 1912


	house.appliances.fridge = 1
	house.appliances.dishwasher = 1 
	house.appliances.washer = 1
	house.appliances.television = 0 
	house.appliances.vacuum = 1
	house.appliances.teapot = 0
	house.appliances.iron = 1
	house.appliances.microwave = 1

	house.object_data.window_overlook.yard = 1
	house.object_data.window_overlook.street = 1

	house.object_data.window_frame_type.wood = 1
	house.object_data.window_frame_type.plastic = 1


	house.object_data.cooking_range_type.electric = 0
	house.object_data.cooking_range_type.gas = 1

	house.location.nearest_metro_stations = []

	save_rental_object(house)





	
	
