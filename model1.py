# import sqlite3;
# # import main;

# conn_1 = sqlite3.connect('my_database.db');
# cursor = conn_1.cursor();

# cursor.execute("Select * from Customers Limit 10");

# print(cursor.fetchall());
# print("Products: /n ")
# cursor.execute("select * from Products Limit 10");
# print(cursor.fetchall())

# conn_1.close();

import ast
string_l = "['Beauty', 'Fashion']"
x = "Beauty, Fashion"
real_list = ast.literal_eval(x)
print(type(string_l))
print(real_list)
print(type(real_list))

for i in real_list:
    print(i)