from passport import Passport
from register import Register
from datetime import date
from prettytable import PrettyTable



class User:
	USER_ID_LIST = [] # список id пользоватлей
	COUNT = 0 # подсчет количетва экземпляров класса User

	def __init__(self, user_id, type_id, name, phone, email):
		# БАЗОВАЯ ИНФОРМАЦИЯ
		self.is_set_user_id = False # флаг создания id
		self.user_id = user_id
		self.type_id = type_id
		self.name = name # Имя
		self.phone = phone # Телефон
		self.email = email # e-mail

		self.passport = None
		self.register = None


		__class__.USER_ID_LIST.append(self.user_id) # добавляем id пользоватлеля в список

		__class__.COUNT += 1

		
	def __repr__(self):
		return f"{self.__class__.__name__}({self.user_id})"




	@property
	def user_id(self):
		return self._user_id

	@user_id.setter
	def user_id(self, value):
		if self.is_set_user_id == True: # попытка изменить id после создания экземпляра
			raise Warning ('Невозможно изменить id пользователя')
		elif value in __class__.USER_ID_LIST: # добавление новго экземпляра с таким же id как у добвленного 
			raise Warning ('Пользователь с таким id уже существует')
		else:
			self._user_id = value
			self.is_set_user_id = True

	# ПАСПОРТНЫЕ ДАННЫЕ
	def passport_default(self):
		"""Очищает паспортные данные"""
		self.passport = None
		self.passport = Passport()

	# РЕГИСТРАЦИОННЫЕ ДАННЫЕ
	def register_default(self):
		"""Добавляет регестрационные данные"""
		self.register = None
		self.register = Register()


class Landlord(User):
	COUNT = 0 # подсчет количетва экземпляров класса Landlord
	def __init__(self, user_id, type_id, name, phone, email, landlord_id, inn):
		super().__init__(user_id, type_id, name, phone, email)
		self.landlord_id = landlord_id
		self.inn = inn # документ-основание для сдачи в аренду
		__class__.COUNT += 1

	def __str__(self):
		user_data = PrettyTable()
		ud = user_data
		ud.field_names = ["id", "type_id", "name", "phone", "email","landlord_id", "inn"] # column name
		ud._min_width = {"id" : 10, "type_id":10, "name": 20, "phone": 20, "email": 20, "Landlord_id":10, "inn":20} # column width 
		ud.align["name"] = "l" # text-align: left
		ud.align["phone"] = "l" # text-align: left
		ud.align["email"] = "l" # text-align: left
		ud.align["basis_for_rent_document"] = "l" # text-align: left
		ud.add_row([self.user_id, self.type_id, self.name, self.phone, self.email, self.landlord_id, self.inn])	
		return str(ud)



class Tenant(User):
	COUNT = 0 # подсчет количетва экземпляров класса Tenant
	def __init__(self, user_id, type_id, name, phone, email, tenant_id):
		super().__init__(user_id, type_id, name, phone, email)
		self.tenant_id = tenant_id
		__class__.COUNT += 1

	def __str__(self):
		user_data = PrettyTable()
		ud = user_data
		ud.field_names = ["id", "type_id", "name", "phone", "email", "tenant_id"] # column name
		ud._min_width = {"id" : 10, "type_id":10, "name": 20, "phone": 20, "email": 20, "tenant_id":10} # column width 
		ud.align["name"] = "l" # text-align: left
		ud.align["phone"] = "l" # text-align: left
		ud.align["email"] = "l" # text-align: left
		ud.add_row([self.user_id, self.type_id, self.name, self.phone, self.email, self.tenant_id])	
		return str(ud)


class Agent(User):
	COUNT = 0 # подсчет количетва экземпляров класса Agent
	def __init__(self, user_id, type_id, name, phone, email, agent_id):
		super().__init__(user_id, type_id, name, phone, email)
		self.agent_id = agent_id
		__class__.COUNT += 1

	def __str__(self):
		user_data = PrettyTable()
		ud = user_data
		ud.field_names = ["id", "type_id", "name", "phone", "email", "agent_id"] # column name
		ud._min_width = {"id" : 10, "type_id":10, "name": 20, "phone": 20, "email": 20, "agent_id":10} # column width 
		ud.align["name"] = "l" # text-align: left
		ud.align["phone"] = "l" # text-align: left
		ud.align["email"] = "l" # text-align: left
		ud.add_row([self.user_id, self.type_id, self.name, self.phone, self.email, self.agent_id])	
		return str(ud)

class Admin(User):
	COUNT = 0 # подсчет количетва экземпляров класса Admin
	def __init__(self, user_id, type_id, name, phone, email, admin_id):
		super().__init__(user_id, type_id, name, phone, email)
		self.admin_id = admin_id
		__class__.COUNT += 1

	def __str__(self):
		user_data = PrettyTable()
		ud = user_data
		ud.field_names = ["id", "type_id", "name", "phone", "email", "admin_id"] # column name
		ud._min_width = {"id" : 10, "type_id":10, "name": 20, "phone": 20, "email": 20, "admin_id":10} # column width 
		ud.align["name"] = "l" # text-align: left
		ud.align["phone"] = "l" # text-align: left
		ud.align["email"] = "l" # text-align: left
		ud.add_row([self.user_id, self.type_id, self.name, self.phone, self.email, self.admin_id])	
		return str(ud)




if __name__ == "__main__":
	...




	
