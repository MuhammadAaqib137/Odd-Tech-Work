# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:22:20 2021

@author: Ashva.javed
"""
import pdb
import sqlite3
from sqlite3 import Error
from datetime import datetime,date
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))

import hashlib

def create_connection_attendence():
    try:
        conn = sqlite3.connect('attendence.db')
        return conn
    except Error as e:
        print(e)
        return None


def create_table_(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False

def get_all_attendence():
    try:
        conn = sqlite3.connect('attendence.db')
        cursor = conn.cursor()
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        cursor.execute(f"select * from Attendence")  
#         print(a)
        returned_data = cursor.fetchall()
#         print(returned_data)
        cursor.close()
        return returned_data
    
    except sqlite3.Error as error:
        cursor.close()
        print("Error", error)
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        return -1

def show_table(table_name):
    try:
        conn = sqlite3.connect('attendence.db')
        cursor = conn.cursor()
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        a = cursor.execute(f"select * from {table_name}")
        returned_data = cursor.fetchall()
#         print(returned_data)
        cursor.close()
        return returned_data
    
    except sqlite3.Error as error:
        cursor.close()
        print("Error", error)
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        return -1
    
def update_table_status(admin_id, status):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    try:
        r =cursor.execute("UPDATE Admins SET status=? WHERE id=?",(status,admin_id))
        conn.commit()
        cursor.close()
        print("No of records updated : ",r.rowcount)
        return r.rowcount
    except Exception  as error:
        print("Error in updating admins records ", error)
        return -1
    
# ["admin_id","admin_email", "status", "admin_name", "role", 'company']
def update_table(admin_id, admin_name=None, role=None, company=None):
    conn = sqlite3.connect('attendence.db')
    sqliteConnection = create_connection_attendence()
    cursor = conn.cursor()
    try:
        r =cursor.execute("UPDATE Admins SET name=?,  company=? WHERE id=?",(admin_name,company, admin_id))
        conn.commit()
        cursor.close()
        print("No of records updated : ",r.rowcount)
        return r.rowcount
    except Exception  as error:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        print("Error in updating admins records ", error)
        return -1
    
    
def insert_Admin( admin_name,admin_email,  password):
    try:
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute("SELECT id FROM Admins WHERE email=?",(admin_email))
        rows = cursor.fetchall()
        if len(rows)>0:
            print("Email already registered")
            return -1
        else:
            data_tuple = (admin_email, admin_name, password)
            data_tuple2 = (admin_email, password)
            
            sqlite_insert_blob_query = """ INSERT INTO Admins
                                      ( fullname, email,  password) 
                                      VALUES (?,  ?, ?)"""
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            cursor.execute("select id from Admins where email=? AND password =?",data_tuple2 )       
            Admin_id = cursor.fetchall()      
            print(admin_email ," details are inserted successfully in Admin table with Admin_id ", Admin_id)
            cursor.close()
            return Admin_id[0][0]
    except sqlite3.Error as error:
        print("Error", error)
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        return -1
    
    
def create_attendence_database():
    conn = create_connection_attendence()
    # Companies should have address as well
   
    
    
# {'role':'superAdmin/admin','company':'*','name':'adminName'}
    sql_create_Admins_table       = """ CREATE TABLE IF NOT EXISTS Admins (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        fullname varchar(45),
                                        email varchar(45),
                                        password varchar(100),
                                        status tinyint NULL,
                                        created_date datetime,
                                        updated_date timestamp NULL
                                );"""

    
    sql_create_Branches_table = """ CREATE TABLE IF NOT EXISTS Branches (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        company_id int ,
                                        name varchar(45) NULL,
                                        address varchar(45) NULL,
                                        status tinyint 
                                        created_date datetime,
                                        updated_date timestamp NULL,
                                        FOREIGN KEY(Company_id) REFERENCES Companies(id)
                                    );  """
    sql_create_Companies_table = """ CREATE TABLE IF NOT EXISTS Companies (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        name varchar(100) UNIQUE NOT NULL,
                                        status tinyint(1) NULL, 
                                        created_date timestamp NOT NULL,
                                        updated_date datetime NULL
                                    ); """
    

    sql_create_Devices_table    = """ CREATE TABLE IF NOT EXISTS Devices (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        branch_id smallint(6), 
                                        name varchar(45),
                                        location varchar(45) NULL,
                                        mac_address varchar(25) UNIQUE NOT NULL,
                                        ip_address varchar(15) NOT NULL 
                                        status tinyint(4),
                                        registtation_date datetime NOT NULL, 
                                        updated_date timestamp  NULL,
                                        FOREIGN KEY(branch_id) REFERENCES Branches(id)
                                );"""
    sql_create_Employees_table = """ CREATE TABLE IF NOT EXISTS Employees (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        cm_employee_id varchar(50) NULL,
                                        company_id int(11) NULL,
                                        shift_id smallint(6) NULL,
                                        first_name varchar(30),
                                        last_name varchar(30) NULL,
                                        status tinyint(4) NOT NULL,
                                        message varchar(100) NULL,
                                        date_join datetime NULL,
                                        date_resign datetime NULL,
                                        created_date datetime  NULL,
                                        updated_date timestamp NULL,
                                        FOREIGN KEY(company_id) REFERENCES Companies(id),
                                        FOREIGN KEY(shift_id) REFERENCES Shifts(id)
                                        ); """
    
    sql_create_Shifts_table   = """ CREATE TABLE IF NOT EXISTS Shifts (
                                        id smallint(6) PRIMARY KEY AUTOINCREMENT,
                                        shift_name varcahr(35) NOT NULL,
                                        shift_start time NOT NULL,
                                        shift_end time NOT NULL,
                                        status tinyint(4)  NULL
                                        created_date datetime  NULL,
                                        updated_date timestamp NULL
                                );"""
    sql_create_Attendence_table = """ CREATE TABLE IF NOT EXISTS Attendence (
                                        id bigint Primary Key 
                                        employee_id integer  ,
                                        branch_id integer,
                                        device_id integer,
                                        entry_time datetime,
                                        entry_type enum('IN','OUT'),
                                        FOREIGN KEY(employee_id) REFERENCES Employees(id),
                                        FOREIGN KEY(branch_id) REFERENCES Branches(id),
                                        FOREIGN KEY(device_id) REFERENCES Devices(id)
                                        ); """
                       
    # create tables
    if not create_table_(conn, sql_create_Admins_table):
        print("Error! cannot create the Admins_table.")

    if not create_table_(conn,  sql_create_Branches_table ):
        print("Error! cannot create Branches table.")

    if not create_table_(conn, sql_create_Companies_table):
        print("Error! cannot create Companies table .")
        
  
    if not create_table_(conn, sql_create_Devices_table):
        print("Error! cannot create Devices Table.")

    if not  create_table_(conn, sql_create_Employees_table):
        print("Error! cannot create Employees table.")
    
    if not  create_table_(conn, sql_create_Shifts_table):
        print("Error! cannot create Shift table.")

    if not  create_table_(conn, sql_create_Attendence_table):
        print("Error! cannot create Attendence table.")
    

    # if not  create_table_(conn, sql_create_log_table):
    #     print("Error! cannot create LOG table.")
    # insert_Admin('admin@gmail.com' , '123')
    


def insert_Company(name , created_date =""):
    try:
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        cursor.execute("select id from Companies where name=?",(name) )   
        company_id = cursor.fetchall()
        if len(company_id)>0:
            print("A company exists with same name")
            return -1
        if created_date=='':
            created_date = date.today().strftime("%d/%m/%Y")
        data_tuple = ( name,created_date)
        sqlite_insert_blob_query = """ INSERT INTO Companies
                                  ( name,created_date) 
                                  VALUES (?, ?)"""
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print(name ," details are inserted successfully in Comapny table of ")
        cursor.execute("select id from Companies where name=? AND created_date =?",data_tuple )       
        company_id = cursor.fetchall()      
        cursor.close()
        return company_id[0][0]
    except sqlite3.Error as error:
        print("Error", error)
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        return -1



def insert_Building(Building_name , Address):
    try:
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT Building_id FROM Building WHERE Building_name=? and Address=?",(Building_name , Address,))
        Building_id = cursor.fetchall()
        if len(Building_id)>0:
            print("Building already registered")
            return Building_id[0][0]
        else:
            data_tuple = (Building_name , Address)
            sqlite_insert_blob_query = """ INSERT INTO Building
                                      ( Building_name , Address) 
                                      VALUES (?, ?)"""
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()

            cursor.execute("SELECT Building_id FROM Building WHERE Building_name=? and Address=?",
                           (Building_name , Address,) )       
            Building_id = cursor.fetchall()      
            print(Building_name ," details are inserted successfully in Building table with Building_id ", Building_id)
            cursor.close()
            return Building_id[0][0]
    except sqlite3.Error as error:
        print("Error", error)
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")
        return -1
    
def insert_branch(  Company_id ,Branch_name, address=''):
    try:
        # create a database connection
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT name FROM Companies WHERE id=?",(Company_id,))
        rows = cursor.fetchall()
        if len(rows)<=0:
            cursor.close()
            print("Company_id not registred")
            return -1 
   
        # cursor.execute("SELECT Building_name  FROM Building WHERE Building_id =?",(Building_id ,))
        # rows = cursor.fetchall()
        # if len(rows)<=0:
        #     cursor.close()
        #     print(f'Building_id: {Building_id} not registred')
        #     return -1 


        data_tuple = (Company_id , Branch_name, address)
        query = """ INSERT INTO Branch
                   (company_id , name,  address) 
                   VALUES (?, ?, ? )"""
        cursor.execute(query, data_tuple)
        sqliteConnection.commit()
        print(" address are inserted successfully in Branch table")
        cursor.execute("""select id from Branches
                        where company_id=? AND name =? AND address=? """,
                       data_tuple )       
        Branch_id = cursor.fetchall()      
        print(Branch_name ," details are inserted successfully in Branch table with Branch ", Branch_id)
        cursor.close()
        return Branch_id[0][0]
    except sqlite3.Error as error:
        cursor.close()
        print("Error", error)
        return -1
# def insert_log(log):
#     sqliteConnection = create_connection_attendence(()
#     cursor = sqliteConnection.cursor()
#     date_time = datetime.utcnow().strftime("%d/%m/%Y  %H:%M:%S")
#     sqlite_insert_blob_query = """ INSERT INTO Logs
#                               ( date_time,detail ) 
#                               VALUES (?, ?)"""
#     cursor.execute(sqlite_insert_blob_query, (date_time, log))
#     sqliteConnection.commit()
#     cursor.close()
    

       
def insert_device_data(branch_id,name, mac_address,registration_date ):
    sqliteConnection = create_connection_attendence()
    cursor = sqliteConnection.cursor()
    print("Connected to ")
    
    if not  if_branch_registered(branch_id):
        cursor.close()
        return -1

    cursor.execute("SELECT id FROM Device_detail WHERE mac_address=? ",(mac_address,))
    Device_id = cursor.fetchall()
    if len(Device_id)>0:
        cursor.close()
        return Device_id[0][0]
    else:
        data_tuple = (name, mac_address,registration_date)
        query = """ INSERT INTO Devices
                    ( name ,mac_address ,Admin_id, registeration_date)
                    VALUES (?, ?, ?, ?);"""
        cursor.execute(query, data_tuple)
        sqliteConnection.commit()
        print("Device  details are inserted successfully Device_detail table")
        cursor.execute("SELECT Device_id FROM Device_detail WHERE mac_address=? ",
              (mac_address,))
        Device_id = cursor.fetchall()
        print(name ," details are inserted successfully in Device table with id ", Device_id)
        cursor.close()
        return Device_id[0][0]


def delete_device_data(unique_key, is_id_not_mac = True ):
    sqliteConnection = create_connection_attendence()
    cursor = sqliteConnection.cursor()
    data_tuple = (unique_key)
    if is_id_not_mac:
        if if_device_registered(unique_key):
            return -1
        query = " DELETE FROM Device_detail WHERE Device_id = ?;  """
    else:
        if if_device_registered_with_mac(unique_key)==-1:
             return -1
        query = " DELETE FROM Device_detail WHERE mac_address = ?;  """
    cursor.execute(query, data_tuple)
    sqliteConnection.commit()
    cursor.close()
    return 1

def if_email_exist(admin_email):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Admins WHERE email=?",(admin_email,))
    rows = cursor.fetchall()
    if len(rows)>0:
        err = "email already registered"
        print(err)
        return False, err
    return True, ''

def if_admin_registered(admin_email):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Admins WHERE email=?",(admin_email,))
    rows = cursor.fetchall()
    if len(rows)<=0:
        print("admin not registred")
        return False
    elif rows[0][0]!='active':
        print(f"admin: {admin_email} is not active")
        return False
    return True


def if_admin_registered_with_id(Admin_id):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Admins WHERE id=?",(Admin_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)<=0:
        print("admin not registred")
        return False
    elif rows[0][0]!='active':
        print(f"admin: {Admin_id} is not active")
        return False
    return True
    

def if_company_registered(name):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Companies WHERE name=?",(name,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)<=0:
        print(name, " comapny not registred")
    elif rows[0][0]!='active':
        print(f"comapny: {name} is not active")
        return False
    return True
        
    
def if_branch_registered(Branch_id):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Branches WHERE id=?",(Branch_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)<=0:
        print(f"branch : {Branch_id}  is not registred")
        return False
    elif rows[0][0]!='active':
        print(f"Branch: {Branch_id} is not active")
        return False
    return True

    
def if_device_registered(device_id):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT mac_address FROM Devices WHERE id=?",(device_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)<=0:
        print("Device not registred")
        return False
    return True

def if_device_registered_with_mac(mac_address):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Devices WHERE mac_address=?",(mac_address,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)<=0:
        print("Device not registred")
        return -1
    return rows[0][0] 
    
def get_device_id_from_mac(mac_address):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Devices WHERE mac_address=?",(mac_address,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)!=0:
        return rows[0][0]
    else:
           return -1
   
    
def get_company_id_from_name(name):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Companies WHERE name=?",(name,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)!=0:
        return rows[0][0]
    else:
           return -1

def get_company_name_from_id(Company_id):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Companies WHERE id=?",(Company_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)!=0:
        return rows[0][0]
    else:
        return -1
def get_admin_email_from_admit_id(Admin_id):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Admins WHERE id=?",(Admin_id,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)!=0:
        return rows[0][0]
    else:
        return -1
def get_admin_id_from_admit_email(admin_email):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Admins WHERE email=?",(admin_email,))
    rows = cursor.fetchall()
    cursor.close()
    if len(rows)!=0:
        return rows[0][0]
    else:
           return -1

def get_branches_of_company_against_id(Company_id):
    sqliteConnection = create_connection_attendence()
    cursor = sqliteConnection.cursor()
    print("Connected to  database")
    try:
        cursor.execute("""SELECT id from Branches where company_id=?""", (Company_id,))
        rows = cursor.fetchall()
        cursor.close()
        return (rows)
    except Exception as error:
        cursor.close()
        print (error)
        return (-1)
    
def update_passward_from_email(admin_email, password):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    password = hashlib.md5(password.encode()).hexdigest()
    try:
        r =cursor.execute("UPDATE Admins SET password=? WHERE email=?",(password, admin_email))
        conn.commit()
        cursor.close()
        print("No of records updated : ",r.rowcount)
        return r.rowcount
    except Exception  as error:
        cursor.close()
        print("Error in updating admins password ", error)
        return -1

def auth_admin(admin_email, password):
    conn = sqlite3.connect('attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password , id, status from Admins WHERE email=?",(admin_email,))
    rows = cursor.fetchall()
    cursor.close()
    password = hashlib.md5(password.encode()).hexdigest()
    print(password)
    if rows[0][-1]!='active':
        print("Not an active admin")
        return False, ''
    else:
        if password==rows[0][0]:
            return True, rows[0][1]
        else:
            return False, rows[0][1]    
    
    
    
def auth_admin2(admin_email, password):
    sqliteConnection = create_connection_attendence()
    cursor = sqliteConnection.cursor()
#     conn = sqlite3.connect('companies.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT password , Admin_id, status from Admins WHERE admin_email=?",(admin_email,))
    cursor.execute("SELECT * from Admins WHERE email=?",(admin_email,))
    rows = cursor.fetchall()
    cursor.close()
    
#     print(rows)
    password = hashlib.md5(password.encode()).hexdigest()
#     print(password)
#     if rows[0][3]!='active':
# #         print("Not an active admin")
#         return False, ''
#     else:
    if password==rows[0][2]:
        return True, rows[0]
    else:
        return False, rows[0]
    
    

def update_Attendence_db(table, field, value, unique_id,unique_id_value):
    try:
        if table=='Companies':
            if not if_company_registered(unique_id_value):
                return -1
        elif table=='Admins':
            if unique_id =='email':
                if not  if_admin_registered(unique_id_value):
                    return -1
            elif unique_id =='id':
                if not  if_admin_registered_with_id(unique_id_value):
                    return -1
            else:
                return -1
        elif table=='Branches':
            if not if_branch_registered(unique_id_value):
                return -1
        elif table=='Devices':
            if unique_id =='mac_address':
                if not if_device_registered_with_mac(unique_id_value):
                    return -1
            elif unique_id =='id':
                if not if_device_registered(unique_id_value):
                    return -1
        else:
            return -1            
        conn = sqlite3.connect('attendence.db')    
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        print("Connected to  database")
        s = f"Update {table} set {field}=? where {unique_id}=?;"
        cursor.execute(s, (value,unique_id_value ))
        conn.commit()
        cursor.close()
        return 1
    except Exception as e:
        cursor.close()
        print(e)
        return -1


def remove_Entry_from_table(table, unique_id,unique_id_value):
    try:
        if table=='Attendence':
            if not if_company_registered(unique_id_value):
                print(f'{unique_id_value} not registered')
                return -1
        elif table=='Admins':
            if unique_id =='mail':
                if not  if_admin_registered(unique_id_value):
                    print(f'{unique_id_value} not registered')
                    return -1
            elif unique_id =='admin_id':
                if not  if_admin_registered_with_id(unique_id_value):
                    print(f'{unique_id_value} not registered')
                    return -1
            else:
                print(f'{unique_id} is not unique')
                return -1
        elif table=='Branches':
            if not if_branch_registered(unique_id_value):
                print(f'{unique_id_value} not registered')
                return -1
        else:
            print(f'{table} does not exists')
            return -1            
            
        sqliteConnection = create_connection_attendence()
        cursor = sqliteConnection.cursor()
        print("Connected to  database")
#         s = f"Update {table} set status='inactive' where {unique_id}=?;"
        s = f"Update {table} set deleted=1 where {unique_id}=?;"
        print(s)
        cursor.execute(s, (unique_id_value, ))
        sqliteConnection.commit()
        cursor.close()
        return 1
    except Exception as e:
        cursor.close()
        print(e)
        return -1
