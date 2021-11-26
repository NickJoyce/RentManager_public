import csv
import json

def from_csv_to_python_list_of_lists(csv_file='districts.csv'):
	with open(csv_file, encoding='utf8') as file:  
	    loaded_data = csv.reader(file)
	    return_data = [] # [['city', 'line_number', 'line_name', 'color', 'station', 'is_closed'],[],[]]
	    for i in loaded_data:
	    	if i != [';;;;;']: # удаляем строки без данных
	    		i = i[0].split(';') # создаем список из строк по разделителю ';''
	    		return_data.append(i) # добавляем списки с данными в списко metro
	    del return_data[0] # удаляем шапку таблицы
	    for i in return_data: 
	    	i = [j.replace('\xa0', '') for j in i] # удаляем лишние неразрывные пробелы \xa0
	    return return_data

print(from_csv_to_python_list_of_lists())