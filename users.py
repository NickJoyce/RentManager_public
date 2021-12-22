from passport import Passport
from register import Register

class User:

	def __init__(self, user_id, name, phone, email, user_type=''):
		# БАЗОВАЯ ИНФОРМАЦИЯ
		self.user_id = user_id

		self.user_type = user_type

		self.name = name 
		self.phone = phone  
		self.email = email 

		self.passport = None
		self.register = None 


	def chek_email(self):
		errors = []
		# вхождение символов '@' и '.'
		if '@' not in self.email or '.' not in self.email:
			errors.append('Неверный email')
		return errors

class Admin(User):
	def __init__(self, user_id, name, phone, email, admin_id, user_type='администратор'):
		super().__init__(user_id, name, phone, email, user_type,)
		self.admin_id = admin_id

	
class Landlord(User):
	def __init__(self, user_id, name, phone, email, landlord_id, inn, user_type='наймодатель'):
		super().__init__(user_id, name, phone, email, user_type)
		self.landlord_id = landlord_id
		self.inn = inn # ИНН



class Tenant(User):
	def __init__(self, user_id, name, phone, email, tenant_id, user_type='наниматель'):
		super().__init__(user_id, name, phone, email, user_type)
		self.tenant_id = tenant_id

	def __repr__(self):
		return f'({self.user_id}, {self.name}, {self.phone}, {self.email}, {self.tenant_id}, {self.user_type})'



class Agent(User):
	def __init__(self,  user_id, name, phone, email, agent_id, user_type='агент'):
		super().__init__(user_id, name, phone, email, user_type)
		self.agent_id = agent_id

	def __repr__(self):
		return f'({self.user_id}, {self.name}, {self.phone}, {self.email}, {self.agent_id}, {self.user_type})'





if __name__ == '__main__':
	...







# TRASH


# # ВЗАИМОДЕЙСТВИЕ С БД
# from database.config import db_config # параметры для подключения к БД
# from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

# from database.use_db import DataManipulation # класс для манипулирования данными в БД


	# @property
	# def landlord_id(self):
	# 	if self._landlord_id == None:
	# 		self._landlord_id = self.db.get_landlord_id(self.user_id)
	# 	return self._landlord_id

	# @property
	# def inn(self):
	# 	if self._inn == None:
	# 		self._inn = self.db.get_landlord_inn(self.user_id)
	# 	return self._inn
	# @inn.setter
	# def inn(self, value):
	# 	self.db.set_landlord_inn(self.user_id, value) # записывам новое значение в БД
	# 	self._inn = value # присваиваем новое значение атрибуту

		# self._db = None
	
	# Для значений в таблице обязательно должно быть соблюдено условия NOT NULL, чтобы коректно отрабатывали условия с None

	# @property
	# def user_id(self):
	# 	return self._user_id

	# @property
	# def db(self): 
	# 	if self._db == None:
	# 		self._db = DataManipulation(db_config, DBcm)
	# 	return self._db

	# @property
	# def passport(self): 
	# 	if self._passport == None:
	# 		self._passport = Passport(self.user_id)
	# 	return self._passport


	# @property
	# def register(self): 
	# 	if self._register == None:
	# 		self._register = Register(self.user_id)
	# 	return self._register



	# @property
	# def user_type_id(self): 
	# 	if self._user_type_id == None:
	# 		self._user_type_id = self.db.get_user_type_id(self.user_id)
	# 	return self._user_type_id


	# @property
	# def name(self): 
	# 	if self._name == None:
	# 		self._name = self.db.get_user_name(self.user_id)
	# 	return self._name
	# @name.setter
	# def name(self, value): 
	# 	self.db.set_user_name(self.user_id, value) # записывам новое значение в БД
	# 	self._name = value # присваиваем новое значение атрибуту

	# @property
	# def phone(self): 
	# 	if self._phone == None:
	# 		self._phone = self.db.get_user_phone(self.user_id)
	# 	return self._phone
	# @phone.setter
	# def phone(self, value): 
	# 	self.db.set_user_phone(self.user_id, value)
	# 	self._phone = value


	# @property
	# def email(self): 
	# 	if self._email == None:
	# 		self._email = self.db.get_user_email(self.user_id)
# 		return self._email
# 	@email.setter
# 	def email(self, value): 
# 		self.db.set_user_email(self.user_id, value) # записывам новое значение в БД
# 		self._email = value # присваиваем новое значение атрибуту



	# @property
	# def admin_id(self):
	# 	if self._admin_id == None:
	# 		self._admin_id = self.db.get_admin_id(self.user_id)
	# 	return self._admin_id



	# @property
	# def landlord_id(self):
	# 	if self._landlord_id == None:
	# 		self._landlord_id = self.db.get_landlord_id(self.user_id)
	# 	return self._landlord_id


	# @property
	# def tenant_id(self):
	# 	if self._tenant_id == None:
	# 		self._tenant_id = self.db.get_tenant_id(self.user_id)
	# 	return self._tenant_id



	# @property
	# def agent_id(self):
	# 	if self._agent_id == None:
	# 		self._agent_id = self.db.get_agent_id(self.user_id)
	# 	return self._agent_id