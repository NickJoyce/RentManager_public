from prettytable import PrettyTable
from datetime import date

class Conditions:
	def __init__(self, rate: float, deposit: float, late_fee: float, start: 'date', end: 'date', payment_day: int, agreement_number: str):
		self.rate = rate # месячная арендная ставка
		self.deposit = deposit # залог
		self.late_fee = late_fee # % от арендной ставки за задержку оплаты (в день)
		self.start = start # начало периода аренды
		self.end = end # конец периода аренды
		self.payment_day = payment_day # день оплаты
		self.agreement_number = agreement_number # номер договора аренда
		# TODO определить все условия съема

	def __repr__(self):
		s = f'{self.__class__.__name__}({self.rate}, {self.deposit}, {self.late_fee}, {self.start}, '
		e = f'{self.end}, {self.payment_day}, {self.agreement_number})'
		return f"{s}{e}"

	def __str__(self):
		conditions_table = PrettyTable()
		ct = conditions_table
		ct.field_names = ["Наименование уловия", "Значение"] # column name
		ct._min_width = {"Наименование уловия" : 30, "Значение" : 15} # column width
		ct.align["Наименование уловия"] = "l" # text-align: left
		ct.align["Значение"] = "l" # text-align: left
		data = {'Месячная арендная ставка': self.rate,
				'Залог': self.deposit,
				'Штраф за задержку, %/день': self.late_fee,
				'Начало периода аренды': self.start,
				'Конец периода аренды': self.end,
				'День оплаты': self.payment_day,
				'Номер договора аренда': self.agreement_number}
		for k, v in data.items():
			ct.add_row([k, v])	
		return str(ct)


if __name__ == '__main__':
	data = [14000, 14000, 3, date(2021, 6, 15), date(2021, 12, 15), 6, '142857 АБ']

	conditions = Conditions(*data)
	print(conditions)