import sqlite3

#establishing connection between database object and python
conn = sqlite3.connect('ems.db')

#creating reference database to work with
conn.execute('''CREATE TABLE UserInfo(
    Fname text not null, Lname text, Email text not null, Password text not null,
    PhoneNumber integer, OrgName text, unique(Email))''')


conn.execute('''CREATE TABLE AdminInfo(
    Fname text not null, Lname text, Email text not null, Password text not null,
    PhoneNumber integer, OrgName text, unique(Email))''')

conn.commit

print('''Database has been generated. Redirect to flask app.py to insert value
           into DB for every instance''')


#database created

#NOTE : RUN ONLY ONCE :
#RUN COUNT : 1

