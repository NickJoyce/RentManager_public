# регистрируем новый шрифт (шрифт предварителньо нужно скачать)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
registerFont(TTFont('Times New Roman', 'Times_New_Roman.ttf'))
registerFont(TTFont('Times New Roman Bold', 'Times_New_Roman_Bold.ttf'))
registerFont(TTFont('Times New Roman Italic', 'Times_New_Roman_Italic.ttf'))
fontName = 'Times New Roman'
fontName_b = 'Times New Roman Bold'
fontName_i = 'Times New Roman Times New Roman Italic'

# выравнивание
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
# шаблон документа, параграф, отступ
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame
# 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# размер страницы по умолчанию (А4)
from reportlab.rl_config import defaultPageSize

# разные размеры страниц
from reportlab.lib.pagesizes import A4, letter

# еденицы измерения длинны
from reportlab.lib.units import inch, mm

# цвета для форматирования
from reportlab.lib import colors

# ширина визиуализированного текста
from reportlab.pdfbase.pdfmetrics import stringWidth

# дата
from datetime import datetime

# конвертация числа в слово его обозначающее
from num2words import num2words

# константы
PAGE_WIDTH=defaultPageSize[0]
PAGE_HEIGHT=defaultPageSize[1]
SECTION_SPACER = Spacer(1, 14*mm)
TEN_mm_SPACER = Spacer(1, 10*mm)
PARAGRAPH_SPACER = Spacer(1, 2.6*mm)
LINE_SPACE = 14

# содержит образцы стилей 
styles = getSampleStyleSheet()

# добавляем свой стиль 
styles.add(ParagraphStyle(name='myStyle', 
						  parent=None,
						  fontName=fontName,
						  fontSize=11,
						  leading=14,
						  leftIndent=0,
						  rightIndent=0,
						  firstLineIndent=0,
						  alignment=TA_JUSTIFY,
						  spaceBefore=0,
						  spaceAfter=0,
						  bulletFontName=fontName,
						  bulletFontSize=10,
						  bulletIndent=0,
						  textColor=colors.black,
						  backColor=None,
						  wordWrap=None,
						  borderWidth=1,
						  borderPadding=0,
						  borderColor=0,
						  borderRadius=None,
						  allowWidows=1,
						  allowOrphans=0,
						  textTransform=None,
						  endDots=None,
						  splitLongWords=1,
						  underlineWidth=0.01,
						  bulletAnchor='start',
						  justifyLastLine=0,
						  justifyBreaks=0,
						  spaceShrinkage=0.05,
						  underlineGap=1,
						  strikeGap=1,
						  linkUnderline=0,
						  underlineColor=None,
						  strikeColor=None,
						  embeddedHyphenation=0,
						  uriWasteReduce=0))
# стиль наследует myStyle. Шрифт меняется на жирыный.
styles.add(ParagraphStyle(name='myStyle_bold',
						  parent=styles["myStyle"],
						  fontName=fontName_b))








def show_style_names(styles):
	"""Выводит все доступные стили"""
	for name, obj in styles.__dict__['byName'].items():
		print(name)

def show_style_by_name(styles, name:str):
	"""Выводит данные стиля по имени"""	
	print(f'СТИЛЬ: {name}')
	for k,v in styles.__dict__['byName'][name].__dict__.items():
		print(f'{k}={v}')

def convert_data(date):
	"""Преобразует дату к формату (dd, 'month', yyyy)"""
	months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
	return (date.day, months[date.month-1], date.year)


def show_doc_settings(doc):
	"""выводит настройки и значения для документа"""
	for setting, value in doc.__dict__.items():
		print(f'{setting} = {value}')


def add_running_title(canvas, doc):
	"""Добавляет нижний колонтитул"""
	canvas.setFont(fontName, 11)
	canvas.drawCentredString(PAGE_WIDTH/4+20, doc.bottomMargin/2+3, 'Наймодатель:_______________')
	canvas.drawCentredString(3*PAGE_WIDTH/4-20, doc.bottomMargin/2+3, 'Наниматель:_______________')


def draw_lines(canvas, doc, padding_top=0, number_lines=3, line_space=14):
	"""рисует горизонтальные параллельные линнии"""
	canvas.setLineWidth(0.25)
	for i in range(number_lines):
		# рисуем линюю
		heigt = PAGE_HEIGHT - padding_top - (i*line_space)
		x1 = doc.leftMargin + 6
		x2 = PAGE_WIDTH - doc.rightMargin - 6
		canvas.line(x1, heigt, x2, heigt)

def get_right_first_space_index(str_):
	"""возвращает индекс первого правого пробела (' ') в строке"""
	for i, j in reversed(list(enumerate(str_))):
		if j == ' ':
			return i

def split_str_by_limit(str_, simbols_limit):
	"""Рекурсивно возвращает список строк
		строка добавляется в список 
		str_ - строка которую нужно разбить
		simbols_limit - лимит символов
		от лимита символов происходит смещение влево до первого пробела
		в этом месте строка разбивается на 2
	"""
	if simbols_limit < 30:
		raise ValueError("simbols_limit must be greater than or equal to 30)")
	line_list = [str_]
	# крайний случай рекурсии: последний элемент списка меньше лимита символов
	if len(line_list[-1]) <= simbols_limit:
		return line_list
	# рекурсия продолжается если последний элемент списка больше лимита символов
	elif len(line_list[-1]) > simbols_limit:
		# удаляем из списка и записываем в переменную последний элемент
		last = line_list.pop()
		# получаем индекс первого пробела с конца строки  (' ')
		index = get_right_first_space_index(last[:simbols_limit])
		# добавляем в список срез удаленного последнего элемента до индекса с пробелом 
		line_list.append(last[:index])
		# добавляем в список срез удаленного последнего элемента после индекса с пробелом
		# добавлением 1 к индексу удаляем пробел
		line_list.append(last[index+1:])

		return line_list[:-1] + split_str_by_limit(line_list[-1], simbols_limit)







# ----------ДОГОВОР НАЙМА ЖИЛОГО ПОМЕЩЕНИЯ----------
def create_ra_pdf(pdf_name = '',
				  rental_agreement_number = '',
				  city = '', 
				  date_of_conclusion = datetime(2000, 1, 1),
				  landlord = '',
				  tenant = '',
				  title_deed = '',
				  renatal_object_type = '',
				  address = '',
				  other_tenants = [],
				  rental_rate = 0,
				  payment_day = 1,
				  deposit = 0,
				  costs = [],
				  cleaning_cost = 0,
				  start_of_term = datetime(2000, 1, 1) ,
				  end_of_term = datetime(2000, 1, 1),
				  late_fee = 0,

				  l_serie = '',
				  l_pass_number = '',
				  l_authority = '',
				  l_registration = '',
				  l_phone = '',
				  l_email = '',

				  t_serie = '',
				  t_pass_number = '',
				  t_authority = '',
				  t_registration = '',
				  t_phone = '',
				  t_email = ''):
	"""Генерирует 4 pdf страницы договора найма"""
	# конвертируем дату в кортеж (dd, month, yyyy)
	date_of_conclusion = convert_data(date_of_conclusion)
	start_of_term = convert_data(start_of_term)
	end_of_term = convert_data(end_of_term)

	# конвертируем числа в соответствующие слова
	rental_rate_to_words = num2words(rental_rate, lang='ru')
	deposit_to_words = num2words(deposit, lang='ru')
	cleaning_cost_to_words = num2words(cleaning_cost, lang='ru')



	def myFirstPage(canvas, doc):
		"""генерирует первую страницу"""
		canvas.saveState()
		canvas.setFont(fontName, 12)
		# город
		canvas.drawString(doc.leftMargin+6, PAGE_HEIGHT-43*mm, f'г. {city}')
		# дата заключения договора
		canvas.drawRightString(PAGE_WIDTH- doc.rightMargin - 6, PAGE_HEIGHT-43*mm, 
							   f"«{date_of_conclusion[0]}»      {date_of_conclusion[1]}      {date_of_conclusion[2]} г.")
		# наймодатель
		canvas.setFont(fontName, 11)
		canvas.drawCentredString(230, PAGE_HEIGHT-172, f'{landlord}')

		# документ основание
		canvas.drawCentredString(doc.leftMargin+319, PAGE_HEIGHT-186, f'{title_deed}')

		# наниматель
		canvas.drawCentredString(230, PAGE_HEIGHT-200, f'{tenant}')

		# подчеркивание типа объекта аренды
		canvas.setLineWidth(0.5)
		heigt=PAGE_HEIGHT/2+115.5
		if renatal_object_type == 'комната':
			x1 = doc.leftMargin+414
			x2 = x1+38.5
		elif renatal_object_type == 'квартира':
			x1 = doc.leftMargin+460
			x2 = x1+43
		elif renatal_object_type == 'дом':
			x1 = doc.leftMargin+510
			x2 = x1+19
		canvas.line(x1, heigt, x2, heigt)
		del heigt; del x1; del x2;

		# адрес
		canvas.drawCentredString(doc.leftMargin+331, PAGE_HEIGHT-317, f'{address}')

		canvas.setLineWidth(0.5)
		number_lines = 3
		for i in range(number_lines):
			# рисуем линюю

			x1 = doc.leftMargin+6
			y1 = PAGE_HEIGHT/2+37.8-(i*LINE_SPACE)
			x2 = PAGE_WIDTH- doc.rightMargin-6
			y2 = PAGE_HEIGHT/2+37.8-(i*LINE_SPACE)
			canvas.line(x1, y1, x2, y2)
			# добавляем текст содержащий жильца
			canvas.setFont(fontName, 11)
			canvas.drawString(PAGE_WIDTH/4, PAGE_HEIGHT/2+40.8-(i*LINE_SPACE), f'{other_tenants[i]}')

		# нижний колонтитул
		add_running_title(canvas, doc)	

		canvas.restoreState()


	def myLaterPages(canvas, doc):
		"""генерирует остальные страницы"""
		canvas.saveState()
		# 2-ая страница
		if doc.page == 2:
			canvas.setFont(fontName, 11)
			# аренндная ставка 
			canvas.drawCentredString(doc.leftMargin+137*mm, doc.bottomMargin + 99, f'{rental_rate} ({rental_rate_to_words}) руб.')
			# день оплаты
			canvas.drawCentredString(doc.leftMargin+102.3*mm, doc.bottomMargin + 84.7, f'{payment_day}')
			# страховая залоговая сумма
			canvas.drawCentredString(doc.leftMargin+54*mm, doc.bottomMargin + 46.8, f'{deposit} ({deposit_to_words}) руб.')
		# 3-я страница
		elif doc.page == 3:
			# расходы на содержание
			canvas.setLineWidth(0.5)
			vertical = PAGE_HEIGHT-155.6
			x1 = doc.leftMargin+6
			y1 = vertical
			x2 = PAGE_WIDTH- doc.rightMargin-6
			y2 = vertical
			canvas.line(x1, y1, x2, y2)
			canvas.setFont(fontName, 11)
			canvas.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT-152.6, f"{', '.join(costs)}")
			# клининг
			canvas.drawCentredString(doc.leftMargin+108*mm, PAGE_HEIGHT-177, f'{rental_rate} ({rental_rate_to_words}) руб.')

			# дата начала действи договора 
			canvas.drawCentredString(doc.leftMargin+79.8*mm, PAGE_HEIGHT-262.3, 
									f"«{start_of_term[0]}»      {start_of_term[1]}      {start_of_term[2]} г.")

			# дата окончания действия договора
			canvas.drawCentredString(doc.leftMargin+158*mm, PAGE_HEIGHT-262.3, 
									f"«{end_of_term[0]}»      {end_of_term[1]}      {end_of_term[2]} г.")	

		# 4-я страница	
		elif doc.page == 4:

			canvas.setFont(fontName, 11)
			# неустойка
			canvas.drawCentredString(doc.leftMargin+59, PAGE_HEIGHT-58.2, f"{late_fee}%")
			
			# верхняя граница грда
			g_top = 280
			canvas.grid([doc.leftMargin+6, PAGE_WIDTH/2, PAGE_WIDTH-doc.rightMargin-6], [doc.bottomMargin+8, 280])

			
			canvas.setFont(fontName, 8)

			def display_participant_details(header, p_name, serie, pass_number, authority, registration, phone, email, 
											g_top=0, g_padding_left=0, g_spacer=0):
				"""Выводит реквизиты сторон в ячейках грида"""

				grid_items = [f"{header}",
							  f"ФИО: {p_name}",
							  f"Паспорт: серия {serie} № {pass_number}",
							  f"Выдан: {authority}",
							  f"Прописан: {registration}",
							  f"Наймодатель: _________________(_______________________)",
							  f"Телефон для связи: {phone}",
							  f"email: {email}"]


				def split_str(grid_items:list, index, simbols_number=60):
					"""Разбивает строку grid_items[index] на 2 если длинна строки больше simbols_number
					   заменяет текущую строку первой частью, добавляет новую строку в список со второй частью
					   за текущим элементом
					   если символов меньше, добавляют новую пустую строку в список следом за текущей строкой
					"""
					# получим индекс первого (справа налево) элемента который равен ' '
					if len(grid_items[index]) > simbols_number:
						first_space_index = None
						for i, j in reversed(list(enumerate(grid_items[index][:simbols_number-1]))):
							if j == ' ':
								first_space_index = i
								break
						# разобъем строку по этому индексу
						f_part = grid_items[index][:first_space_index]
						l_part = grid_items[index][first_space_index+1:]
						grid_items[index] = f_part
						grid_items.insert(index+1, l_part)
					else:
						grid_items.insert(index+1, '')
	 
				split_str(grid_items, 3)
				split_str(grid_items, 5)

				# нарисуем строки
				for i in grid_items:
					canvas.drawString(g_padding_left, g_top-g_spacer, i)
					g_spacer += 20

			display_participant_details('НАЙМОДАТЕЛЬ', landlord, l_serie, l_pass_number, l_authority, l_registration, 
										l_phone, l_email, g_top=g_top, g_padding_left=doc.leftMargin+6+20, g_spacer=20)

			display_participant_details('НАНИМАТЕЛЬ', tenant, t_serie, t_pass_number, t_authority, t_registration, 
										t_phone, t_email, g_top=g_top, g_padding_left=PAGE_WIDTH/2+20, g_spacer=20)
								  
		# нижние колонтитулы на каждой странице
		add_running_title(canvas, doc)	
		canvas.restoreState()


	def go():
		doc = SimpleDocTemplate(pdf_name)
		# поля
		doc.leftMargin = 10*mm
		doc.rightMargin = 10*mm
		doc.topMargin = 10*mm
		doc.bottomMargin = 20*mm
		# загловок
		doc.title = 'Договор найма жилого помещения'
		# автор
		doc.author = "Rental Manager"
		# тема
		doc.subject = "Rental agreement"
		# обводка рабочей области документа
		doc.showBoundary=False
		# show_doc_settings(doc)

		# начало документа
		Story = []
		Story.append(Paragraph(f"<para alignment='center' fontSize='16'>ДОГОВОР №{rental_agreement_number}</para>", styles["myStyle"]))
		Story.append(Spacer(1, 4*mm))
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>НАЙМА ЖИЛОГО ПОМЕЩЕНИЯ</para>", styles["myStyle"]))

		Story.append(Spacer(1,31*mm))

		Story.append(Paragraph('_______________________________________________________________________, именуемый в дальнейшем '+
							   'Наймодатель, действующий на основании_____________________________________, с одной стороны, и '+
							   ' _______________________________________________________________________, именуемый в дальнейшем '+
							   'Наниматель, с другой стороны, совместно именуемые Стороны, заключили настоящий договор о ' +
							   'нижеследующем:', styles["myStyle"]))
		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>1. Предмет договора</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		Story.append(Paragraph("1.1. Наймодатель предоставляет Нанимателю для проживания жилое помещение (комната, квартира, дом) " +
							   "расположенное по адресу:________________________________________________________________________, " +
							   "далее именуемое жилое помещение. ", styles["myStyle"]))

		Story.append(PARAGRAPH_SPACER)
		str_ = "<para>1.2. Совместно с Нанимателем согласно настоящему договору в жилом помещении будут проживать следующие граждане:<br></br> "
		for i in range(3):
			str_ += f"<br></br>"
		str_+= '</para>'
		Story.append(Paragraph(str_, styles["myStyle"]))



		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>2. Обязанности сторон</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)	
		Story.append(Paragraph("<para underlineWidth='0.3'><u>2.1. Наймодатель обязуется:</u></para>", styles["myStyle"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['2.1.1. Предоставить жилое помещение, не обремененное какими-либо обязательствами, способными '+
				'существенно повлиять на предмет настоящего договора и не имеющее скрытых недостатков.',
				'2.1.2. Передать по Акту сдачи-приемки свободное жилое помещение Нанимателю в состоянии, пригодном для ' +
				'проживания и удовлетворяющем требованиям Нанимателя, а также имущество, перечень которого указан в ' +
				'Описи имущества.',
				'2.1.3. Не совершать сделок в отношении жилого помещения в течение срока действия настоящего договора без ' +
				'согласования с Нанимателем.',
				'2.1.4. Не создавать в жилом помещении условий, препятствующих нормальному проживанию Нанимателя и ' +
				'граждан, указанных в п.1.2.',
				'2.1.5. Не посещать жилое помещение без разрешения Нанимателя, кроме случаев несоблюдения п.5.2.1.;5.2.2.',
				'2.1.6. В случае аварии, повреждения инженерного оборудования, имущества и элементов отделки (интерьера) ' +
				'жилого помещения, произошедших не по вине Нанимателя, устранить последствия в кратчайшие сроки, за счет ' +
				'своих средств и своими силами, либо силами Нанимателя с письменного согласия последнего.']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)
		Story.append(Paragraph("<para underlineWidth='0.3'><u>2.2. Наниматель обязуется:</u></para>", styles["myStyle"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['2.2.1. Использовать жилое помещение только в соответствии с п.1.1. настоящего договора',
				'2.2.2. Обеспечить сохранность жилого помещения и содержать его в надлежащем состоянии в соответствии с '+
				'требованиями СЭС, Госпожнадзора, правилами и нормами, установленными для жилых помещений.',
				'2.2.3. Обеспечить сохранность инженерного оборудования и электросети жилого помещения.',
				'2.2.4. Обеспечить сохранность имущества, находящегося в жилом помещении, и не допускать его порчи или '+
				'утраты.',
				'2.2.5. Сообщать Наймодателю обо всех авариях, повреждениях и порче имущества, возникших в жилом '+
				'помещении и принимать меры по их устранению.',
				'2.2.6. В случае исчезновения за время найма переданных во временное пользование предметов или их порчи, '+
				'возместить их стоимость по ценам, указанным в Описи имущества.',
				'2.2.7. Не допускать проживание в жилом помещении граждан, не указанных в настоящем договоре.',
				'2.2.8. Не производить перепланировку жилого помещения без письменного разрешения Наймодателя.',
				'2.2.9. Не проводить ремонт в жилом помещении без письменного разрешения Наймодателя.',
				'2.2.10. Не устанавливать дополнительных замков на двери жилых помещений без письменного согласия '+
				'Наймодателя.',
				'2.2.11. Не допускать присутствия в жилом помещении домашних и иных животных без письменного согласия '+
				'Наймодателя.',
				'2.2.12. Не осуществлять в жилом помещении предпринимательскую деятельность, нарушающую п.1.1. '+
				'настоящего договора и не вывешивать объявления или рекламу снаружи жилого помещения или в жилом '+
				'комплексе.',
				'2.2.13. Не сдавать жилое помещение в поднайм.',
				'2.2.14. Не курить в жилом помещении.',
				'2.2.15. Обеспечивать Наймодателю один раз в месяц беспрепятственный доступ в жилое помещение для его '+
				'осмотра и проверки соблюдения условий настоящего договора, в согласованное сторонами время.',
				'2.2.16. Своевременно производить плату за найм жилого помещения и оплачивать иные расходы, связанные с '+
				'исполнением настоящего договора в размере и сроки, предусмотренные разделом 3 настоящего договора.',
				'2.2.17. Письменно сообщить Наймодателю не позднее, чем за 30 дней, о предстоящем освобождении жилого '+
				'помещения при окончании срока действия настоящего договора либо при его досрочном расторжении.',
				'2.2.18. После окончании срока действия настоящего договора или его досрочном расторжении в течение одного '+
				'дня освободить жилое помещение, передать его и имущество, перечень которого указан в Описи имущества, по '+
				'Акту возврата Наймодателю и возвратить ключи от всех жилых помещений и почтового ящика.',
				'2.2.19. Перед передачей жилого помещения Наймодателю произвести уборку жилого помещения или оплатить '+
				'услугу клининга, стоимость которой указана в п.3.5. настоящего договора.']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))	
			Story.append(PARAGRAPH_SPACER)
		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>3. Расчеты сторон</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['3.1. Плата за найм жилого помещения составляет_____________________________________________________ '+
				'в месяц и вносится ежемесячно Нанимателем не позднее _____ числа каждого месяца.',
				'3.2. При заключении договора Нанимателем внесена страховая залоговая сумма в размере '+
				'_____________________________________________________',
				'3.3. Страховая залоговая сумма возвращается Наймодателем Нанимателю при досрочном расторжении '+
				'договора или по окончанию срока его действия полностью при отсутствии задолженностей у последнего по '+
				'платежам, связанным с выполнением настоящего договора, в срок не позднее 5 календарных дней после '+
				'подписания Акта возврата. Страховая залоговая сумма может быть полностью или частично удержана '+
				'Наймодателем для погашения задолженности Нанимателя, а также в качестве возмещения материального '+
				'ущерба, причиненного жилому помещению или имуществу, перечень которого приведен в Описи имущества.',
				f'<para>3.4. Наниматель оплачивает следующие расходы:<br></br>'+
				'<br></br></para>',
				'3.5. Плата за клининг составляет_____________________________________________________.']

		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)
			Story.append(Spacer(1, 1*mm))


		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>4. Срок действия договора</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		data = ["4.1. Договор вступает в силу с ___________________________ и действует до ___________________________",
				'4.2. Не позднее, чем за 30 дней до окончания срока действия настоящего договора Наймодатель должен '+
				'предложить Нанимателю заключить договор на тех же или иных условиях, либо предупредить Нанимателя об '+
				'отказе от продления договора.',
				'4.3. При подписании договора на новый срок, условия договора могут быть изменены по соглашению сторон.',
				'4.4. После окончания срока действия настоящий договор считается прекращенным']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)

		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>5. Досрочное расторжение договора</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['5.1. Настоящий договор может быть расторгнут в любое время по соглашению сторон.',
				'5.2. Настоящий договор досрочному расторжению Наймодателем в одностороннем порядке не подлежит, за '+
				'исключением следующих случаев:',
				'5.2.1. Если наниматель не вносит плату в размере и сроки, предусмотренные в п.3.1.; 3.3.'
				'5.2.2. Если наниматель не выполняет принятые на себя обязательства по настоящему договору.'
				'5.3. При досрочном расторжении договора Наймодатель предупреждает Нанимателя в письменной форме за 30 '+
				'дней и возвращает Нанимателю остаток внесенной вперед платы в течение 2-х дней со дня расторжения '+
				'договора.',
				'5.4. Наниматель жилого помещения вправе в любое время расторгнуть договор найма с письменным '+
				'предупреждением Наймодателя за 30 дней.',
				'5.5. Настоящий договор может быть, досрочно расторгнут по инициативе Наймодателя в случае наступления '+
				'следующих обстоятельств: смерть Наймодателя, перемена места жительства Наймодателя, рождение ребенка у '+
				'наймодателя, тяжелая болезнь Наймодателя, продажа и иное отчуждение сданного в наем жилого помещения, '+
				'а также при иных обстоятельствах, которые приводят к невозможности продолжения действия настоящего '+
				'договора.',
				'5.6. В случае расторжения договора в соответствии с п.5.5. Наниматель обязан освободить жилое помещение в '+
				'течение 30 календарных дней.']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)

		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>6. Ответственность сторон</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['6.1. В случае невнесения в срок платы за найм Наниматель уплачивает неустойку за каждый день просрочки в '+
				'размере _____ от суммы ежемесячной оплаты жилого помещения.',
				'6.2. Уплата санкций, установленных настоящим договором, не освобождает Нанимателя от выполнения '+
				'лежащих на нем обязательств или устранения нарушений.',
				'6.3. Наниматель возмещает Наймодателю материальный ущерб, причиненный в результате невыполнения '+
				'своих обязанностей, предусмотренных настоящим договором.',
				'6.4. Споры по настоящему договору разрешаются путем переговоров между сторонами, а при не достижении '+
				'согласия в судебном порядке в суде общей юрисдикции по месту нахождения жилого помещения.']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)


		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>6. Заключительные условия</para>", styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		data = ['7.1. Вместе с жилым помещением Нанимателю предоставляется во временное пользование имущество, '+
				'перечень которого приведен в Описи имущества.',
				'7.2. Передача жилого помещения и имущества в нем от Наймодателя к Нанимателю, после подписания '+
				'настоящего договора, оформляется Сторонами посредством подписания Акта сдачи-приемки.',
				'7.3. Передача жилого помещения и имущества в нем от Нанимателя к Наймодателю, после окончания срока '+
				'действия настоящего договора или его досрочном расторжении, оформляется Сторонами посредством '+
				'подписания Акта возврата.',
				'7.4. Все приложения и дополнения к настоящему договору являются его неотъемлемой частью, при условии их '+
				'подписания обеими сторонами.',
				'7.5. Во всем, что предусмотрено настоящим договором, стороны руководствуются действующим '+
				'законодательством РФ.',
				'7.6. Настоящий договор составлен в двух экземплярах, имеющих равную юридическую силу, по одному для '+
				'каждой из сторон.',
				'7.7. Наймодатель гарантирует согласие всех совладельцев, а также прописанных в жилом помещении жильцов '+
				'согласно форме №9.']
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)


		Story.append(SECTION_SPACER)
		Story.append(Paragraph("<para alignment ='center'>РЕКВИЗИТЫ СТОРОН</para>", styles["myStyle_bold"]))

		# конец документа
		# создаем документ, передавая содержиание документа (Story) и функции редактирования
		# первой и последующих страниц
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

	go()



# ----------ОПИСЬ ИМУЩЕСТВА----------
def create_things_pdf(pdf_name = '',
					  rental_agreement_number = '',
					  city = '', 
					  date_of_conclusion = datetime(2000, 1, 1), 
					  things=[]):
	# конвертируем дату в кортеж (dd, month, yyyy)
	date_of_conclusion = convert_data(date_of_conclusion)

	def myFirstPage(canvas, doc):
		canvas.saveState()
		canvas.setFont(fontName, 12)
		# город
		canvas.drawString(doc.leftMargin+6, PAGE_HEIGHT-28*mm, f'г. {city}')
		# дата заключения договора
		canvas.drawRightString(PAGE_WIDTH- doc.rightMargin - 6, PAGE_HEIGHT-28*mm, 
							   f"«{date_of_conclusion[0]}»      {date_of_conclusion[1]}      {date_of_conclusion[2]} г.")

		# нижние колонтитулы на главной странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def myLaterPages(canvas, doc):
		canvas.saveState()

		# нижние колонтитулы на каждой странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def go():
		doc = SimpleDocTemplate(pdf_name)
		# поля
		doc.leftMargin = 10*mm
		doc.rightMargin = 10*mm
		doc.topMargin = 10*mm
		doc.bottomMargin = 20*mm
		# загловок
		doc.title = 'Опись имущества'
		# автор
		doc.author = "Rental Manager"
		# тема
		doc.subject = "Rental agreement"
		# обводка рабочей области документа
		doc.showBoundary=False

		# show_doc_settings(doc)

		# начало документа
		Story = []
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>ОПИСЬ ИМУЩЕСТВА</para>", styles["myStyle_bold"]))
		Story.append(SECTION_SPACER)
		Story.append(TEN_mm_SPACER)
		Story.append(Paragraph(f"<para>1. Следующее имущество находится в жилом помещении:</para>", styles["myStyle"]))
		Story.append(PARAGRAPH_SPACER)

		# таблица
		# ширина таблицы
		t_width = PAGE_WIDTH-20*mm-12-2
		# ширина колонок
		col_1 = 0.1*t_width
		col_2 = 0.5*t_width
		col_3 = 0.2*t_width
		col_4 = 0.2*t_width
		# форматирование таблицы
		table_style = TableStyle(
						[
						# table
						('FONTSIZE', (0,0), (-1,-1), 11),
						('GRID', (0,0), (-1,-1), 0.25, colors.black),
						('BOTTOMPADDING', (0,0), (-1,-1), 3),
						('TOPPADDING', (0,0), (-1,-1), 1),
						# th
						('FONTNAME', (0,0), (-1, 0), fontName_b),
						('ALIGN', (0,0), (-1,0), 'CENTER'),
						('BACKGROUND', (0,0), (-1,0), colors.white),
						('TEXTCOLOR', (0,0), (-1,0), colors.black),
						('BOTTOMPADDING', (0,0), (-1,0), 5),
						('TOPPADDING', (0,0), (-1,-1), 2),
						# td
						('FONTNAME', (0,1), (-1, -1), fontName),
						('BACKGROUND', (0,1), (-1,-1), colors.white),
						('ALIGN', (0,1), (0,-1), 'CENTER'),
						('ALIGN', (1,1), (1,-1), 'LEFT'),
						('ALIGN', (2,1), (2,-1), 'CENTER'),
						('ALIGN', (3,1), (3,-1), 'CENTER'),
						]
						)	
		data = things

		# создаем таблицу, передаем ширину колонок и стили
		table = Table(data,  colWidths=(col_1, col_2, col_3, col_4), style=table_style)

		# разные цвета для рядов
		# row_num = len(data)
		# for i in range(1, row_num):
		# 	if i%2 == 0: # четный ряд
		# 		bc = colors.burlywood
		# 	else: # нечетный ряд
		# 		bc = colors.beige
		# 	ts = TableStyle([('BACKGROUND', (0,i), (-1,i), bc)])
		# 	table.setStyle(ts)

		Story.append(table)

		# конец документа
		# создаем документ, передавая содержиание документа (Story) и функции редактирования
		# первой и последующих страниц
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	go()

# ----------АКТ СДАЧИ-ПРИЕМКИ----------
def create_move_in_pdf(pdf_name = '',
					   rental_agreement_number = '',
					   city = '', 
					   date_of_conclusion_move_in = datetime(2000, 1, 1),
					   date_of_conclusion = datetime(2000, 1, 1),
					   number_of_sets_of_keys = '',
					   number_of_keys_in_set = '', 
					   rental_object_comment = '',
					   things_comment = ''):

	# конвертируем дату в кортеж (dd, month, yyyy)
	date_of_conclusion = convert_data(date_of_conclusion)
	date_of_conclusion_move_in  = convert_data(date_of_conclusion_move_in)

	def myFirstPage(canvas, doc):
		canvas.saveState()
		canvas.setFont(fontName, 12)
		# город
		canvas.drawString(doc.leftMargin+6, PAGE_HEIGHT-28*mm, f'г. {city}')
		# дата заключения договора
		canvas.drawRightString(PAGE_WIDTH - doc.rightMargin - 6, PAGE_HEIGHT-28*mm, 
							   f"«{date_of_conclusion_move_in[0]}»      {date_of_conclusion_move_in[1]}      {date_of_conclusion_move_in[2]} г.")
		
		# Дата заключения договора
		canvas.drawCentredString(doc.leftMargin+393, PAGE_HEIGHT-126.5, 
			f"{date_of_conclusion[0]}      {date_of_conclusion[1]}      {date_of_conclusion[2]} г.")

		# замечания по жилому помещению
		# рисуем стандартные горизонтальные линнии по ширине рабочей области
		draw_lines(canvas, doc, padding_top=250.3, number_lines=3, line_space=14)
		canvas.setFont(fontName, 11)
		# разбиваем строку и получаем список строк
		splitted_list = split_str_by_limit(rental_object_comment, 95)
		# рисуем текст для первых 3 элементов в списке разбитых строк
		for i in range(len(splitted_list)):
			canvas.drawString(doc.leftMargin+26, PAGE_HEIGHT-247.4-(14*i), f'{splitted_list[i]}')
			if i == 2:
				break

		# замечания по имуществу в жилом помещении
		# рисуем стандартные горизонтальные линнии по ширине рабочей области
		draw_lines(canvas, doc, padding_top=313.7, number_lines=3, line_space=14)
		# разбиваем строку и получаем список строк
		splitted_list = split_str_by_limit(things_comment, 95)
		# рисуем текст для первых 3 элементов в списке разбитых строк
		for i in range(len(splitted_list)):
			canvas.drawString(doc.leftMargin+26, PAGE_HEIGHT-310.5-(14*i), f'{splitted_list[i]}')
			if i == 2:
				break

		# нижние колонтитулы на главной странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def myLaterPages(canvas, doc):
		canvas.saveState()
		# нижние колонтитулы на каждой странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def go():
		doc = SimpleDocTemplate(pdf_name)
		# поля
		doc.leftMargin = 10*mm
		doc.rightMargin = 10*mm
		doc.topMargin = 10*mm
		doc.bottomMargin = 20*mm
		# загловок
		doc.title = 'АКТ СДАЧИ-ПРИЕМКИ'
		# автор
		doc.author = "Rental Manager"
		# тема
		doc.subject = "Rental agreement"
		# обводка рабочей области документа
		doc.showBoundary=False
		# show_doc_settings(doc)

		# начало документа
		Story = []
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>АКТ СДАЧИ-ПРИЕМКИ</para>", styles["myStyle_bold"]))
		Story.append(SECTION_SPACER)
		Story.append(TEN_mm_SPACER)
		data = [
			f"1. Во исполнение договора найма жилого помещения №{rental_agreement_number} от ___________________________",
			"Наймодатель передал Нанимателю:",
			f"<para leftIndent=20>a) {number_of_sets_of_keys} комплект из {number_of_keys_in_set} ключей от жилого помещения;</para>",
			f"<para leftIndent=20>б) Имущество, согласно п.1 Описи имущества:</para>",
			"2. Произведен осмотр жилого помещения.",
			"<para>Жилое помещение передается в надлежащем состоянии, за исключением следующих замечаний:<br></br>" +
			"<br></br>"
			"<br></br>"
			"<br></br></para>",

			"<para>Имущество в жилом помещении передается в надлежащем состоянии, за исключением следующих замечаний:<br></br>" +
			"<br></br>"
			"<br></br>"
			"<br></br></para>",

			"5. Наниматель жилое помещение принял и претензий к Наймодателю не имеет.",
			"6. Наниматель с настоящего момента вступает в пользование жилым помещением и несет ответственность по его содержанию."]

		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	go()


	...

# ----------АКТ ВОЗВРАТА----------
def create_move_out_pdf( pdf_name = '',
						 city = '',
					     date_of_conclusion_move_out = datetime(2000, 1, 1),
						 rental_agreement_number = '',
						 date_of_conclusion = datetime(2000, 1, 1),
					   	 number_of_sets_of_keys = '',
					   	 number_of_keys_in_set = '',
					   	 rental_object_comment = '',
					   	 things_comment = '',
						 damage_cost = '',
						 rental_agreeement_debts = '',
						 cleaning = '',
						 deposit_refund = '',
						 prepayment_refund = ''):

	# конвертируем дату в кортеж (dd, month, yyyy)
	date_of_conclusion_move_out = convert_data(date_of_conclusion_move_out)
	date_of_conclusion = convert_data(date_of_conclusion)

	def myFirstPage(canvas, doc):
		canvas.saveState()
		canvas.setFont(fontName, 12)
		# город
		canvas.drawString(doc.leftMargin+6, PAGE_HEIGHT-28*mm, f'г. {city}')
		# дата заключения договора
		canvas.drawRightString(PAGE_WIDTH - doc.rightMargin - 6, PAGE_HEIGHT-28*mm, 
							   f"«{date_of_conclusion_move_out[0]}»      {date_of_conclusion_move_out[1]}      {date_of_conclusion_move_out[2]} г.")

		# Дата заключения договора
		canvas.drawCentredString(doc.leftMargin+393, PAGE_HEIGHT-126.5, 
			f"{date_of_conclusion[0]}      {date_of_conclusion[1]}      {date_of_conclusion[2]} г.")


		canvas.setFont(fontName, 11)
		# замечания по жилому помещению
		# рисуем стандартные горизонтальные линнии по ширине рабочей области
		draw_lines(canvas, doc, padding_top=250.3, number_lines=3, line_space=14)
		# разбиваем строку и получаем список строк
		splitted_list = split_str_by_limit(rental_object_comment, 95)
		# рисуем текст для первых 3 элементов в списке разбитых строк
		for i in range(len(splitted_list)):
			canvas.drawString(doc.leftMargin+26, PAGE_HEIGHT-247.4-(14*i), f'{splitted_list[i]}')
			if i == 2:
				break

		# замечания по имуществу в жилом помещении
		# рисуем стандартные горизонтальные линнии по ширине рабочей области
		draw_lines(canvas, doc, padding_top=313.7, number_lines=3, line_space=14)
		# разбиваем строку и получаем список строк
		splitted_list = split_str_by_limit(things_comment, 95)
		# рисуем текст для первых 3 элементов в списке разбитых строк
		for i in range(len(splitted_list)):
			canvas.drawString(doc.leftMargin+26, PAGE_HEIGHT-310.5-(14*i), f'{splitted_list[i]}')
			if i == 2:
				break


		# оценка ущерба
		canvas.drawCentredString(doc.leftMargin+128, PAGE_HEIGHT-360.4, f"{damage_cost}")

		# задолженность
		canvas.drawCentredString(doc.leftMargin+425, PAGE_HEIGHT-403, f"{rental_agreeement_debts}")

		# клининг (подчеркивание)
		canvas.setLineWidth(0.25)
		height = PAGE_HEIGHT-385
		if cleaning == '1':
			x1 = doc.leftMargin+332.5
			x2 = x1 + 46
		elif cleaning == '0':
			x1 = doc.leftMargin+381.2
			x2 = x1 + 60.8
		canvas.line(x1, height, x2, height)

		# страховая залоговая сумма 
		canvas.drawCentredString(doc.leftMargin+93, PAGE_HEIGHT-438.1, f"{deposit_refund}")

		# предоплата
		canvas.drawCentredString(doc.leftMargin+486, PAGE_HEIGHT-460, f"{prepayment_refund}")



		# нижние колонтитулы на главной странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def myLaterPages(canvas, doc):
		canvas.saveState()



		# нижние колонтитулы на каждой странице
		add_running_title(canvas, doc)
		canvas.restoreState()


	def go():
		doc = SimpleDocTemplate(pdf_name)
		# поля
		doc.leftMargin = 10*mm
		doc.rightMargin = 10*mm
		doc.topMargin = 10*mm
		doc.bottomMargin = 20*mm
		# загловок
		doc.title = 'АКТ ВОЗВРАТА'
		# автор
		doc.author = "Rental Manager"
		# тема
		doc.subject = "Rental agreement"
		# обводка рабочей области документа
		doc.showBoundary=False
		# show_doc_settings(doc)
		# начало документа
		Story = []
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>АКТ ВОЗВРАТА</para>", styles["myStyle_bold"]))
		Story.append(SECTION_SPACER)
		Story.append(TEN_mm_SPACER)
		data = [
			f"1. Во исполнение договора найма жилого помещения №{rental_agreement_number} от ___________________________.",
			'Наниматель передал Наймодателю:',
			f"<para leftIndent=20>a) {number_of_sets_of_keys} комплект из {number_of_keys_in_set} ключей от жилого помещения;</para>",
			f"<para leftIndent=20>б) Имущество, согласно п.1 Описи имущества:</para>",
			"2. Произведен осмотр жилого помещения.",
			"<para>Жилое помещение передается в надлежащем состоянии, за исключением следующих замечаний:<br></br>" +
			"<br></br>"
			"<br></br>"
			"<br></br></para>",

			"<para>Имущество в жилом помещении передается в надлежащем состоянии, за исключением следующих замечаний:<br></br>" +
			"<br></br>"
			"<br></br>"
			"<br></br></para>",

			f"Оценка ущерба: ________________",
			f"Оценка необходимости проведения клининга (нужное подчеркнуть): требуется/не требуется.",
			f"Задолженность Нанимателя по платежам, связанными с выполнения Договора: ________________",
			f"Наймодателем возвращена Нанимателю страховая залоговая сумма за вычетом ущерба и задолженности, в размере: ________________",
			f"Наймодателем возвращен Нанимателю остаток внесенной вперед оплаты за найм, в размере: ________________",
			f"3. Наймодатель жилое помещение принял и претензий к Нанимателю не имеет."
			]

		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)

		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	go()


	...

# ----------СОГЛАШЕНИЕ О РАСТОРЖЕНИИ----------
def create_termination_pdf(pdf_name = '',
						   rental_agreement_number='',
						   date_of_conclusion = datetime(2000, 1, 1),
						   city = 'Санкт-Петербург',
					       date_of_conclusion_early_term = datetime(2000, 1, 1),
					       landlord = '',
					       tenant = '',
						   end_of_term	= datetime(2000, 1, 1),
						   is_landlord_initiator = '',
					       notice_date	 = datetime(2000, 1, 1)):
	# конвертируем дату в кортеж (dd, month, yyyy)
	date_of_conclusion = convert_data(date_of_conclusion)
	date_of_conclusion_early_term = convert_data(date_of_conclusion_early_term)
	end_of_term = convert_data(end_of_term)
	notice_date = convert_data(notice_date)


	def myFirstPage(canvas, doc):
		canvas.saveState()
		canvas.setFont(fontName, 12)
		# город
		canvas.drawString(doc.leftMargin+6, PAGE_HEIGHT-28*mm-20, f'г. {city}')
		# дата заключения соглашения
		canvas.drawRightString(PAGE_WIDTH - doc.rightMargin - 6, PAGE_HEIGHT-28*mm-20, 
							   f"«{date_of_conclusion_early_term[0]}»      " +
							   f"{date_of_conclusion_early_term[1]}      " +
							   f"{date_of_conclusion_early_term[2]} г.")
		canvas.setFont(fontName, 11)
		# наймодатель
		canvas.drawCentredString(doc.leftMargin+6+176, PAGE_HEIGHT-148.1, f'{landlord}')
		# наниматель
		canvas.drawCentredString(doc.leftMargin+6+348, PAGE_HEIGHT-162.1, f'{tenant}')
		# дата заключения договора в тексте соглашения
		canvas.drawCentredString(doc.leftMargin+6+168, PAGE_HEIGHT-211.5, 
		f'«{date_of_conclusion[0]}»      {date_of_conclusion[1]}      {date_of_conclusion[2]} г.')
		# дата расторжения
		canvas.drawCentredString(doc.leftMargin+6+190, PAGE_HEIGHT-225.5, 
		f'«{end_of_term[0]}»      {end_of_term[1]}      {end_of_term[2]} г.')
		# инициатр (подчеркивание)
		is_landlord_initiator = '0'
		canvas.setLineWidth(0.25)
		height = PAGE_HEIGHT-250
		if is_landlord_initiator == '1':
			x1 = doc.leftMargin+428
			x2 = x1 + 61.5
		elif is_landlord_initiator == '0':
			x1 = doc.leftMargin+368
			x2 = x1 + 56.5
		canvas.line(x1, height, x2, height)
		# дата уведомления инициатора расторжения другой стороны
		canvas.drawCentredString(doc.leftMargin+6+94.2, PAGE_HEIGHT-282.2, 
		f'«{notice_date[0]}»      {notice_date[1]}      {notice_date[2]} г.')



		# нижние колонтитулы на главной странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def myLaterPages(canvas, doc):
		canvas.saveState()
		# нижние колонтитулы на каждой странице
		add_running_title(canvas, doc)
		canvas.restoreState()
	def go():
		doc = SimpleDocTemplate(pdf_name)
		# поля
		doc.leftMargin = 10*mm
		doc.rightMargin = 10*mm
		doc.topMargin = 10*mm
		doc.bottomMargin = 20*mm
		# загловок
		doc.title = 'СОГЛАШЕНИЕ О РАСТОРЖЕНИИ'
		# автор
		doc.author = "Rental Manager"
		# тема
		doc.subject = "Rental agreement"
		# обводка рабочей области документа
		doc.showBoundary=False
		# show_doc_settings(doc)
		# начало документа
		Story = []
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>" +
								"СОГЛАШЕНИЕ О РАСТОРЖЕНИИ ДОГОВОРА НАЙМА ЖИЛОГО ПОМЕЩЕНИЯ</para>", 
								styles["myStyle_bold"]))
		Story.append(PARAGRAPH_SPACER)
		Story.append(Paragraph(f"<para alignment='center' fontSize='12'>" +
								f"№{rental_agreement_number} от «{date_of_conclusion[0]}» "+ 
								f"{date_of_conclusion[1]} {date_of_conclusion[2]} г.</para>", 
								styles["myStyle_bold"]))
		Story.append(SECTION_SPACER)
		Story.append(TEN_mm_SPACER)

		data = ["________________________________________________________________, именуемый в дальнейшем " +
				"Наймодатель, с одной стороны, и ________________________________________________________________, " + 
				"именуемый в дальнейшем Наниматель, с другой стороны, заключили настоящее соглашение о следующем:",

				"<para leftIndent=20>1. Наниматель и Наймодатель пришли к соглашению расторгнуть договор найма жилого помещения "+
				f"№{rental_agreement_number} от ___________________________"+
				"(именуемый далее Договор) согласно п.5.1. " +
				f"указанного договора, начиная с ___________________________</para>",

				"<para leftIndent=20>2. Инициатором расторжения Договора является (нужное подчеркнуть): Наниматель/Наймодатель</para>",

				f"<para leftIndent=20>3. Инициатор уведомил другую сторону о своем решении расторгнуть Договор <br></br>" + 
				f"___________________________</para>",

				f"<para leftIndent=20>4. Настоящее Соглашение вступает в силу с момента его подписания Нанимателем и Наймодателем.</para>",

				f"<para leftIndent=20>5. С момента вступления в силу настоящего Соглашения, Наниматель обязан в течение одного дня " +
				"освободить жилое помещение, передать его и имущество, перечень которого указан в Описи имущества, " +
				"по Акту возврата Наймодателю и возвратить ключи от всех жилых помещений и почтового ящика.</para>"]
		for p in data:
			Story.append(Paragraph(p, styles["myStyle"]))
			Story.append(PARAGRAPH_SPACER)
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	go()




if __name__ == '__main__':
	ra_data = dict(
	pdf_name = 'static/pdf/rental_agreements/ra_test.pdf',	
	rental_agreement_number = 'test',
	city = 'Санкт-Петербург', 
	date_of_conclusion = datetime(2022, 1, 10),
	landlord = 'Смирнов Никита Алексеевич',
	tenant = 'Колесникова Наталья Владимировна',
	title_deed = 'Договор Купли-продажи 78 АБ 7269088',
	renatal_object_type = 'комната',
	address = 'Санкт-Петербург, Богатырский проспект 3-11',
	other_tenants = ['Семенова Маргарита Ивановна, +79218898899', '', ''],
	rental_rate = 21000,
	payment_day = 2,
	deposit = 15000,
	costs = ['коммунальные услуги', 'электроэнергия', 'капитальный ремонт', 'интернет', 'газ'],
	cleaning_cost = 1500,
	start_of_term = datetime(2022, 1, 10) ,
	end_of_term = datetime(2022, 1, 30),
	late_fee = 3,

	l_serie = 4008,
	l_pass_number = 522493,
	l_authority = 'ТП№81 отдела УФМС России по Санкт-Петербургу и ленинградской обл. в центральном р-не гор. Санкт-Петербурга',
	l_registration = 'Санкт-Петербург, ул. Гороховая 32-95',
	l_phone = '+79218850028',
	l_email = 'actan-spb@mail.ru',

	t_serie = 6716,
	t_pass_number = 553286,
	t_authority = 'отдел УФМС России по ХМАО-Югре, г. Сургут',
	t_registration = ' г. Сургут, ул. Энтузиастов 8-3 отдел УФМС России по ХМАО-Югре, г. Сургут',
	t_phone = '+79822225328',
	t_email = 'ntash.klv@gmail.com')

	# create_ra_pdf(**ra_data)	

	things_data = dict(	pdf_name = 'static/pdf/things/things_test.pdf',	
						rental_agreement_number='142',
					   city = 'Санкт-Петербург',
					   date_of_conclusion = datetime(2022, 1, 10),
					   things = [('№', 'Наименование предмета', 'Кол-во, шт', 'Стоимость ед., руб.'), 
					   			 (22, 'Стол', 1, 1000),
					   			 (23, 'Стул', 2, 500),
					   			 (43, 'Шкаф', 5, 4000)])

	# create_things_pdf(**things_data)
	move_in_data = dict(pdf_name = 'static/pdf/move_in/move_in_test.pdf',	
						rental_agreement_number='777777',
					    city = 'Санкт-Петербург',
					    date_of_conclusion_move_in = datetime(2022, 1, 10),
					    date_of_conclusion = datetime(2022, 3, 20),
					   	number_of_sets_of_keys = 1,
					   	number_of_keys_in_set =3,
					   	rental_object_comment = '(широко распространённая в мире GNU/Linux  написанная Стином Лумхольтом (Steen Lumholt) и Гвидо ван Россумом[1]. Входит в стандартную библиотеку Python.',
					   	things_comment = 'Без замечаний Без замечаний Без замечаний Без замечаний Без замечаний р'
					   	)

	# create_move_in_pdf(**move_in_data)

	move_out_data = dict(pdf_name = 'static/pdf/move_out/move_out_test.pdf',
						 city = 'Санкт-Петербург',
					     date_of_conclusion_move_out = datetime(2023, 1, 10),
						 rental_agreement_number='777777',
						 date_of_conclusion = datetime(2022, 1, 10),
					   	 number_of_sets_of_keys = '1',
					   	 number_of_keys_in_set = '3',
					   	 rental_object_comment = 'Some comment 1',
					   	 things_comment = 'Some comment 2',
						 damage_cost = '1000',
						 rental_agreeement_debts = '0',
						 cleaning = '1',
						 deposit_refund = '14000',
						 prepayment_refund = '5000')

	# create_move_out_pdf(**move_out_data)



	termination_data = dict(pdf_name = 'static/pdf/termination/termination_test.pdf',
							rental_agreement_number='777777',
						    date_of_conclusion = datetime(2021, 1, 10),
							city = 'Санкт-Петербург',
					     	date_of_conclusion_early_term = datetime(2022, 4, 10),
					     	landlord = 'Иванов Иван Ивановичр',
					     	tenant = 'Сергеев Сергей Сергеевич',
							end_of_term	= datetime(2023, 1, 10),
							is_landlord_initiator = '0',
					     	notice_date	 = datetime(2023, 1, 10)			    
					   	)

	# create_termination_pdf(**termination_data)