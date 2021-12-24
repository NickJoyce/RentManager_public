from users import Admin, Agent, Landlord, Tenant
from rental_objects import Room, Flat, House

from rental_agreement_conditions import Conditions # условия аренды, дополнительны платежи

from rental_agreement_data import RA_RentalObject, RA_Cost, RA_Thing, RA_Landlord, RA_Tenant, RA_Agent, MoveIn, MoveOut, Termination, Renewal 


class RentalAgreement:
	def __init__(self, id_, agreement_number, status): 
				
		# |T|> rental_agreement
		self.id = id_# id договора
		self.agreement_number = agreement_number # номер договора аренда
		self.status = status # статус договора ['черновик', 'заключен', 'досрочно расторгнут', 'завершен', 'продлен'] 
		
		# ОБЪЕКТ АРЕНДЫ
		self.rental_object = None # экземпляр класса RA_RentalObject

		# УЧАСТННИКИ ДОГОВОРА
		self.landlord = None # экземпляр класса RA_Landlord (наймодатель)
		self.tenant = None # экземпляр класса RA_Tenant (наниматель)		
		self.agent = None # экземпляр класса RA_Agent (агент)

		# УСЛОВИЯ АРЕНДЫ 
		self.conditions = None # экземпляр класса Conditions 

		# ОПИСЬ ИМУЩЕСТВА
		self.things = None # список экземпляров класса RA_Thing

		# РАСХОДЫ НА СОДЕРЖАНИЕ
		self.costs = None # список экземпляров класса RA_Cost

		# АКТ СДАЧИ-ПРИЕМКИ
		self.move_in = None # экземпляр класса MoveIn 

		# АКТ ВОЗВРАТА
		self.move_out = None # экземпляр класса MoveOut

		# СОГЛАШЕНИЕ О РАСТОРЖЕНИИ
		self.termination = None # экземпляр класса Termination, список дат окончания срока действия договора (при расторжении)

		# СОГЛАШЕНИЕ О ПРОДЛЕНИИ
		self.renewal = None # список экземпляров Renewal, список дат окончания срока действия договора (при продлении)


		# self.rental_object_type = None # тип объекта аренды
		# self.landlord_id = None # id пользователя (Наймодателя)
		# self.agent_id = None # id пользователя (Агента)
		# self.tenant_id = None # id пользователя (Нанимателя)
		# self.rental_object_id = None # id объекта аренды		


if __name__ == '__main__':

 

	x = RentalAgreement(1)
	print(x.agreement_number)


# # ВЗАИМОДЕЙСТВИЕ С БД
# from database.config import db_config # параметры для подключения к БД
# from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

# from database.use_db import DataManipulation # класс для манипулирования данными в БД
# 		self._db = None
# #____________________________________________setters and getters____________________________________________
	



# 	@property
# 	def rental_agreement_id(self):
# 		return self._rental_agreement_id

# 	@property
# 	def db(self):
# 		if self._db == None:
# 			self._db = DataManipulation(db_config, DBcm)
# 		return self._db


# 	@property
# 	def general_conditions(self):
# 		if self._general_conditions == None:
# 			self._general_conditions = GeneralConditions(self.rental_agreement_id)
# 		return  self._general_conditions

# 	@property
# 	def agent_id(self):
# 	    if self._agent_id == None:
# 	       self._agent_id = self.db.get_rental_agreements_agent_id(self.rental_agreement_id)
# 	    return self._agent_id

# 	@property
# 	def landlord_id(self):
# 	    if self._landlord_id == None:
# 	       self._landlord_id = self.db.get_rental_agreements_landlord_id(self.rental_agreement_id)
# 	    return self._landlord_id

# 	@property
# 	def tenant_id(self):
# 	    if self._tenant_id == None:
# 	       self._tenant_id = self.db.get_rental_agreements_tenant_id(self.rental_agreement_id)
# 	    return self._tenant_id

# 	@property
# 	def rental_object_id(self):
# 	    if self._rental_object_id == None:
# 	       self._rental_object_id = self.db.get_rental_agreements_rental_object_id(self.rental_agreement_id)
# 	    return self._rental_object_id

# 	@property
# 	def agent(self):
# 	    if self._agent == None and self.agent_id != None:
# 	       self._agent = Agent(self.agent_id)
# 	    return self._agent

# 	@property
# 	def landlord(self):
# 	    if self._landlord == None:
# 	       self._landlord = Landlord(self.landlord_id)
# 	    return self._landlord


# 	@property
# 	def tenant(self):
# 	    if self._tenant == None:
# 	       self._tenant = Tenant(self.tenant_id)
# 	    return self._tenant


# 	@property
# 	def rental_object_type(self):
# 	    if self._rental_object_type == None:
# 	       self._rental_object_type = self.db.get_rental_object_type_by_id(self.rental_object_id)
# 	    return self._rental_object_type


# 	@property
# 	def rental_object(self):
# 	    if self._rental_object == None:
# 	    	if self.rental_object_type == 'комната':
# 	    		self._rental_object = Room(self.rental_object_id)
# 	    	elif self.rental_object_type == 'квартира':
# 	    		self._rental_object = Flat(self.rental_object_id)
# 	    	elif self.rental_object_type == 'дом':
# 	    		self._rental_object = House(self.rental_object_id)
# 	    	else:
# 	    		raise ValueError('неверный rental_object_type')
# 	    return self._rental_object


# 	@property
# 	def agreement_number(self):
# 		if self._agreement_number == None:
# 			self._agreement_number = self.db.get_rental_agreements_agreement_number(self.rental_object_id)
# 		return self._agreement_number
# 	@agreement_number.setter
# 	def agreement_number(self, value):
# 		self.db.set_rental_agreements_agreement_number(self.rental_object_id, value)
# 		self._agreement_number = value





	






	
	
