import mysql.connector

database = mysql.connector.connect(
    #host='roundhouse.proxy.rlwy.net', 
    #port='39518',
    #user='root',
    #password='nZBgjJKxBSgsOYdnHYkldoivhAPPfxqf',
    #database='railway'
    host='127.0.0.1', 
    port=3306,
    user='root',
    password='',
    database='bd'
)

#try:
    #db = mysql.connector.connect(**database)
#except mysql.connector.Error as err:
#    print(f"Error: {err}")