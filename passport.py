from datetime import date
from prettytable import PrettyTable

class Passport:
	def __init__(self, first_name: str,  patronymic: str, last_name: str, serie: int, number: int, authority: str,  
		               department_code: str, date_of_issue: 'date', date_of_birth: 'date', place_of_birth: str, registration: str):
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
		dict_ = {'Имя': self.first_name,
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
	passport_data = ['Никита',
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
	passport = Passport(*passport_data)
	print(passport)