from werkzeug.security import generate_password_hash, check_password_hash 
import os
import json
from datetime import date, datetime

# ------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort,make_response # импортируем функции модуля flask

application = Flask(__name__) #создание экземпляра объекта Flask и присваивание его переменной "application" 

application.config['SECRET_KEY'] = 'd1269dcb5c175acb12678fa83e66e9ca1a707cb4'
application.config['PERMANENT_SESSION_LIFETIME'] = 604800 # неприрывное время жизни сеанса в секундах (604800 сек. = 7 суток)
application.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------------------------------------------------------

from login_checker import logged_in, logged_in_admin, logged_in_landlord, logged_in_tenant, logged_in_agent

from users import User, Admin, Agent, Landlord, Tenant # пользователи
from passport import Passport # паспортные данные пользователей
from register import Register # регистрационные данные пользоватлей

from rental_objects import RentalObject, Room, Flat, House # объекты аренды
from rental_object_data import General, ObjectData, Building, Location, Appliances, Thing, Cost

from rental_agreement import RentalAgreement # договор аренд
from rental_agreement_conditions import Conditions# условия аренды
from rental_agreement_data import RA_RentalObject, RA_Cost, RA_Thing, RA_Landlord, RA_Tenant, RA_Agent, MoveIn, MoveOut, Termination, Renewal

# преобразования строк полученных из формы в другие типы
from form_str import FormStr

# генерация pdf документов
from pdf_maker import create_ra_pdf, create_things_pdf, create_move_in_pdf, create_move_out_pdf, create_termination_pdf

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

	return render_template('admin_landlords.html', the_title=the_title, user_name=session['user_name'],
						   landlords=landlords, add_landlord=add_landlord)




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
	# подгружаем данные из БД 
	rental_objects_data = db.get_rental_objects_data_of_landlord(session['landlord_id'])

	# список экземпляров классов Room, Flat или House
	rental_objects = []

	for rental_object in rental_objects_data:
		if rental_object[1] == 'комната':
			# добавляем добавляем недостающий для инициализации класса аргументы (total_area, rooms_number)
			ro = Room(*rental_object+(None,)+(None,))
		elif rental_object[1] == 'квартира':
			ro = Flat(*rental_object+(None,))
		elif rental_object[1] == 'дом':
			ro = House(*rental_object+(None,))

		rental_objects.append(ro)

	return render_template('landlord_rental_objects.html', the_title=the_title, user_name=session['user_name'], rental_objects=rental_objects)




@application.route('/delete_rental_object', methods=['POST','GET']) 
@logged_in_landlord
def delete_rental_object() -> 'html':
	rental_object_id = request.form['rental_object_id']
	landlord_id = session['landlord_id']
	# получаем статус удаляемого объекта аренды
	ro_status  = RentalObject(*db.get_rental_object_data(rental_object_id)).status
	if ro_status == 'занят':
		flash('Невозможно удалить: объект аренды связан с действующим договором',
			   category='error')
	else:
		# удаляем объект аренды
		db.delete_rental_object(rental_object_id)
		session['rental_objects'] = db.get_rental_object_id_of_landlord(landlord_id)
	return redirect(url_for('landlord_rental_objects'))





@application.route('/landlord/rental_objects/add_rental_object', methods=['POST','GET']) 
@logged_in_landlord
def add_rental_object() -> 'html':
	the_title = 'Добавление объекта аренды'
	if request.method == 'POST':

		# записываем данные в таблицу rental_objects
		db.create_rental_object(request.form['type_id'], request.form['name'], 
								'свободен', request.form['rooms_number'],  session['landlord_id'])

		# обновлем список rantal_object_id в session
		session['rental_objects'] = db.get_rental_object_id_of_landlord(session['landlord_id'])
		
		# получаем последний добавленный id для rental_objects
		rental_object_id = db.get_last_rental_object_id()

		flash(f'Объект аренды успешно добавлен', category='success')
		return redirect(url_for('landlord_rental_objects'))

	else:
		# получаем типы объектов
		rental_objects_types = db.get_rental_objects_types()
		# получаем имена агентов
		agents = []
		for agent in db.get_agent_data_of_landlord(session['landlord_id']):
			agents.append(Agent(*agent))


		return render_template('add_rental_object.html', the_title=the_title, rental_objects_types=rental_objects_types, agents=agents)


# __________Главная: наймодатель -> агенты -> агент _________
@application.route('/landlord/rental_objects/edit_rental_object/<int:rental_object_id>', methods=['POST','GET']) 
@logged_in_landlord
def edit_rental_object(rental_object_id) -> 'html':
	""""""
	if rental_object_id in session['rental_objects']:
		the_title = 'Объект аренды'

		if request.method == 'POST':
			if request.form['source'] == 'info_tab':
				db.update_rental_object_name(rental_object_id, request.form['name'])
				db.set_ro_general_data(rental_object_id, request.form['cadastral_number'], request.form['title_deed'])
				try:
					status = request.form['status']
					db.update_rental_object_status(rental_object_id, status)
				except:
					pass
				flash(f"Данные в разделе 'Информация' успешно сохранены", category='success')
				

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
				flash(f"Данные в разделе 'Объект' успешно сохранены", category='success')

			elif request.form['source'] == 'building_tab':
				b = Building(rental_object_id, request.form['building_type'], request.form['win_number'], 
									request.form['garbage_disposal'], request.form['intercom'], request.form['concierge'],
					  		        request.form['building_year'], None)
				b.elevator = {'passenger': request.form['passenger_elevator'], 
							  'freight': request.form['freight_elevator']}

				db.set_ro_building(b.rental_object_id, b.building_type, b.floors_number, 
								   b.garbage_disposal, b.intercom, b.concierge, b.building_year)
				db.set_ro_building_elevator(rental_object_id, b.elevator)
				flash(f"Данные в разделе 'Здание' успешно сохранены", category='success')
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
											   request.form['location_comment'])
				flash(f"Данные в разделе 'Локация' успешно сохранены", category='success')


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
				flash(f"Данные в разделе 'Бытовая техника' успешно сохранены", category='success')


			elif request.form['source'] == 'special_tab':
				rental_object_type = db.get_rental_object_type_by_id(rental_object_id)
				if rental_object_type == 'комната':
					db.set_ro_room_data(rental_object_id, request.form['total_area'])

				elif rental_object_type == 'квартира':
					...

				elif rental_object_type == 'дом':
					...
				flash(f"Данные в разделе '{rental_object_type.title()}' успешно сохранены", category='success')					

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
				flash(f"Данные в разделе 'Вещи' успешно сохранены", category='success')	


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
				flash(f"Данные в разделе 'Расходы' успешно сохранены", category='success')				

			elif request.form['source'] == 'agent_tab':
				# удаляем из таблице ro_id_agent_id строки для данного объекта аренды  
				db.delete_from_ro_id_agent_id(rental_object_id)

				agent_id = request.form['agent_id']
				# если agent_id не пустая строка 
				if agent_id != '':
					# делаем запись в таблице ro_id_agent_id
					db.insert_into_ro_id_agent_id(rental_object_id, agent_id)
				# если пустая, то ничего не делаем
				else:
					pass			
				flash(f"Данные в разделе 'Агент' успешно сохранены", category='success')	

			return redirect(url_for('edit_rental_object', rental_object_id=rental_object_id))



		else:
			# получим тип объекта по id
			rental_object_type = db.get_rental_object_type_by_id(rental_object_id)
			# создадим экземпляр класса Room, Flat или House
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


			# список агентов наймодателя из таблицы users_agents
			agents = [] 
			for agent in db.get_agent_data_of_landlord(session['landlord_id']):
				agents.append(Agent(*agent))

			# связанный с объектом агент
			try:
				rental_object.agent = Agent(*db.get_linked_agent_data(rental_object.id))
			except:
				rental_object.agent = Agent(*[None for i in range(5)])




			test = costs_id

			return render_template('edit_rental_object.html', test=test, the_title=the_title, user_name=session['user_name'],
			 rental_object=rental_object, bathroom_types=bathroom_types, wash_place_types=wash_place_types, building_types=building_types,
			 things_id_list=things_id_list, costs_id=costs_id, agents=agents)

	else:
		abort(401)





# __________Главная: наймодатель -> текущие договоры _________
@application.route('/landlord/rental_agreements/current', methods=['POST','GET']) 
@logged_in_landlord
def landlord_rental_agreements() -> 'html':
	the_title = 'Текущие договоры'

	# получаем данные договоров аренды для данного наймодателя 
	test = []
	rental_agreements = [] 
	for ra_data in db.get_rental_agreement_data_of_landlord(session['landlord_id']):
		rental_agreement = RentalAgreement(*ra_data)

		# подгружаем данные объекта аренды договора
		ra_rental_object_data = db.get_ra_rental_object_data(rental_agreement.id)
		rental_agreement.rental_object = RA_RentalObject(*ra_rental_object_data)

		# подгружаем данные нанимателя договора
		ra_tenant_data = db.get_ra_tenant_data(rental_agreement.id)
		rental_agreement.tenant = RA_Tenant(rental_agreement.id, *ra_tenant_data)

		# подгружаем данные агента договора
		try:
			ra_agent_data = db.get_ra_agent_data(rental_agreement.id)
			rental_agreement.agent = RA_Agent(rental_agreement.id, *ra_agent_data)
		except:
			pass

		# подгружаем данные условий текущего договора 
		rental_agreement.conditions = Conditions(*db.get_ra_conditions_data(rental_agreement.id))

		if rental_agreement.status == 'заключен' or rental_agreement.status == 'продлен':
			rental_agreements.append(rental_agreement)

	return render_template('landlord_rental_agreements.html', the_title=the_title, user_name=session['user_name'], 
							rental_agreements=rental_agreements, landlord_id=session['landlord_id'])



# __________Главная: наймодатель ->  договоры (архив) _________
@application.route('/landlord/rental_agreements/archive', methods=['POST','GET']) 
@logged_in_landlord
def landlord_rental_agreements_archive() -> 'html':
	the_title = 'Договоры (архив)'

	# получаем данные договоров аренды для данного наймодателя 
	test = []
	rental_agreements = [] 
	for ra_data in db.get_rental_agreement_data_of_landlord(session['landlord_id']):
		rental_agreement = RentalAgreement(*ra_data)

		# подгружаем данные объекта аренды договора
		ra_rental_object_data = db.get_ra_rental_object_data(rental_agreement.id)
		rental_agreement.rental_object = RA_RentalObject(*ra_rental_object_data)

		# подгружаем данные нанимателя договора
		ra_tenant_data = db.get_ra_tenant_data(rental_agreement.id)
		rental_agreement.tenant = RA_Tenant(rental_agreement.id, *ra_tenant_data)

		# подгружаем данные агента договора
		try:
			ra_agent_data = db.get_ra_agent_data(rental_agreement.id)
			rental_agreement.agent = RA_Agent(rental_agreement.id, *ra_agent_data)
		except:
			pass


		if rental_agreement.status == 'завершен' or rental_agreement.status == 'досрочно расторгнут':
			rental_agreements.append(rental_agreement)

	return render_template('landlord_rental_agreements_archive.html', 
							the_title=the_title, user_name=session['user_name'], rental_agreements=rental_agreements,
							landlord_id=session['landlord_id'])


@application.route('/add_rental_agreement', methods=['POST','GET']) 
@logged_in_landlord
def add_rental_agreement() -> 'html':
	"""Заключение договора найма"""
	the_title = 'Заключение нового договора найма'
	if request.method == 'POST':
		# подгружаем необходимые для формирования договора данные выбранного объекта аренды
		rental_object_id = request.form['rental_object_id']
		rental_object = RentalObject(*db.get_rental_object_data(rental_object_id))
		rental_object.location = Location(*db.get_location_data(rental_object_id))
		rental_object.general = General(*db.get_general_data(rental_object_id))

		# подгружаем необходимые для формирования договора данные наймодателя
		landlord_id = request.form['landlord_id']
		landlord = Landlord(*db.get_landlord_data_by_landlord_id(landlord_id))
		landlord.passport = Passport(*db.get_passport_data(landlord.user_id))

		# подгружаем необходимые для формирования договора данные нанимателя		
		tenant_id = request.form['tenant_id']
		tenant = Tenant(*db.get_tenant_data_by_tenant_id(tenant_id))
		tenant.passport = Passport(*db.get_passport_data(tenant.user_id))

		try:
			# подгружаем необходимые для формирования договора данные агента (если он привязан к сдаваемому объекту)	
			agent = Agent(*db.get_linked_agent_data(rental_object.id))
			agent.passport = Passport(*db.get_passport_data(agent.user_id))
		except:
			agent = None

		# проверяем есть ли пустые строки в необъодимых для формирования договора данных объекта аренды
		ro_empty_strings = rental_object.location.get_empty_strings() + rental_object.general.get_empty_strings()
		# проверяем есть ли пустые строки в необъодимых для формирования договора данных наймодателя
		landlord_empty_strings = landlord.get_empty_strings() +  landlord.passport.get_empty_strings()
		# проверяем есть ли пустые строки в необъодимых для формирования договора данных нанимателя
		tenant_empty_strings = tenant.get_empty_strings() + tenant.passport.get_empty_strings()
		# проверяем есть ли пустые строки в необъодимых для формирования договора данных агента (если он есть)
		if agent:
			agent_empty_strings = agent.get_empty_strings() +  agent.passport.get_empty_strings()
		else:
			agent_empty_strings = []

		empty_strings = {'Для объекта аренды': ro_empty_strings, 
					     'Для наймодателя': landlord_empty_strings, 
						 'Для нанимателя':tenant_empty_strings, 
						 'Для агента': agent_empty_strings}

		# флаг: есть недостающие данные?
		is_any_empty_str = False
		# cоздаем мгновенные сообщения для вывода наименований недостающих данных
		for k, v in empty_strings.items():
			if v:
				flash(f"{k} не указано: {', '.join(v)}", category='error')
				if not is_any_empty_str:
					is_any_empty_str = True

		# прерываем создание договора и возвращаемся на стр с формой если каких то данных нет
		if is_any_empty_str:
			return redirect(url_for('add_rental_agreement'))
		else:
			# формируем номер договора
			last_renatal_agreement_number = db.get_last_agreement_number()
			if last_renatal_agreement_number:
				renatal_agreement_number = int(last_renatal_agreement_number)+1
			else:
				renatal_agreement_number = 142857

			# получаем текщую дату и время (без микросекунд)
			datetime_of_creation = datetime.now().replace(microsecond=0)

			# создаем запись в таблице rental_agreements
			db.create_rental_agreement(renatal_agreement_number, datetime_of_creation, request.form['city'], 
									   request.form['date_of_conclusion_agreement'], 'заключен', request.form['landlord_id'])
			# обновляем данные в session
			session['rental_agreements'] = db.get_rental_agreement_id_of_landlord(session['landlord_id'])
			
			rental_agreement_id = db.get_last_agreement_id()


			# создаем запись в таблице ra_rental_object (фиксированные данные объекта аренды в договоре)
			db.insert_into_ra_rental_object(rental_agreement_id, rental_object_id, rental_object.type, rental_object.location.address,
											rental_object.general.title_deed)


			# создаем запись в таблице ra_landlord (фиксированные данные наймодателя в договоре)
			db.insert_into_ra_landlord(rental_agreement_id, landlord_id, landlord.passport.last_name, landlord.passport.first_name, 
									   landlord.passport.patronymic, landlord.phone, landlord.email, landlord.passport.serie, 
									   landlord.passport.pass_number, landlord.passport.authority, landlord.passport.registration)


			# создаем запись в таблице ra_tenant (фиксированные данные нанимателя в договоре)
			db.insert_into_ra_tenant(rental_agreement_id, tenant_id, tenant.passport.last_name, tenant.passport.first_name, 
									 tenant.passport.patronymic, tenant.phone, tenant.email, tenant.passport.serie, 
									 tenant.passport.pass_number, tenant.passport.authority, tenant.passport.registration)

			# записываем данные связанного с объектом агента если он есть (фиксированные данные агента в договоре)
			if agent:
				db.insert_into_ra_agent(rental_agreement_id, agent.agent_id, agent.passport.last_name, agent.passport.first_name, 
							 agent.passport.patronymic, agent.phone, agent.email, agent.passport.serie, 
							 agent.passport.pass_number, agent.passport.authority, agent.passport.registration)

			# создаем запись в таблице ra_other_tenants (совместо проживающие с нанимателем граждане)
			other_tenants = [
							 [request.form['name1'], request.form['phone1']], 
							 [request.form['name2'], request.form['phone2']],
							 [request.form['name3'], request.form['phone3']]
							 ]
			for i in other_tenants:
				if i[0]:
					db.insert_into_ra_other_tenants(rental_agreement_id, i[0], i[1])


			# создаем запись в таблице ra_conditions (данные условий договора аренды)
			db.insert_into_ra_conditions(rental_agreement_id, request.form['rental_rate'], request.form['prepayment'], 
										 request.form['deposit'], request.form['late_fee'], request.form['start_of_term'], 
										 request.form['end_of_term'], request.form['payment_day'], request.form['cleaning_cost'])
			# создаем запись в таблице ra_things (фиксированные данные описи имущества в договоре)
			# создаем список для pdf документа

			things_for_pdf = [('№', 'Наименование предмета', 'Кол-во, шт', 'Стоимость ед., руб.')]
			for thing_data in db.get_things(rental_object.id):
				thing = Thing(*thing_data)
				things_for_pdf.append((thing.thing_number, thing.thing_name, thing.amount, int(thing.cost)))
				print()
				db.insert_into_ra_things(rental_agreement_id, thing.thing_number, thing.thing_name, thing.amount, thing.cost)

			# создаем запись в таблице ra_costs (фиксированные данные расходов на содержание в договоре)
			cost_for_pdf = []
			cost_data = db.get_costs_data(rental_object.id)
			for cost in cost_data:
				cost = Cost(*cost)
				cost_for_pdf.append(cost.name)
				print(rental_agreement_id, cost.name, cost.is_payer_landlord)
				db.insert_into_ra_costs(rental_agreement_id, cost.name, cost.is_payer_landlord)

			# создаем запись в таблице ra_move_in (данные Акта сдачи-приемки)
			db.insert_into_ra_move_in(rental_agreement_id, request.form['date_of_conclusion_move_in'],
														request.form['number_of_sets_of_keys'], 
														request.form['number_of_keys_in_set'], 
														request.form['rental_object_comment'], 
														request.form['things_comment'])
			# обновляем статус для объекта аренды
			db.update_rental_object_status(rental_object_id, 'занят')

			# PDF: ДОГОВОР НАЙМА ЖИЛОГО ПОМЕЩЕНИЯ
			# преобразуем строки полученные из формы в тип datetime 
			date_of_conclusion = datetime(*[int(i) for i in request.form['date_of_conclusion_agreement'].split('-')])
			start_of_term = datetime(*[int(i) for i in request.form['start_of_term'].split('-')])
			end_of_term = datetime(*[int(i) for i in request.form['end_of_term'].split('-')])

			# получаем тип объекта аренды
			rental_object_type = db.get_rental_object_type_by_id(rental_object_id)

			# форматируем список other_tenants для pdf 
			other_tenants_for_pdf = []
			for i in other_tenants:
				if i[0] == '':
					other_tenants_for_pdf.append('')
				else:
					other_tenants_for_pdf.append(f'{i[0]}, {i[1]}')

			# определяем часть имени pdf файла для того чтобы повторно созданный файл с
			# тем же номером заказа не кешировался браузером
			ra = RentalAgreement(None, None, datetime_of_creation, None, None,None)
			ra.datetime_of_creation = datetime_of_creation
			anti_cache_part_of_pdf_name = ra.anti_cache_part_of_pdf_name()

			# определяем имя и расположение pdf файла
			ra_pdf = f"static/pdf/rental_agreements/ra_{anti_cache_part_of_pdf_name}_{renatal_agreement_number}.pdf"


			# данные для создания pdf документа 'Договор найма жилого помещения'
			ra_data = dict(	pdf_name = ra_pdf,
							rental_agreement_number = renatal_agreement_number,
						   	city = request.form['city'], 
							date_of_conclusion = date_of_conclusion,
							landlord = f'{landlord.passport.last_name} {landlord.passport.first_name} {landlord.passport.patronymic}',
							tenant = f'{tenant.passport.last_name} {tenant.passport.first_name} {tenant.passport.patronymic}',
							title_deed = f"{rental_object.general.title_deed}",
							renatal_object_type = rental_object_type,
							address = f'{rental_object.location.address}',
							other_tenants = other_tenants_for_pdf,
							rental_rate = f"{int(request.form['rental_rate'])}",
							payment_day = f"{int(request.form['payment_day'])}", 
							deposit = f"{int(request.form['deposit'])}", 
							costs = cost_for_pdf,
							cleaning_cost = f"{int(request.form['cleaning_cost'])}", 
							start_of_term = start_of_term,
							end_of_term = end_of_term,
							late_fee = f"{int(request.form['late_fee'])}",

							l_serie = f'{landlord.passport.serie}',
							l_pass_number = f'{landlord.passport.pass_number}',
							l_authority = f'{landlord.passport.authority}',
							l_registration = f'{landlord.passport.registration}',
							l_phone = f'{landlord.phone}',
							l_email = f'{landlord.email}',

							t_serie = f'{tenant.passport.serie}',
							t_pass_number = f'{tenant.passport.pass_number}',
							t_authority = f'{tenant.passport.authority}',
							t_registration = f'{tenant.passport.registration}',
							t_phone = f'{tenant.phone}',
							t_email = f'{tenant.email}')

			# создаем pdf документ 'Договор найма жилого помещения'
			create_ra_pdf(**ra_data)

			# определяем имя и расположение pdf файла
			things_pdf = f"static/pdf/things/things_{anti_cache_part_of_pdf_name}_{renatal_agreement_number}.pdf"			

			# PDF: ОПИСЬ ИМУЩЕСТВА
			things_data = dict(pdf_name = things_pdf,
							   rental_agreement_number = renatal_agreement_number,
							   city = request.form['city'],
							   date_of_conclusion = date_of_conclusion,
							   things = things_for_pdf)

			create_things_pdf(**things_data)

			# PDF: АКТ СДАЧИ-ПРИЕМКИ
			# преобразуем строки полученные из формы в тип datetime 			
			date_of_conclusion_move_in = datetime(*[int(i) for i in request.form['date_of_conclusion_move_in'].split('-')])


			# определяем имя и расположение pdf файла
			move_in_pdf = f"static/pdf/move_in/move_in_{anti_cache_part_of_pdf_name}_{renatal_agreement_number}.pdf"		

			move_in_data = dict(pdf_name = move_in_pdf,
								rental_agreement_number=renatal_agreement_number,
								city = request.form['city'],
								date_of_conclusion_move_in = date_of_conclusion_move_in,
								date_of_conclusion = date_of_conclusion,
								number_of_sets_of_keys = request.form['number_of_sets_of_keys'],
								number_of_keys_in_set = request.form['number_of_keys_in_set'],
								rental_object_comment = request.form['rental_object_comment'],
								things_comment = request.form['things_comment'])

			create_move_in_pdf(**move_in_data)

			flash(f'Договор успешно заключен', category='success')
			return redirect(url_for('landlord_rental_agreements'))

	else:

		# Для select Объект аренды
		rental_objects_query = db.get_rental_objects_data_of_landlord(session['landlord_id'])
		rental_objects = []
		for rental_object in rental_objects_query:
			ro = RentalObject(*rental_object)
			if ro.status == 'свободен':
				rental_objects.append(ro)
		if not rental_objects:
			flash("Невозможно заключить новый договор: нет объектов аренды со статусом 'свободен'", category='error')
			return redirect(url_for('landlord_rental_agreements'))


		# Для select Наниматель
		tenants_query = db.get_tenant_data_of_landlord(session['landlord_id'])
		tenants = []
		for tenant in tenants_query:
			tenants.append(Tenant(*tenant))


	return render_template('add_rental_agreement.html', the_title=the_title, rental_objects=rental_objects, 
														landlord=session['user_name'], tenants=tenants, 
														landlord_id=session['landlord_id'])





@application.route('/delete_rental_agreement', methods=['POST','GET']) 
@logged_in_landlord
def delete_rental_agreement() -> 'html':
	rental_agreement_id = request.form['rental_agreement_id'] 

	# создаем экземпляр класса RentalAgreement
	ra = RentalAgreement(*db.get_rental_agreement_data(rental_agreement_id))

	# меняем статус объекта аренды который указан в договоре на 'свободен'
	if ra.status == 'заключен' or ra.status == 'продлен':
		rental_object_id = RA_RentalObject(*db.get_ra_rental_object_data(rental_agreement_id)).rental_object_id
		db.update_rental_object_status(rental_object_id, 'свободен')
	else:
		pass

	# получим anti-cache часть имени pdf файла
	anti_cache_part_of_pdf_name = ra.anti_cache_part_of_pdf_name()

	# удаляем договор
	os.remove(f'static/pdf/rental_agreements/ra_{anti_cache_part_of_pdf_name }_{ra.agreement_number}.pdf')
	# удаляем опись имущества
	os.remove(f'static/pdf/things/things_{anti_cache_part_of_pdf_name }_{ra.agreement_number}.pdf')
	# удаляем акт сдачи-приемки
	os.remove(f'static/pdf/move_in/move_in_{anti_cache_part_of_pdf_name }_{ra.agreement_number}.pdf')

	# удаляем акт возврата (его может не быть)
	try:
		os.remove(f'static/pdf/move_out/move_out_{anti_cache_part_of_pdf_name }_{ra.agreement_number}.pdf')
	except:
		pass
	# удаляем соглашение о расторжении (его может не быть)
	try:
		os.remove(f'static/pdf/termination/termination_{anti_cache_part_of_pdf_name }_{ra.agreement_number}.pdf')
	except:
		pass

	# удаляем договор в БД (связанные таблицы удаляются из-за DELETE CASCADE)
	db.delete_rental_agreement(rental_agreement_id)

	# обновляем данные в session
	session['rental_agreements'] = db.get_rental_agreement_id_of_landlord(session['landlord_id'])
	flash(f'Договор успешно удален', category='success')

	# возвращаемся на страницу на которой было произведено удаление
	if request.form['source'] == 'current':
		return redirect(url_for('landlord_rental_agreements'))
	elif request.form['source'] == 'archive':
		return redirect(url_for('landlord_rental_agreements_archive'))




# __________Главная: наймодатель -> договоры -> договор _________
@application.route('/rental_agreement_documents/<int:rental_agreement_id>', methods=['POST','GET']) 
@logged_in_landlord
def rental_agreement_documents(rental_agreement_id) -> 'html':
	the_title = 'Договор'
	if rental_agreement_id in session['rental_agreements']:
		the_title = 'Договор'

		rental_agreement_data = db.get_rental_agreement_data(rental_agreement_id)
		rental_agreement = RentalAgreement(*rental_agreement_data)

		# ОБЪЕКТ АРЕНДЫ
		rental_agreement.rental_object = RA_RentalObject(*db.get_ra_rental_object_data(rental_agreement_id))

		# ОПИСЬ ИМУЩЕСТВА 
		rental_agreement.things =  [RA_Thing(*thing) for thing in db.get_ra_things(rental_agreement_id)]
		# RA_Thing()


		# ЗАТРАТЫ НА СОДЕРЖАНИЕ
		rental_agreement.costs = [RA_Cost(*cost) for cost in db.get_ra_costs(rental_agreement_id)]	


		# НАЙМОДАТЕЛЬ
		# получаем данные наймодателя зафиксированные в договоре
		rental_agreement.lanlord = RA_Landlord(rental_agreement_id, *db.get_ra_landlord_data(rental_agreement_id))



		# НАНИМАТЕЛЬ
		# получаем данные нанимателя зафиксированные в договоре
		rental_agreement.tenant = RA_Tenant(rental_agreement_id, *db.get_ra_tenant_data(rental_agreement_id))



		# АГЕНТ
		# получаем данные нанимателя зафиксированные в договоре
		try:
			rental_agreement.agent = RA_Agent(rental_agreement_id, *db.get_ra_agent_data(rental_agreement_id))
		except:
			pass

		# УСЛОВИЯ ДОГОВОРА
		# создаем экземпляр класса Conditions внутри RentalAgreement
		rental_agreement.conditions = Conditions(*db.get_ra_conditions_data(rental_agreement_id))

		# АКТ СДАЧИ-ПРИЕМКИ
		rental_agreement.move_in = MoveIn(*db.get_ra_move_in_data(rental_agreement_id))

		# АКТ ВОЗВРАТА		
		try:
			rental_agreement.move_out = MoveOut(*db.get_ra_move_out_data(rental_agreement_id))
		except:
			pass

		# ДОСРОЧНОЕ РАСТОРЖЕНИЕ
		try:
			rental_agreement.termination = Termination(*db.get_ra_termination(rental_agreement_id))
		except:
			pass

		# добавляем anti_cache часть имени
		anti_cache_part_of_pdf_name = rental_agreement.anti_cache_part_of_pdf_name()

		# пути к документам
		ra_pdf = f'pdf/rental_agreements/ra_{anti_cache_part_of_pdf_name}_{rental_agreement.agreement_number}.pdf'
		things_pdf = f'pdf/things/things_{anti_cache_part_of_pdf_name}_{rental_agreement.agreement_number}.pdf'
		move_in_pdf = f'pdf/move_in/move_in_{anti_cache_part_of_pdf_name}_{rental_agreement.agreement_number}.pdf'
		move_out_pdf = f'pdf/move_out/move_out_{anti_cache_part_of_pdf_name}_{rental_agreement.agreement_number}.pdf'
		termination_pdf = f'pdf/termination/termination_{anti_cache_part_of_pdf_name}_{rental_agreement.agreement_number}.pdf'

		return render_template('rental_agreement_documents.html', the_title=the_title, user_name=session['user_name'], 
								rental_agreement=rental_agreement, ra_pdf=ra_pdf, things_pdf=things_pdf, move_in_pdf =move_in_pdf,
								move_out_pdf=move_out_pdf, termination_pdf=termination_pdf)


	else:
		abort(401)
	












@application.route('/rental_agreement_termination/<int:rental_agreement_id>', methods=['POST','GET']) 
@logged_in_landlord
def rental_agreement_termination(rental_agreement_id) -> 'html':
	"""Вывод форму для заполнения Акта возврата"""
	the_title = 'Завершение договора аренды'
	return render_template('rental_agreement_termination.html', the_title=the_title, user_name=session['user_name'],
															    rental_agreement_id=rental_agreement_id)


@application.route('/rental_agreement_early_termination/<int:rental_agreement_id>', methods=['POST','GET']) 
@logged_in_landlord
def rental_agreement_early_termination(rental_agreement_id) -> 'html':
	"""Вывод форму для заполнения Акта возврата и Соглашения о расторжении"""
	the_title = 'Досрочное расторжение договора аренды'
	return render_template('rental_agreement_early_termination.html', the_title=the_title, user_name=session['user_name'],
															    rental_agreement_id=rental_agreement_id)


@application.route('/terminate_rental_agreement', methods=['POST','GET']) 
@logged_in_landlord
def terminate_rental_agreement() -> 'html':
	"""Запись данных в соответствующие таблицы при Завершении или Досрочном расторжении"""
	rental_agreement_id = request.form['rental_agreement_id']

	# данные Акт возврата, таблица ra_move_out 
	db.insert_into_ra_move_out(rental_agreement_id, request.form['date_of_conclusion_move'],
							request.form['number_of_sets_of_keys'], request.form['number_of_keys_in_set'], 
						   request.form['rental_object_comment'], request.form['things_comment'], request.form['damage_cost'], 
						   request.form['cleaning'], request.form['rental_agreeement_debts'], 
						   request.form['deposit_refund'], request.form['prepayment_refund'])




	# PDF: АКТ ВОЗВРАТА
	# создаем экземпляр класса RentalAgreement
	ra = RentalAgreement(*db.get_rental_agreement_data(rental_agreement_id))

	# преобразуем строку даты подписания акта возврата полученную из формы в тип datetime 			
	date_of_conclusion_move_out = datetime(*[int(i) for i in request.form['date_of_conclusion_move'].split('-')])
	
	# определяем часть имени pdf файла для того чтобы повторно созданный файл с
	# тем же номером заказа не кешировался браузером
	anti_cache_part_of_pdf_name = ra.anti_cache_part_of_pdf_name()

	# определяем имя и расположение pdf файла
	ra_pdf = f"static/pdf/move_out/move_out_{anti_cache_part_of_pdf_name}_{ra.agreement_number}.pdf"

	move_out_data = dict(pdf_name = ra_pdf,
						 city = ra.city,
					     date_of_conclusion_move_out = date_of_conclusion_move_out,
						 rental_agreement_number=ra.agreement_number,
						 date_of_conclusion = ra.date_of_conclusion,
					   	 number_of_sets_of_keys = request.form['number_of_sets_of_keys'],
					   	 number_of_keys_in_set = request.form['number_of_keys_in_set'],
					   	 rental_object_comment = request.form['rental_object_comment'],
					   	 things_comment = request.form['things_comment'],
						 damage_cost = request.form['damage_cost'],
						 rental_agreeement_debts = request.form['rental_agreeement_debts'],						 
						 cleaning = request.form['cleaning'],
						 deposit_refund = request.form['deposit_refund'],
						 prepayment_refund = request.form['prepayment_refund'])

	create_move_out_pdf(**move_out_data)



	# если завершение в связи с окончанием срока действия договора
	if request.form['source'] == 'termination':
		# обновляем статус в таблице rental_agreements
		db.update_rental_agreements_status(rental_agreement_id, 'завершен')

		flash(f'Договор успешно завершен', category='success')

	# если завершение в связи с досрочным расторжением
	elif request.form['source'] == 'early_termination':
		# записываем данные связанные с расторжением в таблицу ra_termination
		db.insert_into_ra_termination(rental_agreement_id, request.form['date_of_conclusion_early_term'], request.form['notice_date'], 
								      request.form['end_of_term'], request.form['is_landlord_initiator'])
		
		# обновляем статус в таблице rental_agreements
		db.update_rental_agreements_status(rental_agreement_id, 'досрочно расторгнут')

		# PDF: СОГЛАШЕНИЕ О РАСТОРЖЕНИИ
		# преобразуем строки полученные из формы в тип datetime 			
		date_of_conclusion_early_term = datetime(*[int(i) for i in request.form['date_of_conclusion_early_term'].split('-')])
		notice_date = datetime(*[int(i) for i in request.form['notice_date'].split('-')])
		end_of_term = datetime(*[int(i) for i in request.form['end_of_term'].split('-')])


		# получим полные имена наймодателя и нанимателя
		landlord = RA_Landlord(None, *db.get_ra_landlord_data(rental_agreement_id))
		tenant = RA_Tenant(None, *db.get_ra_tenant_data(rental_agreement_id))
		l_name = f"{landlord.last_name} {landlord.first_name} {landlord.patronymic}"
		t_name = f"{tenant.last_name} {tenant.first_name} {tenant.patronymic}"


		# определяем имя и расположение pdf файла
		ra_pdf = f"static/pdf/termination/termination_{anti_cache_part_of_pdf_name}_{ra.agreement_number}.pdf"


		termination_data = dict(pdf_name = ra_pdf,
								rental_agreement_number=ra.agreement_number,
						    	date_of_conclusion = ra.date_of_conclusion,
								city = ra.city,
					     		date_of_conclusion_early_term = date_of_conclusion_early_term,
					     		landlord = l_name,
					     		tenant = t_name,
								end_of_term	= end_of_term,
								is_landlord_initiator = request.form['is_landlord_initiator'],
					     		notice_date	 = notice_date)

		create_termination_pdf(**termination_data)


		flash(f'Договор успешно досрочно расторгнут', category='success')

	# получим rental_object_id для договора аренды 
	rental_object_id =  RA_RentalObject(*db.get_ra_rental_object_data(rental_agreement_id )).rental_object_id
	# меняем статус у объекта аренды
	db.update_rental_object_status(rental_object_id, 'свободен')

	# возвращаемся на страницу landlord_rental_agreements 
	return redirect(url_for('landlord_rental_agreements_archive'))

















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
	application.run(debug=True)













