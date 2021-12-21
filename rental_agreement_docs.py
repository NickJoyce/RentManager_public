
class Move:
	def __init__(self, rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment):	
		self.rental_agreement_id = rental_agreement_id
		self.number_of_sets_of_keys = number_of_sets_of_keys # количество комплектов ключей
		self.number_of_keys_in_set = number_of_keys_in_set # количество ключей в комплекте
		self.rental_object_comment = rental_object_comment # замечания к передаваемомму помещению
		self.things_comment = things_comment # замечания к предметам из Описи имущества


class MoveIn(Move):
	def __init__(self, rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment):	
		super().__init__(rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment)

				
class MoveOut(Move):
	def __init__(self, rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment,
				        damage_cost, cleaning, rental_agreeement_debts, deposit_refund, prepayment_refund):	
		super().__init__(rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment)
		self.damage_cost = damage_cost # оценка ущерба
		self.cleaning = cleaning # нужна ли уборка
		self.rental_agreeement_debts = rental_agreeement_debts # задолженность связанная с выполнением Договора
		self.deposit_refund = deposit_refund # сумма возвращаемого депозита
		self.prepayment_refund = prepayment_refund # сумма возвращаемой предоплаты



class Termination:
	def __init__(self, rental_agreement_id, end_of_term):
		self.rental_agreement_id = rental_agreement_id
		self.end_of_term = end_of_term # дата досрочного расторжения


class Renewal:
	def __init__(self, rental_agreement_id, ends_of_term:list):
		self.rental_agreement_id = rental_agreement_id
		self.ends_of_term = ends_of_term # список дат окончания срока действия договора (при продлении)
		self.last_end_of_term = self.last_data(self.ends_of_term) # последняя дата до которой был продлен Договор

	def last_data(self, ends_of_term):
		if ends_of_term:
			return max(ends_of_term)[0]
		else:
			return 'Договор не продлевался'

if __name__ == '__main__':
	...

 
