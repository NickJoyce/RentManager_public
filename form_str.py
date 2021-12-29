from datetime import date

class FormStr:
	"""преобразования строк полученных из формы в другие типы"""
	def __init__(self, form_str):
		self.form_str = form_str

	def transform_to_date(self):
		"""Преобразует строку в <class 'datetime.date'>"""
		return   date(*[int(i) for i in self.form_str.split('-')])


