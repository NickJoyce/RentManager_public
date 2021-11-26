table_name = 'ra_general_conditions'
attrs = ['rental_rate', 'prepayment', 'deposit', 'late_fee', 'start_of_term', 'end_of_term', 'payment_day']
id_ = 'rental_agreement_id'
table_id_field = 'rental_agreement_id'











def create_setters_and_getters(table_name, attrs):
	for attr in attrs:
		print(f'	@property')
		print(f'	def {attr}(self):')
		print(f'	    if self._{attr} == None:')		
		print(f'	       self._{attr} = self.db.get_{table_name}_{attr}(self.{id_})')
		print(f'	    return self._{attr}')	
		print(f'	@{attr}.setter')
		print(f'	def {attr}(self, value):')
		print(f'	    self.db.set_{table_name}_{attr}(self.{id_}, value)')
		print(f'	    self._{attr} = value')	
		print('')	


def create_get_query(table_name, attrs):
	print(f'	# GET ATTRIBUTES [{table_name}]: {attrs}')
	for attr in attrs:
		print(f'	def get_{table_name}_{attr}(self, {id_}):')
		print(f'		with self.context_manager(self.config) as cursor:')
		print(f'			cursor.execute("""SELECT {attr} FROM {table_name} WHERE {table_id_field}=%s""", ({id_},))')
		print(f'			return bool(cursor.fetchall()[0][0])')
		print('')


def create_set_query(table_name, attrs):
	print(f'	# SET ATTRIBUTES [{table_name}]: {attrs}')
	for attr in attrs:
		print(f'	def set_{table_name}_{attr}(self, {id_}, value):')
		print(f'		with self.context_manager(self.config) as cursor:')
		print(f'			cursor.execute("""UPDATE {table_name} SET {attr}=%s WHERE {table_id_field}=%s""", (value, {id_}))')
		print(f'')		



# create_setters_and_getters(table_name, attrs)
# create_get_query(table_name, attrs)
create_set_query(table_name, attrs)