from flask import session, flash, redirect, url_for, abort

from functools import wraps




def logged_in_admin(func):
	""" выполнен ли вход пользователем с типом 'администратор'"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session: # вход выполнен
			if session['user_type'] == 'администратор': # если записанный в куках тип пользователя 'администратор'
				return func(*args, **kwargs)
			else: # если в куках другой тип
				abort(401)
		else: # не выполнен		
			flash('Вход не выполнен', category='error') 
			return redirect(url_for('login'))
	return wrapper


def logged_in_landlord(func):
	""" выполнен ли вход пользователем с типом 'наймодатель' """
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session: # вход выполнен
			if session['user_type'] == 'наймодатель': 
				return func(*args, **kwargs)
			else: # если в куках другой тип
				abort(401)
		else: # не выполнен		
			flash('Вход не выполнен', category='error') 
			return redirect(url_for('login'))
	return wrapper



def logged_in_tenant(func):
	""" выполнен ли вход пользователем с типом 'наниматель' """
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session: # вход выполнен
			if session['user_type'] == 'наниматель': 
				return func(*args, **kwargs)
			else: # если в куках другой тип
				abort(401)
		else: # не выполнен		
			flash('Вход не выполнен', category='error') 
			return redirect(url_for('login'))
	return wrapper


def logged_in_agent(func):
	""" выполнен ли вход пользователем с типом 'агент' """
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session: # вход выполнен
			if session['user_type'] == 'агент': 
				return func(*args, **kwargs)
			else: # если в куках другой тип
				abort(401)
		else: # не выполнен		
			flash('Вход не выполнен', category='error') 
			return redirect(url_for('login'))
	return wrapper