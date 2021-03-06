from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pandas as pd

from django.contrib.auth.decorators import login_required
import os
from databasefiles.sqlalchemy_pymysql import dbActionReturn
# from django.contrib.admin import login
import datetime


def home_page(request):
	return render(request, "hello_world.html")


@login_required()
def upload(request):
	context = {}

	if request.method == 'GET':
		return render(request, 'file_upload.html', context)

	if 'file_uploads' in request.POST:
		now = datetime.datetime.now()
		datatimenow = now.strftime("%m-%d-%Y %Hh%Mm%Ss")

		uploaded_file = request.FILES['document']

		ext = uploaded_file.name.split('.')[-1]

		fs = FileSystemStorage()

		file_name = uploaded_file.name
		name = file_name.split('.')
		file_name = '{}-{} {}.{}'.format(name[0], str(request.user).upper(), datatimenow, name[-1])
		fs.save(file_name, uploaded_file)

		file_context = [file_name, str(int(uploaded_file.size) / 1024) + ' KB', uploaded_file.content_type]
		context['context'] = file_context

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		media_path = os.path.join(BASE_DIR, 'media')
		file_path = media_path + '/' + file_name

		db_obj = dbActionReturn()
		file = db_obj.read_file(file_path)

		# file = file.iloc[1:3,].applymap(str)
		# dt = file.iloc[1,]

		dt = file.dtypes
		# dt = dt.replace('object','object')
		# dt = dt.replace('\n','')

		# context['frame'] = html
		dt_dict = dt.to_dict()
		context['dt_dict'] = dt_dict
		context['file_path'] = file_path
		context['file_name'] = file_name

		# file = file.applymap(str)
		# request.session['file_dataframe'] = file.to_json()

		return render(request, 'file_upload.html', context)

	if 'select_date' in request.POST:

		get_date = request.POST.dict()

		date_format = get_date.get('_date_format_list')
		month_col = get_date.get('_table_name_list')
		filepath = get_date.get('file_path')
		filedict = get_date.get('file_dict')

		# try:
		# 	session_file_dataframe = request.session.get('file_dataframe')
		# 	file_df = pd.read_json(session_file_dataframe)
		# except:
		# 	pass

		query_data = dbActionReturn()
		query_data.add_month_col(filepath, month_col, date_format)

		filedict = filedict.replace('{', '')
		filedict = filedict.replace("'", '')
		filedict = filedict.replace("dtype", '')
		filedict = filedict.replace("(", '')
		filedict = filedict.replace(")", '')
		filedict = filedict.replace("}", '')
		filedict = filedict.split(',')

		file_dict = {}

		for i in filedict:
			index = i.split(':')
			file_dict[index[0]] = index[-1]

		context['dt_dict'] = file_dict
		context['file_path'] = filepath
		context['date_format'] = date_format

		return render(request, 'file_upload.html', context)


@login_required()
def dbAction(request):
	context = {}
	file_data = request.POST.get('file_dict')

	if file_data:

		file_data = file_data.replace('{', '')
		file_data = file_data.replace("'", '')
		file_data = file_data.replace("dtype", '')
		file_data = file_data.replace("(", '')
		file_data = file_data.replace(")", '')
		file_data = file_data.replace("}", '')
		file_data = file_data.split(',')

		data = {}

		for i in file_data:
			index = i.split(':')
			data[index[0]] = index[-1]

		context['file_columns'] = data

	file_path = request.POST.get('file_path', None)
	file_name = str(file_path).split('/')
	context['file_name'] = file_name[-1]
	context['file_path_again'] = file_path

	if request.POST:

		if '_newdb' in request.POST:
			uploader_name = request.user

			query_data = dbActionReturn()

			login_data = request.POST.dict()
			table_name = login_data.get('_newtable')
			file_path = login_data.get('_file_path')

			msg = query_data.newTable(table_name.lower(), file_path, uploader_name)
			context['exists'] = str(msg)

		if '_insert' in request.POST:
			uploader_name = request.user

			query_data = dbActionReturn()

			login_data = request.POST.dict()
			table_name = login_data.get('_table_name_list')
			file_path = login_data.get('_file_path_insert')

			msg = query_data.insert_file(table_name.capitalize(), file_path, uploader_name)
			context['exists'] = str(msg)

		if '_update' in request.POST:
			uploader_name = request.user

			query_data = dbActionReturn()

			update_data = request.POST.dict()

			table_name = update_data.get('_table_name_list')
			date_format = update_data.get('_select_month')
			file_path = update_data.get('_file_path_update')

			msg = query_data.update_table(table_name, date_format, file_path, uploader_name)
			context['exists'] = msg

	query_data = dbActionReturn()

	context['dbTables'] = query_data.columns()

	return render(request, 'fileCalculations.html', context)


@login_required()
def view_tables(request):
	table_data = dbActionReturn()
	tables = table_data.get_tables()

	# print(tables)
	context = {'table': tables}
	return render(request, 'show_tables.html', context)


@login_required()
def database_to_select(request):
	table_data = dbActionReturn()
	table_name = table_data.tables()  # returns -> [('anotherdb',), ('attendence',)]
	filtered_table_name = [x[0] for x in table_name]

	context = {'table_name': filtered_table_name}

	return render(request, 'select_database.html', context)


@login_required()
def show_data(request):
	data_of_month = request.POST.get('_select_month')
	data_of_table = request.POST.get('_table_name_list')

	if not (data_of_month and data_of_table):
		return redirect('/view-db/')

	elif data_of_month and data_of_table:

		select_context = {}
		query_data = dbActionReturn()

		msg = query_data.return_single_table(data_of_table, data_of_month)

		select_context['tbl_name'] = data_of_table
		select_context['table_data'] = msg

		return render(request, 'data.html', select_context)

	else:
		return redirect('/view-db/')


@login_required()
def search_form_with_table(request):
	# return render(request, 'search_form_with_table.html')

	select_context = {}

	data_of_month = request.POST.get('_select_month')
	data_of_table = request.POST.get('_table_name_list')

	if not (data_of_month and data_of_table):
		return redirect('/view-db/')

	# <Date to String Month Name>
	from datetime import datetime

	dt = datetime.strptime(data_of_month, '%Y-%m')
	str_month = dt.strftime('%B')

	# </Date to String Month Name>

	select_context['tbl_name'] = data_of_table
	select_context['month_name'] = str_month

	db_obj = dbActionReturn()
	column_names = db_obj.table_columns(data_of_table)
	column_names.remove('id')
	column_names.remove('dbuploadername')
	remove_db = [x[2:] for x in column_names]

	select_context['select_month'] = data_of_month
	select_context['table_name_list'] = data_of_table

	select_context['column_names'] = remove_db

	if '_search' in request.POST:

		search_return = request.POST.dict()
		data_of_month = search_return.get('_select_month')
		data_of_table = search_return.get('_table_name_list')

		search_column = search_return.get('_column_name')
		search_text = search_return.get('_search_text')

		select_context['_select_month'] = data_of_month
		select_context['_table_name_list'] = data_of_table

		query_data = dbActionReturn()

		rows_count = query_data.return_query_rows_count(data_of_table, data_of_month, search_column, search_text)


		msg = query_data.return_search_table(data_of_table, data_of_month, search_column, search_text)

		select_context['table_data'] = msg

		return render(request, 'search_form_with_table.html', select_context)

	return render(request, 'search_form_with_table.html', select_context)

# if request.POST:

# 	return render(request, 'data.html', context)
# else:
# 	context = {}

# 	table_data = dbActionReturn()

# 	table_name = table_data.tables() # returns -> [('anotherdb',), ('attendence',)]
# 	filtered_table_name = [x[0] for x in table_name]

# 	context = {'table_name':filtered_table_name}
# 	return render(request, 'select_database.html', context)

# CREATE TABLE Serhhst (id int NOT NULL AUTO_INCREMENT,
# serialnumber  varchar(255),
# sku  varchar(255),
# skudescription  varchar(255),
# datetime  varchar(255),
# owninglocation  varchar(255),
# inventorystatus  varchar(255),
# soaprocess  varchar(255),
# system  varchar(255),
# inventorystate  varchar(255),
# stoinstorewarrantyorder  varchar(255),
# trackingnumber  varchar(255),
# fromlocation  varchar(255),
# tolocation  varchar(255),
# month  varchar(255),
# PRIMARY KEY (id))


# @login_required(login_url='/admin/login/')
