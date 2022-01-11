import json
import csv
from werkzeug.security import generate_password_hash, check_password_hash 

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
																email VARCHAR(100) DEFAULT '',
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





			# LINK ADMINS WITH LANDLORDS
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_admin_id_lanlord_id(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			   admin_id INT NOT NULL,
																 			   landlord_id INT NOT NULL,
																			   FOREIGN KEY(admin_id)
																 					REFERENCES users_admins(id)
																 					ON DELETE CASCADE,																 			   
																			   FOREIGN KEY(landlord_id)
																 					REFERENCES users_landlords(id)
																 					ON DELETE CASCADE
																 				UNIQUE(admin_id, landlord_id)
																	 		   ) ENGINE = InnoDB""" )



			# LINK LANDLORDS WITH TENANTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_landlord_id_tenant_id(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			   landlord_id INT NOT NULL,
																 			   tenant_id INT NOT NULL,
																			   FOREIGN KEY(landlord_id)
																 					REFERENCES users_landlords(id)
																 					ON DELETE CASCADE,
																			   FOREIGN KEY(tenant_id)
																 					REFERENCES users_tenants(id)
																 					ON DELETE CASCADE
																 			   UNIQUE(landlord_id, tenant_id)
																	 		   ) ENGINE = InnoDB""" )


			# LINK LANDLORDS WITH RENTAL AGREEMENTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_landlord_id_rental_agreements_id(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			   landlord_id INT NOT NULL,
																 			   rental_agreement_id INT NOT NULL,
																			   FOREIGN KEY(landlord_id)
																 					REFERENCES users_landlords(id)
																 					ON DELETE CASCADE,
																			   FOREIGN KEY(rental_agreement_id)
																 					REFERENCES rental_agreements(id)
																 					ON DELETE CASCADE
																 			   UNIQUE(landlord_id, rental_agreement_id)	
																	 		   ) ENGINE = InnoDB""" )







			# passport
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_passport (user_id INT PRIMARY KEY NOT NULL,
																	     first_name VARCHAR(100) DEFAULT '',
																	     patronymic VARCHAR(100) DEFAULT '',
																	     last_name VARCHAR(100) DEFAULT '',
																	     serie VARCHAR(100) DEFAULT '',
																	     pass_number VARCHAR(100) DEFAULT '',
																	     authority VARCHAR(255) DEFAULT '', 
																	     department_code VARCHAR(100) DEFAULT '',
																	     date_of_issue DATE DEFAULT '2000-01-01', 
																	     date_of_birth DATE DEFAULT '2000-01-01', 
																	     place_of_birth VARCHAR(100) DEFAULT '',
																	     registration VARCHAR(100) DEFAULT '',
																	     INDEX user_id_idx (user_id),
																	     FOREIGN KEY(user_id)
																	 		REFERENCES users(id)
																	 		ON DELETE CASCADE
																	     ) ENGINE = InnoDB""" )

			print('CREATE TABLE IF NOT EXISTS `users_passport`')

			# register
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_register (user_id  INT PRIMARY KEY NOT NULL,
																   		 login VARCHAR(100) UNIQUE,
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
			

			# rental_object_statuses - типы объктов
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_object_statuses (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																   			  status VARCHAR(100) UNIQUE

																   			  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_object_statuses`')


			# rental_objects - объекты аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_objects (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 type_id INT NOT NULL,
																		 name VARCHAR(100),
																		 status VARCHAR(100),
																		 FOREIGN KEY (status)
																		 	REFERENCES rental_object_statuses(status)
																		) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_objects`')

			# LINK LANDLORDS WITH RENTAL OBJECTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS users_landlord_id_rental_object_id(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			   landlord_id INT NOT NULL,
																 			   rental_object_id INT NOT NULL,
																			   FOREIGN KEY(landlord_id)
																 					REFERENCES users_landlords(id)
																 					ON DELETE CASCADE,
																			   FOREIGN KEY(rental_object_id)
																 					REFERENCES rental_objects(id)
																 					ON DELETE CASCADE
																	 		   ) ENGINE = InnoDB""" )


			# ro_general
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_general (rental_object_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	 cadastral_number VARCHAR(100) DEFAULT '',
																	 title_deed VARCHAR(255) DEFAULT '',
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
																	 bathroom_type_id INT DEFAULT 1,
																	 wash_place_type_id INT DEFAULT 1,
																	 area FLOAT, 
																	 ceilings_height FLOAT,
																	 win_number INT,
																	 balcony BOOL DEFAULT 0,
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
																	  building_type_id INT DEFAULT 1,
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
																	  country VARCHAR(100) DEFAULT 'РФ',
																	  federal_district VARCHAR(100) DEFAULT '',
																	  region VARCHAR(100) DEFAULT '',
																	  city VARCHAR(100) DEFAULT '',
																	  city_district VARCHAR(100) DEFAULT '',
																	  street VARCHAR(100) DEFAULT '',
																	  building_number VARCHAR(100) DEFAULT '',
																	  block_number VARCHAR(100) DEFAULT '',
																	  appt VARCHAR(100) DEFAULT '',
																	  entrance_number VARCHAR(100) DEFAULT '',
																	  floor VARCHAR(100) DEFAULT '',
																	  coords VARCHAR(100) DEFAULT '',
																	  nearest_metro_stations VARCHAR(255) DEFAULT '', 
																	  location_comment VARCHAR(255) DEFAULT '',

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

			# ro_things
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_costs (	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	rental_object_id INT,
																	name VARCHAR(255) DEFAULT '',
																	is_payer_landlord BOOL DEFAULT 0,
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


			# LINK RENTAL OBJECTS WITH AGENTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS ro_id_agent_id(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 			   rental_object_id INT NOT NULL,
																 			   agent_id INT NOT NULL,
																			   FOREIGN KEY(rental_object_id)
																 					REFERENCES rental_objects(id)
																 					ON DELETE CASCADE,
																			   FOREIGN KEY(agent_id)
																 					REFERENCES users_agents(id)
																 					ON DELETE CASCADE,
																 			   UNIQUE(rental_object_id, agent_id)
																	 		   ) ENGINE = InnoDB""" )




class RentalAgreementDD:
	"""Определение данных для таблиц связанных с договором аренды"""
	def create_all_rental_agreement_tables(self):
		with self.context_manager(self.config) as cursor:

			# RENTAL AGREEMENT STATUSES
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_statuses (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																    status VARCHAR(50) UNIQUE
																	) ENGINE = InnoDB""" )	


			# rental_agreements - договоры аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS rental_agreements (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		   agreement_number VARCHAR(50),
																		   city VARCHAR(100),
																		   date_of_conclusion DATE DEFAULT '2000-01-01',
																		   status VARCHAR(50),
																		   FOREIGN KEY(status)
																		       REFERENCES ra_status(status),
																		   UNIQUE(agreement_number)
															 	  		   ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `rental_agreements`')


			# ra_other_tenants - лица проживающие совместно с нанимателем (указывается в договоре)
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_other_tenants (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		   rental_agreement_id INT NOT NULL,
																		   full_name VARCHAR(255),
																		   phone VARCHAR(50),
																		   FOREIGN KEY (rental_agreement_id)
																				REFERENCES rental_agreements(id)
																				ON DELETE CASCADE
															 	  		   ) ENGINE = InnoDB""" )			


			# LINK RENTAL AGREEMENTS WITH TENANTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_id_tenant_id (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 		  				rental_agreement_id INT NOT NULL,
																 	     			    tenant_id INT NOT NULL,
																				        FOREIGN KEY(rental_agreement_id)
																		 			      REFERENCES rental_agreements(id)
																		 				  ON DELETE CASCADE,
																					     FOREIGN KEY(tenant_id)
																		 					REFERENCES users_tenants(id)
																		 					ON DELETE CASCADE
																		 				UNIQUE(rental_agreement_id, tenant_id)
																	 		   			 ) ENGINE = InnoDB""" )		

			# # LINK RENTAL AGREEMENTS WITH AGENTS
			# cursor.execute("""CREATE TABLE IF NOT EXISTS ra_id_agent_id (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
			# 													 		  				rental_agreement_id INT NOT NULL,
			# 													 	     			    agent_id INT NOT NULL,
			# 																	        FOREIGN KEY(rental_agreement_id)
			# 															 			      REFERENCES rental_agreements(id)
			# 															 				  ON DELETE CASCADE,
			# 																		     FOREIGN KEY(agent_id)
			# 															 					REFERENCES users_agents(id)
			# 															 					ON DELETE CASCADE
			# 															 				UNIQUE(rental_agreement_id, agent_id)
			# 														 		   			 ) ENGINE = InnoDB""" )

			# LINK RENTAL AGREEMENTS WITH RENTAL OBJECTS
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_id_rental_object_id (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																 		  				rental_agreement_id INT NOT NULL,
																 	     			    rental_object_id INT NOT NULL,
																				        FOREIGN KEY(rental_agreement_id)
																		 			      REFERENCES rental_agreements(id)
																		 				  ON DELETE CASCADE,
																					     FOREIGN KEY(rental_object_id)
																		 					REFERENCES rental_objects(id)
																		 					ON DELETE CASCADE
																		 				 UNIQUE(rental_agreement_id, rental_object_id)
																	 		   			 ) ENGINE = InnoDB""" )




			# ra_conditions - условия аренды
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_conditions (rental_agreement_id INT PRIMARY KEY NOT NULL,
																	 rental_rate INT DEFAULT 0,
																	 prepayment INT DEFAULT 100,
																	 deposit INT DEFAULT 0,
																	 late_fee FLOAT DEFAULT 3,
																	 start_of_term DATE DEFAULT '2000-01-01',
																	 end_of_term DATE DEFAULT '2000-01-01',
																	 payment_day INT DEFAULT 0,
																	 cleaning_cost INT DEFAULT 0,
															  		 FOREIGN KEY (rental_agreement_id )
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE
															 	  	  ) ENGINE = InnoDB""" )
			print('CREATE TABLE IF NOT EXISTS `ra_conditions`')

			

			# ra_move_in - Акт сдачи-приемки (один для каждого договора)
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_move_in (rental_agreement_id INT PRIMARY KEY NOT NULL,
																	 date_of_conclusion DATE DEFAULT '2000-01-01',
																	 number_of_sets_of_keys INT DEFAULT 0, 
																	 number_of_keys_in_set INT DEFAULT 0,
																	 rental_object_comment VARCHAR(1000) DEFAULT '',
																	 things_comment VARCHAR(1000) DEFAULT '',
															  		 FOREIGN KEY (rental_agreement_id )
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE,
																	 UNIQUE(rental_agreement_id)
 																	 ) ENGINE = InnoDB""" )
		


			# ra_move_out - Акт возврата (один для каждого договора)
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_move_out (rental_agreement_id INT PRIMARY KEY NOT NULL,
																     date_of_conclusion DATE DEFAULT '2000-01-01',
																	 number_of_sets_of_keys INT DEFAULT 0, 
																	 number_of_keys_in_set INT DEFAULT 0,
																	 rental_object_comment VARCHAR(1000) DEFAULT '',
																	 things_comment VARCHAR(1000) DEFAULT '',
																	 damage_cost FLOAT DEFAULT 0.0,
																	 cleaning BOOL DEFAULT 0, 
																	 rental_agreeement_debts FLOAT DEFAULT 0.0,
																	 deposit_refund FLOAT DEFAULT 0.0,
																	 prepayment_refund FLOAT DEFAULT 0.0,
															  		 FOREIGN KEY (rental_agreement_id )
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE,
																	 UNIQUE(rental_agreement_id)
 																	 ) ENGINE = InnoDB""" )

			# ra_termination - Соглашение о досрочном расторжении (только одно для каждого договора)
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_termination (rental_agreement_id INT PRIMARY KEY NOT NULL,
																		 date_of_conclusion DATE DEFAULT '2000-01-01',
																		 notice_date DATE DEFAULT '2000-01-01',
																	 	 end_of_term DATE DEFAULT '2000-01-01',
																	 	 is_landlord_initiator BOOL,
															  		 	 FOREIGN KEY (rental_agreement_id )
																			 REFERENCES rental_agreements(id)
																			 ON DELETE CASCADE,
																		 UNIQUE(rental_agreement_id)
 																	 	) ENGINE = InnoDB""" )			

			# ra_renewal - Соглашение о продлении (может выполняться неограниченное число раз, даты не могут повторятся)
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_renewal (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		 rental_agreement_id INT NOT NULL,
																		 date_of_conclusion DATE DEFAULT '2000-01-01',
																	 	 end_of_term DATE, 
															  		 	 FOREIGN KEY (rental_agreement_id )
																			 REFERENCES rental_agreements(id)
																			 ON DELETE CASCADE,
																		 UNIQUE(end_of_term)
 																	 	) ENGINE = InnoDB""" )	
			




			# ra_rental_object - фиксированные данные объекта аренды
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_rental_object (rental_agreement_id INT PRIMARY KEY NOT NULL,
																		 rental_object_id INT NOT NULL,
																		 type VARCHAR(255),
																	 	 address VARCHAR(255),
																	 	 title_deed VARCHAR(255),
															  		 	 FOREIGN KEY (rental_agreement_id )
																			 REFERENCES rental_agreements(id)
																			 ON DELETE CASCADE
 																	 	) ENGINE = InnoDB""" )	

			# ra_things - фиксированные данные о вещах в объекте аренды (опись имущества) 
			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_things (	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																		rental_agreement_id INT,
																		thing_number INT,
																		thing_name VARCHAR(255), 
																		amount INT,
																		cost FLOAT,
															  		 	FOREIGN KEY (rental_agreement_id )
																			REFERENCES rental_agreements(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )


			# ra_costs - фиксированные данные о расходах на содержание объекта аренды 

			cursor.execute("""CREATE TABLE IF NOT EXISTS ra_costs (	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
																	rental_agreement_id INT,
																	name VARCHAR(255) DEFAULT '',
																	is_payer_landlord BOOL DEFAULT 0,
															  		FOREIGN KEY(rental_agreement_id)
																		REFERENCES rental_agreements(id)
																		ON DELETE CASCADE
															 		) ENGINE = InnoDB""" )



			# ra_landlord - фиксированные данные наймодателя в договоре
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_landlord (rental_agreement_id INT PRIMARY KEY NOT NULL,
																	  landlord_id INT,
																	  last_name VARCHAR(255) DEFAULT '',
																	  first_name VARCHAR(255) DEFAULT '',
																	  patronymic VARCHAR(255) DEFAULT '',
																	  phone VARCHAR(255) DEFAULT '',
																	  email VARCHAR(255) DEFAULT '',
																	  serie VARCHAR(255) DEFAULT '', # серия паспорта
																	  pass_number VARCHAR(255) DEFAULT '', # номер паспорта
																	  authority VARCHAR(255) DEFAULT '', # орган выдавший паспорт
																	  registration VARCHAR(255) DEFAULT '', # прописка
															  		  FOREIGN KEY (rental_agreement_id )
																			REFERENCES rental_agreements(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )																				
			# ra_tenant - фиксированные данные нанимателя в договоре
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_tenant (rental_agreement_id INT PRIMARY KEY NOT NULL,
																	  tenant_id INT,
																	  last_name VARCHAR(255) DEFAULT '',
																	  first_name VARCHAR(255) DEFAULT '',
																	  patronymic VARCHAR(255) DEFAULT '',
																	  phone VARCHAR(255) DEFAULT '',
																	  email VARCHAR(255) DEFAULT '',
																	  serie VARCHAR(255) DEFAULT '', # серия паспорта
																	  pass_number VARCHAR(255) DEFAULT '', # номер паспорта
																	  authority VARCHAR(255) DEFAULT '', # орган выдавший паспорт
																	  registration VARCHAR(255) DEFAULT '', # прописка
															  		  FOREIGN KEY (rental_agreement_id )
																			REFERENCES rental_agreements(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )	
			# ra_agent - фиксированные данные агента в договоре
			сursor.execute("""CREATE TABLE IF NOT EXISTS ra_agent (rental_agreement_id INT PRIMARY KEY NOT NULL,
																	  agent_id INT,
																	  last_name VARCHAR(255) DEFAULT '',
																	  first_name VARCHAR(255) DEFAULT '',
																	  patronymic VARCHAR(255) DEFAULT '',
																	  phone VARCHAR(255) DEFAULT '',
																	  email VARCHAR(255) DEFAULT '',
																	  serie VARCHAR(255) DEFAULT '', # серия паспорта
																	  pass_number VARCHAR(255) DEFAULT '', # номер паспорта
																	  authority VARCHAR(255) DEFAULT '', # орган выдавший паспорт
																	  registration VARCHAR(255) DEFAULT '', # прописка
															  		  FOREIGN KEY (rental_agreement_id )
																			REFERENCES rental_agreements(id)
																			ON DELETE CASCADE
															 			) ENGINE = InnoDB""" )




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

	# ------------------------ ПЕРЕВОД ADMIN_ID, LANDLORD_ID ИЛИ TENANT_ID В USER_ID ------------------------

	def get_user_id_by_admin_id(self, admin_id):
		"""Возвращает user_id по admin_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id FROM users_admins WHERE id=%s""", (admin_id,))
			return cursor.fetchall()[0][0]	

	def get_user_id_by_landlord_id(self, landlord_id):
		"""Возвращает user_id по landlord_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id FROM users_landlords WHERE id=%s""", (landlord_id,))
			return cursor.fetchall()[0][0]	


	def get_user_id_by_tenant_id(self, tenant_id):
		"""Возвращает user_id по tenant_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id FROM users_tenants WHERE id=%s""", (tenant_id,))
			return cursor.fetchall()[0][0]	


	def get_user_id_by_agent_id(self, agent_id):
		"""Возвращает user_id по agent_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id FROM users_agents WHERE id=%s""", (agent_id,))
			return cursor.fetchall()[0][0]	


	# ------------------------ СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ (вспомогательные функции) ------------------------




	def get_user_type_id_by_user_type(self, user_type):
		"""id типа пользователя по наименованию типа"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM user_types WHERE type=%s""", (user_type,))
			return cursor.fetchall()[0][0] 

	def add_user_entry(self, user_type_id, name, phone, email):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO users(type_id, name, phone, email) VALUES(%s, %s, %s, %s)""", (user_type_id, name, phone, email))


	def get_last_user_id(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users ORDER BY id DESC LIMIT 1""")
			return cursor.fetchall()[0][0]

	def create_passport(self, user_id):
		with self.context_manager(self.config) as cursor:		
			cursor.execute("""INSERT INTO users_passport(user_id) VALUES(%s)""", (user_id,))

	def create_register(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO users_register(user_id) VALUES(%s)""", (user_id,))



	# ------------------------ СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ ------------------------ 
	def create_user(self, user_type, name, phone, email, login, hashed_password, admin_id=None, landlord_id=None):
		# получаем id типа пользователя по наименованию типа
		user_type_id = self.get_user_type_id_by_user_type(user_type)

		# создаем запись в таблице users
		self.add_user_entry(user_type_id, name, phone, email)		

		# получем id (user_id) созданного пользователя (генерируется в БД)
		user_id = self.get_last_user_id()

		# создаем запись в таблице users_passport привязанную к user_id
		self.create_passport(user_id)

		# создаем запись в таблице users_passport users_register привязанную к user_id
		self.create_register(user_id)

		# записываем в БД логин и пароль
		self.set_register_login(user_id, login)				
		self.set_register_password(user_id, hashed_password)

		if user_type == 'администратор':
			self.add_admin_data(user_id)
		elif user_type == 'наймодатель':
			self.add_landlord_data(user_id, admin_id)
		elif user_type == 'наниматель':
			self.add_tenant_data(user_id, landlord_id)
		elif user_type == 'агент':
			self.add_agent_data(user_id, landlord_id)


	def add_admin_data(self, user_id):
		with self.context_manager(self.config) as cursor:
			# создаем запись в таблице users_admins привязанную к user_id	
			cursor.execute("""INSERT INTO users_admins(user_id) VALUES(%s)""", (user_id,))


	def add_landlord_data(self, user_id, admin_id):
		with self.context_manager(self.config) as cursor:
			# создаем запись в таблице users_landlords привязанную к user_id		
			cursor.execute("""INSERT INTO users_landlords(user_id) VALUES(%s)""", (user_id,))
			# получаем id записи (landlord_id) (генерируется в БД)
			cursor.execute("""SELECT MAX(id) FROM users_landlords""") 
			landlord_id = cursor.fetchall()[0][0] 
			# связываем admin_id и landlord_id в таблице users_admin_id_lanlord_id
			cursor.execute("""INSERT INTO users_admin_id_lanlord_id(admin_id, landlord_id) 
						   VALUES (%s, %s)""", (admin_id, landlord_id))

	def add_tenant_data(self, user_id, landlord_id):
		with self.context_manager(self.config) as cursor:
			# создаем запись в таблице users_tenants привязанную к user_id	
			cursor.execute("""INSERT INTO users_tenants(user_id) VALUES(%s)""", (user_id,))
			# получаем id записи (tenant_id) (генерируется в БД)
			cursor.execute("""SELECT MAX(id) FROM users_tenants""") 
			tenant_id = cursor.fetchall()[0][0] 
			# связываем landlord_id и tenant_id в таблице users_landlord_id_tenant_id
			cursor.execute("""INSERT INTO users_landlord_id_tenant_id(landlord_id, tenant_id) 
						   VALUES (%s, %s)""", (landlord_id, tenant_id))

	def add_agent_data(self, user_id, landlord_id):
		with self.context_manager(self.config) as cursor:
			# создаем запись в таблице users_agents привязанную к user_id	
			cursor.execute("""INSERT INTO users_agents(user_id) VALUES(%s)""", (user_id,))
			# получаем id записи (agent_id) (генерируется в БД)
			cursor.execute("""SELECT MAX(id) FROM users_agents""") 
			agent_id = cursor.fetchall()[0][0] 
			# связываем landlord_id и tenant_id в таблице users_landlord_id_tenant_id
			cursor.execute("""INSERT INTO users_landlord_id_agent_id(landlord_id, agent_id) 
						   VALUES (%s, %s)""", (landlord_id, agent_id))



	# ------------------------ УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ------------------------ 
	def delete_user(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM users WHERE id=%s""", (user_id,))


	# ------------------------ ВХОД ------------------------

	def get_logins(self):
		"""возвращает логины"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT login FROM users_register""")
			return [i[0] for i in cursor.fetchall()]		

	def is_login(self, login):
		"""Есть ли login в БД, если да то вернет user_id, если нет то ничего не вернет"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT login from users_register WHERE login=%s""", (login,))
			if cursor.fetchall():
				return True
			else:
				return False

	def get_password_by_login(self, login):
		"""Возвращает пароль по логину"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT password FROM users_register WHERE login=%s""", (login,))
			return cursor.fetchall()[0][0]

	def get_user_id_by_login(self, login):
		"""Возвращает пароль по логину"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id FROM users_register WHERE login=%s""", (login,))
			return cursor.fetchall()[0][0]

	def get_user_type_by_user_id(self, user_id):
		"""Возвращает тип пользователя по id пользователя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ut.type 
							  FROM users AS u
							  JOIN user_types AS ut
							  ON u.type_id=ut.id
							  WHERE u.id=%s""", (user_id,))
			return cursor.fetchall()[0][0]
	




	# GET USER DATA BY ID
	def get_user_data_by_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, name, phone, email FROM users WHERE id=%s""", (user_id,))
			return cursor.fetchall()[0]



	# FOR LANDLORDS DATA OF ADMIN OUTPUT
	def get_landlord_user_id_of_admin(self, admin_id):
		"""возвращает список user_id наймодателей данного администратора"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ul.user_id
							  FROM users_admin_id_lanlord_id AS uaili
							  JOIN users_landlords AS ul
							  ON  uaili.landlord_id=ul.id
							  WHERE uaili.admin_id = %s""", (admin_id,))	
			return  [i[0] for i in cursor.fetchall()]


	def get_landlord_data_of_admin(self, admin_id):
		"""возвращает данные всех наймодателей конткретного администатора (класс Landlord)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ul.id, ul.inn # u.type_id, ul.inn
							  FROM users AS u
							  JOIN users_landlords AS ul
							  ON u.id=ul.user_id
							  JOIN	users_admin_id_lanlord_id AS uaili
							  ON uaili.landlord_id=ul.id
							  WHERE uaili.admin_id=%s""", (admin_id,))
			return cursor.fetchall()

	def get_landlord_data(self, user_id):
		"""возвращает данные любого наймодателя безотносительно к администратору (класс Landlord)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ul.id, ul.inn # u.type_id, ul.inn
							  FROM users AS u
							  JOIN users_landlords AS ul
							  ON u.id=ul.user_id
							  WHERE u.id=%s""", (user_id,))
			return cursor.fetchall()[0]

	def get_landlord_data_by_landlord_id(self, landlord_id):
		"""возвращает данные любого наймодателя безотносительно к администратору (класс Landlord) по landlord_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ul.id, ul.inn # u.type_id, ul.inn
							  FROM users_landlords AS ul
							  JOIN users AS u
							  ON ul.user_id = u.id
							  WHERE ul.id=%s""", (landlord_id,))
			return cursor.fetchall()[0]




	# FOR TENANTS DATA OF LADLORD OUTPUT
	def get_tenant_user_id_of_landlord(self, landlord_id):
		"""возвращает список user_id нанимателей данного наймодателя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ut.user_id
							  FROM users_landlord_id_tenant_id AS uliti
							  JOIN users_tenants AS ut
							  ON uliti.tenant_id=ut.id
							  WHERE uliti.landlord_id = %s""", (landlord_id,))	
			return  [i[0] for i in cursor.fetchall()]


	def get_tenant_data_of_landlord(self, landlord_id):
		"""возвращает данные всех нанимателей конткретного наймодателя (класс Tenant)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ut.id
							  FROM users AS u
							  JOIN users_tenants AS ut
							  ON u.id=ut.user_id
							  JOIN	users_landlord_id_tenant_id AS uliti
							  ON uliti.tenant_id=ut.id
							  WHERE uliti.landlord_id=%s""", (landlord_id,))
			return cursor.fetchall()

	def get_tenant_data(self, user_id):
		"""возвращает данные любого нанимателя безотносительно к наймодателю (класс Tenant)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ut.id
							  FROM users AS u
							  JOIN users_tenants AS ut
							  ON u.id=ut.user_id
							  WHERE u.id=%s""", (user_id,))
			return cursor.fetchall()[0]

	def get_tenant_data_by_tenant_id(self, tenant_id):
		"""возвращает данные любого нанимателя безотносительно к наймодателю (класс Tenant) по tenant_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ut.id
							  FROM users_tenants AS ut
							  JOIN users AS u
							  ON ut.user_id=u.id
							  WHERE ut.id=%s""", (tenant_id,))
			return cursor.fetchall()[0]



	# FOR AGENTS DATA OF LADLORD OUTPUT
	def get_agent_user_id_of_landlord(self, landlord_id):
		"""возвращает список user_id агентов данного наймодателя"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ua.user_id
							  FROM users_landlord_id_agent_id AS uliai
							  JOIN users_agents AS ua
							  ON uliai.agent_id=ua.id
							  WHERE uliai.landlord_id = %s""", (landlord_id,))	
			return  [i[0] for i in cursor.fetchall()]


	def get_agent_data_of_landlord(self, landlord_id):
		"""возвращает данные всех агентов конткретного наймодателя (класс Agent)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ua.id
							  FROM users AS u
							  JOIN users_agents AS ua
							  ON u.id=ua.user_id
							  JOIN	users_landlord_id_agent_id AS uliai
							  ON uliai.agent_id=ua.id
							  WHERE uliai.landlord_id=%s""", (landlord_id,))
			return cursor.fetchall()



	def get_agent_data(self, user_id):
		"""возвращает данные любого агента безотносительно к наймодателю (класс Landlord)"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ua.id
							  FROM users AS u
							  JOIN users_agents AS ua
							  ON u.id=ua.user_id
							  WHERE u.id=%s""", (user_id,))
			return cursor.fetchall()[0]

	def get_agent_data_by_agent_id(self, agent_id):
		"""возвращает данные любого агента безотносительно к наймодателю (класс Landlord) по agent_id"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ua.id
							  FROM users_agents AS ua
							  JOIN users AS u
							  ON ua.user_id=u.id
							  WHERE ua.id=%s""", (agent_id,))
			return cursor.fetchall()[0]



	# ПОЛУЧЕНИЕ ДАННЫХ ПОЛЬЗОВАТЛЕЙ ПО НОМЕРУ ДОГОВОРА		
	def get_tenant_data_by_rental_agreement_id(self, rental_agreement_id):
		"""возвращает данные user по rental_agreement_id, tables: [ra_id_tenant_id, users_tenants, users] """
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ut.id
							  FROM ra_id_tenant_id AS riti
							  JOIN users_tenants AS ut
							  ON riti.tenant_id=ut.id
							  JOIN users AS u
							  ON u.id=ut.user_id
							  WHERE riti.rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()

	def get_agent_data_by_rental_agreement_id(self, rental_agreement_id):
		"""возвращает данные user по rental_agreement_id, tables: [ra_id_tenant_id, users_agents, users] """
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ua.id
							  FROM ra_id_agent_id AS riai
							  JOIN users_agents AS ua
							  ON riai.agent_id=ua.id
							  JOIN users AS u
							  ON u.id=ua.user_id
							  WHERE riai.rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()





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


	# GET ATTRIBUTES [ADMIN]: id
	def get_admin_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_admins WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]


	# GET ATTRIBUTES [lANDLORD]: id, user_id, inn
	def get_landlord_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_landlords WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_landlord_inn(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT inn FROM users_landlords WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]


	# GET ATTRIBUTES [TENANT]: id
	def get_tenant_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_tenants WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]


	# GET ATTRIBUTES [AGENT]: id
	def get_agent_id(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id FROM users_agents WHERE user_id=%s""", (user_id,))
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

	# GET ALL PASSPORT DATA: 
	def get_passport_data(self, user_id):
		"""возвращает данные наймодателя, необходимые для создания экземпляра класса Landlord"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
									 department_code, date_of_issue, date_of_birth, place_of_birth, registration 
							  FROM users_passport
							  WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]




	# GET ATTRIBUTES [REGISTER]: login, password
	def get_register_login(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT login FROM users_register WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	def get_register_password(self, user_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT password FROM users_register WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0][0]

	# GET ALL REGISTER DATA: 
	def get_register_data(self, user_id):
		"""возвращает данные наймодателя, необходимые для создания экземпляра класса Landlord"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT login, password, user_id
							  FROM users_register
							  WHERE user_id=%s""", (user_id,))
			return cursor.fetchall()[0]




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

	# SET ALL USER DATA: 
	def set_user_data(self, user_id, name, phone, email):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users SET name=%s, phone=%s, email=%s WHERE id=%s""", (name, phone, email, user_id,))



	# SET ATTRIBUTES [LANDLORD]: inn
	def set_landlord_inn(self, user_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_landlords SET inn=%s WHERE user_id=%s""", (value, user_id,))

	# SET ALL LANDLORD DATA: 
	def set_landlord_data(self, user_id, inn):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_landlords SET inn=%s WHERE user_id=%s""", (inn, user_id,))



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
	
	# SET ALL PASSPORT DATA: 
	def set_passport_data(self, user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
						  department_code, date_of_issue, date_of_birth, place_of_birth, registration):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE users_passport 
							  SET first_name=%s, patronymic=%s, last_name=%s, serie=%s, pass_number=%s, authority=%s, 
						  		  department_code=%s, date_of_issue=%s, date_of_birth=%s, place_of_birth=%s, registration=%s 
						  	  WHERE user_id=%s""", 
						  	  (first_name, patronymic, last_name, serie, pass_number, authority, 
						  	   department_code, date_of_issue, date_of_birth, place_of_birth, registration, user_id,))




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

	def add_rental_object_status(self, status):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO rental_object_statuses(status) VALUES (%s)""", (status,))		


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



	# ------------------------ СОЗДАНИЕ ОБЪЕКТОВ АРЕНДЫ (вспомогательные функции) ------------------------
	# def get_renatal_object_type_by_renatal_object_type_id(self, landlord_id):
	# 	with self.context_manager(self.config) as cursor:		
	# 		cursor.execute("""SELECT rot.type 
	# 						  FROM rental_objects AS ro
	# 						  JOIN rental_object_types AS rot
	# 						  ON ro.type_id=rot.id
	# 						  WHERE ro.landlord_id=%s""", (landlord_id,))
	# 		return cursor.fetchall()[0][0]


	# ------------------------ СОЗДАНИЕ ОБЪЕКТОВ АРЕНДЫ ------------------------
	def create_rental_object(self, type_id, name, status, landlord_id): 
		"""Добавление объекта аренды"""
		with self.context_manager(self.config) as cursor:

			# rental_objects (базовая таблица)
			cursor.execute("""INSERT INTO rental_objects(type_id, name, status) VALUES(%s, %s, %s)""", (type_id, name, status))

			# получаем последний id таблицы rental_objects
			cursor.execute("""SELECT max(id) FROM rental_objects""") 
			rental_object_id = cursor.fetchall()[0][0]

			# связываем объект аренды с наймодателем
			cursor.execute("""INSERT INTO users_landlord_id_rental_object_id(landlord_id, rental_object_id)
							  VALUE (%s, %s)""", (landlord_id, rental_object_id))	


			# получаем тип объекта по id типа объекта
			cursor.execute("""SELECT type from rental_object_types WHERE id=%s""", (type_id,))
			type_ = cursor.fetchall()[0][0]

			# создание записей в таблице в зависимости от типа объекта аренды
			if type_  == 'комната':
				cursor.execute("""INSERT INTO ro_room(rental_object_id) VALUES(%s)""", (rental_object_id,))
			elif type_  == 'квартира':
				cursor.execute("""INSERT INTO ro_flat(rental_object_id) VALUES(%s)""", (rental_object_id,))
			elif type_  == 'дом':
				cursor.execute("""INSERT INTO ro_house(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_general (общая информация)
			cursor.execute("""INSERT INTO ro_general(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_appliances (бытовая техника)
			cursor.execute("""INSERT INTO ro_appliances(rental_object_id) VALUES(%s)""", (rental_object_id,))
					
			# ro_building (здание)
			cursor.execute("""INSERT INTO ro_building(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_object_data (объект аренды)
			cursor.execute("""INSERT INTO ro_object_data(rental_object_id) VALUES(%s)""", (rental_object_id,))

			# ro_location (локация)
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



	# ------------------------ УДАЛЕНИЕ ОБЪЕКТОВ АРЕНДЫ ------------------------ 
	def delete_rental_object(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM rental_objects WHERE id=%s""", (rental_object_id,))	











	# FOR RENATAL OBJECTS DATA OF LADLORD OUTPUT
	def get_rental_object_id_of_landlord(self, landlord_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id FROM users_landlord_id_rental_object_id WHERE landlord_id=%s""", (landlord_id,))
			return [i[0] for i in cursor.fetchall()]


	def get_rental_objects_data_of_landlord(self, landlord_id):
		"""возвращает данные всех объектов аренды данного наймодателя
		   для landlord_id, tenant_id и agent_id подставляются соответствующие user_id  
		"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro.id, rot.type, ro.name, ro.status
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id = rot.id
							  JOIN users_landlord_id_rental_object_id AS uliroi
							  ON ro.id = uliroi.rental_object_id
							  WHERE uliroi.landlord_id=%s""", (landlord_id,))
			return cursor.fetchall()



	# GET RENTAL OBJECT TYPES WITH ID
	def get_rental_objects_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type FROM rental_object_types""")
			return [i for i in cursor.fetchall()]	

	# GET BATHROOM TYPES WITH ID
	def get_bathroom_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type FROM bathroom_types""")
			return [i for i in cursor.fetchall()]

	# GET WASH PLACE TYPES WITH ID
	def get_wash_place_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type FROM wash_place_type""")
			return [i for i in cursor.fetchall()]

	# GET BUILDING TYPES WITH ID
	def get_building_types(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type FROM building_types""")
			return [i for i in cursor.fetchall()]


	# GET COUNTRIES WITH ID
	def get_countries(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, country FROM countries""")		
			return [i for i in cursor.fetchall()]

	# GET CITIES WITH ID AND COUNTRY_ID
	def get_cities(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, country_id, city FROM cities""")		
			return [i for i in cursor.fetchall()]

	# GET DISTRICTS WITH ID AND CITY_ID
	def get_districts(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, city_id, district FROM districts""")		
			return [i for i in cursor.fetchall()]
















	# GET RENTAL OBJECT DATA
	def get_rental_object_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, type_id, name, status  FROM rental_objects WHERE id=%s""", (rental_object_id ,))
			return cursor.fetchall()[0]



	# GET RENTAL OBJECT ROOM DATA
	def get_rental_object_data_room(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro.id, rot.type, ro.name, ro.status, rr.total_area, rr.rooms_number
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id=rot.id
							  JOIN ro_room AS rr
							  ON ro.id=rr.rental_object_id
							  WHERE ro.id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]

	# GET RENTAL OBJECT FLAT DATA
	def get_rental_object_data_flat(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro.id, rot.type, ro.name, ro.status
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id=rot.id
							  JOIN ro_flat AS rf
							  ON ro.id=rf.rental_object_id
							  WHERE ro.id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]


	# GET RENTAL OBJECT HOUSE DATA
	def get_rental_object_data_house(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro.id, rot.type, ro.name, ro.status
							  FROM rental_objects AS ro
							  JOIN rental_object_types AS rot
							  ON ro.type_id=rot.id
							  JOIN ro_house AS rh
							  ON ro.id=rh.rental_object_id
							  WHERE ro.id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]

	# GET GENERAL DATA
	def get_general_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, cadastral_number, title_deed FROM ro_general WHERE rental_object_id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]



	# GET OBJECT DATA
	def get_object_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro_od.rental_object_id, bt.type, wpt.type, ro_od.area, ro_od.ceilings_height, 
									 ro_od.win_number, ro_od.balcony, ro_od.air_conditioner, ro_od.wi_fi, ro_od.furniture
							  FROM ro_object_data AS ro_od
							  JOIN bathroom_types AS bt
							  ON ro_od.bathroom_type_id=bt.id
							  JOIN wash_place_type AS wpt
							  ON ro_od.wash_place_type_id=wpt.id						  
							  WHERE ro_od.rental_object_id=%s""", (rental_object_id,))
			object_data = [i for i in cursor.fetchall()[0]]


			cursor.execute("""SELECT street, yard 
							  FROM ro_object_data_window_overlooks
							  WHERE rental_object_id=%s""", (rental_object_id,))
			gotten_data = cursor.fetchall()[0]
			window_overlooks = {'street':gotten_data[0], 'yard':gotten_data[1]}
			object_data.append(window_overlooks)


			cursor.execute("""SELECT wood, plastic 
							  FROM ro_object_data_window_frame_types
							  WHERE rental_object_id=%s""", (rental_object_id,))
			gotten_data = cursor.fetchall()[0]
			window_frame_type = {'wood':gotten_data[0], 'plastic':gotten_data[1]}
			object_data.append(window_frame_type)

			cursor.execute("""SELECT electric, gas
							  FROM ro_object_data_cooking_range_types
							  WHERE rental_object_id=%s""", (rental_object_id,))
			gotten_data = cursor.fetchall()[0]
			cooking_range_types = {'electric':gotten_data[0], 'gas':gotten_data[1]}
			object_data.append(cooking_range_types)

			return object_data
			

	# GET BUILDING DATA
	def get_building_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ro_b.rental_object_id, bt.type, ro_b.floors_number, ro_b.garbage_disposal, 
									 ro_b.intercom, ro_b.concierge, ro_b.building_year
							  FROM ro_building AS ro_b
							  JOIN building_types AS bt
							  ON ro_b.building_type_id = bt.id
							  WHERE ro_b.rental_object_id=%s""", (rental_object_id,))
			building_data = [i for i in cursor.fetchall()[0]]

			cursor.execute("""SELECT passenger, freight
							  FROM ro_building_elevators 
							  WHERE rental_object_id=%s""", (rental_object_id,))
			gotten_data = cursor.fetchall()[0]
			elevators = {'passenger':gotten_data[0], 'freight':gotten_data[1]}
			building_data.append(elevators)

			return building_data 


	# GET LOCATION DATA
	def get_location_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, country, federal_district, region, city, city_district, street, building_number, 
				                     block_number, appt, entrance_number, floor, coords, nearest_metro_stations, location_comment
							  FROM ro_location
							  WHERE rental_object_id=%s""", (rental_object_id,))

			location_data = [i for i in cursor.fetchall()[0]]
			return location_data

	# GET APPLIANCE DATA
	def get_appliances_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave
							  FROM ro_appliances
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]



	# GET RENTAL OBJECT THINGS DATA
	def get_ro_things_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, rental_object_id, thing_number, thing_name, amount, cost
							  FROM ro_things
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()



	# GET COSTS DATA
	def get_costs_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, rental_object_id, name, is_payer_landlord
							  FROM ro_costs
							  WHERE rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()

	# GET LAST RENTAL OBJECT ID
	def get_last_rental_object_id(self):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""SELECT max(id) FROM rental_objects""")
			return cursor.fetchall()[0][0]


	# GET LINKED AGENT DATA
	def get_linked_agent_data(self, rental_object_id):
		"""вовзращает данные для создания экземпляра клaсса Agent
		   для связанного с объектом аренды агента
		"""
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""SELECT u.id, u.name, u.phone, u.email, ua.id
							  FROM ro_id_agent_id AS riai
							  JOIN users_agents AS ua
							  ON riai.agent_id=ua.id
							  JOIN users AS u
							  ON ua.user_id=u.id
							  WHERE riai.rental_object_id=%s""", (rental_object_id,))
			return cursor.fetchall()[0]

	# DELETE FROM ro_id_agent_id BY RENTAL OBJECT ID

	def delete_from_ro_id_agent_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM ro_id_agent_id WHERE rental_object_id=%s""", (rental_object_id,))	






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


	# GET ALL GENERAL DATA [ro_general]
	def get_ro_general_data(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_object_id, cadastral_number, title_deed FROM ro_general WHERE rental_object_id=%s""", (rental_object_id,))
			return [i for i in cursor.fetchall()[0]]






	# GET ATTRIBUTES [ro_things]: ['things']
	def get_things(self, rental_object_id):
		"""Возвращает данные о вещах в объекте"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, rental_object_id, thing_number, thing_name, amount, cost
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








	# INSERT INTO ro_id_agent_id
	def insert_into_ro_id_agent_id(self, rental_object_id, agent_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ro_id_agent_id(rental_object_id, agent_id)
							  VALUES (%s, %s)""", (rental_object_id, agent_id))




	# INSERT INTO ra_rental_object
	def insert_into_ra_rental_object(self, rental_agreement_id, rental_object_id, type_, address, title_deed):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_rental_object(rental_agreement_id, rental_object_id, type, address, title_deed)
							  VALUES (%s,%s,%s,%s,%s)""", (rental_agreement_id, rental_object_id, type_, address, title_deed))		

	# INSERT INTO ra_landlord
	def insert_into_ra_landlord(self,rental_agreement_id, landlord_id, last_name, first_name, patronymic, phone, 
								email, serie, pass_number, authority, registration):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_landlord(rental_agreement_id, landlord_id, last_name, first_name, patronymic, phone, 
												      email, serie, pass_number, authority, registration)
							  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, landlord_id, last_name, first_name, patronymic, phone, 
							   email, serie, pass_number, authority, registration))						
	# INSERT INTO ra_tenant
	def insert_into_ra_tenant(self, rental_agreement_id, tenant_id, last_name, first_name, patronymic, phone, 
									email, serie, pass_number, authority, registration):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_tenant(rental_agreement_id, tenant_id, last_name, first_name, patronymic, phone, 
												      email, serie, pass_number, authority, registration)
							  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, tenant_id, last_name, first_name, patronymic, phone, 
							   email, serie, pass_number, authority, registration))					

	# INSERT INTO ra_agent
	def insert_into_ra_agent(self, rental_agreement_id, agent_id, last_name, first_name, patronymic, phone, 
									email, serie, pass_number, authority, registration):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_agent(rental_agreement_id, agent_id, last_name, first_name, patronymic, phone, 
												      email, serie, pass_number, authority, registration)
							  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, agent_id, last_name, first_name, patronymic, phone, 
							   email, serie, pass_number, authority, registration))	

	# INSERT INTO ra_other_tenants
	def insert_into_ra_other_tenants(self, rental_agreement_id, name, phone):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_other_tenants(rental_agreement_id, full_name, phone)
							  VALUES (%s,%s,%s)""",
							  (rental_agreement_id, name, phone))		



	# INSERT INTO ra_conditions
	def insert_into_ra_conditions(self, rental_agreement_id, rental_rate, prepayment, deposit, late_fee, 
										start_of_term, end_of_term, payment_day, cleaning_cost):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""INSERT INTO ra_conditions(rental_agreement_id, rental_rate, prepayment, deposit, late_fee, 
														start_of_term, end_of_term, payment_day, cleaning_cost)
							  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, rental_rate, prepayment, deposit, late_fee, 
							   start_of_term, end_of_term, payment_day, cleaning_cost))
	
	# INSERT INTO ra_things
	def insert_into_ra_things(self, rental_agreement_id, thing_number, thing_name, amount, cost):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""INSERT INTO ra_things(rental_agreement_id, thing_number, thing_name, amount, cost)
							  VALUES (%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, thing_number, thing_name, amount, cost))		
	# INSERT INTO ra_costs
	def insert_into_ra_costs(self, rental_agreement_id, name, is_payer_landlord):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""INSERT INTO ra_costs(rental_agreement_id, name, is_payer_landlord)
							  VALUES (%s,%s,%s)""", 
							  (rental_agreement_id, name, is_payer_landlord))
	
	# INSERT INTO ra_move_in
	def insert_into_ra_move_in(self, rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
								  rental_object_comment, things_comment):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""INSERT INTO ra_move_in(rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, 
										  number_of_keys_in_set, rental_object_comment, things_comment)
							  VALUES (%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, 
							   number_of_keys_in_set, rental_object_comment, things_comment))

	# INSERT INTO ra_move_out
	def insert_into_ra_move_out(self, rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
								  rental_object_comment, things_comment, damage_cost, cleaning, rental_agreeement_debts, 
								  deposit_refund, prepayment_refund):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_move_out (rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
								  rental_object_comment, things_comment, damage_cost, cleaning, rental_agreeement_debts, 
								  deposit_refund, prepayment_refund)
							  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
							   rental_object_comment, things_comment, damage_cost, cleaning, rental_agreeement_debts, 
							   deposit_refund, prepayment_refund))

	# INSERT INTO ra_termination
	def insert_into_ra_termination(self, rental_agreement_id, date_of_conclusion, notice_date, end_of_term, is_landlord_initiator):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_termination(rental_agreement_id, date_of_conclusion, notice_date, end_of_term, 
														 is_landlord_initiator)
							  VALUES (%s,%s,%s,%s,%s)""", 
							  (rental_agreement_id, date_of_conclusion, notice_date, end_of_term, is_landlord_initiator))		


	# INSERT INTO ra_renewal
	def insert_into_ra_renewal(self, rental_agreement_id, date_of_conclusion, end_of_term):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_renewal(rental_agreement_id, date_of_conclusion, end_of_term)
							  VALUES (%s,%s,%s)""", (rental_agreement_id, date_of_conclusion, end_of_term))

	# UPDATE status IN rental_agreements
	def update_rental_agreements_status(self, rental_agreement_id, status):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE rental_agreements SET status=%s WHERE id=%s""", (status, rental_agreement_id))		














	# UPDATE ATTRIBUTES [rental_objects]: name, status
	def update_rental_object_name(self, rental_object_id, name):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE rental_objects SET name=%s WHERE id=%s""", (name, rental_object_id,))

	def update_rental_object_status(self, rental_object_id, status):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE rental_objects SET status=%s WHERE id=%s""", (status, rental_object_id,))


	# SET ATTRIBUTES [ro_general]: ['name', 'cadastral_number', 'title_deed']
	def set_ro_general_cadastral_number(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general SET cadastral_number=%s WHERE rental_object_id=%s""", (value, rental_object_id,))

	def set_ro_general_title_deed(self, rental_object_id, value):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general SET title_deed=%s WHERE rental_object_id=%s""", (value, rental_object_id,))


	# SET ALL GENERAL DATA [ro_general]
	def set_ro_general_data(self, rental_object_id, cadastral_number, title_deed):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_general 
							  SET cadastral_number=%s, title_deed=%s 
							  WHERE rental_object_id=%s""", (cadastral_number, title_deed, rental_object_id,))


	# SET ATTRIBUTES [ro_things]: ['things']
	def set_ro_things(self, rental_object_id, things:list):
		with self.context_manager(self.config) as cursor:
			# удаляем все данные о вещах для этого объекта аренды
			cursor.execute("""DELETE FROM ro_things WHERE rental_object_id=%s""", (rental_object_id,))
			# загружаем новые данные
			for i in things:
				cursor.execute("""INSERT INTO ro_things(rental_object_id, thing_number, thing_name, amount, cost) 
							      VALUES (%s, %s, %s, %s, %s)""", 
							      (rental_object_id, i[0], i[1], i[2], i[3]))

	def del_all_things_by_rental_object_id(self, rental_object_id):
		with self.context_manager(self.config) as cursor:
			# удаляем все данные о вещах для этого объекта аренды
			cursor.execute("""DELETE FROM ro_things WHERE rental_object_id=%s""", (rental_object_id,))		


	def update_ro_costs(self, cost_id, name, is_payer_landlord):
		with self.context_manager(self.config) as cursor:
			# обновляем существующие
			cursor.execute("""UPDATE ro_costs 
						      SET name=%s, is_payer_landlord=%s
						      WHERE id=%s""", 
						      (name, is_payer_landlord, cost_id))
			
	def insert_ro_costs(self, rental_object_id, name, is_payer_landlord):
		with self.context_manager(self.config) as cursor:
			# загружаем новые данные
			cursor.execute("""INSERT INTO ro_costs(rental_object_id, name, is_payer_landlord) 
							  VALUES (%s, %s, %s)""", 
						      (rental_object_id, name, is_payer_landlord))

	def del_cost(self, cost_id):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""DELETE FROM ro_costs WHERE id=%s""", (cost_id,))	







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



	def set_ro_object_data(self, rental_object_id, bathroom_type_id, wash_place_id, area, ceilings_height, win_number, balcony, 
							  air_conditioner, wi_fi, furniture):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_object_data 
							  SET bathroom_type_id=%s, 
							  	  wash_place_type_id=%s, 

							  	  area=%s, 
							  	  ceilings_height=%s, 
							      win_number=%s, 

							      balcony=%s, air_conditioner=%s, wi_fi=%s, furniture=%s
							  WHERE rental_object_id=%s""", (bathroom_type_id, wash_place_id, area, ceilings_height, win_number, balcony, 
							  air_conditioner, wi_fi, furniture, rental_object_id,))	



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



	def set_ro_building(self, rental_object_id, building_type_id, floors_number, garbage_disposal, intercom, concierge, building_year):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_building
							  SET building_type_id=%s, floors_number=%s, garbage_disposal=%s, 
							      intercom=%s, concierge=%s, building_year=%s
							  WHERE rental_object_id=%s""", (building_type_id, floors_number, garbage_disposal, 
							  								 intercom, concierge, building_year, rental_object_id))



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


	# SET ALL LOCATION DATA [ro_location]:
	def set_ro_location_data(self, rental_object_id, country, federal_district, region, city, city_district, street, building_number,
					   block_number, appt, entrance_number, floor, coords, nearest_metro_stations, location_comment):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_location
							  SET country=%s, federal_district=%s, region=%s, city=%s, city_district=%s, street=%s, building_number=%s,
					   			  block_number=%s, appt=%s, entrance_number=%s, floor=%s, coords=%s, nearest_metro_stations=%s, location_comment=%s
					   		  WHERE rental_object_id=%s""", 
					   		  ( country, federal_district, region, city, city_district, street, building_number,
					   block_number, appt, entrance_number, floor, coords, nearest_metro_stations, location_comment, rental_object_id))





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


	# SET ALL APPLIANCES DATA [ro_appliances]:
	def set_ro_appliances_data(self, rental_object_id,  fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""UPDATE ro_appliances
							  SET fridge=%s, dishwasher=%s, washer=%s, television=%s, vacuum=%s, teapot=%s, iron=%s, microwave=%s
							  WHERE rental_object_id=%s""", 
							  (fridge, dishwasher, washer, television, vacuum, teapot, iron, microwave,rental_object_id))	

	# SET ALL ROOM DATA [ro_room]:
	def set_ro_room_data(self, rental_object_id, total_area, rooms_number):
		with self.context_manager(self.config) as cursor: 
			cursor.execute("""UPDATE ro_room 
							  SET total_area=%s, rooms_number=%s
							  WHERE rental_object_id=%s""", 
							  (total_area, rooms_number, rental_object_id))		




class RentalAgreementDM:
	def add_rental_agreement_status(self, status):
		"""Добавление типа пользователей"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""INSERT INTO ra_status(status) VALUES (%s)""", (status,))

	"""Создание договора аренды"""
	def create_rental_agreement(self, agreement_number, city, date_of_conclusion, status, landlord_id):
		with self.context_manager(self.config) as cursor:
			# создаем таблицу договоров аренды
			cursor.execute("""INSERT INTO rental_agreements(agreement_number, city, date_of_conclusion,  status)
						      VALUES (%s, %s, %s, %s)""", (agreement_number, city, date_of_conclusion, status))
			
			# получаем последний добавленный в таблицу rental_agreements id
			cursor.execute("""SELECT id FROM rental_agreements WHERE id=LAST_INSERT_ID()""") 
			rental_agreement_id = cursor.fetchall()[0][0] 

			# добавляем связь договора с наймодателем через таблицу users_landlord_id_rental_agreements_id
			cursor.execute("""INSERT INTO users_landlord_id_rental_agreements_id(landlord_id, rental_agreement_id)
							  VALUES (%s, %s)""", (landlord_id, rental_agreement_id))			



	def delete_rental_agreement(self, rental_agreement_id):
		"""удаление договора аренды"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""DELETE FROM rental_agreements WHERE id=%s""", (rental_agreement_id,))		










	# FOR RENATAL OBJECTS DATA OF LADLORD OUTPUT
	def get_rental_agreement_id_of_landlord(self, landlord_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id FROM users_landlord_id_rental_agreements_id WHERE landlord_id=%s""", (landlord_id,))
			return [i[0] for i in cursor.fetchall()]





	def get_rental_agreement_data_of_landlord(self, landlord_id):
		"""возвращает данные всех договоров аренды данного наймодателя
		"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT ra.id, ra.agreement_number, ra.city, ra.date_of_conclusion, ra.status 
						      FROM rental_agreements AS ra
						      JOIN users_landlord_id_rental_agreements_id AS ulira
						      ON ulira.rental_agreement_id=ra.id
						      WHERE ulira.landlord_id=%s""", (landlord_id,))
			return cursor.fetchall()


	# GET RANTAL OBJECT DATA BY RENATAL AGREEMENT ID
	def get_rental_object_data_by_rental_agreement_id(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:	
			cursor.execute("""SELECT ro.id, rot.type, ro.name, ro.status
							  FROM rental_objects AS ro
							  JOIN ra_id_rental_object_id AS riroi
							  ON ro.id=riroi.rental_object_id
							  JOIN rental_object_types AS rot
							  ON ro.type_id=rot.id
							  WHERE riroi.rental_agreement_id = %s""", (rental_agreement_id,))
			return cursor.fetchall()



	def get_last_agreement_number(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT max(agreement_number) FROM rental_agreements""")
			return cursor.fetchall()[0][0]


	def get_last_agreement_id(self):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT max(id) FROM rental_agreements""")
			return cursor.fetchall()[0][0]			


	# GET RENTAL AGREEMENT DATA
	def get_rental_agreement_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, agreement_number, city, date_of_conclusion, status
							  FROM rental_agreements
							  WHERE id=%s""", (rental_agreement_id,))
			return [i for i in cursor.fetchall()[0]]



	# GET RENTAL OBJECT DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_rental_object_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rro.rental_agreement_id, rro.rental_object_id, rot.type, rro.address, rro.title_deed
							  FROM ra_rental_object AS rro 
							  JOIN rental_object_types AS rot
							  ON rro.type=rot.id
							  WHERE rro.rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0]

	# GET LANDLORD DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_landlord_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT landlord_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration
							  FROM ra_landlord 
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0]

	# GET TENANT DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_tenant_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT tenant_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration
							  FROM ra_tenant 
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0]

	# GET AGENT DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_agent_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT agent_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration
							  FROM ra_agent 
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0]

	# GET CONDITIONS DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_conditions_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id, rental_rate, prepayment, deposit, late_fee, 
									 start_of_term, end_of_term, payment_day, cleaning_cost
							  FROM ra_conditions
							  WHERE rental_agreement_id=%s""", (rental_agreement_id ,))
			return cursor.fetchall()[0]		

	# GET MOVE-IN DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_move_in_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
									 rental_object_comment, things_comment
							  FROM ra_move_in
							  WHERE rental_agreement_id=%s""", (rental_agreement_id ,))
			return cursor.fetchall()[0]		

	# GET MOVE-IN DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_move_out_data(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id, date_of_conclusion, number_of_sets_of_keys, number_of_keys_in_set, 
									 rental_object_comment, things_comment, damage_cost, cleaning, 
									 rental_agreeement_debts, deposit_refund, prepayment_refund
							  FROM ra_move_out
							  WHERE rental_agreement_id=%s""", (rental_agreement_id ,))
			return cursor.fetchall()[0]	

	# GET TERMINATION DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_termination(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id, date_of_conclusion, notice_date, end_of_term, is_landlord_initiator
							  FROM ra_termination
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()[0]

	# GET RENEWAL DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_renewal(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_agreement_id, date_of_conclusion, end_of_term
							  FROM ra_renewal
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()

	# GET THINGS DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_things(self, rental_agreement_id):
		"""Возвращает данные о вещах в объекте"""
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, rental_agreement_id, thing_number, thing_name, amount, cost
							  FROM ra_things
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			things = []
			for thing in cursor.fetchall():
				things.append([i for i in thing])
			return things

	# GET COSTS DATA (CURRENT RENATAL AGREEMENT)
	def get_ra_costs(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT id, rental_agreement_id, name, is_payer_landlord
							  FROM ra_costs
							  WHERE rental_agreement_id=%s""", (rental_agreement_id,))
			return cursor.fetchall()









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


	# GET ATTRIBUTES [ra_conditions]: ['rental_rate', 'prepayment', 'deposit', 'late_fee', 'start_of_term', 'end_of_term', 'ayment_day']
	def get_ra_general_conditions_rental_rate(self, rental_agreement_id):
		with self.context_manager(self.config) as cursor:
			cursor.execute("""SELECT rental_rate FROM ra_conditions WHERE rental_agreement_id=%s""", (rental_agreement_id,))
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

		bathroom_types = ['не указано','совмещенный', 'раздельный']
		for type_ in bathroom_types:
			self.add_bathroom_type(type_)

		wash_place_type = ['не указано', 'ванна', 'душевая кабина']
		for type_ in wash_place_type:
			self.add_wash_place_type(type_)

		building_type = ['не указано', 'кирпичный', 'панельный'] 
		for type_ in building_type:
			self.add_building_type(type_)

		countries = ['Российская Федерация']
		for country in countries:
			self.add_country(country)

		city_data = [(1,'Санкт-Петербург'), (1, 'Москва')]
		for country_id, city in city_data:
			self.add_city(country_id, city)

		self.create_user('администратор', 'Админ Никита', '+792188550028', 'admin@admin.ru', 'admin', generate_password_hash('12345'))


		rental_object_statuses = ['свободен', 'занят', 'не сдается']
		for status in rental_object_statuses:
			self.add_rental_object_status(status)

		rental_agreement_statuses = ['заключен', 'досрочно расторгнут', 'завершен', 'продлен'] 
		for status in rental_agreement_statuses:
			self.add_rental_agreement_status(status)

		self.add_districts_data()

		self.add_metro_station_data()



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
			...
			

if __name__ == '__main__':
	...
