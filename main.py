from werkzeug.security import generate_password_hash, check_password_hash 
import os

# ------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort,make_response # импортируем функции модуля flask

application = Flask(__name__) #создание экземпляра объекта Flask и присваивание его переменной "application" 

application.config['SECRET_KEY'] = 'd1269dcb5c175acb12678fa83e66e9ca1a707cb4'
application.config['PERMANENT_SESSION_LIFETIME'] = 604800 # неприрывное время жизни сеанса в секундах (604800 сек. = 7 суток)
application.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------------------------------------------------------

from datetime import date

from login_checker import logged_in_admin, logged_in_landlord, logged_in_tenant, logged_in_agent

from rental_agreement import RentalAgreement # договор аренды

from users import User, Admin, Agent, Landlord, Tenant # пользователи
from passport import Passport # паспортные данные пользователей
from register import Register # регистрационные данные пользоватлей

from rental_objects import Room, Flat, House # объекты аренды

from rental_agreement_conditions import GeneralConditions# условия аренды, дополнительны платежи

from rental_object_data import General, ObjectData, Building, Location, Appliance, Costs

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
	landlords_data = db.get_landlord_general_data_of_admin(session['admin_id'])
	
	# создаем экземпляры используя загруженные данные
	landlords = []
	for landlord_data in landlords_data:
		landlords.append(Landlord(*landlord_data))

	add_landlord = url_for('add_landlord') # адрес ссылки для onclick

	return render_template('admin_landlords.html', the_title=the_title, user_name=session['user_name'], landlords=landlords, add_landlord=add_landlord)



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
		...	
	elif user_type =='агент':
		...	

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



@application.route('/delete_landlord', methods=['POST','GET'])
@logged_in_admin
def delete_landlord() -> 'html':
	user_id = request.form['user_id']
	db.delete_user(user_id)
	# обновляем список user_id наймодателей, данного администратора 
	session['landlords'] = db.get_landlord_user_id_of_admin(session['admin_id']) 
	return redirect(url_for('admin_landlords'))




# __________ГЛАВНАЯ: НАЙМОДАТЕЛЬ_________
@application.route('/landlord', methods=['POST','GET']) 
@logged_in_landlord
def index_landlord() -> 'html':
	""""""
	the_title = 'Наймодатель'
	user_name = session['user_name']
	return render_template('index_landlord.html', the_title=the_title, user_name=user_name)

@application.route('/landlord_tenants', methods=['POST','GET']) 
@logged_in_landlord
def landlord_tenants() -> 'html':
	the_title = 'Жильцы'
	...














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





	# ПЕРЕЗАГРУЗКА ТАБЛИЦ И ТЕСТОВЫХ ДАННЫХ
	# print(db.is_login('admin'))
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













