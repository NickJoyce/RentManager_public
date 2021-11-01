class DataDefinition:
	def create_all_tables(self):
		"""Создает все таблицы в БД"""
		with self.context_manager(self.config) as cursor:

			##### ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ #####
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
		









			##### ДАННЫЕ ОБЪЕКТА АРЕНДЫ #####
			# rental_object_types - типы объктов
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_object_types (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   			  type VARCHAR(100) UNIQUE
																   			  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_object_types`')

			# rental_objects - объекты аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_objects (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 type_id INT,
																		 address VARCHAR(255) DEFAULT '',
																		 is_rented BOOL DEFAULT 0,
																		 rental_agreement_id INT,
																		 photos VARCHAR(100),
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

			# rental_objects_general - общие данные об объекте
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general (rental_object_id INT PRIMARY KEY NOT NULL,
																	 bathroom_type_id INT,
																	 wash_place_type_id INT,
																	 area FLOAT, 
																	 floor INT,
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
			print('CREATE TABLE IF NOT EXISTS `ro_general`')

			# ro_general_window_overlooks
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general_window_overlooks (rental_object_id INT PRIMARY KEY NOT NULL,
																					  street BOOL DEFAULT 0,
																					  yard BOOL DEFAULT 0,
																				  	  FOREIGN KEY(rental_object_id)
																			  			  REFERENCES ro_general(rental_object_id)
																			  			  ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_general_window_overlooks`')

			# ro_general_window_frame_types
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general_window_frame_types (rental_object_id INT PRIMARY KEY NOT NULL,
																					    wood BOOL DEFAULT 0,
																					    plastic BOOL DEFAULT 0,
																				  	  	FOREIGN KEY(rental_object_id)
																			  			  REFERENCES ro_general(rental_object_id)
																			  			  ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_general_window_frame_types`')

			# ro_general_cooking_range_types
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general_cooking_range_types (rental_object_id INT PRIMARY KEY NOT NULL,
																					     electric BOOL DEFAULT 0,
																					     gas BOOL DEFAULT 0,
																				  	  	 FOREIGN KEY(rental_object_id)
																			  			    REFERENCES ro_general(rental_object_id)
																			  			    ON DELETE CASCADE	
																					   ) ENGINE = InnoDB""" )															  																						  				
			print('CREATE TABLE IF NOT EXISTS `ro_general_cooking_range_types`')

			





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
																	  building_year BOOL DEFAULT 0,
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




			# ro_district
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_district (rental_object_id INT PRIMARY KEY NOT NULL,
																	 FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
																	 ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ro_general`')




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
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_things (rental_object_id INT PRIMARY KEY NOT NULL,
																		thing VARCHAR(255), 
																		amount INT,
																		cost FLOAT,
															  			FOREIGN KEY(rental_object_id)
																			REFERENCES rental_objects(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_things`')



			# ro_room
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_room (rental_object_id INT PRIMARY KEY NOT NULL,
																  total_area FLOAT,
																  rooms_number INT,
															  	  FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_room`')

			# ro_flat
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_flat (rental_object_id INT PRIMARY KEY NOT NULL,
															  		FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_flat`')

			# ro_house
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_house (rental_object_id INT PRIMARY KEY NOT NULL,
															  		FOREIGN KEY(rental_object_id)
																		REFERENCES rental_objects(id)
																		ON DELETE CASCADE
															 	  ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `ro_house`')








			##### ДОГОВОР АРЕНДЫ #####
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
		self.create_all_tables()


	def show_tables(self):
		"""Выводит список всех таблиц"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SHOW TABLES""")
			print([table[0] for table in cursor.fetchall()])