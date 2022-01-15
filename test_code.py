from rental_agreement import RentalAgreement # договор аренд

# ВЗАИМОДЕЙСТВИЕ С БД
from database.config import db_config # параметры для подключения к БД
from database.context_manager import DBContext_Manager as DBcm # менеджер контекста

from database.use_db import DataDefinition # класс для определения и модификации объектов(таблиц, базданных)
from database.use_db import DataManipulation # класс для манипулирования данными в БД

db_def = DataDefinition(db_config, DBcm)
db = DataManipulation(db_config, DBcm) # экземпляр класса для взаимодействия с БД
# -------------------------------------------------------------------------------------------------------------
import datetime

now = datetime.datetime.now().replace(microsecond=0)

part_of_pdf_name = f'{now.day}{now.month}{now.year}{now.hour}{now.minute}{now.second}'

print(now)
print(type(now))
print(part_of_pdf_name)



ra = RentalAgreement(*db.get_rental_agreement_data(228))
now = ra.datetime_of_creation
part_of_pdf_name = f'{now.day}{now.month}{now.year}{now.hour}{now.minute}{now.second}'

print('>>>', now)
print('>>>',type(now))
print('>>>',part_of_pdf_name)

print(ra.anti_cache_part_of_pdf_name())