class Conditions:
	def __init__(self):
		# УCЛОВИЯ АРЕНДЫ |T| rental_agreement> ra_conditions
		self.rental_rate = 0.0 # месячная арендная ставка
		self.prepayment = 0.0 # предоплата (% от месячной арендной ставки)
		self.deposit = 0.0 # залог
		self.late_fee = 0.0 # % от арендной ставки за задержку оплаты (в день)
		self.start_of_term = None # начало периода аренды
		self.end_of_term = None # конец периода аренды
		self.payment_day = None # день оплаты

class AdditionalPayments:
	def __init__(self):
		# ДОПОЛНИТЕЛЬНЫЕ ПЛАТЕЖИ |T| rental_agreement> ra_additional_payments Кто платит? ['landlord', 'tenant', None]
		self.general_utilities = None # общие ку
		self.gas = None # газ
		self.electricity = None # электричество
		self.overhaul = None # капитальный ремонт
		self.water = None # вода
		self.internet = None # интернет


if __name__ == '__main__':
	...