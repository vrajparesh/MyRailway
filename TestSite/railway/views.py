from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection

import MySQLdb

# Create your views here.

def home(request):
	'''
		render home.html
	'''
	return HttpResponse(render(request, "home.html"))

@login_required
def traininfo(request):
	'''
		This method can be called iff user is signed in
		Case 1: GET request
			render 	traininfo.html
		Case 2: POST request
			check for validation of inputs
			if valid render modified traininfo.html
	'''
	if request.method == "POST":
		trainno = request.POST.get('trainno')
		if trainno == "" or 'e' in trainno:
			return HttpResponse("invalid train number")		
		trainno = int(trainno)
		c = connection.cursor()
		c.execute('SELECT * FROM Train WHERE Train_No = %d' %(trainno))
		train = c.fetchone()
		c.execute('SELECT * FROM Stoppage as s,Station as st WHERE (Train_No = %d and s.Station_Code = st.Station_Code) order by Arrival_Time' %(trainno))
		#from stoppage as s,station as st where ( Train_No = '12215' and s.Station_Code = st.Station_Code) order by Arrival_Time
		stoppage = c.fetchall()

		c.execute('SELECT * FROM Station')
		scode = {}
		for row in c.fetchall():
			scode[str(row[0])] = str(row[1])
		station = {}
		for row in stoppage:
			station[str(row[1])] = scode[str(row[1])]

		context = {"info":train, "stop":stoppage, "station":station, "show":True}
		if train == None:
			return HttpResponse(render(request, "404.html",context))
		else:
			return HttpResponse(render(request, "traininfo.html", context))
	else:
		return HttpResponse(render(request, "traininfo.html", {"show":False,}))

@login_required
def findtrains(request):
	'''
		This method can be called iff user is signed in
		Case 1: GET request
			render 	findtrains.html
		Case 2: POST request
			check for validation of inputs
			if valid render modified findtrains.html
	'''
	if request.method == "POST":
		fstation = request.POST.get('fstation')
		sstation = request.POST.get('sstation')

		if len(fstation) == 0 or len(sstation) == 0:
			return HttpResponse("station code can't be empty")

		for c in fstation:
			if c == " ":
				return HttpResponse("space is not allowed")

		for c in sstation:
			if c == " ":
				return HttpResponse("space is not allowed")

		if fstation == sstation:
			return HttpResponse("station code must be different")

		c = connection.cursor()
		c.execute('''select a.Train_No from Stoppage as a join Stoppage as b on a.Train_No = b.Train_No 
			         where a.Station_Code = "%s" and b.Station_Code = "%s" ''' %(fstation, sstation))
		
		trains = c.fetchall()

		if len(trains) == 0:
			return HttpResponse(render(request,'404.html'))

		context = {"trains":trains, "show":True}

		return HttpResponse(render(request, "findtrains.html", context))
		
	else:
		return HttpResponse(render(request, "findtrains.html", {"show":False}))	

@login_required
def ticket(request):
	'''
		This method can be called iff user is signed in
		Case 1: GET request
			render 	ticket.html
		Case 2: POST request
			check for validation of inputs
			if valid render modified ticket.html
	'''
	if request.method == "POST":
		tnumber = request.POST.get('tnumber')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		gender = request.POST.get('gender')
		age = request.POST.get('age')
		tclass = request.POST.get('tclass')
		number = request.POST.get('number')

		c = connection.cursor()
		c.execute("SELECT * FROM Train where Train_No = '%s' " %(tnumber))

		train = c.fetchall()

		if len(train) == 0:
			return HttpResponse("<h3>Incorrect Train Number.</h3> Press back on your browser to continue to fill form. ")

		train = train[0]

		alpha = list(map(chr, range(97, 123)))

		invalid = False
		
		if len(fname) == 0:
			invalid = True

		for c in fname:
			if c not in alpha:
				invalid = True
				break	

		if invalid:
			return HttpResponse("<h3>Invalid fname, characters allowed [a-z].</h3> Press back on your browser to continue to fill form.")

		invalid = False
		
		if len(lname) == 0:
			invalid = True

		for c in lname:
			if c not in alpha:
				invalid = True
				break

		if invalid:
			return HttpResponse("Invalid lname, characters allowed [a-z].</h3> Press back on your browser to continue to fill form.")

		if age == "" or 'e' in age or int(age) > 100:
			return HttpResponse("Invalid age. Press back on your browser to continue to fill form.")

		num = list(map(chr, range(48, 58)))
		invalid = False

		if len(number) != 10:
			invalid = True
		for c in number:
			if c not in num:
				invalid = True
				break

		if invalid:
			return HttpResponse("<h3>Invalid phone number</h3> Press back on your browser to continue to fill form.")

		gender = gender[0]
		if str(tclass) == "sleeper" and int(train[2]) <= 0:
			return HttpResponse("Seat unavailable in sleeper class. Press back on your browser to continue to fill form.")
		if str(tclass) == "first class ac" and int(train[3]) <= 0:
			return HttpResponse("Seat unavailable in first class ac. Press back on your browser to continue to fill form.")
		if str(tclass) == "second class ac" and int(train[4]) <= 0:
			return HttpResponse("Seat unavailable in second class ac. Press back on your browser to continue to fill form.")
		if str(tclass) == "third class ac" and int(train[5]) <= 0:
			return HttpResponse("Seat unavailable in third class ac. Press back on your browser to continue to fill form.")

		c = connection.cursor()		
		c.execute("SELECT * FROM Ticket")
		maximum = 0
		for row in c.fetchall():
			maximum = max(maximum, int(row[0]))

		ticketno = maximum + 1
		import datetime
		now = datetime.datetime.now()
		now = str(now)
		jdate = (now.split())[0]
		
		c.execute('''INSERT INTO Ticket VALUES("%s", "%s", "%s", "%s")
					 ''' %(ticketno, tnumber, jdate, request.user))

		c.execute('''INSERT INTO Passenger(First_name, Last_name, Gender, Phone_No,
			         Ticket_No, Age, Class) VALUES
			         ("%s", "%s", "%s", "%s", "%s", "%s", "%s")
			         ''' %(fname, lname, gender, number, ticketno, age, tclass))
        
		if str(tclass) == "sleeper":
			c.execute('''UPDATE Train set Seat_Sleeper = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[2])-1, tnumber))
		if str(tclass) == "first class ac":
			c.execute('''UPDATE Train set Seat_First_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[3])-1, tnumber))
		if str(tclass) == "second class ac":
			c.execute('''UPDATE Train set Seat_Second_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[4])-1, tnumber))
		if str(tclass) == "third class ac":
			c.execute('''UPDATE Train set Seat_Third_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[5])-1, tnumber))			

		return HttpResponse(render(request, "ticket.html", {"show":True}))
	else:
		return HttpResponse(render(request, "ticket.html", {"show":False}))	

def signup(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		address = request.POST.get('address')
		fnumber = request.POST.get('fnumber')
		snumber = request.POST.get('snumber')

		num = list(map(chr, range(48, 58)))
		alphanum = list(map(chr, range(97, 123))) + num
		

		invalid = False
		
		if len(username) == 0:
			invalid = True

		for c in username:
			if c not in alphanum:
				invalid = True
				break

		if invalid:
			return HttpResponse("<h3>Invalid username, characters allowed [a-z] and [0-9]. <h3> Press back on your browser to continue to fill form ")


		invalid = False

		if len(password) == 0:
			invalid = True

		for c in password:
			if c == " ":
				invalid = True
				break

		if invalid:
			return HttpResponse("<h3>Spaces are not allowed in password.</h3> Press back on your browser to continue to fill form")
		
		if len(address) == address.count(' '):
			return HttpResponse("<h3> Invalid address. <h3> Press back on your browser to continue to fill form")

		
		invalidf, invalids = False, False	

		if len(fnumber) != 10:
			invalidf = True
		for c in fnumber:
			if c not in num:
				invalidf = True
				break

		if len(snumber) != 10:
			invalids = True
		for c in snumber:
			if c not in num:
				invalids = True
				break

		if invalidf and invalids:
			return HttpResponse("<h3>Atleast one contact must be valid.</h3> Press back on your browser to continue to fill form")

		try:
			user = User.objects.create_user(username, None, password)
			c = connection.cursor()
			c.execute('INSERT INTO Account VALUES("%s", "%s", "%s", "%s")' %(username, password, email, address))
			if not invalidf:	
				c.execute('INSERT INTO Contact VALUES("%s", "%s")' %(username, fnumber))
			if not invalids:	
				c.execute('INSERT INTO Contact VALUES("%s", "%s")' %(username, snumber))
			
			return HttpResponse("<h3>Signup Successful!</h3> Go Back to Login")

		except Exception as e:
			print(e)
		finally:
			c.close()
	else:
		return HttpResponse(render(request, "form_signup.html"))

def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username = username, password = password)		

		if user:
			login(request, user)
			return HttpResponse(render(request, "login_success.html"))
			
		else:
			return HttpResponse("Invalid Credentials. Press back on your browser to go back to Login")

		'''
		try:
			c = connection.cursor()
			c.execute('SELECT * FROM Account WHERE Username = "%s" and Password = "%s"' %(username, password))
			table = c.fetchall()
			if len(table) != 1:
				return HttpResponse("invalid credentials")
			return HttpResponse("login successful! cheers")

		except Exception as e:
			print e
		finally:
			c.close()
		'''	

	return HttpResponse(render(request, "form_login.html"))

@login_required
def logout_user(request):	
	logout(request)	
	return HttpResponseRedirect("/home/")