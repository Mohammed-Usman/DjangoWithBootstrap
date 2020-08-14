import mysql.connector
import pandas as pd 
import xlrd
# from sqlalchemy import create_engine
# import pymysql
# import MYSQL



class dbActionReturn():

	def __init__(self):
		
		self.dbname = 'djangoRealTime'

		self.mydb = mysql.connector.connect(

		  host 		= "localhost",
		  user 		= "root",
		  password 	= "usman123",
		  database 	= self.dbname,
		)

		self.cr = self.mydb.cursor()


		
		# host 		= "localhost",
		# user 		= "root",
		# password 	= "1234",
		# database 	= 'djangoRealTime'

		# # self.cr = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port,database ))		
		# self.engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, password, host,database ))

		# self.cr = self.engine.connect()

		

	def tables(self):

		list_tables = []
		self.cr.execute('SHOW TABLES')

		for i in self.cr:
			if '_' not in str(i):
				list_tables.append(i)

		return list_tables

	def columns(self):

		table_dict = {}

		table_name_list = self.tables()

		for tableName in table_name_list:
			column_dict = {}

			self.cr.execute("SELECT COLUMN_NAME, DATA_TYPE  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'".format(self.dbname,tableName[0]))


			for i in self.cr:
				# if i[0] != 'id':
				column_dict[i[0]] = i[1]

			# using tableName[0] bcz cursor returning tuple -> ('customers',)

			table_dict[str(tableName[0])] = column_dict
		return table_dict
		
	def newTable(self, msg, file_path):

		table_name_list = self.tables()
		table_name = [x[0].lower() for x in table_name_list]

		print('FILE PATH',file_path)

		if msg in table_name:
			
			returning_msg = "Database Name '{}' Already Exists!!!".format(msg.capitalize())

			return returning_msg

		ext = file_path.split('.')[-1]

		if 'csv' in  ext:	

			file = pd.read_csv(file_path)
			

		elif 'xlsx' or 'xls' in ext:
		
			file = pd.read_excel(file_path)

		try:

			tbl_name = msg.capitalize()
			print(tbl_name)
			# file.to_sql(name=tbl_name,con=self.mydb, if_exists='append',index=False)

		except Exception as e:

			print(e)

	def retrieve_all_tables(self):
		table_dict = {}

		table_name_list = self.tables()
		# print(table_name_list)
		for tableName in table_name_list:
			column_dict = {}

			self.cr.execute("SELECT * FROM {} LIMIT 10".format(tableName[0]))


			for i in self.cr:
				# if i[0] != 'id':
				print(i)

			# using tableName[0] bcz cursor returning tuple -> ('customers',)

			table_dict[str(tableName[0])] = column_dict
		return table_dict


# data = dbActionReturn()
# print(data.retrieve_all_tables())