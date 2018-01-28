from http.server import BaseHTTPRequestHandler, HTTPServer
from budgets_db import BudgetsDB
import urllib.parse
import json
import sys
from session_store import SessionStore
from http import cookies
from passlib.hash import bcrypt

gSessionStore = SessionStore()

# list resource
class MyHandler(BaseHTTPRequestHandler) :
	def do_GET(self):
		self.load_session()

		if self.path == "/budgets":
			if "userId" in self.session:
				self.handleBudgetList()
			else:
				self.handle401()
		elif self.path == "/users":
			self.handle401()
		elif self.path.split("/")[1] == "budgets":
			if "userId" in self.session:
				self.handleBudgetRetrieve()
			else:
				self.handle401()
		else:
			self.handle404()

	def do_DELETE(self):
		self.load_session()
		if self.path.split("/")[1] == "budgets":
			if "userId" in self.session:
				self.handleDeleteBudget()
			else:
				self.handle401()
		else:
			self.handle404()

	def do_OPTIONS(self):
		self.load_session()
		self.send_response(200)
		self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		self.send_header('Access-Control-Allow-Headers', 'Content-Type')
		self.end_headers()

	def do_POST(self):
		self.load_session()
		if self.path == "/budgets":
			if "userId" in self.session:
				self.handleBudgetCreate()
			else:
				self.handle401()
		elif self.path == "/users":
			self.handleCreateUser()
		elif self.path.split("/")[1] == "sessions":
			self.handleLogin()
		else:
			self.handle404()

	def do_PUT(self):
		self.load_session()
		if self.path.split("/")[1] == "budgets":
			if "userId" in self.session:
				self.handleBudgetUpdate()
			else:
				self.handle401()
		else:
			self.handle404()

	def end_headers(self):
		self.send_cookie()
		self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
		self.send_header('Access-Control-Allow-Credentials', 'true')
		BaseHTTPRequestHandler.end_headers(self)

	def handleLogin(self):
		db = BudgetsDB()
		length = int(self.headers["Content-length"])
		body = self.rfile.read(length).decode("utf-8")
		postData = dict(urllib.parse.parse_qsl(body))

		email = postData["Email"]
		password = postData["Password"]

		
		arr = db.checkUserEmail(email)

		if len(arr) > 0:
			print(arr)
			arr = arr[0]
			userData = {
				'id': arr['id'],
				'FirstName': arr['firstname'],
				'LastName': arr['lastname'],
				'Email': arr['email'],
				'Password': arr['password']
			}

			if bcrypt.verify(password, userData['Password']): 
				self.session["userId"] = userData["id"]
				self.send_response(200)
				self.send_header("Content-Type", "text/plain")
				self.end_headers()
				self.wfile.write(bytes(str(userData["FirstName"]) + " " + str(userData["LastName"]) + " logged in successfully.", "utf-8"))
			else:
				self.handle401()
		else:
			self.handle401()

	def handleCreateUser(self):
		db = BudgetsDB()
		length = int(self.headers["Content-length"])
		body = self.rfile.read(length).decode("utf-8")
		postData = dict(urllib.parse.parse_qsl(body))

		firstName = postData["FirstName"]
		lastName = postData["LastName"]
		email = postData["Email"]
		password = bcrypt.encrypt(postData["Password"])

		if len(db.checkUserEmail(email)) == 0:
			rowId = db.createUser(firstName, lastName, email, password)

			self.session["userId"] = rowId

			self.send_response(201)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write(bytes(str(firstName) + str(lastName) + "was registered successfully.", "utf-8"))
		else:
			self.send_response(422)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write(bytes("This email is already registered.", "utf-8"))

	def handleBudgetUpdate(self):
		db = BudgetsDB()
		print(self.path.split("/")[2])
		print(db.getBudget(self.path.split("/")[2], self.session["userId"]))
		if len(db.getBudget(self.path.split("/")[2], self.session["userId"])) > 0:
			length = int(self.headers["Content-length"])
			body = self.rfile.read(length).decode("utf-8")
			postData = dict(urllib.parse.parse_qsl(body))

			category = postData["Category"]
			budget = postData["Budget"]
			actual = postData["Actual"]
			difference = postData["Difference"]
			month = postData["Month"]
			notes = postData["Notes"]

			print(self.path.split("/")[2])
			db.updateBudget(self.path.split("/")[2], category, budget, actual, difference, month, notes, self.session["userId"])

			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes((postData["Category"] + " changed."), "utf-8"))
		else:
			self.handle404()

	def handleBudgetCreate(self):
		db = BudgetsDB()
		length = int(self.headers["Content-length"])
		body = self.rfile.read(length).decode("utf-8")
		postData = dict(urllib.parse.parse_qsl(body))

		category = postData["Category"]
		budget = postData["Budget"]
		actual = postData["Actual"]
		difference = postData["Difference"]
		month = postData["Month"]
		notes = postData["Notes"]

		rowId = db.createBudget(category, budget, actual, difference, month, notes, self.session["userId"])

		self.send_response(201)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(bytes(str(rowId), "utf-8"))

	def handleBudgetList(self):
		db = BudgetsDB()
		data = db.getBudgets(self.session["userId"])
		dictData = []
		for arr in data:
			dictData.append({
				'id': arr['id'],
				'Category': arr['category'],
				'Budget': arr['budget'],
				'Actual': arr['actual'],
				'Difference': arr['difference'],
				'Month': arr['month'],
				'Notes': arr['notes'],
				'UserId': arr['userid']
			})
		json_string = json.dumps(dictData)

		self.send_response(200)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		self.wfile.write(bytes(json_string, "utf-8"))

	def handle404(self):
		self.send_response(404)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(bytes("Not Found.", "utf-8"))

	def handle401(self):
		self.send_response(401)
		self.send_header("Content-Type", "text/plain")
		self.end_headers()
		self.wfile.write(bytes("You are not authorized for this request.", "utf-8"))

	def handleBudgetRetrieve(self):
		db = BudgetsDB()
		if len(db.getBudget(self.path.split("/")[2], self.session["userId"])) > 0:
			arr = db.getBudget(self.path.split("/")[2], self.session["userId"])[0]

			json_string = json.dumps({
				'id': arr['id'],
				'Category': arr['category'],
				'Budget': arr['budget'],
				'Actual': arr['actual'],
				'Difference': arr['difference'],
				'Month': arr['month'],
				'Notes': arr['notes']
			})

			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json_string, "utf-8"))
		else:
			self.handle404()

	def handleDeleteBudget(self):
		db = BudgetsDB()
		if len(db.getBudget(self.path.split("/")[2], self.session["userId"])) > 0:
			db.deleteBudget(self.path.split("/")[2], self.session["userId"])

			self.send_response(200)
			self.send_header("Content-Type", "text/plain")
			self.end_headers()
			self.wfile.write(bytes("Deleted " + self.path.split("/")[2], "utf-8"))
		else:
			self.handle404()

	def handleSessionCreate(self):
		sessionId = gSessionStore.createSession()
		self.cookie["sessionId"] = sessionId
		self.session = gSessionStore.getSession(sessionId)

	def load_session(self):
		self.load_cookie()
		if "sessionId" in self.cookie:
			sessionId = self.cookie["sessionId"].value
			sessionData = gSessionStore.getSession(sessionId)
			if sessionData is not None:
				self.session = sessionData
			else:
				self.handleSessionCreate()
		else:
			self.handleSessionCreate()

	def load_cookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

	def send_cookie(self):
		for attribute in self.cookie.values():
			self.send_header("Set-Cookie", attribute.OutputString())



def main():
    db = BudgetsDB()
    db.createUsersTable()
    db.createBudgetsTable()
    db = None # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()

main()
