from datetime import date
from prettytable import PrettyTable

class Passport:
	def __init__(self, passport_id, user_id, first_name, patronymic, last_name, serie, number, authority, department_code,
		               date_of_issue, date_of_birth, place_of_birth,  registration):
		self.passport_id = passport_id # id паспорта
		self.user_id = user_id # id пользователя
		self.first_name = first_name # имя
		self.patronymic = patronymic # отчетсво
		self.last_name = last_name # фамилия
		self.serie = serie # серия
		self.number = number # номер
		self.authority = authority # орган выдавший паспорт
		self.department_code = department_code # код подразделения
		self.date_of_issue = date_of_issue # дата выдачи
		self.date_of_birth = date_of_birth # дата рождения
		self.place_of_birth = place_of_birth # место рождения
		self.registration = registration # адрес прописки

	# TODO сделать геттеры и сеттеры атрибутов для проверки соответствия типов данных

	def __repr__(self):
		name = f'{self.last_name}, {self.first_name}, {self.patronymic}, '
		ser_num = f'{self.serie}, {self.number}, '
		others = f'{self.authority}, {self.department_code}, {self.date_of_issue}, {self.date_of_birth}, {self.place_of_birth}, {self.registration}'
		return f"{self.__class__.__name__}({name}{ser_num}{others})"


	def __str__(self):
		passport_data = PrettyTable()
		pd = passport_data
		pd.field_names = ["Наименование данных", "Значения"] # column name
		pd._min_width = {"Наименование данных" : 25, "Значения" : 30} # column width 
		pd.align["Наименование данных"] = "l" # text-align: left
		pd.align["Значения"] = "l" # text-align: left
		dict_ = {'passport_id':self.passport_id,
				 'user_id':self.user_id,
				 'Имя': self.first_name,
				 'Отчество': self.patronymic,
				 'Фамилия': self.last_name,
				 'Серия и номер': f'{self.serie} {self.number}',
				 'Орган выдавший паспорт': self.authority,
				 'Код подразделения': self.department_code,
				 'Дата выдачи': f'{self.date_of_issue.day}.{self.date_of_issue.month}.{self.date_of_issue.year}',
				 'Дата рождения': f'{self.date_of_birth.day}.{self.date_of_birth.month}.{self.date_of_birth.year}',
				 'Место рождения': self.place_of_birth,
				 'Адрес прописки': self.registration}
		for k, v in dict_.items():
			pd.add_row([k, v])	
		return str(pd)


if __name__ == '__main__':

	passport = Passport(1)
	print(passport)