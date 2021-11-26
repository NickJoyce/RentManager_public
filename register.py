from werkzeug.security import generate_password_hash, check_password_hash # шифрование паролей

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД


class Register:

	# _DB = None

	# @property
	# def DB(self): 
	# 	if self._DB == None: 
	# 		_DB = DataManipulation(db_config, DBcm)
	# 	return _DB


	def __init__(self, login, password, user_id=None):
		self.user_id = user_id
		self.login = login
		self.password = password
		self.hashed_password = None



	def chek_login(self, existed_logins: list):
		errors = []
		# количество символов
		if len(self.login) < 4:
			errors.append('Логин меньше 4 символов')

		# допустимые значения
		for i in self.login:
			if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
				errors.append(f"Символ '{i}' недопустим. В логине могут быть использованы строчные и заглавные буквы латинского алфавита, а также цифры")
				break

		if self.login in existed_logins:
			errors.append('Такой логин уже существует')
		return errors



	def chek_password(self):
		"""Проверка корректности введенного пароля"""
		errors = []
		# количество символов
		if len(self.password) < 4:
			errors.append('Пароль меньше 4 символов')
		# допустимые значения
		for i in self.password:
			if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
				errors.append(f"Символ '{i}' недопустим. В пароле могут быть использованы строчные и заглавные буквы латинского алфавита, а также цифры")
				break
		return errors


	@staticmethod
	def is_correct_password(hash_pwd, current_pwd):
		"""Проверка соответствия введенного пароля"""
		if check_password_hash(hash_pwd, current_pwd): 
			return True
		else:
			return False


	def generate(self):
		self.hashed_password = generate_password_hash(self.password)


	# # ГЕТТЕРЫ И СЕТТЕРЫ
	# @property
	# def user_id(self):
	# 	return self._user_id

	# @property
	# def login(self): # запрос к БД происходит только один раз (если в переменной None), потом используется записанное в переменную значение
	# 	if self._login == None: 
	# 		self._login = self.DB.get_register_login(self.user_id) 
	# 	return self._login
	# @login.setter # в случае изменения значения пользователем, новое значение загружается в БД и перезаписывается зпщищенная переменная
	# def login(self, value):
	# 	self.DB.set_register_login(self.user_id, value) # новое значение загружается в БД
	# 	self._login = value # перезаписывается защищенная переменная


	# @property
	# def password(self):
	# 	if self._password == None:
	# 		self._password = self.DB.get_register_password(self.user_id)
	# 	return self._password
	# @password.setter
	# def password(self, value):
	# 	hashed_value = generate_password_hash(value) # хэшируем пароль
	# 	self.DB.set_register_password(self.user_id, hashed_value)
	# 	self._password = hashed_value







if __name__ == '__main__':
	...