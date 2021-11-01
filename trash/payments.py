from prettytable import PrettyTable

class Payments:
	def __init__(self):
		self.general_utilities = 0.0 # общие ку
		self.gas = 0.0 # газ
		self.electricity = 0.0 # электричество
		self.overhaul = 0.0 # капитальный ремонт
		self.water = 0.0 # вода

	def __repr__(self):
		return f'{self.__class__.__name__}({self.general_utilities}, {self.gas}, {self.electricity}, {self.overhaul}, {self.water})'

	def __str__(self):
		table = PrettyTable()
		table.field_names = ["Наименование платежа", "Значение"] # column name
		table._min_width = {"Наименование платежа" : 30, "Значение": 15} # column width 
		table.align["Наименование платежа"] = "l" # text-align: left
		table.align["Значение"] = "l" # text-align: left
		data = {'Общие ку': self.general_utilities,
				'Газ': self.gas,
				'Электричество': self.electricity,
				'Капитальный ремонт': self.overhaul,
				'Вода': self.water}
		for k, v in data.items():
			table.add_row([k, v])
		return str(table)

if __name__ == '__main__':
	payments = Payments()
	print(payments)