from functools import wraps 

def context(original_function):
	"""
	Декоратор оборачивает методы в диспетчер контекта
	В декорируемую функцию необходимо по-мимо self передавать cursor=None при ее объявлении
	"""
	@wraps(original_function)
	def wrapper(self, *args, **kwargs):
		with self.context_manager(self.config) as cursor:
			return original_function(self, cursor=cursor, *args, **kwargs)
	return wrapper
