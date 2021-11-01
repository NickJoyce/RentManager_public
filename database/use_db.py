import json

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
																name VARCHAR(100) DEFAULT '',
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
																		 type_id INT,
																		 name VARCHAR(255) DEFAULT '',
																		 cadastral_number VARCHAR(255) DEFAULT '',
																		 title_deed VARCHAR(255) DEFAULT '', 
																		 is_rented BOOL DEFAULT 0,
																		 current_rental_agreement_id INT,
																		 FOREIGN KEY(type_id)
																			REFERENCES rental_object_types(id)
																		) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_objects`')

			# cities- города
			cursor.execute("""CREATE TABLE IF NOT EXISTS cities (id INT PRIMARY KEY NOT NULL,
																 city VARCHAR(100)
																 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `cities`')		

			# cities_districts - города и районы
			cursor.execute("""CREATE TABLE IF NOT EXISTS cities_districts (id INT PRIMARY KEY NOT NULL,
																 		   city_id INT,
																 		   district VARCHAR(255),
																 		   FOREIGN KEY(city_id)
																			   	REFERENCES cities(id)
																				ON DELETE CASCADE
																 			) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `cities_districts`')	


			# ro_cities_districts - город и район объекта аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_cities_districts (rental_object_id INT PRIMARY KEY NOT NULL,
																			  cities_districts_id INT,
																 			  FOREIGN KEY (rental_object_id)
																			  	REFERENCES rental_objects(id)
																				ON DELETE CASCADE,
																 			  FOREIGN KEY (cities_districts_id)
																 				REFERENCES cities_districts(id)
																 			   ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_cities_districts`')	




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






			# metro_stations
			cursor.execute("""CREATE TABLE IF NOT EXISTS metro_stations (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																         city VARCHAR(100) NOT NULL,
																		 line_number VARCHAR(100),
																		 line_name VARCHAR(100),
																		 color VARCHAR(100),
																		 station VARCHAR(100) NOT NULL,
																		 is_valid BOOL DEFAULT 1,
																		 UNIQUE (city, line_number, station)
																		 ) ENGINE = InnoDB""" )
																			  									
			print('CREATE TABLE IF NOT EXISTS `metro_stations`')



			# rental_object_metro_stations - связь объекта аренды со станциями метро
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_objects_metro_stations (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																			rental_object_id INT NOT NULL,
																			metro_station_id INT NOT NULL,
																			FOREIGN KEY(rental_object_id)
																				REFERENCES rental_objects(id),
																			FOREIGN KEY(metro_station_id)
																				REFERENCES metro_stations(id),
																			UNIQUE (rental_object_id, metro_station_id)
																			) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_metro_stations`')



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
																		thing VARCHAR(255), 
																		amount INT,
																		cost FLOAT,
															  			FOREIGN KEY(rental_object_id)
																			REFERENCES rental_objects(id)
																			ON DELETE CASCADE
																		UNIQUE (rental_object_id, thing)
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
																		   agreement_number VARCHAR(50),
																		   agent_id INT,
																		   landlord_id INT,
																		   tenant_id INT,
																		   rental_object_id INT,
																		   conditions_id INT,
																		   additional_payments_id INT,
															  			   FOREIGN KEY(rental_object_id)
																				REFERENCES rental_objects(id)
																				ON DELETE CASCADE
															 	  		   ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_agreements`')


			# conditions - условия аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_conditions (rental_agreement_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	 rental_rate FLOAT,
																	 prepayment FLOAT,
																	 deposit FLOAT,
																	 late_fee FLOAT,
																	 start_of_term DATE,
																	 end_of_term DATE,
																	 payment_day INT,
															  		 FOREIGN KEY (rental_agreement_id )
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE
															 	  	  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ra_conditions`')


			# additional_payment_payers - плательщики 
			cursor.execute("""CREATE TABLE IF NOT EXISTS additional_payment_payers (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			        payer VARCHAR(50)
															 	 				    ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `additional_payment_payers`')


			# additional_payments
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_additional_payments (rental_agreement_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	 		  general_utilities VARCHAR(50),
																	 		  gas VARCHAR(50),
																	 		  electricity VARCHAR(50),
																	 		  overhaul VARCHAR(50),
																	 		  water VARCHAR(50),
																	 		  internet VARCHAR(50),
															  		 		  FOREIGN KEY (rental_agreement_id )
																				REFERENCES rental_agreements(id)
																				ON DELETE CASCADE
															 	  	  		  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ra_additional_payments`')



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
	def insert_user_type(self, type_):
		"""Добавление типа пользователей"""
		with self.context_manager(self.config) as cursor:
			try:
				cursor.execute("""INSERT INTO user_types(type) VALUES (%s)""", (type_,))
			except:
				raise Warning(f'Тип пользователя {type_} уже есть в БД')

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

	




	def get_user_type_by_id(self, user_id):
		"""Возвращает наименование типа пользователя по id пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ut.type
							  FROM users AS u 
							  JOIN user_types AS ut
							  ON u.type_id = ut.id
							  WHERE u.id=%s
							  """, (user_id,))
			return cursor.fetchall()[0][0]


	def get_user_data(self, user_id):
		"""Возвращает общме данные пользователя (базовый класс)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type_id, name, phone, email FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0]


	def get_passport_data(self, user_id):
		"""Возвращает паспортные данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
				                     department_code, date_of_issue, date_of_birth, place_of_birth, registration
							  FROM users_passport WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]


	def get_register_data(self, user_id):
		"""Возвращает регистрационные данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, user_id, login, password FROM users_register WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]


	def get_landlord_user_data(self, user_id):
		"""Возврает спецефические для дочернего класса 'landlord' данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, inn FROM users_landlords WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]


	def get_tenant_user_data(self, user_id):
		"""Возврает спецефические для дочернего класса 'tenant' данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_tenants WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]




	def get_admin_user_data(self, user_id):
		"""Возврает спецефические для дочернего класса 'tenant' данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_admins WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]

	def get_agent_user_data(self, user_id):
		"""Возврает спецефические для дочернего класса 'tenant' данные пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_agents WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]


	# UPDATE
	def update_user_data(self, user_id, name, phone, email):
		"""Изменяет данные в таблице users"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users SET name=%s, phone=%s, email=%s WHERE id=%s""", (name, phone, email, user_id))

	def update_landlord_user_data(self, user_id, inn):
		"""Изменяет данные в таблице users_landlords"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_landlords SET inn=%s WHERE user_id=%s""", (inn, user_id))


	def update_tenant_user_data(self, user_id):
		"""Изменяет данные в таблице users_landlords"""
		with self.context_manager(self.config) as cursor:
			...	

	def update_admin_user_data(self, user_id):
		"""Изменяет данные в таблице users_landlords"""
		with self.context_manager(self.config) as cursor:
			...	


	def update_agent_user_data(self, user_id):
		"""Изменяет данные в таблице users_landlords"""
		with self.context_manager(self.config) as cursor:
			...	

	def update_passport_data(self, user_id, first_name, patronymic, last_name, serie, pass_number, authority, department_code,
		               date_of_issue, date_of_birth, place_of_birth,  registration):
		"""Изменяет имеющиеся данные в таблице users"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport 
							  SET first_name=%s, patronymic=%s, last_name=%s, serie=%s, pass_number=%s, authority=%s, 
								  department_code=%s, date_of_issue=%s, date_of_birth=%s, place_of_birth=%s,  
								  registration=%s WHERE user_id=%s""", 
								  (first_name, patronymic, last_name, serie, pass_number, authority, department_code,
			               		   date_of_issue, date_of_birth, place_of_birth,  registration, user_id))

	def update_register_data(self, user_id, login, password):
		"""Изменяет имеющиеся данные в таблице users"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_register SET login=%s, password=%s WHERE user_id=%s""", (login, password, user_id))



class RentalObgectDM:

	def add_rental_object_type(self, type_):
		"""Добавление типа пользователей"""
		with self.context_manager(self.config) as cursor:
			try:
				cursor.execute("""INSERT INTO rental_object_types(type) VALUES (%s)""", (type_,))
			except:
				raise Warning(f'Тип пользователя {type_} уже есть в БД')

	def add_bathroom_type(self, type_):
		"""Добавление типа санузла"""
		with self.context_manager(self.config) as cursor:
			try:
				cursor.execute("""INSERT INTO bathroom_types(type) VALUES (%s)""", (type_,))
			except:
				raise Warning(f'Тип ванной комнаты {type_} уже есть в БД')

	def add_wash_place_type(self, type_):
		"""Добавление типа места для мытья"""
		with self.context_manager(self.config) as cursor:
			try:
				cursor.execute("""INSERT INTO wash_place_type(type) VALUES (%s)""", (type_,))
			except:
				raise Warning(f'Тип места для мытья {type_} уже есть в БД')

	def add_building_type(self, type_):
		"""Добавление типа здания"""
		with self.context_manager(self.config) as cursor:
			try:
				cursor.execute("""INSERT INTO building_types(type) VALUES (%s)""", (type_,))
			except:
				raise Warning(f'Тип здания {type_} уже есть в БД')


	def add_thing(self, rental_object_id, thing, amount, cost):
		"""Добавление вещи в объекте недвижимости. значение thing уникально для объекта недвижимости"""	
		with self.context_manager(self.config) as cursor:
			# проверяем уникально ли наименование вещи
			cursor.execute("""SELECT thing FROM ro_things WHERE rental_object_id=%s""", (rental_object_id,))
			if thing in [thing[0] for thing in cursor.fetchall()]:
				raise ValueError(f'Наименование {thing} уже есть в списке вещей')
			else:
				cursor.execute("""INSERT INTO ro_things(rental_object_id, thing, amount, cost) 
						      VALUES (%s, %s, %s, %s)""", (rental_object_id, thing, amount, cost))

	def add_metro_station(self, rental_object_id, metro_station_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO rental_objects_metro_stations(rental_object_id, metro_station_id) 
							  VALUES (%s, %s)""", (rental_object_id, metro_station_id))




	def create_rental_object(self, rental_object_type, name):
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
			cursor.execute("""INSERT INTO rental_objects(type_id, name) VALUES(%s, %s)""", (rental_object_type_id, name))

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


			# ro_cities_districts (город-район)
			cursor.execute("""INSERT INTO ro_cities_districts(rental_object_id) VALUES(%s)""", (rental_object_id,))


	def get_rental_object_data(self, rental_object_id):
		"""Получение данных из таблицы rental_objects"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id
							  FROM rental_objects WHERE id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]



	def get_rental_object_type_by_id(self, rental_object_id):
		"""Получение типа объекта аренды по id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rot.type 
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id=rot.id
							  WHERE ro.id = %s""", (rental_object_id,))
			return cursor.fetchall()[0][0]


	def get_room_rental_object_data(self, rental_object_id):
		"""Возвращает спецефические для дочернего класса 'Room' данные объекта аренды"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, total_area, rooms_number FROM ro_room WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	def get_flat_rental_object_data(self, rental_object_id):
		"""Возвращает спецефические для дочернего класса 'Flat' данные объекта аренды"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM ro_flat WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	def get_house_rental_object_data(self, rental_object_id):
		"""Возвращает спецефические для дочернего класса 'House' данные объекта аренды"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM ro_house WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]





	def get_location_data(self, rental_object_id):
		"""Возвращает данные локации объекта (для экземпляра класса Location)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, coords, country, region, city, district, street, 
									building_number, block_number, appt, entrance_number, floor, location_comment 
							  FROM ro_location 
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	def get_location_nearest_metro_stations_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ms.id
							  FROM rental_objects_metro_stations as roms
							  JOIN metro_stations AS ms
							  ON roms.metro_station_id = ms.id
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return [i[0] for i in cursor.fetchall()]	






	def get_object_data(self, rental_object_id):
		"""Возвращает общие данные объекта (для экземпляра класса ObjectData)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, bathroom_type_id, wash_place_type_id, area, ceilings_height, 
								     win_number, balcony, air_conditioner, wi_fi, furniture
							  FROM ro_object_data
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]



	def get_object_window_overlook_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT street, yard 
							  FROM ro_object_data_window_overlooks 
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	def get_object_window_frame_type_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT wood, plastic
							  FROM ro_object_data_window_frame_types
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]


	def get_object_cooking_range_type_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT electric, gas
							  FROM ro_object_data_cooking_range_types
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	def get_building_elevator_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT passenger, freight
							  FROM ro_building_elevators
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]









	def get_building_data(self, rental_object_id):
		"""Возвращает данные о здании (для экземпляра класса Building)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, building_type_id, floors_number, garbage_disposal, intercom, 
								     concierge, building_year
							  FROM ro_building
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]


	def get_appliances_data(self, rental_object_id):
		"""Возвращает данные о бытовой технике в объекте (для экземпляра класса Appliances)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave
							  FROM ro_appliances
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]


	def get_things_data(self, rental_object_id):
		"""Возвращает данные о вещах в объекте"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT thing, amount, cost
							  FROM ro_things
							  WHERE rental_object_id=%s""", (rental_object_id,))
			things = {}
			for thing in cursor.fetchall():
				things[thing[0]] = [thing[1], thing[2]]
			return things







	def update_rental_object_data(self, rental_object_id, name, cadastral_number, title_deed, is_rented, current_rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE rental_objects 
							  SET name=%s, cadastral_number=%s, title_deed=%s, is_rented=%s, current_rental_agreement_id=%s
							  WHERE id=%s""", (name, cadastral_number, title_deed, is_rented, current_rental_agreement_id, rental_object_id))


	def update_room_rental_object_data(self, rental_object_id, total_area, rooms_number):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_room
							  SET total_area=%s, rooms_number=%s
							  WHERE rental_object_id=%s 
							  """, (total_area, rooms_number, rental_object_id))

					
	def update_flat_rental_object_data(self, rental_object_id):
		...

	def update_house_rental_object_data(self, rental_object_id):
		...


	def update_location_data(self, rental_object_id, coords, country, region, city, 
							 district, street, building_number, block_number, appt, entrance_number, 
							 floor, location_comment):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location
							  SET coords=%s, country=%s, region=%s, city=%s,  district=%s, street=%s, building_number=%s, 
							      block_number=%s, appt=%s, entrance_number=%s, floor=%s, location_comment=%s
							  WHERE rental_object_id=%s""", 
							  (coords, country, region, city,  district, street, building_number, block_number, appt, 
							   entrance_number, floor, location_comment, rental_object_id))


	def update_location_nearest_metro_stations_data(self, rental_object_id, nearest_metro_station_ids:list):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM rental_objects_metro_stations WHERE rental_object_id=%s""", (rental_object_id,))
			for metro_station_id in nearest_metro_station_ids:
				cursor.execute("""INSERT INTO rental_objects_metro_stations(rental_object_id, metro_station_id)
								  VALUES (%s, %s)""", (rental_object_id, metro_station_id))









	def update_object_data(self, rental_object_id, bathroom_type_id, wash_place_type_id, area, ceilings_height, 
							 win_number, balcony, air_conditioner, wi_fi, furniture):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data
							  SET bathroom_type_id=%s, wash_place_type_id=%s, area=%s, ceilings_height=%s, win_number=%s, 
							  balcony=%s, air_conditioner=%s, wi_fi=%s, furniture=%s
							  WHERE rental_object_id=%s""", 
							  (bathroom_type_id, wash_place_type_id, area, ceilings_height, 
							 win_number, balcony, air_conditioner, wi_fi, furniture, rental_object_id))



	def update_object_data_window_overlook(self, rental_object_id, is_street, is_yard):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data_window_overlooks
							  SET street=%s, yard=%s
							  WHERE rental_object_id=%s""", (is_street, is_yard, rental_object_id))

	def update_object_data_window_frame_type(self, rental_object_id, is_wood, is_plastic):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data_window_frame_types
							  SET wood=%s, plastic=%s
							  WHERE rental_object_id=%s""", (is_wood, is_plastic, rental_object_id))

	def update_object_data_cooking_range_type(self, rental_object_id, is_electric, is_gas):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data_cooking_range_types
							  SET electric=%s, gas=%s
							  WHERE rental_object_id=%s""", (is_electric, is_gas, rental_object_id))



	def update_building_data(self, rental_object_id, building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building
							  SET building_type_id=%s, floors_number=%s, garbage_disposal=%s, intercom=%s, concierge=%s, building_year=%s
							  WHERE rental_object_id=%s""", 
							  (building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year, rental_object_id))




	def update_appliances_data(self, rental_object_id, fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances
							  SET fridge=%s, dishwasher=%s, washer=%s, television=%s, vacuum=%s, teapot=%s, iron=%s, microwave=%s
							  WHERE rental_object_id=%s""", 
							  (fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave, rental_object_id))



	def update_things_data(self, rental_object_id, things: dict):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM ro_things WHERE rental_object_id=%s""", (rental_object_id,)) # чистим все прошлые записи
			for k,v in things.items():
				cursor.execute("""INSERT INTO ro_things(rental_object_id, thing, amount, cost)
								  VALUES (%s,%s,%s,%s)""", (rental_object_id, k, v[0], v[1])) # заливаем новые





	@staticmethod
	def get_metro_data(json_file='data/metro.json'):
		"""приобразует json-файл в питоновские список"""
		with open(json_file) as file:
			data = json.load(file)
		return data  
			

	def add_metro_data(self):
		"""добавляет данные о станциях метро в БД"""
		with self.context_manager(self.config) as cursor:
			metro_data = self.get_metro_data()
			for data in metro_data:
				data[5] = str(data[5])
				cursor.execute("""INSERT INTO metro_stations(city, line_number, line_name, color, station, is_valid) 
								  VALUES (%s, %s, %s, %s, %s, %s)""",
								  (data[0], data[1], data[2], data[3], data[4], data[5]))



class RentalAgreementDM:
	...


class DataManipulation(Database, UserDM, RentalObgectDM, RentalAgreementDM):
	def __init__(self, config, context_manager):
		super().__init__(config, context_manager)


if __name__ == '__main__':
	...
