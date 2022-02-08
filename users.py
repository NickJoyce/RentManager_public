from passport import Passport
from register import Register

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataDefinition # класс для определения и модификации объектов(таблиц, базданных)
from database.use_db import DataManipulation # класс для манипулирования данными в БД

db_def = DataDefinition(db_config, DBcm)
db = DataManipulation(db_config, DBcm) # экземпляр класса для взаимодействия с БД


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

	def get_empty_strings(self):
		"""Возвращает список названий полей, данные в которых являются пустыми строками
		   и которые используются для записи в таблицы ra_landlord, ra_tenant, ra_agent
		"""
		strs = {'телефон':self.phone, 'email':self.email, }
		empty_strs = []
		for name, str_ in strs.items():
			if str_ == '':
				empty_strs.append(name)
		return empty_strs

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
	agent = Agent(*db.get_linked_agent_data(59))





