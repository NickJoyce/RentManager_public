import json
import csv

##################################################   DATABASE CONNECTION   ##################################################
class Database:
	"""Инициализция инструмента для передачи запросов к БД, основной базывый класс"""
	def __init__(self, config, context_manager):
		self.config = config # параметры подключения к БД
		self.context_manager = context_manager # менеджер контекста БД

##################################################   DATA DEFINITION   #######################################################

class UserDD:
	"""Определение данных для таблиц связанных с пользователями"""
	def create_all_user_tables(self):
		"""Создает все таблицы в БД"""
		with self.context_manager(self.config) as cursor:

			# user_types - типы пользоватлей
			cursor.execute("""CREATE TABLE IF NOT EXISTS user_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   	 type VARCHAR(100) UNIQUE
																   	 ) ENGINE = InnoDB""" )		

			# users
			cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																type_id INT,
																name VARCHAR(100)  DEFAULT '',
																phone VARCHAR(100) DEFAULT '',
																email VARCHAR(100) UNIQUE,
																FOREIGN KEY(type_id)
																 	REFERENCES user_types(id)													
																) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `users`')

			# admins
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_admins (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 user_id INT NOT NULL,
																 INDEX user_id_idx (user_id),
																 FOREIGN KEY(user_id)
																 	REFERENCES users(id)
																 	ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `users_admins`')
			# agents
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_agents (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 user_id INT NOT NULL,
																 INDEX user_id_idx (user_id),
																 FOREIGN KEY(user_id)
																 	REFERENCES users(id)
																 	ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `users_agents`')
			# landlords
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_landlords (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 user_id INT NOT NULL,
																 INDEX user_id_idx (user_id),
																 inn VARCHAR(100) DEFAULT '',
																 FOREIGN KEY(user_id)
																 	REFERENCES users(id)
																 	ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `users_landlords`')
			# tenants
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_tenants (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 user_id INT NOT NULL,
																 INDEX user_id_idx (user_id),
																 FOREIGN KEY(user_id)
																 	REFERENCES users(id)
																 	ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `users_tenants`')
			# passport
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_passport (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   user_id INT NOT NULL,
																   first_name VARCHAR(100),
																   patronymic VARCHAR(100),
																   last_name VARCHAR(100),
																   serie VARCHAR(100),
																   pass_number VARCHAR(100),
																   authority VARCHAR(100), 
																   department_code VARCHAR(100),
																   date_of_issue DATE DEFAULT '0001-01-01', 
																   date_of_birth DATE DEFAULT '0001-01-01', 
																   place_of_birth VARCHAR(100),
																   registration VARCHAR(100),
																   INDEX user_id_idx (user_id),
																   FOREIGN KEY(user_id)
																 		REFERENCES users(id)
																 		ON DELETE CASCADE
																   ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `users_passport`')

			# register
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_register (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   user_id INT NOT NULL,
																   login VARCHAR(100),
																   password VARCHAR(255),
																   INDEX user_id_idx (user_id),
																   FOREIGN KEY(user_id)
																 		REFERENCES users(id)
																 		ON DELETE CASCADE
																   ) ENGINE = InnoDB""" )													

			print('CREATE TABLE IF NOT EXISTS `users_register`')
		

class RentalObjectDD:
	"""Определение данных для таблиц связанных с объектом аренды"""
	def create_all_rental_object_tables(self):
		with self.context_manager(self.config) as cursor:

			# rental_object_types - типы объктов
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_object_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   			  type VARCHAR(100) UNIQUE
			
																   			  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_object_types`')
			# rental_objects - объекты аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_objects (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 type_id INT NOT NULL,
																		 landlord_id INT NOT NULL,
																		 tenant_id INT, 
																		 agent_id INT, 
																		 rental_agreement_id INT,
																		 FOREIGN KEY (type_id)
																			REFERENCES rental_object_types(id),
																		 FOREIGN KEY (landlord_id)
																			REFERENCES users_landlords(id),
																		 FOREIGN KEY (tenant_id)
																			REFERENCES users_tenants(id),
																		 FOREIGN KEY (agent_id)
																			REFERENCES users_agents(id)
																		) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_objects`')


			# ro_general
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general (rental_object_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	 name VARCHAR(100),
																	 cadastral_number VARCHAR(100),
																	 title_deed VARCHAR(255),
																	 FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE																	 
															 	  	  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_general`')	





			# maintenance_costs
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_maintenance_costs (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																			   rental_object_id INT NOT NULL,
																			   cost_number INT DEFAULT 0,
																			   cost_name VARCHAR(100) NOT NULL DEFAULT '',
																			   user_type_id INT, # плательщик по договору
																			   FOREIGN KEY (rental_object_id)
																			   		REFERENCES rental_objects(id)
																			   		ON DELETE CASCADE,
																			   FOREIGN KEY (user_type_id)
																			   		REFERENCES user_types(id),
																			   	UNIQUE(rental_object_id, cost_name)
															 	  	  		    ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ra_additional_payments`')





			#СТРАНЫ, ГОРОДА, РАЙОНЫ, СТАНЦИИ МЕТРО
			# countries - страны
			cursor.execute("""CREATE TABLE IF NOT EXISTS countries (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 	country VARCHAR(100),
																 	UNIQUE (country)
																    ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `countries`')	

			# cities города
			cursor.execute("""CREATE TABLE IF NOT EXISTS cities (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 country_id INT NOT NULL,
																 city VARCHAR(100),
																 FOREIGN KEY (country_id)
																	REFERENCES countries(id)
																	ON DELETE CASCADE,
																 UNIQUE (country_id, city)															 
																 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `cities`')


			# districts - районы
			cursor.execute("""CREATE TABLE IF NOT EXISTS districts (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 		   city_id INT,
																 		   district VARCHAR(255),
																 		   FOREIGN KEY(city_id)
																			   	REFERENCES cities(id)
																				ON DELETE CASCADE,
																			UNIQUE (city_id, district)
																 			) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `districts`')	

			# metro_stations
			cursor.execute("""CREATE TABLE IF NOT EXISTS metro_stations (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																         city_id INT NOT NULL,
																		 line_number VARCHAR(100),
																		 line_name VARCHAR(100),
																		 color VARCHAR(100),
																		 station VARCHAR(100) NOT NULL,
																		 is_valid BOOL DEFAULT 1,
																 		 FOREIGN KEY (city_id)
																			REFERENCES cities(id)
																			ON DELETE CASCADE,																		 
																		 UNIQUE (city_id, line_number, station)
																		 ) ENGINE = InnoDB""" )														  									
			print('CREATE TABLE IF NOT EXISTS `metro_stations`')


			#ПРИВЯЗКА ОБЪЕКТА АРЕНДЫ К СТРАНЕ, ГОРОДУ, РАЙОНУ
			# ro_country_city_district
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_country_city_district (rental_object_id INT PRIMARY KEY NOT NULL,
																	 country_id INT,
																	 city_id INT,
																	 district_id INT,
																 	 FOREIGN KEY (rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE,
																 	  FOREIGN KEY (country_id)
																 		REFERENCES countries(id),
																  	  FOREIGN KEY (city_id)
																 		REFERENCES cities(id),
																 	  FOREIGN KEY (district_id)
																 		REFERENCES districts(id)
																 	  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_country_city_district`')	

			#ПРИВЯЗКА ОБЪЕКТА АРЕНДЫ К СТАНЦИЯМ МЕТРО
			# rental_objects_metro_stations
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_metro_stations (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																			 rental_object_id INT NOT NULL,
																			 metro_station_id INT NOT NULL,
																 			  FOREIGN KEY (rental_object_id)
																			  	REFERENCES rental_objects(id)
																				ON DELETE CASCADE,
																 			  FOREIGN KEY (metro_station_id)
																 				REFERENCES metro_stations(id)
																 			   ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_metro_stations`')








			# bathroom_types - типы ванной
			cursor.execute("""CREATE TABLE IF NOT EXISTS bathroom_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 type VARCHAR(100) UNIQUE
																		 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `bathroom_types`')

			# wash_place_type - типы места для мытья
			cursor.execute("""CREATE TABLE IF NOT EXISTS wash_place_type (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		  type VARCHAR(100) UNIQUE
																		  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `wash_place_type`')

			# ro_object_data - общие данные об объекте
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_object_data (rental_object_id INT PRIMARY KEY NOT NULL,
																	 bathroom_type_id INT,
																	 wash_place_type_id INT,
																	 area FLOAT, 
																	 ceilings_height FLOAT,
																	 win_number INT,
																	 balcony INT DEFAULT 0,
																	 air_conditioner BOOL DEFAULT 0,
																	 wi_fi BOOL DEFAULT 0,
																	 furniture BOOL DEFAULT 0,
																	 FOREIGN KEY(rental_object_id)
																			REFERENCES rental_objects(id)
																			ON DELETE CASCADE,
																	 FOREIGN KEY(bathroom_type_id)
																			REFERENCES bathroom_types(id),
																	 FOREIGN KEY(wash_place_type_id)
																			REFERENCES wash_place_type(id)
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_object_data`')

			# ro_object_data_window_overlooks
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_object_data_window_overlooks (rental_object_id INT PRIMARY KEY NOT NULL,
																					  street BOOL DEFAULT 0,
																					  yard BOOL DEFAULT 0,
																				  	  FOREIGN KEY(rental_object_id)
																			  			  REFERENCES ro_object_data(rental_object_id)
																			  			  ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_object_data_window_overlooks`')

			# ro_object_data_window_frame_types
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_object_data_window_frame_types (rental_object_id INT PRIMARY KEY NOT NULL,
																					    wood BOOL DEFAULT 0,
																					    plastic BOOL DEFAULT 0,
																				  	  	FOREIGN KEY(rental_object_id)
																			  			  REFERENCES ro_object_data(rental_object_id)
																			  			  ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_object_data_window_frame_types`')

			# ro_object_data_cooking_range_types
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_object_data_cooking_range_types (rental_object_id INT PRIMARY KEY NOT NULL,
																					     electric BOOL DEFAULT 0,
																					     gas BOOL DEFAULT 0,
																				  	  	 FOREIGN KEY(rental_object_id)
																			  			    REFERENCES ro_object_data(rental_object_id)
																			  			    ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_object_data_cooking_range_types`')

			
			# building_types - типы домов
			cursor.execute("""CREATE TABLE IF NOT EXISTS building_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 type VARCHAR(100) UNIQUE
																		 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `building_types`')

			# ro_building - данные о доме
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_building (rental_object_id INT PRIMARY KEY NOT NULL,
																	  building_type_id INT,
																	  floors_number INT,
																	  garbage_disposal BOOL DEFAULT 0,
																	  intercom BOOL DEFAULT 0,
																	  concierge BOOL DEFAULT 0,
																	  building_year VARCHAR(10) DEFAULT 0,
																	  FOREIGN KEY(rental_object_id)
																		 REFERENCES rental_objects(id)
																		 ON DELETE CASCADE,
																	  FOREIGN KEY(building_type_id)
																		 REFERENCES building_types(id)
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_building`')


			# ro_building_elevators
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_building_elevators (rental_object_id INT PRIMARY KEY NOT NULL,
																				passenger BOOL DEFAULT 0,
																				freight BOOL DEFAULT 0,
																				FOREIGN KEY(rental_object_id)
																			  		REFERENCES ro_building(rental_object_id)
																			  		ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_building_elevators`')






			# ro_location
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_location (rental_object_id INT PRIMARY KEY NOT NULL,
																	  coords VARCHAR(100),
																	  country VARCHAR(100),
																	  region VARCHAR(100),
																	  city VARCHAR(100),
																	  district VARCHAR(100),
																	  street VARCHAR(100),
																	  building_number VARCHAR(100),
																	  block_number VARCHAR(100),
																	  appt VARCHAR(100),
																	  entrance_number VARCHAR(100),
																	  floor INT,
																	  location_comment VARCHAR(255),
																	  FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_location`')


			# ro_appliances
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_appliances (rental_object_id INT PRIMARY KEY NOT NULL,
																		fridge BOOL DEFAULT 0,
																		dishwasher BOOL DEFAULT 0,
																		washer BOOL DEFAULT 0,
																		television BOOL DEFAULT 0,
																		vacuum BOOL DEFAULT 0,
																		teapot BOOL DEFAULT 0,
																		iron BOOL DEFAULT 0,
																		microwave BOOL DEFAULT 0,
																	  	FOREIGN KEY(rental_object_id)
																			REFERENCES rental_objects(id)
																			ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_appliances`')




			# ro_things
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_things (	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		rental_object_id INT,
																		thing_number INT,
																		thing_name VARCHAR(255), 
																		amount INT,
																		cost FLOAT,
															  			FOREIGN KEY(rental_object_id)
																			REFERENCES rental_objects(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_things`')



			# ro_room
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_room (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																  rental_object_id INT,
																  INDEX rental_object_id_idx (rental_object_id),
																  total_area FLOAT,
																  rooms_number INT,
															  	  FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_room`')

			# ro_flat
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_flat (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																  rental_object_id INT,
																  INDEX rental_object_id_idx (rental_object_id),
															  		FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_flat`')

			# ro_house
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_house (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																  rental_object_id INT,
																  INDEX rental_object_id_idx (rental_object_id),
															  		FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_house`')


class RentalAgreementDD:
	"""Определение данных для таблиц связанных с договором аренды"""
	def create_all_rental_agreement_tables(self):
		with self.context_manager(self.config) as cursor:

			# rental_agreements - договоры аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_agreements (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		   agreement_number VARCHAR(50) DEFAULT '',
																		   agent_id INT,
																		   landlord_id INT,
																		   tenant_id INT,
																		   rental_object_id INT
															 	  		   ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_agreements`')


			# ra_general_conditions - условия аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_general_conditions (rental_agreement_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	 rental_rate INT DEFAULT 0,
																	 prepayment INT DEFAULT 0,
																	 deposit INT DEFAULT 0,
																	 late_fee FLOAT DEFAULT 3,
																	 start_of_term DATE DEFAULT '0000-00-00',
																	 end_of_term DATE DEFAULT '0000-00-00',
																	 payment_day INT DEFAULT 0,
															  		 FOREIGN KEY (rental_agreement_id )
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE
															 	  	  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ra_general_conditions`')

			



class DataDefinition(Database, UserDD, RentalObjectDD, RentalAgreementDD):
	def __init__(self, config, context_manager):
		super().__init__(config, context_manager)

	def drop_all_tables(self):
		"""Удаляет все таблицы БД"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SHOW TABLES""")
			tables = [table[0] for table in cursor.fetchall()]

			cursor.execute("""SET FOREIGN_KEY_CHECKS = %s""", (0,))

			cursor.execute("""SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`') # конкотинируем строку запроса и имена таблиц
							  FROM information_schema.tables
							  WHERE table_schema = 'rent_manager_db'""")

			delete_table_queries = [i[0] for i in cursor.fetchall()] # сгенерированные запросы для удаления всех таблиц

			for delete_table_query in delete_table_queries:
				print(delete_table_query)
				cursor.execute(delete_table_query)

			cursor.execute("""SET FOREIGN_KEY_CHECKS = %s""", (1,))

	def reload_all_tables(self):
		"""Удаляет таблицы, затем создает их"""
		print('Успешно выполнены следующие SQL запросы:\n')
		print('___УДАЛЕНИЕ ТАБЛИЦ___')
		self.drop_all_tables()
		print('\n___СОЗДАНИЕ ТАБЛИЦ___')
		self.create_all_user_tables()
		self.create_all_rental_object_tables()
		self.create_all_rental_agreement_tables()



	def show_tables(self):
		"""Выводит список всех таблиц"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SHOW TABLES""")
			print([table[0] for table in cursor.fetchall()])


##################################################   DATA MANIPULATION   #####################################################

class UserDM:
	def add_user_type(self, type_):
		"""Добавление типа пользователей"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO user_types(type) VALUES (%s)""", (type_,))


	def create_user(self, user_type, name, phone, email):
		"""Добавление пользователя"""
		# проверяем верно ли введен тип пользователя
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT type FROM user_types""")
			exist_user_types = [i[0] for i in cursor.fetchall()]
			if user_type not in exist_user_types:
				raise ValueError('Такого типа пользователя не существует')

			# получаем id типа пользователя
			cursor.execute("""SELECT id FROM user_types WHERE type=%s""", (user_type,))
			user_type_id = cursor.fetchall()[0][0] 

			# создаем запись в таблице users
			cursor.execute("""INSERT INTO users(type_id, name, phone, email)
							  VALUES(%s, %s, %s, %s)""", 
							  (user_type_id, name, phone, email))

			# получаем последний id таблицы users
			cursor.execute("""SELECT id FROM users WHERE id=LAST_INSERT_ID()""") 
			user_id = cursor.fetchall()[0][0] 

			# создание записей в таблице в зависимости от типа пользователя
			if user_type == 'администратор':
				cursor.execute("""INSERT INTO users_admins(user_id) VALUES(%s)""", (user_id,))
			elif user_type == 'агент':
				cursor.execute("""INSERT INTO users_agents(user_id) VALUES(%s)""", (user_id,))
			elif user_type == 'наймодатель':
				cursor.execute("""INSERT INTO users_landlords(user_id) VALUES(%s)""", (user_id,))
			elif user_type == 'наниматель':
				cursor.execute("""INSERT INTO users_tenants(user_id) VALUES(%s)""", (user_id,))

			# привязка к паспортным и регестриционным данным
			cursor.execute("""INSERT INTO users_passport(user_id) VALUES(%s)""", (user_id,))
			cursor.execute("""INSERT INTO users_register(user_id) VALUES(%s)""", (user_id,)) 


	# GET ATTRIBUTES [USER]: type_id, name, phone, email
	def get_user_type_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT type_id FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_user_name(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT name FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_user_phone(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT phone FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_user_email(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT email FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	# GET ATTRIBUTES [lANDLORD]: inn
	def get_landlord_inn(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT inn FROM users_landlords WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]






	# GET ATTRIBUTES [PASSPORT]: 
	# first_name, patronymic, last_name, serie, pass_number, authority, department_code, date_of_issue, date_of_birth, place_of_birth, registration
	def get_passport_first_name(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT first_name FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_patronymic(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT patronymic FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_last_name(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT last_name FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_serie(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT serie FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_pass_number(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT pass_number FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_authority(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT authority FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_department_code(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT department_code FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_date_of_issue(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT date_of_issue FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_date_of_birth(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT date_of_birth FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_place_of_birth(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT place_of_birth FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_passport_registration(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT registration FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	# GET ATTRIBUTES [REGISTER]: register_id, login, password
	def get_register_login(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT login FROM users_register WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_register_password(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT password FROM users_register WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]








	# SET ATTRIBUTES [USER]: name, phone, email
	def set_user_name(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users SET name=%s WHERE id=%s""", (value, user_id,))

	def set_user_phone(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users SET phone=%s WHERE id=%s""", (value, user_id,))

	def set_user_email(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users SET email=%s WHERE id=%s""", (value, user_id,))

	# SET ATTRIBUTES [LANDLORD]: inn
	def set_landlord_inn(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_landlords SET inn=%s WHERE user_id=%s""", (value, user_id,))

	# SET ATTRIBUTES [PASSPORT]:
	# first_name, patronymic, last_name, serie, pass_number, authority, department_code, date_of_issue, date_of_birth, place_of_birth, registration
	def set_passport_first_name(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET first_name=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_patronymic(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET patronymic=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_last_name(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET last_name=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_serie(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET serie=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_pass_number(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET pass_number=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_authority(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET authority=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_department_code(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET department_code=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_date_of_issue(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET date_of_issue=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_date_of_birth(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET date_of_birth=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_place_of_birth(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET place_of_birth=%s WHERE user_id=%s""", (value, user_id,))

	def set_passport_registration(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport SET registration=%s WHERE user_id=%s""", (value, user_id,))
	

	# SET ATTRIBUTES [REGISTER]: login, password
	def set_register_login(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_register SET login=%s WHERE user_id=%s""", (value, user_id,))

	def set_register_password(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_register SET password=%s WHERE user_id=%s""", (value, user_id,))



class RentalObgectDM:

	def add_rental_object_type(self, type_):
		"""Добавление типа пользователей"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO rental_object_types(type) VALUES (%s)""", (type_,))

	def add_bathroom_type(self, type_):
		"""Добавление типа санузла"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO bathroom_types(type) VALUES (%s)""", (type_,))

	def add_wash_place_type(self, type_):
		"""Добавление типа места для мытья"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO wash_place_type(type) VALUES (%s)""", (type_,))

	def add_building_type(self, type_):
		"""Добавление типа здания"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO building_types(type) VALUES (%s)""", (type_,))

	def add_country(self, country):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO countries(country) VALUES(%s)""", (country,))

	def add_city(self, country_id, city):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO cities(country_id, city) VALUES(%s, %s)""", (country_id, city))

	def add_district(self, city_id, district):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO districts(city_id, district) VALUES(%s, %s)""", (city_id, district))

	def add_metro_station(self, city_id, line_number, line_name, color, station, is_valid):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO metro_stations(city_id, line_number, line_name, color, station, is_valid) 
				VALUES(%s, %s, %s, %s, %s, %s)""", (city_id, line_number, line_name, color, station, is_valid))
	

	@staticmethod	
	def transform_csv_file_to_python_list_of_lists(csv_file):
		with open(csv_file, encoding='utf8') as file:  
		    loaded_data = csv.reader(file)
		    return_data = [] # [['city', 'line_number', 'line_name', 'color', 'station', 'is_closed'],[],[]]
		    for i in loaded_data:
		    	if i != [';;;;;']: # удаляем строки без данных
		    		i = i[0].split(';') # создаем список из строк по разделителю ';''
		    		return_data.append(i) # добавляем списки с данными в списко metro
		    del return_data[0] # удаляем шапку таблицы
		    for i in return_data: 
		    	i = [j.replace('\xa0', '') for j in i] # удаляем лишние неразрывные пробелы \xa0
		    return return_data

	def create_rental_object(self, rental_object_type, landlord_id): # landlord_id = user_id
		"""Добавление объекта аренды"""
		with self.context_manager(self.config) as cursor:
			# проверяем верно ли введен тип объекта аренды
			cursor.execute("""SELECT type FROM rental_object_types""")
			exist_rental_object_types = [i[0] for i in cursor.fetchall()]
			if rental_object_type not in exist_rental_object_types:
				raise ValueError('Такого объекта аренды не существует')

			# получаем id типа объекта аренды
			cursor.execute("""SELECT id FROM rental_object_types WHERE type=%s""", (rental_object_type,))
			rental_object_type_id = cursor.fetchall()[0][0]
			
			# rental_objects (базовая таблица)
			cursor.execute("""INSERT INTO rental_objects(type_id, landlord_id) VALUES(%s, %s)""", (rental_object_type_id, landlord_id))

			# получаем последний id таблицы rental_objects
			cursor.execute("""SELECT id FROM rental_objects WHERE id=LAST_INSERT_ID()""") 
			rental_object_id = cursor.fetchall()[0][0] 

			# создание записей в таблице в зависимости от типа объекта аренды
			if rental_object_type == 'комната':
				cursor.execute("""INSERT INTO ro_room(rental_object_id) VALUES(%s)""", (rental_object_id,))
			elif rental_object_type == 'квартира':
				cursor.execute("""INSERT INTO ro_flat(rental_object_id) VALUES(%s)""", (rental_object_id,))
			elif rental_object_type == 'дом':
				cursor.execute("""INSERT INTO ro_house(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_general (общая информация)
			cursor.execute("""INSERT INTO ro_general(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_appliances (бытовая техника)
			cursor.execute("""INSERT INTO ro_appliances(rental_object_id) VALUES(%s)""", (rental_object_id,))
					
			# ro_building (здание)
			cursor.execute("""INSERT INTO ro_building(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data (объект аренды)
			cursor.execute("""INSERT INTO ro_object_data(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data (объект аренды)
			cursor.execute("""INSERT INTO ro_location(rental_object_id) VALUES(%s)""", (rental_object_id,))

	

			# ro_building_elevators (лифты)
			cursor.execute("""INSERT INTO ro_building_elevators(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data_cooking_range_types (тип плиты)
			cursor.execute("""INSERT INTO ro_object_data_cooking_range_types(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data_window_frame_types (окна)
			cursor.execute("""INSERT INTO ro_object_data_window_frame_types(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data_window_overlooks (вид из окна)
			cursor.execute("""INSERT INTO ro_object_data_window_overlooks(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_country_city_district (страна-город-район)
			cursor.execute("""INSERT INTO ro_country_city_district(rental_object_id) VALUES(%s)""", (rental_object_id,))








	# GET ATTRIBUTES [RENTAL OBJECT]: type_id, tenant_id, agent_id, rental_agreement_id
	def get_rental_object_type_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT type_id FROM rental_objects WHERE id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_rental_object_tenant_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT tenant_id FROM rental_objects WHERE id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_rental_object_agent_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT agent_id FROM rental_objects WHERE id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]


	def get_rental_object_rental_agreement_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id FROM rental_objects WHERE id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]





	# GET ATTRIBUTES [ro_general]: ['name', 'cadastral_number', 'title_deed']
	def get_ro_general_name(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT name FROM ro_general WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_general_cadastral_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT cadastral_number FROM ro_general WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_general_title_deed(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT title_deed FROM ro_general WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]


	# GET ATTRIBUTES [ro_things]: ['things']
	def get_things(self, rental_object_id):
		"""Возвращает данные о вещах в объекте"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT thing_number, thing_name, amount, cost
							  FROM ro_things
							  WHERE rental_object_id=%s""", (rental_object_id,))
			things = []
			for thing in cursor.fetchall():
				things.append([i for i in thing])
			return things


	# GET ATTRIBUTES [ro_maintenance_costs]: ['maintenance_costs']
	def get_maintenance_costs(self, rental_object_id):
		"""Возвращает данные о расходах на содержание объекта"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT cost_number, cost_name, user_type_id
							  FROM ro_maintenance_costs
							  WHERE rental_object_id=%s""", (rental_object_id,))
			maintenance_costs = []
			for cost in cursor.fetchall():
				maintenance_costs.append([i for i in cost])
			return maintenance_costs







	# GET ATTRIBUTES [ro_things]: ['things']
	def get_rental_object_things(self, rental_object_id):
		"""Возвращает данные о вещах в объекте"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT thing_number, thing_name, amount, cost
							  FROM ro_things
							  WHERE rental_object_id=%s""", (rental_object_id,))
			things = []
			for thing in cursor.fetchall():
				things.append([i for i in thing])
			return things




	# GET ATTRIBUTES [ROOM]: total_area, rooms_number 
	def get_ro_room_total_area(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT total_area FROM ro_room WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_room_rooms_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rooms_number FROM ro_room WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]




	# GET ATTRIBUTES [OBJECT DATA]: bathroom_type_id, wash_place_type_id, area, ceilings_height, win_number, balcony, air_conditioner
	# GET ATTRIBUTES [OBJECT DATA]: wi_fi, furniture, window_overlook, window_frame_type, cooking_range_type
	def get_ro_object_data_bathroom_type_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT bathroom_type_id FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_wash_place_type_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT wash_place_type_id FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_area(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT area FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_ceilings_height(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ceilings_height FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_win_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT win_number FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_balcony(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT balcony FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_air_conditioner(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT air_conditioner FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_wi_fi(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT wi_fi FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_furniture(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT furniture FROM ro_object_data WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_object_data_window_overlook(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT street, yard FROM ro_object_data_window_overlooks WHERE rental_object_id=%s""", (rental_object_id,))
			data = cursor.fetchall()[0]
			res = {}
			res['street'] = data[0]
			res['yard'] = data[1]
			return res

	def get_ro_object_data_window_frame_type(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT wood, plastic FROM ro_object_data_window_frame_types WHERE rental_object_id=%s""", (rental_object_id,))
			data = cursor.fetchall()[0]
			res = {}
			res['wood'] = data[0]
			res['plastic'] = data[1]
			return res

	def get_ro_object_data_cooking_range_type(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT electric, gas FROM ro_object_data_cooking_range_types WHERE rental_object_id=%s""", (rental_object_id,))
			data = cursor.fetchall()[0]
			res = {}
			res['electric'] = data[0]
			res['gas'] = data[1]
			return res


	# GET ATTRIBUTES [BUILDING]: building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year, elevator
	def get_ro_building_building_type_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT building_type_id FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_building_floors_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT floors_number FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_building_garbage_disposal(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT garbage_disposal FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_building_intercom(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT intercom FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_building_concierge(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT concierge FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_building_building_year(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT building_year FROM ro_building WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_building_elevator(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT passenger, freight 
						      FROM ro_building_elevators 
						      WHERE rental_object_id=%s""", (rental_object_id,))
			data = cursor.fetchall()[0]
			res = {}
			res['passenger'] = data[0]
			res['freight'] = data[1]
			return res


	# GET ATTRIBUTES [LOCATION]: coords, country, region, city, district, street, building_number, block_number,
	#                            appt, entrance_number, floor, location_comment, nearest_metro_stations 
	def get_ro_location_coords(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT coords FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_country(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT country FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_region(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT region FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_city(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT city FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_district(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT district FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_street(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT street FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_building_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT building_number FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_block_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT block_number FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_appt(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT appt FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_entrance_number(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT entrance_number FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_floor(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT floor FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_location_comment(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT location_comment FROM ro_location WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]

	def get_ro_location_nearest_metro_stations(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ms.station
				      		  FROM rental_objects_metro_stations AS roms
				      		  JOIN metro_stations AS ms
				      		  ON ms.id = roms.metro_station_id
				     		  WHERE rental_object_id=%s""", (rental_object_id,))

			return [i[0] for i in cursor.fetchall()]




	# GET ATTRIBUTES [ro_appliances]: ['fridge', 'dishwasher', 'washer', 'television', 'vacuum', 'teapot', 'iron', 'microwave', 'nearest_metro_stations']
	def get_ro_appliances_fridge(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT fridge FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_dishwasher(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT dishwasher FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_washer(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT washer FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_television(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT television FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_vacuum(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT vacuum FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_teapot(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT teapot FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_iron(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT iron FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])

	def get_ro_appliances_microwave(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT microwave FROM ro_appliances WHERE rental_object_id=%s""", (rental_object_id,))
			return bool(cursor.fetchall()[0][0])



	def get_rental_object_type_by_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rot.type
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id = rot.id
							  WHERE ro.id=%s""", (rental_object_id,))
			return cursor.fetchall()[0][0]






	# SET ATTRIBUTES [rental_objects]: tenant_id, agent_id, rental_agreement_id

	# def set_rental_object_tenant_id(self, rental_object_id, value):
	# 	with self.context_manager(self.config) as cursor:
	# 		cursor.execute("""UPDATE general_objects SET tenant_id=%s WHERE rental_object_id=%s""", (value, rental_object_id,))



	# SET ATTRIBUTES [ro_general]: ['name', 'cadastral_number', 'title_deed']
	def set_ro_general_name(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general SET name=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_general_cadastral_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general SET cadastral_number=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_general_title_deed(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general SET title_deed=%s WHERE rental_object_id=%s""", (value, rental_object_id,))


	# SET ATTRIBUTES [ro_things]: ['things']
	def set_things(self, rental_object_id, things:list):
		with self.context_manager(self.config) as cursor:
			# удаляем все данные о вещах для этого объекта аренды
			cursor.execute("""DELETE FROM ro_things WHERE rental_object_id=%s""", (rental_object_id,))
			# загружаем новые данные
			for i in things:
				cursor.execute("""INSERT INTO ro_things(rental_object_id, thing_number, thing_name, amount, cost) 
							      VALUES (%s, %s, %s, %s, %s)""", 
							      (rental_object_id, i[0], i[1], i[2], i[3]))

	# SET ATTRIBUTES [ro_maintenance_costs]: ['maintenance_costs']
	def set_maintenance_costs(self, rental_object_id, maintenance_costs:list):

		with self.context_manager(self.config) as cursor:
			for i in maintenance_costs:
				cursor.execute("""INSERT INTO ro_maintenance_costs(rental_object_id, cost_number, cost_name, user_type_id) 
							      VALUES (%s, %s, %s, %s)""", 
							      (rental_object_id, i[0], i[1], i[2]))



	# SET ATTRIBUTES [ROOM]: total_area, rooms_number 
	def set_ro_room_total_area(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_room SET total_area=%s WHERE id=%s""", (value, rental_object_id,))

	def set_ro_room_rooms_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_room SET rooms_number=%s WHERE id=%s""", (value, rental_object_id,))


	# SET ATTRIBUTES [OBJECT DATA]: bathroom_type_id, wash_place_type_id, area, ceilings_height, win_number, balcony, air_conditioner
	# SET ATTRIBUTES [OBJECT DATA]: wi_fi, furniture, window_overlook, window_frame_type, cooking_range_type

	def set_ro_object_data_bathroom_type_id(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET bathroom_type_id=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_wash_place_type_id(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET wash_place_type_id=%s WHERE rental_object_id=%s""", (value, rental_object_id,))


	def set_ro_object_data_area(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET area=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_ceilings_height(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET ceilings_height=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_win_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET win_number=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_balcony(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET balcony=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_air_conditioner(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET air_conditioner=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_wi_fi(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET wi_fi=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_object_data_furniture(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data SET furniture=%s WHERE rental_object_id=%s""", (value, rental_object_id,))




	def set_ro_object_data_data_window_overlook(self, rental_object_id, value:dict):
		with self.context_manager(self.config) as cursor:
			for k,v in value.items():
				if k == 'street':
					cursor.execute("""UPDATE ro_object_data_window_overlooks 
							  	      SET street=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))
				elif k == 'yard':
					cursor.execute("""UPDATE ro_object_data_window_overlooks 
							  	      SET yard=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))


	def set_ro_object_data_window_frame_type(self, rental_object_id, value:dict):
		with self.context_manager(self.config) as cursor:
			for k,v in value.items():
				if k == 'wood':
					cursor.execute("""UPDATE ro_object_data_window_frame_types
							  	      SET wood=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))
				elif k == 'plastic':
					cursor.execute("""UPDATE ro_object_data_window_frame_types 
							  	      SET plastic=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))


	def set_ro_object_data_cooking_range_type(self, rental_object_id, value:dict):
		with self.context_manager(self.config) as cursor:
			for k,v in value.items():
				if k == 'electric':
					cursor.execute("""UPDATE ro_object_data_cooking_range_types
							  	      SET electric=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))
				elif k == 'gas':
					cursor.execute("""UPDATE ro_object_data_cooking_range_types 
							  	      SET gas=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))





	# SET ATTRIBUTES [BUILDING]: building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year, elevator
	def set_ro_building_building_type_id(self, rental_object_id, value:int):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET building_type_id=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_floors_number(self, rental_object_id, value:int):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET floors_number=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_garbage_disposal(self, rental_object_id, value:bool):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET garbage_disposal=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_intercom(self, rental_object_id, value:bool):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET intercom=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_concierge(self, rental_object_id, value:bool):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET concierge=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_building_year(self, rental_object_id, value:str):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET building_year=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_building_elevator(self, rental_object_id, value:dict):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building SET X=%s WHERE rental_object_id=%s""", (value, rental_object_id,))


	def set_ro_building_elevator(self, rental_object_id, value:dict):
		with self.context_manager(self.config) as cursor:
			for k,v in value.items():
				if k == 'passenger':
					cursor.execute("""UPDATE ro_building_elevators
							  	      SET passenger=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))
				elif k == 'freight':
					cursor.execute("""UPDATE ro_building_elevators
							  	      SET freight=%s
							 	      WHERE rental_object_id=%s""", (v, rental_object_id,))


	# SET ATTRIBUTES [LOCATION]: coords, country, region, city, district, street, building_number, block_number,
	#                            appt, entrance_number, floor, location_comment, nearest_metro_stations 


	def set_ro_location_coords(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET coords=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_country(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET country=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_region(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET region=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_city(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET city=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_district(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET district=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_street(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET street=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_building_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET building_number=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_block_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET block_number=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_appt(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET appt=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_entrance_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET entrance_number=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_floor(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET floor=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_location_location_comment(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location SET location_comment=%s WHERE rental_object_id=%s""", (value, rental_object_id))


	def get_ro_location_nearest_metro_stations(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ms.station
				      		  FROM rental_objects_metro_stations AS roms
				      		  JOIN metro_stations AS ms
				      		  ON ms.id = roms.metro_station_id
				     		  WHERE rental_object_id=%s""", (rental_object_id,))

			return [i[0] for i in cursor.fetchall()]


	def set_ro_location_nearest_metro_stations(self, rental_object_id, value:list): # value - список id станций метро
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM rental_objects_metro_stations WHERE rental_object_id=%s""", (rental_object_id,))
			for id_ in value:
				cursor.execute("""INSERT INTO rental_objects_metro_stations(rental_object_id, metro_station_id) 
							      VALUES (%s, %s)""", (rental_object_id, id_))




	# SET ATTRIBUTES [ro_appliances]: ['fridge', 'dishwasher', 'washer', 'television', 'vacuum', 'teapot', 'iron', 'microwave']
	def set_ro_appliances_fridge(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET fridge=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_dishwasher(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET dishwasher=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_washer(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET washer=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_television(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET television=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_vacuum(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET vacuum=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_teapot(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET teapot=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_iron(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET iron=%s WHERE rental_object_id=%s""", (value, rental_object_id))

	def set_ro_appliances_microwave(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances SET microwave=%s WHERE rental_object_id=%s""", (value, rental_object_id))




class RentalAgreementDM:
	"""Создание договора аренды"""
	def create_rental_agreement(self, landlord_user_id, tenant_user_id, rental_object_id, agent_user_id=None):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO rental_agreements(agent_id, landlord_id, tenant_id, rental_object_id)
						      VALUES (%s, %s, %s, %s)""", (agent_user_id, landlord_user_id, tenant_user_id, rental_object_id))
			
			cursor.execute("""SELECT id FROM rental_agreements WHERE id=LAST_INSERT_ID()""") 
			rental_agreement_id = cursor.fetchall()[0][0] 

			cursor.execute("""INSERT INTO ra_general_conditions(rental_agreement_id)
							  VALUES(%s) """, (rental_agreement_id,))



	# GET ATTRIBUTES [rental_agreements]: ['agent_id', 'landlord_id', 'tenant_id', 'rental_object_id', 'agreement_number', ]
	def get_rental_agreements_agent_id(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT agent_id FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_rental_agreements_landlord_id(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT landlord_id FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_rental_agreements_tenant_id(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT tenant_id FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_rental_agreements_rental_object_id(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_rental_agreements_agreement_number(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT agreement_number FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]		


	# GET ATTRIBUTES [ra_general_conditions]: ['rental_rate', 'prepayment', 'deposit', 'late_fee', 'start_of_term', 'end_of_term', 'ayment_day']
	def get_ra_general_conditions_rental_rate(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_rate FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_ra_general_conditions_prepayment(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT prepayment FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_ra_general_conditions_deposit(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT deposit FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_ra_general_conditions_late_fee(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT late_fee FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_ra_general_conditions_start_of_term(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT start_of_term FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return str(cursor.fetchall()[0][0])

	def get_ra_general_conditions_end_of_term(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT end_of_term FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]

	def get_ra_general_conditions_payment_day(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT payment_day FROM ra_general_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0][0]




	# SET ATTRIBUTES [rental_agreements]: ['agreement_number']
	def set_rental_agreements_agreement_number(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE rental_agreements SET agreement_number=%s WHERE id=%s""", (value, rental_agreement_id))

	# SET ATTRIBUTES [ra_general_conditions]: ['rental_rate', 'prepayment', 'deposit', 'late_fee', 'start_of_term', 'end_of_term', 'payment_day']
	def set_ra_general_conditions_rental_rate(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET rental_rate=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_prepayment(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET prepayment=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_deposit(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET deposit=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_late_fee(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET late_fee=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_start_of_term(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET start_of_term=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_end_of_term(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET end_of_term=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))

	def set_ra_general_conditions_payment_day(self, rental_agreement_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ra_general_conditions SET payment_day=%s WHERE rental_agreement_id=%s""", (value, rental_agreement_id))		



class DataManipulation(Database, UserDM, RentalObgectDM, RentalAgreementDM):
	def __init__(self, config, context_manager):
		super().__init__(config, context_manager)

	# добавление данных 'по умолчанию'
	def add_default_data(self):
		user_types = ['наймодатель', 'наниматель', 'администратор', 'агент']
		for type_ in user_types:
			self.add_user_type(type_)

		rental_object_types = ['комната', 'квартира', 'дом']
		for type_ in rental_object_types:
			self.add_rental_object_type(type_)

		bathroom_types = ['совмещенный', 'раздельный']
		for type_ in bathroom_types:
			self.add_bathroom_type(type_)

		wash_place_type = ['ванна', 'душевая кабина']
		for type_ in wash_place_type:
			self.add_wash_place_type(type_)

		building_type = ['кирпичный', 'панельный'] 
		for type_ in building_type:
			self.add_building_type(type_)

		countries = ['Российская Федерация']
		for country in countries:
			self.add_country(country)

		city_data = [(1,'Санкт-Петербург'), (1, 'Москва')]
		for country_id, city in city_data:
			self.add_city(country_id, city)

	def add_districts_data(self):
		with self.context_manager(self.config) as cursor:	
			district_data = self.transform_csv_file_to_python_list_of_lists('database/additional_data/csv_files/districts.csv')
			for city, district in district_data:
				cursor.execute("""SELECT id FROM cities WHERE city=%s""", (city,))
				city_id = cursor.fetchall()[0][0]
				self.add_district(city_id, district)


	def add_metro_station_data(self):
		with self.context_manager(self.config) as cursor:	
			metro_station_data = self.transform_csv_file_to_python_list_of_lists('database/additional_data/csv_files/metro_stations.csv')
			for city, line_number, line_name, color, station, is_valid in metro_station_data:
				cursor.execute("""SELECT id FROM cities WHERE city=%s""", (city,))
				city_id = cursor.fetchall()[0][0]
				self.add_metro_station(city_id, line_number, line_name, color, station, is_valid)
	
			

	def add_test_data(self):
		with self.context_manager(self.config) as cursor:
			self.create_user('наймодатель', 'Никита', '+79218850028', 'actan-spb@mail.ru')
			self.create_user('наниматель', 'Алина', '+79992347654', 'al@al.ru') # работает только если одна запись в users_tenants
			self.create_user('администратор', 'Игорь', '911', 'igor@mail.ru') # работает только если одна запись в users_admins
			self.create_user('агент', 'Светлана', '+79218763322', 'sveta@net.ru') # работает только если одна запись в users_agents

			self.create_rental_object('комната', 1)
			self.create_rental_object('квартира', 1)
			self.create_rental_object('дом', 1)

			self.create_rental_agreement(1, 1, 1, 1)

			


if __name__ == '__main__':
	...