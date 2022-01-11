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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
# 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# размер страницы по умолчанию (А4)
from reportlab.rl_config import defaultPageSize
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

def covert_data(date):
	"""Преобразует дату к формату (dd, 'month', yyyy)"""
	months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
	return (date.day, months[date.month-1], date.year)










# ----------ДОГОВОР НАЙМА ЖИЛОГО ПОМЕЩЕНИЯ----------
def create_ra_pdf(rental_agreement_number = '',
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
	date_of_conclusion = covert_data(date_of_conclusion)
	start_of_term = covert_data(start_of_term)
	end_of_term = covert_data(end_of_term)

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

		# нижний колонтитул
		canvas.drawCentredString(PAGE_WIDTH/4+20, doc.bottomMargin/2+3, 'Наймодатель:_______________')
		canvas.drawCentredString(3*PAGE_WIDTH/4-20, doc.bottomMargin/2+3, 'Наниматель:_______________')

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
			canvas.grid([doc.leftMargin+6, PAGE_WIDTH/2, PAGE_WIDTH-doc.rightMargin-6], [doc.bottomMargin, 280])

			
			canvas.setFont(fontName, 8)

			def display_participant_details(header, p_name, serie, pass_number, authority, registration, phone, email, 
											g_top=0, g_padding_left=0, g_spacer=0):
				"""Выводит реквизиты сторон в ячейках грида"""

				grid_items = [f"{header}",
							  f"ФИО: {p_name}",
							  f"Паспорт: серия {serie} № {pass_number}",
							  f"Выдан: {authority}",
							  f"Прописан: {registration}",
							  f"Наймодатель: _________(_________________)",
							  f"Телефон для связи: {phone}",
							  f"email:{email}"]


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
		canvas.setFont(fontName, 11)	
		canvas.drawCentredString(PAGE_WIDTH/4+20, doc.bottomMargin/2+3, 'Наймодатель:_______________')
		canvas.drawCentredString(3*PAGE_WIDTH/4-20, doc.bottomMargin/2+3, 'Наниматель:_______________')		
		canvas.restoreState()


	def go():
		doc = SimpleDocTemplate(f"static/pdf/rental_agreements/ra_{rental_agreement_number}.pdf")
		def show_doc_settings(doc):
			"""выводит настройки и значения для документа"""
			for setting, value in doc.__dict__.items():
				print(f'{setting} = {value}')
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
def create_things_pdf():
	def myFirstPage(canvas, doc):
		canvas.saveState()
		...
		canvas.restoreState()
	def myLaterPages(canvas, doc):
		canvas.saveState()
		...
		canvas.restoreState()
	def go():
		doc = SimpleDocTemplate(f"static/pdf/things/things_{rental_agreement_number}.pdf")
		def show_doc_settings(doc):
			"""выводит настройки и значения для документа"""
			for setting, value in doc.__dict__.items():
				print(f'{setting} = {value}')
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


		# конец документа
		# создаем документ, передавая содержиание документа (Story) и функции редактирования
		# первой и последующих страниц
		doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

# ----------АКТ СДАЧИ-ПРИЕМКИ----------
def create_move_in_pdf():
	...

# ----------АКТ ВОЗВРАТА----------
def create_move_out_pdf():
	...

# ----------СОГЛАШЕНИЕ О РАСТОРЖЕНИИ----------
def create_termination_pdf():
	...

# ----------СОГЛАШЕНИЕ О ПРОДЛЕНИИ----------
def create_renewal_pdf():
	...


if __name__ == '__main__':
	ra_data = dict(
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

	create_ra_pdf(**ra_data)	


