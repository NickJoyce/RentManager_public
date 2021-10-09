from passport import Passport
from register import Register
from datetime import date
from prettytable import PrettyTable

class User:
	USER_ID_LIST = [] # список id пользоватлей
	COUNT = 0 # подсчет количетва экземпляров класса User

	def __init__(self, user_id: int, name: str, phone: str, email: str, user_type='user', passport=None, register=None):
		self.is_set_user_id = False # флаг создания id
		self.user_id = user_id
		self.user_type = user_type # тип пользователя
		self.name = name # Имя
		self.phone = phone # Телефон
		self.email = email # e-mail

		self.register = register # экземпляр класса Register (регистрационные данные)

		self.passport = passport # экземпляр класса Passport (паспортные данные)
		self.is_passport = False # флаг добавления паспортных данных

		__class__.USER_ID_LIST.append(self.user_id) # добавляем id пользоватлеля в список

		__class__.COUNT += 1

		
	def __repr__(self):
		return f"{self.__class__.__name__}({self.user_id}, {self.name}, {self.phone}, {self.email}, {self.user_type})"

	def __str__(self):
		user_data = PrettyTable()
		ud = user_data
		ud.field_names = ["id", "name", "phone", "email", "user_type"] # column name
		ud._min_width = {"id" : 10, "name": 20, "phone": 20, "email": 20, "user_type": 20} # column width 
		ud.align["name"] = "l" # text-align: left
		ud.align["phone"] = "l" # text-align: left
		ud.align["email"] = "l" # text-align: left
		ud.align["user_type"] = "l" # text-align: left
		ud.add_row([self.user_id, self.name, self.phone, self.email, self.user_type])	
		return str(ud)


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
	def add_passport(self, passport_data: (list, tuple)):
		"""Добавляет паспортные данные"""
		self.passport = Passport(*passport_data) # экземпляр класса Passport
		self.is_passport = True

	def drop_passport(self):
		"""Очищает паспортные данные"""
		self.passport = None
		self.is_passport = False

	# РЕГИСТРАЦИОННЫЕ ДАННЫЕ
	def reg(self, login, password):
		"""Добавляет регестрационные данные"""
		self.register = Register(login, password)


class Admin(User):
	COUNT = 0 # подсчет количетва экземпляров класса Admin
	def __init__(self, user_id, name = '-', phone = '-', email = '-', user_type='admin'):
		super().__init__(user_id, name, phone, email, user_type)
		__class__.COUNT += 1


class Landlord(User):
	COUNT = 0 # подсчет количетва экземпляров класса Landlord
	def __init__(self, user_id, name: str, phone: str, email: str, basis_for_rent: str, user_type='landlord'):
		super().__init__(user_id, name, phone, email, user_type)
		self.basis_for_rent = basis_for_rent # документ-основание для сдачи в аренду
		__class__.COUNT += 1


class Tenant(User):
	COUNT = 0 # подсчет количетва экземпляров класса Tenant
	def __init__(self, user_id, name: str, phone: str, email: str, user_type='tenant'):
		super().__init__(user_id, name, phone, email, user_type)
		__class__.COUNT += 1



if __name__ == "__main__":

	sofia = Landlord(2, 'София', '+79218887722', 'sofia@mail.ru', 'Дговор купли-продажи 78 АБ')
	print(sofia)
	sofia_passport_data = ['София',
				 'Алексеевна',
				 'Бонд',
				 4345,
				 601588,
				 'ТП №56 северного района гор. Санкт-Петербурга',
				 '503-304',
				 date(2006, 2, 11),
				 date(1986, 3, 25),
				 'Ленинград',
				 'Санкт-Петербург, Невский проспект 50-12']

	sofia.add_passport(sofia_passport_data)

	sofia.reg('sofia1234', 'xc2sacv45')

	print(sofia.passport)

	print(sofia.register)




	

	nikita = Admin(1)
	ashot = Tenant(3, 'Ашот', '+79110998723', 'ashot@mail.ru')
	ashot_passport_data = ['Ашот',
			 'Саркесянович',
			 'Ахмедов',
			 4145,
			 611588,
			 'ТП №23 горного райна Дагестана',
			 '503-304',
			 date(2003, 5, 12),
			 date(1980, 4, 1),
			 'Село Мужская честь',
			 'Краснодарский край, Село Мужская честь, ул. Брутальная 12']

	ashot.add_passport(ashot_passport_data)
	ashot.reg('ashot1', 'dcgds002')



