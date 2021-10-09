from prettytable import PrettyTable

class Payments:
	def __init__(self, general_utilities: float, gas: float, electricity: float, overhaul: float, water: float):
		self.general_utilities = general_utilities # общие ку
		self.gas = gas # газ
		self.electricity = electricity # электричество
		self.overhaul = overhaul # капитальный ремонт
		self.water = water # вода

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
	test_data =  [2500.02, 216.88, 418.12, 337.01, 329.15]
	payments = Payments(*test_data)
	print(payments)