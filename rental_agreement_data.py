class RA_RentalObject:
	def __init__(self, rental_agreement_id, rental_object_id, type_, address, title_deed):
		self.rental_agreement_id = rental_agreement_id
		self.rental_object_id = rental_object_id
		self.type = type_
		self.address = address
		self.title_deed = title_deed




class RA_Cost:
	def __init__(self, id_, rental_agreement_id, name, is_payer_landlord):
		self.id = id_
		self.rental_agreement_id = rental_agreement_id
		self.name = name
		self._is_payer_landlord = is_payer_landlord
		self.payer = self.get_payer()

	def get_payer(self):
		if self._is_payer_landlord == 0:
			return 'наниматель'
		else:
			return 'наймодатель'





class RA_Thing:
	def __init__(self, id_, rental_agreement_id, thing_number, thing_name, amount, cost):
		self.id = id_
		self.rental_agreement_id = rental_agreement_id
		self.thing_number = thing_number
		self.thing_name = thing_name
		self.amount = amount
		self.cost = cost



class Participant:
	def __init__(self, rental_agreement_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration):
		self.rental_agreement_id = rental_agreement_id
		self.last_name = last_name
		self.first_name = first_name
		self.patronymic = patronymic
		self.phone = phone
		self.email = email
		self.serie = serie
		self.pass_number = pass_number
		self.authority = authority
		self.registration = registration



class RA_Landlord(Participant):
	def __init__(self, rental_agreement_id, landlord_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration):
		super().__init__(rental_agreement_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration)
		self.landlord_id = landlord_id


class RA_Tenant(Participant):
	def __init__(self, rental_agreement_id, tenant_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration):
		super().__init__(rental_agreement_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration)
		self.tenant_id = tenant_id


class RA_Agent(Participant):
	def __init__(self, rental_agreement_id, agent_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration):
		super().__init__(rental_agreement_id, last_name, first_name, patronymic, phone, email, serie, pass_number, authority, registration)
		self.agent_id = agent_id



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
	def __init__(self, rental_agreement_id, notice_date, end_of_term, is_landlord_initiator):
		self.rental_agreement_id = rental_agreement_id
		self.notice_date # дата увдомления инициатора другой стороны о решении расторгнуть договор
		self.end_of_term = end_of_term # дата досрочного расторжения
		self.is_landlord_initiator = is_landlord_initiator # является ли инициатором расторжения наймодатель


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

 
