from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3
import pandas as pd
import os
import numpy as np


app = Flask(__name__)

#HOME PAGE 
@app.route('/')
def index():
        return render_template('index.html')
@app.route('/about')
def about_fun():
        return render_template('about.html')

@app.route('/login')
def login_fun():
        return render_template('login_pages/login.html')

@app.route('/signup')
def signup_fun():
        return render_template('signup_pages/signup.html')

@app.route('/admin_signup')
def admin_singup():
        return render_template('signup_pages/admin_signup.html')
@app.route('/admin_login')
def admin_login():
        return render_template('login_pages/admin_login.html')

#now to store_signup info in database
@app.route('/store_signup_info', methods =['GET','POST'])
def store_func():

        fname = request.form['Fname']
        lname = request.form['Lname']
        email = request.form['Email']
        password = request.form['password']
        phno = request.form['PhoneNumber']
        org_name = request.form['Organization']

        #now to store in our database
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO UserInfo VALUES(?,?,?,?,?,?)''',(fname,lname,email,password,phno,org_name))
                con.commit
        return render_template('signup_pages/signup_conf.html')

#this route is called after user enters login information
@app.route('/login_check', methods = ['GET', 'POST'])
def login_check_fun():
        email = request.form['Email']
        password = request.form['Password']
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from UserInfo where Email = ?''',(email,))
                correct_password = cur.fetchall()
        if(correct_password[0][0]==password):
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT fname from UserInfo where Email = ?''',(email,))
                        fname_ = cur.fetchall()
                #redirect to user (non-admin) portal
                return render_template('user_portal_pages/user_portal.html', items = fname_[0][0])
        else:
                return render_template('login_pages/unsuccessful_user_login.html')






'''
ROUTES BELOW ARE USED TO HANDLE ALL ADMIN RELATED TASKS. KINDLY REFER TO HOW CONTROL IS PASSED FROM EACH WEBPAGE AND INFORMATION IS EXTRACTED
THE SECTION AFTER THIS COVERS ROUTES USED FOR OUR USER PORTAL.
'''




#route is  called to store admin signup info
@app.route('/admin_store_signup_info', methods =['GET','POST'])
def store_func_admin():

        fname = request.form['Fname']
        lname = request.form['Lname']
        email = request.form['Email']
        password = request.form['password']
        phno = request.form['PhoneNumber']
        org_name = request.form['Organization']

        #now to store in our database
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO AdminInfo VALUES(?,?,?,?,?,?)''',(fname,lname,email,password,phno,org_name))
                con.commit
        return render_template('signup_pages/signup_conf.html')

#this route is used to check admin login
@app.route('/admin_login_check', methods = ['GET', 'POST'])
def login_check_fun_admin():
        email = request.form['Email']
        password = request.form['Password']
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from AdminInfo where Email = ?''',(email,))
                correct_password = cur.fetchall()
        if(correct_password[0][0]==password):
                #redirect to admin portal
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT fname from AdminInfo where Email = ?''',(email,))
                        fname_ = cur.fetchall()
                return render_template('admin_portal_pages/admin_portal.html' ,items = fname_[0][0])
        else:
                return render_template('login_pages/unsuccessful_admin_login.html')
@app.route('/reroute_to_admin_portal')
def show_admin_portal():
        return render_template('admin_portal_pages/admin_portal.html')
        

#route is called when the admin clicks on the create new project option for the first time
@app.route('/create_project')
def create_project():
        return render_template('admin_portal_pages/admin_create_new_project.html')

#route is called to store the project details that the admin has entered in the database
@app.route('/store_admin_project_details', methods = ['GET', 'POST'])
def store_admin_proj_details():
        admin_email = request.form['AdminEmail']
        org_name = request.form['OrganizationName']
        proj_name = request.form['ProjectName']
        proj_domain = request.form['ProjectDomain']
        proj_description = request.form['ProjectDescription']

        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO AdminProjectInfo VALUES(?,?,?,?,?)''',(admin_email,org_name, proj_name, proj_domain, proj_description))
                con.commit

        return render_template('admin_portal_pages/project_addition_confirmation.html')




#below routes are used for viewing projects created by administrators




#route is called when admin clicks on view projects - displays status
@app.route('/admin_view_projects')
def show_admin_projects():
        return render_template('admin_portal_pages/admin_view_extract_info.html')
#route is called by the /admin_view_projects route to store info entered in the admin_view_extract_info.html page and relevant info is projected
@app.route('/validate_admin_info_show', methods = ['GET', 'POST'])
def show_admin_projects_page():
        admin_email = request.form['AdminEmail']
        org_name = request.form['OrganizationName']
        password = request.form['Password']

        #now to validate with the Admin information data base table
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from AdminInfo where Email =?''',(admin_email,))
                correct_pass = cur.fetchall()

        if(correct_pass[0][0]==password):
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT OrgName from AdminInfo where Email =?''',(admin_email,))
                        correct_org = cur.fetchall()
                if(correct_org[0][0] == org_name):
                        with sqlite3.connect('ems.db') as con:
                                cur= con.cursor()
                                cur.execute('''SELECT*FROM AdminProjectInfo where OrganizationName = ?''',(org_name,))
                                
                        return render_template('admin_portal_pages/show_admin_org_projects.html',items = cur.fetchall())
                else:
                        return render_template('admin_portal_pages/back_to_homepage.html')
        else:
                return render_template('admin_portal_pages/back_to_homepage.html')
                

#below routes are for viewing members :

#route is called when admin clicks on view members - displays status
@app.route('/admin_view_members')
def show_admin_members():
        return render_template('admin_portal_pages/admin_member_extract_info.html')
#rote is called by the above route to validate :
@app.route('/validate_admin_info_show_members', methods = ['GET', 'POST'])
def show_admin_members_page():
        admin_email = request.form['AdminEmail']
        org_name = request.form['OrganizationName']
        password = request.form['Password']

        #now to validate with the Admin information data base table
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from AdminInfo where Email =?''',(admin_email,))
                correct_pass = cur.fetchall()

        if(correct_pass[0][0]==password):
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT OrgName from AdminInfo where Email =?''',(admin_email,))
                        correct_org = cur.fetchall()
                if(correct_org[0][0] == org_name):
                        with sqlite3.connect('ems.db') as con:
                                cur= con.cursor()
                                cur.execute('''SELECT*FROM UserInfo where OrgName = ?''',(org_name,))            
                                
                        return render_template('admin_portal_pages/show_admin_org_members.html',items = cur.fetchall())
                else:
                        return render_template('admin_portal_pages/back_to_homepage.html')
        else:
                return render_template('admin_portal_pages/back_to_homepage.html')



'''
ROUTES BELOW ARE USED TO HANDLE ALL USER PORTAL RELATED FUNCTIONALITY. KINDLY REFER TO HOW CONTROL IS PASSED BETWEEN WEBPAGES AND THE DATABASE
THERE IS A STRONG SIMILARITY BETWEEN THE ABOVE TWO TYPES OF ROUTES IN TERMS OF OPERATION.
'''

#route to return to user portal
@app.route('/reroute_to_user_portal')
def return_to_user_portal():
        return render_template('user_portal_pages/user_portal.html')
@app.route('/user_view_join_project')
def show_join_user_project():
        return render_template('user_portal_pages/user_view_extract_info.html')

@app.route('/validate_user_info_show_projects', methods = ['GET', 'POST'])
def show_join_user_project_page():
        admin_email = request.form['UserEmail']
        org_name = request.form['OrganizationName']
        password = request.form['Password']

        #now to validate with the Admin information data base table
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from UserInfo where Email =?''',(admin_email,))
                correct_pass = cur.fetchall()

        if(correct_pass[0][0]==password):
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT OrgName from UserInfo where Email =?''',(admin_email,))
                        correct_org = cur.fetchall()
                if(correct_org[0][0] == org_name):
                        with sqlite3.connect('ems.db') as con:
                                cur= con.cursor()
                                cur.execute('''SELECT*FROM AdminProjectInfo where OrganizationName = ?''',(org_name,))
                                
                        return render_template('user_portal_pages/show_user_org_projects.html',items = cur.fetchall())
                else:
                        return render_template('user_portal_pages/back_to_homepage.html')
        else:
                return render_template('user_portal_pages/back_to_homepage.html')

        
#this route is called once user validation has been done in the previous routes
@app.route('/select_user_project', methods = ['GET', 'POST'])
def select_user_proj_validate():
        proj_name = request.form['selection']
        #now to store attributes of project selected into the User projects information table in our database :
        email = request.form['email']
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT OrgName from UserInfo where Email =?''',(email,))
                org_name = cur.fetchall()[0][0]

                cur.execute('''SELECT ProjectDomain from AdminProjectInfo where ProjectName = ?''',(proj_name,))
                proj_domain = cur.fetchall()[0][0]

                cur.execute('''SELECT ProjectDescription  from AdminProjectInfo where ProjectName =?''',(proj_name,))
                proj_desc = cur.fetchall()[0][0]
        #now to populate our table :
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO UserProjectInfo VALUES(?,?,?,?,?)''',(email,org_name,proj_name,proj_domain,proj_desc))
                con.commit
        return render_template('user_portal_pages/project_joining_conf.html')

@app.route('/user_view_projects')
def ask_user_org_pass():
        return render_template('user_portal_pages/extract_user_org_pass.html')
@app.route('/validate_user_details_show_joined_projects', methods=['GET', 'POST'])
def show_user_joined_project_details():
        org_name = request.form['OrganizationName']
        password = request.form['Password']
        #authenticate and show details or goback to user portal
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Password from UserInfo where OrgName =?''',(org_name,))
                correct_pass = cur.fetchall()[0][0]

        if (correct_pass == password):
                with sqlite3.connect('ems.db') as con:
                        cur = con.cursor()
                        cur.execute('''SELECT Email from UserInfo where Password =?''',(password,))
                        email = cur.fetchall()[0][0]

                        cur.execute('''SELECT ProjectName, ProjectDomain, ProjectDescription FROM UserProjectInfo WHERE UserEmail =?''',(email,))
                return render_template('user_portal_pages/show_joined_proj_details_user.html', items = cur.fetchall())
        else:
                return render_template('user_portal_pages/back_to_homepage.html')

#route to show members belonging to an organization  => this feature is open to all users for purposes of networking and identifying people
@app.route('/user_view_org_members')
def show_org_entry_page():
        return render_template('user_portal_pages/org_name_entry_page.html')
@app.route('/validate_org_display_results', methods =['GET','POST'])
def show_org_emp__info():
        org_name = request.form['OrganizationName']
        proj_name = request.form['ProjectName']
        with sqlite3.connect('ems.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT Fname, Lname, Email,PhoneNumber from UserInfo where OrgName =?''',(org_name,))
                i1 = cur.fetchall()
                
                cur.execute('''SELECT UserEmail from UserProjectInfo where ProjectName =?''',(proj_name,))
                email = cur.fetchall()[0][0]
                #showing details based on interested project (project teams)
                cur.execute('''SELECT Fname, Lname, Email,PhoneNumber from UserInfo where Email=?''',(email,))
                i2= cur.fetchall()
        return render_template('user_portal_pages/show_details_with_org_values.html', items1 = i1, items2 = i2)
        

#route is called to handle error cases
@app.errorhandler(500)
def page_not_found(e):
        #in case of internal server error
        return render_template('error.html')


if __name__ == '__main__':
        app.run(debug=True)
