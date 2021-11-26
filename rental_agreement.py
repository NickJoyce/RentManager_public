from users import Admin, Agent, Landlord, Tenant
from rental_objects import Room, Flat, House

from rental_agreement_conditions import GeneralConditions # условия аренды, дополнительны платежи

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataManipulation # класс для манипулирования данными в БД


class RentalAgreement:
	def __init__(self, rental_agreement_id): 
				
		# |T|> rental_agreement
		self._rental_agreement_id = rental_agreement_id # id договора

		self._db = None

		# TODO # УСЛОВИЯ АРЕНДЫ 
		self._general_conditions = None # экземпляр класса GeneralConditions

		self._agent_id = None # id пользователя (Агента)
		self._landlord_id = None # id пользователя (Наймодателя)
		self._tenant_id = None # id пользователя (Нанимателя)
		self._rental_object_id = None # id объекта аренды		

		# УЧАСТННИКИ ДОГОВОРА
		self._agent = None # экземпляр класса Agent (агент)
		self._landlord = None # экземпляр класса Landlord (наймодатель)
		self._tenant = None # экземпляр класса Tenant (наниматель)

		# ОБЪЕКТ АРЕНДЫ
		self._rental_object = None # экземпляр класса Room, Flat или House
		self._rental_object_type = None # тип объекта аренды


		self._agreement_number = None # номер договора аренда 



	#____________________________________________setters and getters____________________________________________
	



	@property
	def rental_agreement_id(self):
		return self._rental_agreement_id

	@property
	def db(self):
		if self._db == None:
			self._db = DataManipulation(db_config, DBcm)
		return self._db


	@property
	def general_conditions(self):
		if self._general_conditions == None:
			self._general_conditions = GeneralConditions(self.rental_agreement_id)
		return  self._general_conditions

	@property
	def agent_id(self):
	    if self._agent_id == None:
	       self._agent_id = self.db.get_rental_agreements_agent_id(self.rental_agreement_id)
	    return self._agent_id

	@property
	def landlord_id(self):
	    if self._landlord_id == None:
	       self._landlord_id = self.db.get_rental_agreements_landlord_id(self.rental_agreement_id)
	    return self._landlord_id

	@property
	def tenant_id(self):
	    if self._tenant_id == None:
	       self._tenant_id = self.db.get_rental_agreements_tenant_id(self.rental_agreement_id)
	    return self._tenant_id

	@property
	def rental_object_id(self):
	    if self._rental_object_id == None:
	       self._rental_object_id = self.db.get_rental_agreements_rental_object_id(self.rental_agreement_id)
	    return self._rental_object_id

	@property
	def agent(self):
	    if self._agent == None and self.agent_id != None:
	       self._agent = Agent(self.agent_id)
	    return self._agent

	@property
	def landlord(self):
	    if self._landlord == None:
	       self._landlord = Landlord(self.landlord_id)
	    return self._landlord


	@property
	def tenant(self):
	    if self._tenant == None:
	       self._tenant = Tenant(self.tenant_id)
	    return self._tenant


	@property
	def rental_object_type(self):
	    if self._rental_object_type == None:
	       self._rental_object_type = self.db.get_rental_object_type_by_id(self.rental_object_id)
	    return self._rental_object_type


	@property
	def rental_object(self):
	    if self._rental_object == None:
	    	if self.rental_object_type == 'комната':
	    		self._rental_object = Room(self.rental_object_id)
	    	elif self.rental_object_type == 'квартира':
	    		self._rental_object = Flat(self.rental_object_id)
	    	elif self.rental_object_type == 'дом':
	    		self._rental_object = House(self.rental_object_id)
	    	else:
	    		raise ValueError('неверный rental_object_type')
	    return self._rental_object


	@property
	def agreement_number(self):
		if self._agreement_number == None:
			self._agreement_number = self.db.get_rental_agreements_agreement_number(self.rental_object_id)
		return self._agreement_number
	@agreement_number.setter
	def agreement_number(self, value):
		self.db.set_rental_agreements_agreement_number(self.rental_object_id, value)
		self._agreement_number = value




if __name__ == '__main__':

 

	x = RentalAgreement(1)







	






	
	
