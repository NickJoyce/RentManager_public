from datetime import date
# from prettytable import PrettyTable

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД



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










if __name__ == '__main__':
	passport = Passport(1)


	print(passport._user_id)
	print(passport._first_name)
	print(passport._patronymic)
	print(passport._last_name)
	print(passport._serie)
	print(passport._pass_number)
	print(passport._authority)
	print(passport._department_code)
	print(passport._date_of_issue)
	print(passport._date_of_birth)
	print(passport._place_of_birth)
	print(passport._registration)

	print(passport.user_id)
	print(passport.first_name)
	print(passport.patronymic)
	print(passport.last_name)
	print(passport.serie)
	print(passport.pass_number)
	print(passport.authority)
	print(passport.department_code)
	print(passport.date_of_issue)
	print(passport.date_of_birth)
	print(passport.place_of_birth)
	print(passport.registration)

	passport.first_name = 'Никита'
	passport.patronymic = 'Алексеевич'
	passport.last_name = 'Смирнов'
	passport.serie = '4008'
	passport.pass_number = '522493'
	passport.authority = 'ТП №81'
	passport.department_code = '380-012'
	passport.date_of_issue = date(2008, 7, 7)
	passport.date_of_birth = date(1988, 6, 23)
	passport.place_of_birth = 'г. Ленинград'
	passport.registration = 'Санкт-Петербург, ул. гороховая 32-95'

	print(passport.user_id)
	print(passport.first_name)
	print(passport.patronymic)
	print(passport.last_name)
	print(passport.serie)
	print(passport.pass_number)
	print(passport.authority)
	print(passport.department_code)
	print(passport.date_of_issue)
	print(passport.date_of_birth)
	print(passport.place_of_birth)
	print(passport.registration)

