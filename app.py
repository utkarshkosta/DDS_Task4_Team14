import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
	""" create a database connection to the SQLite database
	    specified by the db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def new_user(conn):
	name = input("Enter the user name :")
	password = input("Enter the password :")
	entry = (name,password,)
	# query = "INSERT INTO USERS(username,password) VALUES("+name+","+password+")"
	query = "INSERT INTO USERS(username,password) VALUES(?,?)"
	cur = conn.cursor()
	cur.execute(query,entry)
	conn.commit()
	pass

def new_album(conn):
	select_all_tasks(conn, "ARTISTS")
	print("Select the artist for the album : ")
	artistid = input()
	print("Enter the album name : ")
	albumname = input()
	cur = conn.cursor()
	tup = (artistid, albumname)
	query = "INSERT INTO ALBUMS(artist_id, name) VALUES (?,?)"
	cur.execute(query,tup)
	conn.commit()
	pass

def new_artist(conn):
	name = input("Enter the artist name :")
	entry = (name,)
	query = "INSERT INTO ARTISTS(name) VALUES(?)"
	cur = conn.cursor()
	cur.execute(query,entry)
	conn.commit()
	pass

def new_playlist(conn,user_id):
	# select_all_tasks(conn, "USERS")
	plname = input("Enter the playlist name : ")
	tup = (user_id, plname)
	query = "INSERT INTO PLAYLISTS(user_id, name) VALUES (?,?)"
	cur = conn.cursor()
	cur.execute(query, tup)
	conn.commit()
	pass

def add_to_playlist(conn,user_id):
	print("printing the playlist table ...\n")
	cur = conn.cursor()

	# cur.execute("SELECT * FROM USERS where id=?",(tablename,))
	query = "SELECT * FROM PLAYLISTS WHERE user_id="+str(user_id)
	cur.execute(query)
	rows = cur.fetchall()
	for row in rows:
	    print(row)

	playlist_id = input("enter the playlist id :")


	print("printing songs ... \n")
	select_all_tasks(conn,"SONGS")
	song_id = input("Enter the song id ... ")


	entry =(playlist_id,song_id,)
	query = "INSERT INTO PLAYLISTS_SONGS(playlist_id,song_id) VALUES(?,?)"
	cur = conn.cursor()
	cur.execute(query,entry)
	conn.commit()

def new_song(conn):
	print("printing the albums table ...\n")
	select_all_tasks(conn,"ALBUMS")
	album_id = input("Enter the album id ... ")

	print("printing the artist table ...\n")
	select_all_tasks(conn,"ARTISTS")
	artist_id = input("Enter the artist id ...")

	name = input("enter name of song ")
	filename = input("enter file name ")

	query = "INSERT INTO SONGS(album_id, artist_id, name, filename) VALUES(?,?,?,?)"
	entry = (album_id,artist_id,name,filename)
	cur = conn.cursor()
	cur.execute(query,entry)
	conn.commit()

def select_all_tasks(conn,tablename):
	"""
	Query all rows in the tasks table
	:param conn: the Connection object
	:return:
	"""
	cur = conn.cursor()

	# cur.execute("SELECT * FROM USERS where id=?",(tablename,))
	query = "SELECT * FROM "+tablename
	cur.execute(query)

	rows = cur.fetchall()

	for row in rows:
	    print(row)

def select_all_playlist(conn,uid):
	cur = conn.cursor()

	# cur.execute("SELECT * FROM USERS where id=?",(tablename,))
	query = "SELECT * FROM PLAYLISTS WHERE user_id="+str(uid)
	cur.execute(query)

	rows = cur.fetchall()

	for row in rows:
	    print(row)


    
def init():
	path = "/home/utkarsh/DDS/music"
	conn = create_connection(path)
	cur = conn.cursor()
	un = input("Enter the username : ")
	pss = input("Enter the password : ")
	q = "SELECT * FROM USERS WHERE username = "+un
	cur.execute(q)
	rows = cur.fetchall()
	if(len(rows) == 0):
		print("Authentication failed! Please try again.")
		return

	uid = rows[0][0]
	check = rows[0][2]
	# print(check)
	# print(pss)
	# print(un)

	if(check != pss):
		print("Authentication failed! Please try again.")
		return

	while(1):
		if(un == '"admin"'):
			print("1.Add song\n2.Add artist\n3.Add album\n4.Display table\n5.Add user\n6.Exit")
			choice = input("Enter your choice : ")
			if(choice == '1'):
				new_song(conn)
			elif(choice == '2'):
				new_artist(conn)
			elif(choice == '3'):
				new_album(conn)
			elif(choice == '4'):
				tn = input("Enter table name : ")
				select_all_tasks(conn, tn)
			elif(choice == '5'):
				new_user(conn)
			else:
				break

		else:
			print("1.Create new playlist\n2.Add song to existing playlist\n3.show all my playlists\n4.Exit")
			choice = input("Enter your choice : ")
			if(choice == '1'):
				new_playlist(conn, uid)
			elif(choice == '2'):
				add_to_playlist(conn, uid)
			elif(choice == '3'):
				select_all_playlist(conn,uid)
			else:
				break

if __name__ == '__main__':
	init()