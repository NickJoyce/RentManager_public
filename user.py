from passport import Passport

class User:
	NEXT_USER_ID = 142857
	LAST_USER_ID = 0
	USER_ID_LIST = [] # список id пользоватлей


	def __init__(self, name: str, phone: str, email: str, user_type='user', passport=None):
		self.user_type = user_type # тип пользователя
		self.name = name # Имя
		self.phone = phone # Телефон
		self.email = email # e-mail
		self.passport = passport # экземпляр класса с паспортными данными
		self.is_passport = False # флаг добавления паспортных данных
		self.is_set_user_id = False # флаг создания id
		self.user_id = self.NEXT_USER_ID  # id пользователя для созданного экземпляра
		__class__.LAST_USER_ID = self.user_id # последнее присвоенное id
		__class__.USER_ID_LIST.append(self.NEXT_USER_ID) # добавляем id пользоватлеля в список
		__class__.NEXT_USER_ID += 1 # увеличиваем значение для следующего id
		
		

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name}, {self.phone}, {self.email}, {self.user_type})"


	@property
	def user_id(self):
		return self._user_id

	@user_id.setter
	def user_id(self, value):
		if self.is_set_user_id == False: # id устанавливается только при создании экземпляра, 1 раз
			self._user_id = value
			self.is_set_id = True
		else:
			raise Warning ('Невозможно изменить id пользователя')



	def add_passport(self, passport_data: (list, tuple)):
		"""Добавляет паспортные данные"""
		self.passport = Passport(*passport_data) # экземпляр класса Passport
		self.is_passport = True

	def drop_passport(self):
		"""Очищает паспортные данные"""
		self.passport = None
		self.is_passport = False



class Admin(User):
	def __init__(self, name = '-', phone = '-', email = '-', user_type='admin'):
		super().__init__(name, phone, email, user_type)



class Landlord(User):
	def __init__(self, name: str, phone: str, email: str, basis_for_rent: str, user_type='landlord'):
		super().__init__(name, phone, email, user_type)
		self.basis_for_rent = basis_for_rent # документ-основание для сдачи в аренду



class Tenant(User):
	def __init__(self, name: str, phone: str, email: str, user_type='tenant'):
		super().__init__(name, phone, email, user_type)


if __name__ == "__main__":
	admin = Admin()

	landlord_data = ['Смирнов Никита Алексеевич', 911, '55@sdsd.ru', 'Договор дарения 78 АБ 4270028']
	landlord = Landlord(*landlord_data)

	tenant_data = ['Никита', 911, '55@sdsd.ru']
	tenant = Tenant(*tenant_data)
	tenant2 = Tenant(*tenant_data)

	print(admin)
	print(landlord)
	print(tenant)

	print(admin.user_id)
	print(landlord.user_id)
	print(tenant.user_id)
	print(tenant2.user_id)

	# tenant.user_id = 142860



	print(User.NEXT_USER_ID, User.LAST_USER_ID)



	print(tenant.USER_ID_LIST)


	from datetime import date
	pd = ['Никита',
	      'Алексеевич',
		  'Фролов',
		  4345,
		  601588,
		 'ТП №56 северного района гор. Санкт-Петербурга',
		 '503-304',
		 date(2006, 2, 11),
		 date(1986, 3, 25),
		 'Ленинград',
		 'Санкт-Петербург, Невский проспект 50-12']

	tenant.add_passport(pd)
	print(tenant.passport)
	print(tenant.is_passport)
	tenant.passport.first_name = 'Василий' # изменение паспортных данных
	print(tenant.passport.first_name) 

