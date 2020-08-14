from sqlalchemy import create_engine

import pymysql

import pandas as pd

sqlEngine  = create_engine('mysql+pymysql://root:usman123@127.0.0.1/djangoRealTime')
dbConnection = sqlEngine.connect()

print(sqlEngine)

print('done')


data = pd.read_csv('location.csv')

data['id'] = None
data.set_index('id',inplace=True)


try:
	frame = data.to_sql('location', dbConnection, if_exists='append');
	#print('try'#
except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s Inserted successfully."%'location');   

finally:

    dbConnection.close()

print(data)

# frame = pd.read_sql("SELECT * FROM MyGuests LIMIT 10", dbConnection);

 

# pd.set_option('display.expand_frame_repr', False)
# dbConnection.close()
# print(frame)