class Conditions:
	# УCЛОВИЯ АРЕНДЫ |T| rental_agreement> ra_general_conditions
	def __init__(self, rental_agreement_id, rental_rate, prepayment, deposit, late_fee, start_of_term, end_of_term,
					   payment_day, cleaning_cost):
		self.rental_agreement_id = rental_agreement_id
		self.rental_rate = rental_rate # месячная арендная ставка
		self.prepayment = prepayment  # предоплата 
		self.deposit = deposit # залог
		self.late_fee = late_fee # % от арендной ставки за задержку оплаты (в день)
		self.start_of_term = start_of_term # начало периода аренды
		self.end_of_term = end_of_term # конец периода аренды 
		self.payment_day = payment_day # день оплаты
		self.cleaning_cost = cleaning_cost # стоимость клининга




if __name__ == '__main__':
	...


	# 	#____________________________________________setters and getters____________________________________________
	# @property
	# def rental_rate(self):
	#     if self._rental_rate == None:
	#        self._rental_rate = self.db.get_ra_general_conditions_rental_rate(self.rental_agreement_id)
	#     return self._rental_rate
	# @rental_rate.setter
	# def rental_rate(self, value):
	#     self.db.set_ra_general_conditions_rental_rate(self.rental_agreement_id, value)
	#     self._rental_rate = value

	# @property
	# def prepayment(self):
	#     if self._prepayment == None:
	#        self._prepayment = self.db.get_ra_general_conditions_prepayment(self.rental_agreement_id)
	#     return self._prepayment
	# @prepayment.setter
	# def prepayment(self, value):
	#     self.db.set_ra_general_conditions_prepayment(self.rental_agreement_id, value)
	#     self._prepayment = value

	# @property
	# def deposit(self):
	#     if self._deposit == None:
	#        self._deposit = self.db.get_ra_general_conditions_deposit(self.rental_agreement_id)
	#     return self._deposit
	# @deposit.setter
	# def deposit(self, value):
	#     self.db.set_ra_general_conditions_deposit(self.rental_agreement_id, value)
	#     self._deposit = value

	# @property
	# def late_fee(self):
	#     if self._late_fee == None:
	#        self._late_fee = self.db.get_ra_general_conditions_late_fee(self.rental_agreement_id)
	#     return self._late_fee
	# @late_fee.setter
	# def late_fee(self, value):
	#     self.db.set_ra_general_conditions_late_fee(self.rental_agreement_id, value)
	#     self._late_fee = value

	# @property
	# def start_of_term(self):
	#     if self._start_of_term == None:
	#        self._start_of_term = self.db.get_ra_general_conditions_start_of_term(self.rental_agreement_id)
	#     return self._start_of_term
	# @start_of_term.setter
	# def start_of_term(self, value):
	#     self.db.set_ra_general_conditions_start_of_term(self.rental_agreement_id, value)
	#     self._start_of_term = value

	# @property
	# def end_of_term(self):
	#     if self._end_of_term == None:
	#        self._end_of_term = self.db.get_ra_general_conditions_end_of_term(self.rental_agreement_id)
	#     return self._end_of_term
	# @end_of_term.setter
	# def end_of_term(self, value):
	#     self.db.set_ra_general_conditions_end_of_term(self.rental_agreement_id, value)
	#     self._end_of_term = value

	# @property
	# def payment_day(self):
	#     if self._payment_day == None:
	#        self._payment_day = self.db.get_ra_general_conditions_payment_day(self.rental_agreement_id)
	#     return self._payment_day
	# @payment_day.setter
	# def payment_day(self, value):
	#     self.db.set_ra_general_conditions_payment_day(self.rental_agreement_id, value)
	#     self._payment_day = value