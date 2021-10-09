from prettytable import PrettyTable

class Register:
	def __init__(self, login, password):
		self.login = login
		self.password = password

	def __repr__(self):
		return f"{self.__class__.__name__}({self.login}, {self.password})"

	def __str__(self): 
		register_data = PrettyTable()
		rd = register_data
		rd.field_names = ["login", "password"] # column name
		rd._min_width = {"login" : 20, "password" : 20} # column width 
		rd.add_row([self.login, self.password])	
		return str(rd)


	# ГЕТТЕРЫ И СЕТТЕРЫ
	@property
	def login(self):
		return self._login

	@login.setter
	def login(self, value):
		# проверки для value
		self._login = value
	
	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, value):
		# проверки для password
		self._password = value


if __name__ == '__main__':
	register = Register('1234', '1234')
	print(register)

