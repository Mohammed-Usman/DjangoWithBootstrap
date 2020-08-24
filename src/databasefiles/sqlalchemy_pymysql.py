from sqlalchemy import create_engine
import pymysql
import pandas as pd
import re





class dbActionReturn():

	def __init__(self):

		self.dbname = 'djangoRealTime'
		self.sqlEngine  = create_engine('mysql+pymysql://root:usman123@127.0.0.1/{}'.format(self.dbname))
		#self.dbConnection = sqlEngine.connect()

	def tables(self):

		list_tables = []

		with self.sqlEngine.connect() as cr:
			
			result = cr.execute('SHOW TABLES')

			for i in result:
				if '_' not in str(i):
					list_tables.append(i)
		return list_tables


	def columns(self):

		table_dict = {}
		table_name_list = self.tables()

		with self.sqlEngine.connect() as cr:

			for tableName in table_name_list:
				column_dict = {}

				result = cr.execute("SELECT COLUMN_NAME, DATA_TYPE  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(self.dbname,tableName[0]))

				for i in result:
					if i[0] != 'id':
						column_dict[i[0][2:]] = i[1]
				# using tableName[0] bcz cursor returning tuple -> ('customers',)

				table_dict[str(tableName[0])] = column_dict
		return table_dict

	def table_columns(self, tableName):

		
		table_col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(self.dbname,tableName)

		with self.sqlEngine.connect() as cr:
			result = cr.execute(table_col_query)
			columns_list = [i[0] for i in result]	
		return columns_list

	def create_table(self, connection, table_name, cols):

		create_db_str = 'CREATE TABLE {} (id int NOT NULL AUTO_INCREMENT,dbuploadername varchar(20),{} PRIMARY KEY (id))'
		col_str = ''
		col = [x.replace(' ','').lower() for x in cols]
		col = [re.sub(r"[^A-Za-z]+", '', i) for i in col]

		for i in col:
			col_str = col_str + i + "  varchar(255), "

		
		create_query = create_db_str.format(table_name.lower(), col_str)
		# print(create_query)

		connection.execute(create_query)

	def extra_columns(self,tableName, file_cols):

		tbl_cols = self.table_columns(tableName)

		return [i for i in file_cols if i not in tbl_cols]

		
	def populate_table(self,connection,tbl_name, file, uploader_name):

		file = file.applymap(str)
		cols = file.columns
		file.columns = [i.replace(' ','').lower() for i in cols]
		file.columns = [re.sub(r"[^A-Za-z]+", '', i) for i in file.columns]
		file['dbuploadername'] = str(uploader_name).title()

		file.drop(columns = self.extra_columns(tbl_name.lower(), list(file.columns)), inplace=True)
		print(file.columns)

		if len(file.columns) < 3:
			raise Exception('Database Columns Does Not Match')
		else:
			frame = file.to_sql(tbl_name.lower(), connection, index= False, if_exists='append')

	def read_file(self, file_path):

		ext = file_path.split('.')[-1]
		if 'csv' in ext:	

			file = pd.read_csv(file_path)
			file.columns = [re.sub(r"[^A-Za-z]+", '', i) for i in file.columns]
			return file	

		elif 'xlsx' or 'xls' in ext:

			file = pd.read_excel(file_path)
			file.columns = [re.sub(r"[^A-Za-z]+", '', i) for i in file.columns]
			return file	

	def insert_file(self, tbl_name, file_path, uploader_name):

		#print('Sql Alchemy',tbl_name, file_path)

		try:
			connection = self.sqlEngine.connect()

			file = self.read_file(file_path)
			self.populate_table(connection,tbl_name, file, uploader_name)

			connection.close()

			returning_msg = "'{}' named Database is populated".format(tbl_name)
			return str(returning_msg)

		except Exception as e:

			return str(e)


	def newTable(self, msg, file_path, uploader_name):

		table_name_list = self.tables()
		table_name = [x[0].lower() for x in table_name_list]

		if msg in table_name:
			
			returning_msg = "Database Name '{}' Already Exists!!!".format(msg.capitalize())
			return returning_msg

		tbl_name = msg.capitalize()

		try:

			file = self.read_file(file_path)

		except Exception as e:

			return str(e)

		try:

			connection = self.sqlEngine.connect()
			# tbl_name = msg.capitalize()
			cols = file.columns

			self.create_table(connection, tbl_name, cols)
			self.populate_table(connection,tbl_name, file, uploader_name)	

		except Exception as e:

			connection.close()
			return str(e)

		
		returning_msg = "'{}' named Database is created & populated".format(tbl_name)
		return str(returning_msg)


	def del_before_update(self, connection, tbl_name, month_to_del):

		from datetime import datetime
	
		dt = datetime.strptime(month_to_del, '%Y-%m')
		str_month = dt.strftime('%B')

		del_month_data = "DELETE FROM {} where dbmonth = '{}'".format(tbl_name, str_month.capitalize())
		connection.execute(del_month_data)
		return str_month


	def update_table(self, tbl_name, month_to_del,file_path, uploader_name):

		table_name = tbl_name.capitalize()

		try:

			connection = self.sqlEngine.connect()

			str_month = self.del_before_update(connection, tbl_name, month_to_del)

			file = self.read_file(file_path)

			self.populate_table(connection, tbl_name, file, uploader_name)

		except Exception as e:

			connection.close()
			return e

		returning_msg = "'{}' named Database is updated for dbmonth {}".format(tbl_name, str_month)
		return returning_msg

		
	def int_to_month(self, int_month):

		import datetime
		str_month = datetime.date(1900, int_month, 1).strftime('%B')
		return str_month


	def add_month_col(self, file_path, date_col, date_format):

		# file = file_df
		file = self.read_file(file_path)
		file['Month'] = pd.to_datetime(file[date_col], format=date_format).dt.strftime('%B')
		file.columns = ['db'+i for i in file.columns]

		ext = file_path.split('.')[-1]

		if 'csv' in ext:	

			file.to_csv(file_path,index=False)

		elif 'xlsx' or 'xls' in ext:

			file.to_excel(file_path,index=False)

	def get_tables(self):


		'''
		Returns all database tables by limiting rows to 20    
	

		'''
		table_name_list = self.tables()
		table_names = [x[0].capitalize() for x in table_name_list]

		connection = self.sqlEngine.connect()

		db_to_html_list = []
		# db_to_html_list = {}

		for tbl_name in table_names:


			query = "SELECT * FROM {} LIMIT 20".format(tbl_name)
			tbl = pd.read_sql(query, connection)
			tbl.drop(['id'], axis=1, inplace=True)
			tbl.columns = tbl.columns.str.capitalize()
			# tbl_dict = tbl.to_dict()
			# tbl = pd.read_sql_table(tbl_name, connection)
			tbl = tbl.to_html(classes=["table ","table-hover", "table-bordered"],  table_id = "example1")
			# db_to_html_list[tbl_name] = tbl_dict
			db_to_html_list.append(tbl)
			
		connection.close()
		return db_to_html_list

	def return_single_table(self, table_name, month_to_del):

		from datetime import datetime
	
		dt = datetime.strptime(month_to_del, '%Y-%m')
		str_month = dt.strftime('%B')

		connection = self.sqlEngine.connect()	

		query = "SELECT * FROM {} WHERE dbmonth = '{}'".format(table_name.lower(), str_month.capitalize())

		tbl_data = pd.read_sql(query, connection)
		tbl_data.drop(['id'], axis=1, inplace=True)
		tbl_data.columns = [col[2:] for col in tbl_data.columns]
		tbl_data.columns = tbl_data.columns.str.capitalize()

		tbl_data.replace('nan','',inplace=True)
		tbl = tbl_data.to_html(classes=["table ","table-hover", "table-bordered", "table-info", "table-striped"],  table_id = "example2", show_dimensions=True,index=False, justify='center')

		connection.close()

		return tbl
