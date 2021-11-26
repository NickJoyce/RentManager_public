from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД


class RentalAgreementConditions:
	def __init__(self, rental_agreement_id):
		self._rental_agreement_id = rental_agreement_id

		self._db = None
	#____________________________________________setters and getters____________________________________________

	@property
	def rental_agreement_id(self):
		return self._rental_agreement_id


	@property
	def db(self):
		if self._db == None:
			self._db = DataManipulation(db_config, DBcm)
		return self._db


class GeneralConditions(RentalAgreementConditions):
	# УCЛОВИЯ АРЕНДЫ |T| rental_agreement> ra_general_conditions
	def __init__(self, rental_agreement_id):
		super().__init__(rental_agreement_id)

		self._rental_rate = None # месячная арендная ставка
		self._prepayment = None # предоплата 
		self._deposit = None # залог
		self._late_fee = None # % от арендной ставки за задержку оплаты (в день)
		self._start_of_term = None # начало периода аренды
		self._end_of_term = None # конец периода аренды
		self._payment_day = None # день оплаты
	#____________________________________________setters and getters____________________________________________
	@property
	def rental_rate(self):
	    if self._rental_rate == None:
	       self._rental_rate = self.db.get_ra_general_conditions_rental_rate(self.rental_agreement_id)
	    return self._rental_rate
	@rental_rate.setter
	def rental_rate(self, value):
	    self.db.set_ra_general_conditions_rental_rate(self.rental_agreement_id, value)
	    self._rental_rate = value

	@property
	def prepayment(self):
	    if self._prepayment == None:
	       self._prepayment = self.db.get_ra_general_conditions_prepayment(self.rental_agreement_id)
	    return self._prepayment
	@prepayment.setter
	def prepayment(self, value):
	    self.db.set_ra_general_conditions_prepayment(self.rental_agreement_id, value)
	    self._prepayment = value

	@property
	def deposit(self):
	    if self._deposit == None:
	       self._deposit = self.db.get_ra_general_conditions_deposit(self.rental_agreement_id)
	    return self._deposit
	@deposit.setter
	def deposit(self, value):
	    self.db.set_ra_general_conditions_deposit(self.rental_agreement_id, value)
	    self._deposit = value

	@property
	def late_fee(self):
	    if self._late_fee == None:
	       self._late_fee = self.db.get_ra_general_conditions_late_fee(self.rental_agreement_id)
	    return self._late_fee
	@late_fee.setter
	def late_fee(self, value):
	    self.db.set_ra_general_conditions_late_fee(self.rental_agreement_id, value)
	    self._late_fee = value

	@property
	def start_of_term(self):
	    if self._start_of_term == None:
	       self._start_of_term = self.db.get_ra_general_conditions_start_of_term(self.rental_agreement_id)
	    return self._start_of_term
	@start_of_term.setter
	def start_of_term(self, value):
	    self.db.set_ra_general_conditions_start_of_term(self.rental_agreement_id, value)
	    self._start_of_term = value

	@property
	def end_of_term(self):
	    if self._end_of_term == None:
	       self._end_of_term = self.db.get_ra_general_conditions_end_of_term(self.rental_agreement_id)
	    return self._end_of_term
	@end_of_term.setter
	def end_of_term(self, value):
	    self.db.set_ra_general_conditions_end_of_term(self.rental_agreement_id, value)
	    self._end_of_term = value

	@property
	def payment_day(self):
	    if self._payment_day == None:
	       self._payment_day = self.db.get_ra_general_conditions_payment_day(self.rental_agreement_id)
	    return self._payment_day
	@payment_day.setter
	def payment_day(self, value):
	    self.db.set_ra_general_conditions_payment_day(self.rental_agreement_id, value)
	    self._payment_day = value

	



if __name__ == '__main__':
	x = GeneralConditions(1)
	print(x.rental_rate)
	print(x.prepayment)
	print(x.deposit)
	print(x.late_fee)
	print(x.start_of_term)
	print(x.end_of_term)
	print(x.payment_day)

	x.rental_rate = 14000
	x.prepayment = 14000
	x.deposit = 14000
	x.late_fee = 3.5
	x.start_of_term = '2021-11-10'
	x.end_of_term = '2022-11-10'
	x.payment_day = 20

	print(x.rental_rate)
	print(x.prepayment)
	print(x.deposit)
	print(x.late_fee)
	print(x.start_of_term)
	print(x.end_of_term)
	print(x.payment_day)