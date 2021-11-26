import mysql.connector # подключение драйвера MySql Connector

class DBContext_Manager: 
	"""Диспетчер контекста для подключения БД"""
	def __init__(self, config: dict) -> None:
		"""Инициализация атрибутов класса UseDatabase"""
		self.configuration = config # параметры соеденения с базой данных

	def __enter__(self) -> 'cursor':
		self.conn = mysql.connector.connect(**self.configuration) # используем словарь с параметрами, чтобы подключиться к MySQL
		self.cursor = self.conn.cursor() # Создаем курсор БД
		return self.cursor

	def __exit__(self, exc_type, exc_value, exc_trace) -> None:
		self.conn.commit() # запись в БД всех значений присвоенных атрибутам
		self.cursor.close() # закрываем курсор
		self.conn.close() # закрываем соеденение

