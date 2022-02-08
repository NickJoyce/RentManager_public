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
















