from datetime import date
# from prettytable import PrettyTable

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataDefinition # класс для определения и модификации объектов(таблиц, базданных)
from database.use_db import DataManipulation # класс для манипулирования данными в БД

db_def = DataDefinition(db_config, DBcm)
db = DataManipulation(db_config, DBcm) # экземпляр класса для взаимодействия с БД



class Passport:
		
	# _DB = None

	# @property
	# def DB(self): 
	# 	if self._DB == None: 
	# 		_DB = DataManipulation(db_config, DBcm)
	# 	return _DB

	def __init__(self, user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
					   department_code, date_of_issue, date_of_birth, place_of_birth, registration):
		self._user_id = user_id # id пользователя
		self.first_name = first_name  # имя
		self.patronymic = patronymic # отчетсво
		self.last_name = last_name # фамилия
		self.serie = serie # серия
		self.pass_number = pass_number # номер
		self.authority = authority # орган выдавший паспорт
		self.department_code = department_code   # код подразделения
		self.date_of_issue = date_of_issue # дата выдачи
		self.date_of_birth = date_of_birth # дата рождения
		self.place_of_birth = place_of_birth # место рождения
		self.registration = registration # адрес прописки

	def get_empty_strings(self):
		"""Возвращает список названий полей, данные в которых являются пустыми строками
		   и которые используются для записи в таблицы ra_landlord, ra_tenant, ra_agent
		"""
		strs = {'фамилия':self.last_name, 'имя':self.first_name, 'отчество':self.patronymic, 'серия':self.serie, 
				 'номер':self.pass_number, 'орган выдавший паспорт':self.authority, 'прописка':self.registration}
		empty_strs = []
		for name, str_ in strs.items():
			if str_ == '':
				empty_strs.append(name)
		return empty_strs








if __name__ == '__main__':
	passport = Passport(*db.get_passport_data(18))
	print(passport.get_empty_strings())







	# # Для значений в таблице обязательно должно быть соблюдено условия NOT NULL, чтобы коректно отрабатывали условия с None

	# @property
	# def user_id(self): 
	# 	return self._user_id


	# @property
	# def first_name (self):
	# 	if self._first_name == None: 
	# 		self._first_name  = self.DB.get_passport_first_name(self.user_id)
	# 	return self._first_name 
	# @first_name.setter
	# def first_name(self, value): 
	# 	self.DB.set_passport_first_name(self.user_id, value) # записывам новое значение в БД
	# 	self._first_name = value # присваиваем новое значение атрибуту


	# @property
	# def patronymic(self): 
	# 	if self._patronymic == None: 
	# 		self._patronymic = self.DB.get_passport_patronymic(self.user_id)
	# 	return self._patronymic
	# @patronymic.setter
	# def patronymic(self, value):
	# 	self.DB.set_passport_patronymic(self.user_id, value) # записывам новое значение в БД
	# 	self._patronymic = value # присваиваем новое значение атрибуту

	# @property
	# def last_name(self):
	# 	if self._last_name == None: 
	# 		self._last_name = self.DB.get_passport_last_name(self.user_id)
	# 	return self._last_name
	# @last_name.setter
	# def last_name(self, value): 
	# 	self.DB.set_passport_last_name(self.user_id, value) # записывам новое значение в БД
	# 	self._last_name = value # присваиваем новое значение атрибуту

	# @property
	# def serie(self): 
	# 	if self._serie == None:
	# 		self._serie = self.DB.get_passport_serie(self.user_id)
	# 	return self._serie
	# @serie.setter
	# def serie(self, value):
	# 	self.DB.set_passport_serie(self.user_id, value) # записывам новое значение в БД
	# 	self._serie = value # присваиваем новое значение атрибуту

	# @property
	# def pass_number(self): 
	# 	if self._pass_number == None:
	# 		self._pass_number = self.DB.get_passport_pass_number(self.user_id)
	# 	return self._pass_number
	# @pass_number.setter
	# def pass_number(self, value):
	# 	self.DB.set_passport_pass_number(self.user_id, value) # записывам новое значение в БД
	# 	self._pass_number = value # присваиваем новое значение атрибуту

	# @property
	# def authority(self): 
	# 	if self._authority == None:
	# 		self._authority = self.DB.get_passport_authority(self.user_id)
	# 	return self._authority
	# @authority.setter
	# def authority(self, value):
	# 	self.DB.set_passport_authority(self.user_id, value) # записывам новое значение в БД
	# 	self._authority = value # присваиваем новое значение атрибуту


	# @property
	# def department_code(self): 
	# 	if self._department_code == None:
	# 		self._department_code = self.DB.get_passport_department_code(self.user_id)
	# 	return self._department_code
	# @department_code.setter
	# def department_code(self, value): 
	# 	self.DB.set_passport_department_code(self.user_id, value) # записывам новое значение в БД
	# 	self._department_code = value # присваиваем новое значение атрибуту


	# @property
	# def date_of_issue(self): 
	# 	if self._date_of_issue == None:
	# 		self._date_of_issue = self.DB.get_passport_date_of_issue(self.user_id)
	# 	return self._date_of_issue
	# @date_of_issue.setter
	# def date_of_issue(self, value): 
	# 	self.DB.set_passport_date_of_issue(self.user_id, value) # записывам новое значение в БД
	# 	self._date_of_issue = value # присваиваем новое значение атрибуту



	# @property
	# def date_of_birth(self): 
	# 	if self._date_of_birth == None:
	# 		self._date_of_birth = self.DB.get_passport_date_of_birth(self.user_id)
	# 	return self._date_of_birth
	# @date_of_birth.setter
	# def date_of_birth(self, value):
	# 	self.DB.set_passport_date_of_birth(self.user_id, value) # записывам новое значение в БД
	# 	self._date_of_birth = value # присваиваем новое значение атрибуту


	# @property
	# def place_of_birth(self): 
	# 	if self._place_of_birth== None:
	# 		self._place_of_birth = self.DB.get_passport_place_of_birth(self.user_id)
	# 	return self._place_of_birth
	# @place_of_birth.setter
	# def place_of_birth(self, value): 
	# 	self.DB.set_passport_place_of_birth(self.user_id, value) # записывам новое значение в БД
	# 	self._place_of_birth = value # присваиваем новое значение атрибуту



	# @property
	# def registration(self): 
	# 	if self._registration == None:
	# 		self._registration = self.DB.get_passport_registration(self.user_id)
	# 	return self._registration
	# @registration.setter
	# def registration(self, value): 
	# 	self.DB.set_passport_registration(self.user_id, value) # записывам новое значение в БД
	# 	self._registration = value # присваиваем новое значение атрибуту












