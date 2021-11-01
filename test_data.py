	bathroom_types = ['совмещенный', 'раздельный'] 
	wash_place_type = ['ванна', 'душевая кабина']
	building_type = ['кирпичный', 'панельный'] 


	db.insert_bathroom_type()

	db.reload_all_tables()
	
	user_types = ['наймодатель', 'наниматель', 'администратор', 'агент']
	for type_ in user_types:
		db.insert_user_type(type_)

	db.create_user('наймодатель', 'Никита', '+79218850028', 'actan-spb@mail.ru')

	db.create_user('наниматель', 'Ирина', '+79021364777', 'eirenesaar@gmail.com')
	db.create_user('наниматель', 'Алина', '+79811924591', 'alonavrn@gmail.com')
	db.create_user('наниматель', 'Наталья', '+79822225328', 'ntash.kiv@gmail.com')

	# ЕДАКТИРОВАНИЕ ДАННЫХ НАЙМОДАТЕЛЕЙ
	user = create_user_instance_by_id(1)
	# user.name = ''
	# user.phone = ''
	# user.email = ''
	user.inn = '162-789-133 00'

	user.passport.first_name = 'Никита'
	user.passport.patronymic = 'Алексеевич'  
	user.passport.last_name = 'Смирнов' 
	user.passport.serie = '4008' 
	user.passport.number = '522493'  
	user.passport.authority = 'ТП №81'  
	user.passport.department_code = '780-081' 
	user.passport.date_of_issue = date(2008, 7, 7)
	user.passport.date_of_birth = date(1988, 6, 23) 
	user.passport.place_of_birth = 'г. Ленинград'  
	user.passport.registration = 'Санкт-Петербург, ул. гороховая 32-95'

	# user.register.login = ''
	# user.register.password = ''
	save_user(user)

	# РЕДАКТИРОВАНИЕ ДАННЫХ НАНИМАТЛЕЙ
	user = create_user_instance_by_id(2)
	# user.name = ''
	# user.phone = ''
	# user.email = ''

	user.passport.first_name = 'Ирина'
	user.passport.patronymic = 'Максимовна'  
	user.passport.last_name = 'Саранская' 
	user.passport.serie = '4721' 
	user.passport.number = '743479'  
	user.passport.authority = 'УМВД России по Мурманской области'  
	user.passport.department_code = '' 
	user.passport.date_of_issue = date(1,1,1)
	user.passport.date_of_birth = date(1,1,1) 
	user.passport.place_of_birth = ''  
	user.passport.registration = 'обл. Мурманская, г. Апатиты, ул. Дзержинского 59-43'

	# user.register.login = ''
	# user.register.password = ''
	save_user(user)

	user = create_user_instance_by_id(3)
	# user.name = ''
	# user.phone = ''
	# user.email = ''

	user.passport.first_name = 'Алина'
	user.passport.patronymic = 'Гусейновна'  
	user.passport.last_name = 'Магамедова' 
	user.passport.serie = '2019' 
	user.passport.number = '802512'  
	user.passport.authority = 'УФМС РФ по Воронежской области в коминтерновском районе г. Воронежа'  
	user.passport.department_code = '' 
	user.passport.date_of_issue = date(1,1,1)
	user.passport.date_of_birth = date(1,1,1) 
	user.passport.place_of_birth = ''  
	user.passport.registration = 'г. Воронеж пер. Новоселов д. 12'

	# user.register.login = ''
	# user.register.password = ''
	save_user(user)



	user = create_user_instance_by_id(4)
	# user.name = ''
	# user.phone = ''
	# user.email = ''

	user.passport.first_name = 'Наталья'
	user.passport.patronymic = 'Владимировна'  
	user.passport.last_name = 'Колесникова' 
	user.passport.serie = '6716' 
	user.passport.number = '553286'  
	user.passport.authority = 'УФМС РФ по ХМАО-югре, г. Сургут'  
	user.passport.department_code = '' 
	user.passport.date_of_issue = date(1,1,1)
	user.passport.date_of_birth = date(1,1,1) 
	user.passport.place_of_birth = ''  
	user.passport.registration = 'г. Сургут, ул Энтузиастов 8-3'

	# user.register.login = ''
	# user.register.password = ''
	save_user(user)
