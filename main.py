from werkzeug.security import generate_password_hash, check_password_hash 
import os
import json

# ------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort,make_response # импортируем функции модуля flask

application = Flask(__name__) #создание экземпляра объекта Flask и присваивание его переменной "application" 

application.config['SECRET_KEY'] = 'd1269dcb5c175acb12678fa83e66e9ca1a707cb4'
application.config['PERMANENT_SESSION_LIFETIME'] = 604800 # неприрывное время жизни сеанса в секундах (604800 сек. = 7 суток)
application.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------------------------------------------------------

from datetime import date

from login_checker import logged_in, logged_in_admin, logged_in_landlord, logged_in_tenant, logged_in_agent

from users import User, Admin, Agent, Landlord, Tenant # пользователи
from passport import Passport # паспортные данные пользователей
from register import Register # регистрационные данные пользоватлей

from rental_objects import RentalObject, Room, Flat, House # объекты аренды
from rental_object_data import General, ObjectData, Building, Location, Appliances, Thing, Cost

from rental_agreement import RentalAgreement # договор аренд
from rental_agreement_conditions import Conditions# условия аренды, дополнительны платежи
from rental_agreement_docs import MoveIn, MoveOut, Termination, Renewal


# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataDefinition # класс для определения и модификации объектов(таблиц, базданных)
from database.use_db import DataManipulation # класс для манипулирования данными в БД

db_def = DataDefinition(db_config, DBcm)
db = DataManipulation(db_config, DBcm) # экземпляр класса для взаимодействия с БД


# __________РЕДИРЕКТ НА ГЛАВНУЮ СТРАНИЦУ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ________
@application.route('/user_index_redirect')
def user_index_redirect() -> 'html':
	"""редирект на главную страницу текущего пользователя"""
	if 'admin_id' in session:
		return redirect(url_for('index_admin'))
	elif 'landlord_id' in session:
		return redirect(url_for('index_landlord'))
	elif 'tenant_id' in session:
		return redirect(url_for('index_tenant'))
	elif 'agent_id' in session:
		return redirect(url_for('index_agent'))
	else:
		return redirect(url_for('index'))		


# __________ВХОД________
@application.route('/login', methods=['POST','GET'])
def login() -> 'html':
	"""Вход для всех типов пользователей"""
	the_title = 'Вход'
	if request.method == 'POST':
		login = request.form['login']
		current_password = request.form['password']

		if db.is_login(login): # если есть такой логин проверим соответствие пароля
			hash_password = db.get_password_by_login(login) # получаем хэшированный пароль из БД
			if check_password_hash(hash_password, current_password): # если пароли соответствуют
				# получим и запишем данные о пользователе в session
				session['logged_in'] = True # статус входа
				session['user_id'] = db.get_user_id_by_login(login) # user_id
				session['user_type'] = db.get_user_type_by_user_id(session['user_id']) # тип пользователя

				session['user_name'] = db.get_user_name(session['user_id']) # имя пользователя

				if session['user_type'] == 'администратор':
					session['admin_id'] = db.get_admin_id(session['user_id']) # id администратора
					session['landlords'] = db.get_landlord_user_id_of_admin(session['admin_id']) # список user_id наймодателей, данного администратора 
				elif session['user_type'] == 'наймодатель':
					session['landlord_id'] = db.get_landlord_id(session['user_id']) # id наймодателя
					session['tenants'] = db.get_tenant_user_id_of_landlord(session['landlord_id'])
					session['agents'] = db.get_agent_user_id_of_landlord(session['landlord_id']) 
					session['rental_objects'] = db.get_rental_object_id_of_landlord(session['landlord_id'])
					session['rental_agreements'] = db.get_rental_agreement_id_of_landlord(session['landlord_id']) 
				elif session['user_type'] == 'наниматель':
					session['tenant_id'] = db.get_tenant_id(session['user_id'])	# id нанимателя				
				elif session['user_type'] == 'агент':
					session['agent_id'] = db.get_agent_id(session['user_id']) # id агента

				flash(f"Вход успешно выполнен. Здравствуйте, {session['user_name']}!", category='success')

				# редирект на главнаю страницу пользователя соответствующего типа
				return redirect(url_for('user_index_redirect'))

			else: # если пароли не соответствуют
				flash(f"'{current_password}' - неверный пароль", category='error')
				return redirect(url_for('login'))
		else: # если такого логина нет
			flash(f"Логина '{login}' не существует", category='error')
			return redirect(url_for('login'))
	return render_template('login.html',the_title=the_title)



# __________ВЫХОД________
@application.route('/logout') 
def logout() -> 'html':
	"""Выход для всех типов пользоватей"""
	session.clear()
	return redirect(url_for('login'))	



# __________ГЛАВНАЯ_________
@application.route('/', methods=['POST','GET']) 
def index() -> 'html':
	if session:
		return redirect(url_for('user_index_redirect'))
	else:
		return redirect(url_for('login'))		



# __________Проверка вводимых данных_________
@application.route('/check_user_data', methods=['POST','GET'])
def check_user_data():
	"""Проверка вводимых пользователем данных при регистрации"""

	user_type = request.form['user_type']

	name = request.form['name']
	phone = request.form['phone']
	email = request.form['email']

	login = request.form['login']	
	password = request.form['password']

	# url страница на которую производиться возврат в случае ошибок во вводе
	if user_type == 'администратор':
		...
	elif user_type == 'наймодатель':
		url = url_for('add_landlord')
	elif user_type == 'наниматель':
		url = url_for('add_tenant')
	elif user_type =='агент':
		url = url_for('add_agent')

	# проверки
	user = User(None, None, None, email)
	# ошибки при вводе email
	email_errors = user.chek_email()
	if email_errors:
		for i in email_errors:
			flash(f"{i}", category='error')
		return redirect(url)

	register = Register(login, password)
	# ошибки при вводе логина
	login_errors = register.chek_login(db.get_logins()) 
	if login_errors:
		for i in login_errors:
			flash(f"{i}", category='error')
		return redirect(url)

	# ошибки при вводе пароля	
	password_errors = register.chek_password() 
	if password_errors:
		for i in password_errors:
			flash(f"{i}", category='error')
		return redirect(url)

	# хэшируем пароль
	register.generate()

	# если все проверки прошли времнно запишем данные в session
	session['temp_name'] = name
	session['temp_phone'] = phone
	session['temp_email'] = email

	session['temp_login'] = login
	session['temp_password'] = register.hashed_password

	session['temp_chek'] = True

	# делаем редирект на обработчик создания пользователя в зависимости от типа пользователя
	# session['temp_chek'] - флаг для запуска процесса создания вместо вывода страницей с формой 
	return redirect(url)




# __________АДМИНИСТРАТОР_________
# __________Главная: администратор_________
@application.route('/admin', methods=['POST','GET']) 
@logged_in_admin
def index_admin() -> 'html':
	""""""
	the_title = 'Главная: aдминистратор'

	return render_template('index_admin.html', the_title=the_title, user_name=session['user_name'])


# __________Главная: администратор -> наймодатели_________
@application.route('/admin/landlords', methods=['POST','GET']) 
@logged_in_admin
def admin_landlords() -> 'html':
	""""""
	the_title = 'Наймодатели'

	# одним запросом получаем данные из БД необходимые для создания экземпляров класса Landlord 
	landlords_data = db.get_landlord_data_of_admin(session['admin_id'])
	
	# создаем экземпляры используя загруженные данные
	landlords = []
	for landlord_data in landlords_data:
		landlords.append(Landlord(*landlord_data))

	add_landlord = url_for('add_landlord') # адрес ссылки для onclick

	return render_template('admin_landlords.html', the_title=the_title, user_name=session['user_name'], landlords=landlords, add_landlord=add_landlord)




# __________Главная: администратор -> наймодатели -> добавление наймодателя _________
@application.route('/add_landlord', methods=['POST','GET'])
@logged_in_admin
def add_landlord() -> 'html':
	the_title = 'Добавление наймодателя'
	if 'temp_chek' in session:
		# создаем пользователя
		db.create_user('наймодатель', 
						session['temp_name'], 
						session['temp_phone'], 
						session['temp_email'], 
						session['temp_login'], 
						session['temp_password'], 
						admin_id=session['admin_id'])
		# получаем обновленный список user_id наймодателей для данного администратора
		session['landlords'] = db.get_landlord_user_id_of_admin(session['admin_id']) 

		# удаляем временные данные из session
		del session['temp_chek']
		del session['temp_name'] 
		del session['temp_phone']
		del session['temp_email']
		del session['temp_login']
		del session['temp_password']

		return redirect(url_for('admin_landlords'))
	else:
		return render_template('add_landlord.html', the_title=the_title, user_name=session['user_name'])



# __________Главная: администратор -> наймодатели -> наймодатель _________
@application.route('/edit_landlord/<int:user_id>', methods=['POST','GET']) 
@logged_in_admin
def edit_landlord(user_id) -> 'html':
	""""""
	if user_id in session['landlords']:
		the_title = 'Наймодатель'
		if request.method == 'POST':
			if request.form['source'] == 'landlord_info_tab':
				db.set_user_data(request.form['user_id'],request.form['name'], request.form['phone'], request.form['email'])
				db.set_landlord_data(request.form['user_id'], request.form['inn'])

				flash(f"Личные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_landlord', user_id=user_id))
	
			elif request.form['source'] == 'passport_tab':
				db.set_passport_data(
					user_id,
					request.form['first_name'],
					request.form['patronymic'],
					request.form['last_name'],
					request.form['serie'],
					request.form['pass_number'],
					request.form['authority'],
					request.form['department_code'],
					request.form['date_of_issue'],
					request.form['date_of_birth'],
					request.form['place_of_birth'],
					request.form['registration']
					)
				flash(f"Паспортные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_landlord', user_id=user_id))

			elif request.form['source'] == 'register_tab':
				gotten_admin_password = request.form['admin_password']
				admin_hashed_password = db.get_register_password(session['user_id'])
				reg_login = Register(None, None)
				if reg_login.is_correct_password(admin_hashed_password, gotten_admin_password):
					landlord_password = request.form['landlord_password']
					reg_landlord = Register(None, landlord_password)
					errors = reg_landlord.chek_password()
					if errors:
						for error in errors:
							flash(f"{error}", category='error')
						return redirect(url_for('edit_landlord', user_id=user_id))
					else:
						reg_landlord.generate()
						db.set_register_password(user_id, reg_landlord.hashed_password)
						flash(f"Пароль для учетной записи наймодателя успешно изменены!", category='success')
						return redirect(url_for('edit_landlord', user_id=user_id))

				else:
					flash(f"Неверный пароль текущего пользователя!", category='error')
					return redirect(url_for('edit_landlord', user_id=user_id))
				

		else:
			landlord = Landlord(*db.get_landlord_data(user_id))
			landlord.passport = Passport(*db.get_passport_data(user_id))
			landlord.register = Register(*db.get_register_data(user_id))
			return render_template('edit_landlord.html', the_title=the_title, user_name=session['user_name'], landlord=landlord)
	else:
		abort(401)





# ------------------------------------------------------------------------------------------------------------------------------------------------

# __________НАЙМОДАТЕЛЬ_________
# __________Главная: администратор_________
@application.route('/landlord', methods=['POST','GET']) 
@logged_in_landlord
def index_landlord() -> 'html':
	""""""
	the_title = 'Наймодатель'
	user_name = session['user_name']
	return render_template('index_landlord.html', the_title=the_title, user_name=user_name)


# __________Главная: наймодатель -> наниматели_________
@application.route('/landlord/tenants', methods=['POST','GET']) 
@logged_in_landlord
def landlord_tenants() -> 'html':
	the_title = 'Наниматели'
	...
	# подгружаем данные из БД для создания экземпляров класса Tenant
	tenants_data = db.get_tenant_data_of_landlord(session['landlord_id'])

	tenants = []
	for tenant_data in tenants_data:
		tenants.append(Tenant(*tenant_data))

	add_tenant_url = url_for('add_tenant')

	return render_template('landlord_tenants.html', the_title=the_title, user_name=session['user_name'], tenants=tenants, add_tenant_url=add_tenant_url)


# __________Главная: наймодатель -> наниматели -> добавление нанимателя _________
@application.route('/add_tenant', methods=['POST','GET'])
@logged_in_landlord
def add_tenant() -> 'html':
	the_title = 'Добавление нанимателя'
	if 'temp_chek' in session:
		# создаем пользователя
		db.create_user('наниматель', 
						session['temp_name'], 
						session['temp_phone'], 
						session['temp_email'], 
						session['temp_login'], 
						session['temp_password'], 
						landlord_id=session['landlord_id'])
		# получаем обновленный список user_id наймодателей для данного администратора
		session['tenants'] = db.get_tenant_user_id_of_landlord(session['landlord_id']) 

		# удаляем временные данные из session
		del session['temp_chek']
		del session['temp_name'] 
		del session['temp_phone']
		del session['temp_email']
		del session['temp_login']
		del session['temp_password']

		return redirect(url_for('landlord_tenants'))
	else:
		return render_template('add_tenant.html', the_title=the_title, user_name=session['user_name'])


# __________Главная: наймодатель -> наниматели -> наниматель _________
@application.route('/edit_tenant/<int:user_id>', methods=['POST','GET']) 
@logged_in_landlord
def edit_tenant(user_id) -> 'html':
	""""""
	if user_id in session['tenants']:
		the_title = 'Наниматель'
		if request.method == 'POST':
			if request.form['source'] == 'info_tab':
				db.set_user_data(request.form['user_id'],request.form['name'], request.form['phone'], request.form['email'])

				flash(f"Личные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_tenant', user_id=user_id))
	
			elif request.form['source'] == 'passport_tab':
				db.set_passport_data(
					user_id,
					request.form['first_name'],
					request.form['patronymic'],
					request.form['last_name'],
					request.form['serie'],
					request.form['pass_number'],
					request.form['authority'],
					request.form['department_code'],
					request.form['date_of_issue'],
					request.form['date_of_birth'],
					request.form['place_of_birth'],
					request.form['registration']
					)
				flash(f"Паспортные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_tenant', user_id=user_id))

			elif request.form['source'] == 'register_tab':
				gotten_tenant_password = request.form['tenant_password']
				tenant_hashed_password = db.get_register_password(session['user_id'])
				reg_login = Register(None, None)
				if reg_login.is_correct_password(tenant_hashed_password, gotten_tenant_password):
					tenant_password = request.form['tenant_password']
					reg_tenant = Register(None, tenant_password)
					errors = reg_tenant.chek_password()
					if errors:
						for error in errors:
							flash(f"{error}", category='error')
						return redirect(url_for('edit_tenant', user_id=user_id))
					else:
						reg_tenant.generate()
						db.set_register_password(user_id, reg_tenant.hashed_password)
						flash(f"Пароль для учетной записи нанимателя успешно изменен!", category='success')
						return redirect(url_for('edit_tenant', user_id=user_id))

				else:
					flash(f"Неверный пароль текущего пользователя!", category='error')
					return redirect(url_for('edit_tenant', user_id=user_id))
				

		else:
			tenant = Tenant(*db.get_tenant_data(user_id))
			tenant.passport = Passport(*db.get_passport_data(user_id))
			tenant.register = Register(*db.get_register_data(user_id))
			return render_template('edit_tenant.html', the_title=the_title, user_name=session['user_name'], tenant=tenant)
	else:
		abort(401)

# ------------------------------------------------------------------------------------------------------------------------------------------------


# __________Главная: наймодатель -> агенты_________
@application.route('/landlord/agents', methods=['POST','GET']) 
@logged_in_landlord
def landlord_agents() -> 'html':
	the_title = 'Агенты'
	...
	# подгружаем данные из БД для создания экземпляров класса Tenant
	agents_data = db.get_agent_data_of_landlord(session['landlord_id'])

	agents = []
	for agent_data in agents_data:
		agents.append(Tenant(*agent_data))

	add_agent_url = url_for('add_agent')

	return render_template('landlord_agents.html', the_title=the_title, user_name=session['user_name'], agents=agents, add_agent_url=add_agent_url)


# __________Главная: наймодатель -> агенты -> добавление агента _________
@application.route('/add_agent', methods=['POST','GET'])
@logged_in_landlord
def add_agent() -> 'html':
	the_title = 'Добавление агента'
	if 'temp_chek' in session:
		# создаем пользователя
		db.create_user('агент', 
						session['temp_name'], 
						session['temp_phone'], 
						session['temp_email'], 
						session['temp_login'], 
						session['temp_password'], 
						landlord_id=session['landlord_id'])
		# получаем обновленный список user_id наймодателей для данного администратора
		session['agents'] = db.get_agent_user_id_of_landlord(session['landlord_id']) 

		# удаляем временные данные из session
		del session['temp_chek']
		del session['temp_name'] 
		del session['temp_phone']
		del session['temp_email']
		del session['temp_login']
		del session['temp_password']

		return redirect(url_for('landlord_agents'))
	else:
		return render_template('add_agent.html', the_title=the_title, user_name=session['user_name'])


# __________Главная: наймодатель -> агенты -> агент _________
@application.route('/edit_agent/<int:user_id>', methods=['POST','GET']) 
@logged_in_landlord
def edit_agent(user_id) -> 'html':
	""""""
	if user_id in session['agents']:
		the_title = 'Наниматель'
		if request.method == 'POST':
			if request.form['source'] == 'info_tab':
				db.set_user_data(request.form['user_id'],request.form['name'], request.form['phone'], request.form['email'])

				flash(f"Личные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_agent', user_id=user_id))
	
			elif request.form['source'] == 'passport_tab':
				db.set_passport_data(
					user_id,
					request.form['first_name'],
					request.form['patronymic'],
					request.form['last_name'],
					request.form['serie'],
					request.form['pass_number'],
					request.form['authority'],
					request.form['department_code'],
					request.form['date_of_issue'],
					request.form['date_of_birth'],
					request.form['place_of_birth'],
					request.form['registration']
					)
				flash(f"Паспортные данные успешно сохранены!", category='success')
				return redirect(url_for('edit_agent', user_id=user_id))

			elif request.form['source'] == 'register_tab':
				gotten_agent_password = request.form['agent_password']
				agent_hashed_password = db.get_register_password(session['user_id'])
				reg_login = Register(None, None)
				if reg_login.is_correct_password(agent_hashed_password, gotten_agent_password):
					agent_password = request.form['agent_password']
					reg_agent = Register(None, agent_password)
					errors = reg_agent.chek_password()
					if errors:
						for error in errors:
							flash(f"{error}", category='error')
						return redirect(url_for('edit_agent', user_id=user_id))
					else:
						reg_agent.generate()
						db.set_register_password(user_id, reg_agent.hashed_password)
						flash(f"Пароль для учетной записи успешно изменен!", category='success')
						return redirect(url_for('edit_agent', user_id=user_id))

				else:
					flash(f"Неверный пароль текущего пользователя!", category='error')
					return redirect(url_for('edit_agent', user_id=user_id))
				

		else:
			agent = Agent(*db.get_agent_data(user_id))
			agent.passport = Passport(*db.get_passport_data(user_id))
			agent.register = Register(*db.get_register_data(user_id))
			return render_template('edit_agent.html', the_title=the_title, user_name=session['user_name'], agent=agent)
	else:
		abort(401)



# ------------------------------------------------------------------------------------------------------------------------------------------------

# __________Главная: наймодатель -> объекты аренды _________
@application.route('/landlord/rental_objects', methods=['POST','GET']) 
@logged_in_landlord
def landlord_rental_objects() -> 'html':
	the_title = 'Объекты аренды'
	...
	# подгружаем данные из БД для создания экземпляров класса Tenant
	rental_objects_data = db.get_rental_objects_data_of_landlord(session['landlord_id'])

	# список экземпляров классов Room, Flat или House
	rental_objects = []

	for rental_object in rental_objects_data:
		if rental_object[1] == 'комната':
			# добавляем добавляем недостающий для инициализации класса аргументы (total_area, rooms_number)
			ro = Room(*rental_object+(None,)+(None,))
		elif rental_object[1] == 'квартира':
			ro = Flat(*rental_object)
		elif rental_object[1] == 'дом':
			ro = House(*rental_object)

		rental_objects.append(ro)

	return render_template('landlord_rental_objects.html', the_title=the_title, user_name=session['user_name'], rental_objects=rental_objects)

@application.route('/landlord/rental_objects/add_rental_object', methods=['POST','GET']) 
@logged_in_landlord
def add_rental_object() -> 'html':
	the_title = 'Добавление объекта аренды'
	if request.method == 'POST':
		type_id = request.form['type_id']
		name = request.form['name']
		landlord_id = session['landlord_id']
		db.create_rental_object(type_id, name, landlord_id)
		session['rental_objects'] = db.get_rental_object_id_of_landlord(session['landlord_id'])
		return redirect(url_for('landlord_rental_objects'))

	else:
		rental_objects_types = db.get_rental_objects_types()
		return render_template('add_rental_object.html', the_title=the_title, rental_objects_types=rental_objects_types)


# __________Главная: наймодатель -> агенты -> агент _________
@application.route('/landlord/rental_objects/edit_rental_object/<int:rental_object_id>', methods=['POST','GET']) 
@logged_in_landlord
def edit_rental_object(rental_object_id) -> 'html':
	""""""
	if rental_object_id in session['rental_objects']:
		the_title = 'Объект аренды'

		if request.method == 'POST':
			if request.form['source'] == 'info_tab':
				db.set_rental_object_name(rental_object_id, request.form['name'])
				db.set_ro_general_data(rental_object_id, request.form['cadastral_number'], request.form['title_deed'])
				

			elif request.form['source'] == 'object_tab':
				od = ObjectData(rental_object_id, request.form['bathroom'], request.form['wash_place'],
					  			request.form['area'], request.form['ceilings_height'], request.form['win_number'],
								request.form['balcony'], request.form['air_conditioner'],request.form['wi_fi'],
								request.form['furniture'], None, None, None)
				od.window_overlook = {'street': request.form['street_overlook'], 
									  'yard': request.form['yard_overlook']}

				od.window_frame_type = {'wood': request.form['wood_frame'], 
									    'plastic': request.form['plastic_frame']}

				od.cooking_range_type = {'electric': request.form['electric_cooking_range'], 
										 'gas': request.form['gas_cooking_range']}

				# если в поле в соответствующей форме ничего не ввели
				if od.area == '': od.area = None 
				if od.ceilings_height == '': od.ceilings_height = None 
				if od.win_number == '': od.win_number = None 

				db.set_ro_object_data(od.rental_object_id, od.bathroom_type, od.wash_place_type, od.area, od.ceilings_height,
								      od.win_number, od.balcony, od.air_conditioner, od.wi_fi, od.furniture)
				db.set_ro_object_data_data_window_overlook(rental_object_id, od.window_overlook)
				db.set_ro_object_data_window_frame_type(rental_object_id, od.window_frame_type)
				db.set_ro_object_data_cooking_range_type(rental_object_id, od.cooking_range_type)


			elif request.form['source'] == 'building_tab':
				b = Building(rental_object_id, request.form['building_type'], request.form['win_number'], 
									request.form['garbage_disposal'], request.form['intercom'], request.form['concierge'],
					  		        request.form['building_year'], None)
				b.elevator = {'passenger': request.form['passenger_elevator'], 
							  'freight': request.form['freight_elevator']}

				db.set_ro_building(b.rental_object_id, b.building_type, b.floors_number, 
								   b.garbage_disposal, b.intercom, b.concierge, b.building_year)
				db.set_ro_building_elevator(rental_object_id, b.elevator)
				return redirect(url_for('edit_rental_object', rental_object_id=rental_object_id))

			elif request.form['source'] == 'location_tab':
				db.set_ro_location_data(rental_object_id, request.form['country'], 
											   request.form['federal_district'], 
											   request.form['region'],
											   request.form['city'],
											   request.form['city_district'],
											   request.form['street'],
											   request.form['building_number'],
											   request.form['block_number'],
											   request.form['appt'],
											   request.form['entrance_number'],
											   request.form['floor'],
											   request.form['coords'],
											   request.form['nearest_metro_stations'],
											   request.form['location_comment']
											   )


			elif request.form['source'] == 'appliances_tab':
				db.set_ro_appliances_data(rental_object_id,
										  request.form['fridge'],
										  request.form['dishwasher'],
										  request.form['washer'],
										  request.form['television'],
										  request.form['vacuum'],
										  request.form['teapot'],
										  request.form['iron'],
										  request.form['microwave'])

			elif request.form['source'] == 'special_tab':
				rental_object_type = db.get_rental_object_type_by_id(rental_object_id)
				if rental_object_type == 'комната':
					db.set_ro_room_data(rental_object_id, request.form['total_area'], request.form['rooms_number'])

				elif rental_object_type == 'квартира':
					...

				elif rental_object_type == 'дом':
					...
					

			elif request.form['source'] == 'things_tab':
				# загружаем список id вещей, предварительно преобразовав в список python из json
				things_id_list = json.loads(request.form['things_id_list'])

				if things_id_list == ['all']:
					db.del_all_things_by_rental_object_id(rental_object_id)
				else:
					things_list = []
					for id_ in things_id_list:
						things_list.append([int(request.form[f'number_{id_}']),
										    request.form[f'name_{id_}'],
											int(request.form[f'amount_{id_}']),
											float(request.form[f'cost_{id_}'])])
					db.set_ro_things(rental_object_id, things_list)

			elif request.form['source'] == 'costs_tab':
				# загружаем список id расходов, предварительно преобразовав в список python из json
				# список всех id
				all_costs_id = json.loads(request.form['all_costs_id'])

				# список добавленных id 
				added_costs_id = json.loads(request.form['added_costs_id'])
				
				# список существующих id
				db_costs_id = json.loads(request.form['db_costs_id'])

				# список удаляемых из БД id (1 значение)
				del_cost_id = json.loads(request.form['del_cost_id'])

				print('список всех id: ', all_costs_id)
				print('список добавленных id: ', added_costs_id)
				print('список существующих id: ',db_costs_id)
				print('удаленный id: ', bool(del_cost_id))

				# если есть элемент для удаления				
				if del_cost_id:
					db.del_cost(del_cost_id)
				else:
					# обновляем данные для существующих записей
					for id_ in db_costs_id:
						db.update_ro_costs(id_, request.form[f'name_{id_}'], request.form[f'is_payer_landlord_{id_}'])

					# создаем новые записи
					for id_ in added_costs_id:
						db.insert_ro_costs(rental_object_id, request.form[f'name_{id_}'], request.form[f'is_payer_landlord_{id_}'])
			
			return redirect(url_for('edit_rental_object', rental_object_id=rental_object_id))



		else:
			# создадим экземпляр класса Roon, Flat или House
			rental_object_type = db.get_rental_object_type_by_id(rental_object_id)

			if rental_object_type == 'комната':
				rental_object = Room(*db.get_rental_object_data_room(rental_object_id))
			elif rental_object_type == 'квартира':
				rental_object = Flat(*db.get_rental_object_data_flat(rental_object_id))
			elif rental_object_type == 'дом':
				rental_object = House(*db.get_rental_object_data_house(rental_object_id))

			rental_object.general = General(*db.get_general_data(rental_object_id))

			rental_object.object_data = ObjectData(*db.get_object_data(rental_object_id))
			bathroom_types = json.dumps(db.get_bathroom_types())
			wash_place_types = json.dumps(db.get_wash_place_types())

			rental_object.building = Building(*db.get_building_data(rental_object_id))
			building_types = json.dumps(db.get_building_types())

			rental_object.location = Location(*db.get_location_data(rental_object_id))

			rental_object.appliances = Appliances(*db.get_appliances_data(rental_object_id))

			rental_object.things = []
			for thing_data in db.get_ro_things_data(rental_object_id):
				rental_object.things.append(Thing(*thing_data))

			# список айдишников вещей json-формат
			things_id_list = json.dumps([i.id for i in rental_object.things])

			rental_object.costs = []
			for cost_data in db.get_costs_data(rental_object_id):
				rental_object.costs.append(Cost(*cost_data))
			
			# список айдишников расходов json-формат
			costs_id = json.dumps([i.id for i in rental_object.costs])


			test = costs_id

			return render_template('edit_rental_object.html', test=test, the_title=the_title, user_name=session['user_name'],
			 rental_object=rental_object, bathroom_types=bathroom_types, wash_place_types=wash_place_types, building_types=building_types,
			 things_id_list=things_id_list, costs_id=costs_id)

	else:
		abort(401)


# __________Главная: наймодатель -> договоры _________
@application.route('/landlord/rental_agreements', methods=['POST','GET']) 
@logged_in_landlord
def landlord_rental_agreements() -> 'html':
	the_title = 'Договоры'

	# получаем данные договоров аренды для данного наймодателя 
	rental_agreements = [] 
	for data in db.get_rental_agreement_data_of_landlord(session['landlord_id']):
		rental_agreements.append(RentalAgreement(*data))



	return render_template('landlord_rental_agreements.html', the_title=the_title, user_name=session['user_name'], rental_agreements=rental_agreements,
															  landlord_id=session['landlord_id'])

#todo
@application.route('/add_rental_agreement', methods=['POST','GET']) 
@logged_in_landlord
def add_rental_agreement() -> 'html':
	"""Заключение договора найма"""
	the_title = 'Заключение нового договора найма'
	if request.method == 'POST':
		last_renatal_agreement_number = db.get_last_agreement_number()
		if last_renatal_agreement_number:
			renatal_agreement_number = int(last_renatal_agreement_number)+1
		else:
			renatal_agreement_number = 142857

		# создаем запись в таблице rental_agreements
		db.create_rental_agreement(renatal_agreement_number, 'заключен', request.form['landlord_id'])
		# обновляем данные в session
		session['rental_agreements'] = db.get_rental_agreement_id_of_landlord(session['landlord_id'])
		
		rental_agreement_id = ... # ???

		# создаем запись в таблице ra_rental_object (фиксированные данные объекта аренды в договоре)
		# ra_rental_object: [ rental_agreement_id, rental_object_id, type, address, title_deed ]
		# подгузка из rental_objects, ro_general, ro_location по rental_object_id
		rental_object_id = request.form['rental_object_id']

		# создаем запись в таблице ra_landlord (фиксированные данные наймодателя в договоре)
		# ra_landlord: [rental_agreement_id, landlord_id, last_name, first_name, patronymic, phone, 
		# email, serie, pass_number, authority, registration]
		# подгрузка из users, users_landlords, users_passport
		landlord_id = request.form['landlord_id']

		# создаем запись в таблице ra_tenant (фиксированные данные нанимателя в договоре)
		# ra_landlord: [rental_agreement_id, tenant_id, last_name, first_name, patronymic, phone, 
		# email, serie, pass_number, authority, registration]
		# подгрузка из users, users_tenants, users_passport		
		tenant_id = request.form['tenant_id']

		# создаем запись в таблице ra_agent, если он добавлен (фиксированные данные агента в договоре)
		# ra_landlord: [rental_agreement_id, agent_id, last_name, first_name, patronymic, phone, 
		# email, serie, pass_number, authority, registration]
		# подгрузка из users, users_agents, users_passport		
		agent_id = request.form['agent_id']

		# создаем запись в таблице ra_conditions (данные условий договора аренды)
		# ra_conditions: [rental_agreement_id, rental_rate, prepayment, deposit, late_fee, 
		# start_of_term, end_of_term, payment_day, cleaning_cost]
		...

		# создаем запись в таблице ra_things (фиксированные данные описи имущества в договоре)
		# ra_things: [id, rental_agreement_id, thing_number, thing_name, amount, cost]
		# подгрузка из ro_things по rental_object_id 
		...

		# создаем запись в таблице ra_costs (фиксированные данные расходов на содержание в договоре)
		# ra_costs: [id, rental_agreement_id, name, is_payer_landlord]
		# подгрузка из ro_costs по rental_object_id 
		...

		# создаем запись в таблице ra_move_in (данные Акта сдачи-приемки)
		# ra_move_in: [rental_agreement_id, number_of_sets_of_keys, number_of_keys_in_set, rental_object_comment, things_comment]
		...

		return redirect(url_for('landlord_rental_agreements'))

	else:



		# Для select Объект аренды
		rental_objects_query = db.get_rental_objects_data_of_landlord(session['landlord_id'])
		rental_objects = []
		for rental_object in rental_objects_query:
			rental_objects.append(RentalObject(*rental_object))

		# Для select Наниматель
		tenants_query = db.get_tenant_data_of_landlord(session['landlord_id'])
		tenants = []
		for tenant in tenants_query:
			tenants.append(Tenant(*tenant))

		# Для select Агент
		agents_query = db.get_agent_data_of_landlord(session['landlord_id'])
		agents = []
		for agent in agents_query:
			agents.append(Agent(*agent))


	return render_template('add_rental_agreement.html', the_title=the_title, rental_objects=rental_objects, 
														landlord=session['user_name'], tenants=tenants, agents=agents, 
														landlord_id=session['landlord_id'])





@application.route('/delete_rental_agreement', methods=['POST','GET']) 
@logged_in_landlord
def delete_rental_agreement() -> 'html':
	db.delete_rental_agreement(request.form['rental_agreement_id'])
	# обновляем данные в session
	session['rental_agreements'] = db.get_rental_agreement_id_of_landlord(session['landlord_id']) 
	return redirect(url_for('landlord_rental_agreements'))




# __________Главная: наймодатель -> договоры -> договор _________
@application.route('/rental_agreement_documents/<int:rental_agreement_id>', methods=['POST','GET']) 
@logged_in_landlord
def rental_agreement_documents(rental_agreement_id) -> 'html':
	the_title = 'Договор'
	if rental_agreement_id in session['rental_agreements']:
		the_title = 'Договор'
		if request.method == 'POST':
			if request.form['source'] == 'info_tab':
				...
			if request.form['source'] == 'conditions_tab':
				...

			...
		else:
			rental_agreement_data = db.get_rental_agreement_data(rental_agreement_id)
			rental_agreement = RentalAgreement(*rental_agreement_data)

			# ОБЪЕКТ АРЕНДЫ
			ra_rental_object = db.get_ra_rental_object_data(rental_agreement_id)

			# создаем экземпляр класса Room, Flat или House внутри экземпляра класса RentalAgreement
			# заполняем недостающие значения атрибутов заглушками (None)
			rental_object_type = ra_rental_object[1]
			if rental_object_type == 'комната':
				rental_agreement.rental_object = Room(ra_rental_object[0], rental_object_type, None, None, None)
			elif rental_object_type == 'квартира':
				rental_agreement.rental_object = Flat(ra_rental_object[0], rental_object_type, None, None, None)
			elif rental_object_type == 'дом':
				rental_agreement.rental_object = House(ra_rental_object[0], rental_object_type, None, None, None)

			# создаем экземпляр класса Location внутри созданного экземпляра Room, Flat или House
			rental_agreement.rental_object.location = Location(*[None for i in range(0, 15)])
			rental_agreement.rental_object.location.address = ra_rental_object[2]

			# создаем экземпляр класса General внутри созданного экземпляра Room, Flat или House
			# передаем значение последнего атрибута (title_deed)
			rental_agreement.rental_object.general = General(None, None, ra_rental_object[3])

			# НАЙМОДАТЕЛЬ
			# получаем данные наймодателя зафиксированные в договоре
			ra_lanlord = db.get_ra_landlord_data(rental_agreement_id)

			# создаем экземпляр класса Landlord(user_id, name, phone, email, landlord_id, inn) внутри RentalAgreement
			rental_agreement.landlord = Landlord(None, None, ra_lanlord[4], ra_lanlord[5], ra_lanlord[0], None)
			# создаем экземпляр класса Passport внутри Landlord
			# Passport(user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
			# department_code, date_of_issue, date_of_birth, place_of_birth, registration)
			rental_agreement.landlord.passport = Passport(None, ra_lanlord[2], ra_lanlord[3], ra_lanlord[1], ra_lanlord[6], ra_lanlord[7],
													ra_lanlord[8], None, None, None, None, ra_lanlord[9])


			# НАНИМАТЕЛЬ
			# получаем данные нанимателя зафиксированные в договоре
			ra_tenant = db.get_ra_tenant_data(rental_agreement_id)
			# создаем экземпляр класса Landlord(user_id, name, phone, email, landlord_id, inn) внутри RentalAgreement
			rental_agreement.tenant = Tenant(None, None, ra_tenant[4], ra_tenant[5], ra_tenant[0], None)
			# создаем экземпляр класса Passport внутри Landlord
			# Passport(user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
			# department_code, date_of_issue, date_of_birth, place_of_birth, registration)
			rental_agreement.tenant.passport = Passport(None, ra_tenant[2], ra_tenant[3], ra_tenant[1], ra_tenant[6], ra_tenant[7],
													ra_tenant[8], None, None, None, None, ra_tenant[9])


			# АГЕНТ
			# получаем данные нанимателя зафиксированные в договоре
			ra_agent = db.get_ra_agent_data(rental_agreement_id)
			# создаем экземпляр класса Landlord(user_id, name, phone, email, landlord_id, inn) внутри RentalAgreement
			rental_agreement.agent = Agent(None, None, ra_agent[4], ra_agent[5], ra_agent[0], None)
			# создаем экземпляр класса Passport внутри Landlord
			# Passport(user_id, first_name, patronymic, last_name, serie, pass_number, authority, 
			# department_code, date_of_issue, date_of_birth, place_of_birth, registration)
			rental_agreement.agent.passport = Passport(None, ra_agent[2], ra_agent[3], ra_agent[1], ra_agent[6], ra_agent[7],
													ra_agent[8], None, None, None, None, ra_agent[9])


			# УСЛОВИЯ ДОГОВОРА
			# создаем экземпляр класса Conditions внутри RentalAgreement
			rental_agreement.conditions = Conditions(*db.get_ra_conditions_data(rental_agreement_id))

			# АКТ СДАЧИ-ПРИЕМКИ
			rental_agreement.move_in = MoveIn(*db.get_ra_move_in_data(rental_agreement_id))

			# АКТ ВОЗВРАТА		
			rental_agreement.move_out = MoveOut(*db.get_ra_move_out_data(rental_agreement_id))

			# ДОСРОЧНОЕ РАСТОРЖЕНИЕ		
			rental_agreement.termination = Termination(*db.get_ra_termination(rental_agreement_id))
			if not rental_agreement.termination.end_of_term:
				rental_agreement.termination.end_of_term = 'Договор не расторгался'


			# ДОСРОЧНОЕ ПРОДЛЕНИЕ				
			rental_agreement.renewal = Renewal(rental_agreement_id, db.get_ra_renewal(rental_agreement_id))


	else:
		abort(401)
	return render_template('rental_agreement_documents.html', the_title=the_title, user_name=session['user_name'], rental_agreement=rental_agreement)











# удаление пользователя объекта недвижимости
@application.route('/delete_rental_object', methods=['POST','GET']) 
@logged_in_landlord
def delete_rental_object() -> 'html':
	db.delete_rental_object(request.form['rental_object_id'])
	session['rental_objects'] = db.get_rental_object_id_of_landlord(session['landlord_id'])
	return redirect(url_for('landlord_rental_objects'))


# __________ГЛАВНАЯ: НАНИМАТЕЛЬ_________
@application.route('/tenant', methods=['POST','GET']) 
@logged_in_tenant
def index_tenant() -> 'html':
	""""""
	the_title = 'Наниматель'
	user_name = session['user_name']
	return render_template('index_tenant.html', the_title=the_title, user_name=user_name)

# __________ГЛАВНАЯ: АГЕНТ_________
@application.route('/agent', methods=['POST','GET'])
@logged_in_agent
def index_agent() -> 'html':
	""""""
	the_title = 'Агент'
	user_name = session['user_name']
	return render_template('index_agent.html', the_title=the_title, user_name=user_name)


# удаление пользователя
@application.route('/delete_user', methods=['POST','GET'])
@logged_in
def delete_user() -> 'html':
	user_id = request.form['user_id']
	user_type = request.form['user_type']

	db.delete_user(user_id)
	if user_type == 'администратор':
		...
	elif user_type == 'наймодатель':
		# обновляем список user_id наймодателей, данного администратора 
		session['landlords'] = db.get_landlord_user_id_of_admin(session['admin_id']) 
		# редирект на список всех наймодателей данного администратора
		return redirect(url_for('admin_landlords'))
	elif user_type == 'наниматель':
		# обновляем список user_id нанимателей, данного наймодателя 
		session['tenants'] = db.get_tenant_user_id_of_landlord(session['landlord_id']) 
		# редирект на список всех нанимателей данного наймодателя
		return redirect(url_for('landlord_tenants'))
	elif user_type == 'агент':
		...








# __________ОРАБОТКА ОШИБКИ 404________
@application.errorhandler(404)
def page_not_found(error):
	return render_template('page404.html', the_title='Страница не найдена'), 404


# __________ОРАБОТКА ОШИБКИ 401________
@application.errorhandler(401)
def page_not_found(error):
	return render_template('page401.html', the_title='Доступ запрещен'), 401


if __name__ == '__main__':
	application.run(debug=True) # запуск локально
	# db.create_rental_object('комната', 1)

	# # 
	# print(db.get_rental_object_data(2))
	# print(db.get_general_data(2))
	# print(db.get_object_data(2))
	# print(db.get_building_data(2))
	# print(db.get_location_data(2))
	# print(db.get_appliance_data(2))





	# ПЕРЕЗАГРУЗКА ТАБЛИЦ И ТЕСТОВЫХ ДАННЫХ
	# db_def.reload_all_tables()
	# db.add_default_data()
	# db.add_test_data()



	# ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ ДЛЯ ВХОДА
	# db.create_user('администратор', 'Админ Никита', '+792188550028', 'admin@admin.ru', 'admin', generate_password_hash('12345'))
	# print(db.get_last_insert_id_users())

	# landlord = Landlord(2)
	# landlord.register.login = 'landlord'
	# landlord.register.password = '12345'

	# tenant = Tenant(3)
	# tenant.register.login = 'tenant'
	# tenant.register.password = '12345'


	# agent = Agent(4)
	# agent.register.login = 'agent'
	# agent.register.password = '12345'


	# db.create_landlord('Софья', '+79218899988', 'sofia@sofia.ru', 1)













