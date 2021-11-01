from conditions import Conditions, AdditionalPayments # условия аренды, дополнительны платежи

class RentalAgreement:
	def __init__(self, rental_agreement_id, landlord, tenant, agent, rental_object): 
				
		# |T|> rental_agreement
		self.rental_agreement_id = None # id договора
		self.agreement_number = '' # номер договора аренда

		# УЧАСТННИКИ ДОГОВОРА
		self.agent = agent # экземпляр класса Agent (агент)
		self.landlord = landlord # экземпляр класса Landlord (наймодатель)
		self.tenant = tenant # экземпляр класса Tenant (наниматель)

		# ОБЪЕКТ АРЕНДЫ
		self.rental_object = rental_object # экземпляр класса Room, Flat или House

		# УСЛОВИЯ АРЕНДЫ
		self.conditions = None # экземпляр класса Conditions

		# ДОПОЛНИТЕЛЬНЫЕ ПЛАТЕЖИ
		self.additional_payments = None # экземпляр класса Conditions

		self.is_valid: False # действует ли договор



if __name__ == '__main__':
	from users import Admin, Agent, Landlord, Tenant
	from rental_objects import Room, Flat, House
	from conditions import Conditions 
	...
	
