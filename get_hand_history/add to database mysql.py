import mysql
import mysql.connector
from mysql.connector import Error
import itertools
import os
import time 
def mysql_change_pass(new_pass) :
    run("SET PASSWORD FOR 'root'@'localhost' = '%s';" % (new_pass))
    print("Password for 'root' user in changed no '%s'" % (new_pass))
def connect(db):
    try:
        conn = mysql.connector.connect(
                                        host = 'localhost',
                                        database = db,
                                        user = 'root',
                                        password = 'opangangnamstyle'
                                    )
        if conn.is_connected():
            print('Connected to %s database' % db)
            return conn
    except Error :
        print(Error)
    else :
        conn.close()
db_name = 'poker'
conn = connect(db_name)
cursor = conn.cursor()
run, run_many = cursor.execute, cursor.executemany
run("SET GLOBAL local_infile=1;")



#mysql_change_pass('opangangnamstyle')
#run("CREATE TABLE hist (id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(10000), mode VARCHAR(5))")

#run('ALTER TABLE temphist ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY')
command = {
    'create database' : 'CREATE DATABASE %s',
    'create table' : 'CREATE TABLE %s (%s)',#table_name, (col_name col_type, ...)
    'add column' : 'ALTER TABLE %s ADD COLUMN %s',
    'append line' : 'INSERT INTO %s (%s) VALUES (%s)' #name_table, (name _col), (data)
}

conn.commit()

run('SHOW DATABASES')
print(*[i[0] for i in cursor])
run('SHOW TABLES')
print(*[i[0] for i in cursor])

time.sleep(10)
path = 'C:/Users/Danilo/Desktop/poker/get_hand_history/hand_hist_database/'
modes = ['ps']
for mode in modes :
    temppath = path + mode + '/'
    id_among_mode = 2
    #if mode == 'ps' : break #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11

    for filename in list(os.listdir(temppath)) :
        f = open(temppath + filename, 'r')
        file = f.read()
        f.close()
        
        print(mode, id_among_mode)
        #run_many('INSERT INTO abs(hand, room) VALUES(%s, %s)', [(f, mode) for f in file.split('opangangnamstyle\n')[1:] if 'shows [' in f.split('show down')[1]])
        #run_many('INSERT INTO ong(hand, room) VALUES(%s, %s)', [(f, mode) for f in file.split('opangangnamstyle\n')[1:] if all(a in f.split('summary')[-1] for a in ['[', ']', 'net', 'seat'])])
        run_many('INSERT INTO ps(hand, room) VALUES(%s, %s)', [(f, mode) for f in file.split('opangangnamstyle\n')[1:] if 'showed [' in f.split('summary')[-1]])
        
        #run("LOAD DATA LOCAL INFILE '%s' INTO TABLE abs LINES TERMINATED BY 'opangangnamstyle\n';" % (temppath + filename))
        #run()
        
        conn.commit()
        id_among_mode += 1
#run('SELECT FROM hist_abs_files WHERE id = 1')
#print([c for c in cursor.fetchall()])


#runn(append, [('aaaaaaaaa', i) for  i in range(10)])
#conn.commit()
#run('SELECT * FROM temphist')
#run("DELETE FROM temphist WHERE ")
#run("SELECT * FROM temphist WHERE number = 5 ORDER BY id DESC")

#print(*[str(i) + '\n' for i in cursor.fetchall()])






