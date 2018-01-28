import os
import psycopg2
import psycopg2.extras
import urllib.parse

class BudgetsDB:

	def __init__(self):
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

		self.connection = psycopg2.connect(
			cursor_factory=psycopg2.extras.RealDictCursor,
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)

		self.cursor = self.connection.cursor()

	def __del__(self):
		self.connection.close()

	def createUsersTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, FirstName VARCHAR(255), LastName VARCHAR(255), Email VARCHAR(255), Password VARCHAR(255))")
		self.connection.commit()

	def createUser(self, firstName, lastName, email, password):
		sql = "INSERT INTO users (FirstName, LastName, Email, Password) VALUES (%s,%s,%s,%s)"
		vals = (firstName, lastName, email, password)
		self.cursor.execute(sql, vals)
		self.connection.commit()
		return self.cursor.lastrowid

	def checkUserEmail(self, email):
		sql = "SELECT * FROM users WHERE users.email = %s"
		self.cursor.execute(sql,(email,))
		rows = self.cursor.fetchall()
		return rows

	def createBudgetsTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS budgets (id SERIAL PRIMARY KEY, Category VARCHAR(255), Budget VARCHAR(255), Actual VARCHAR(255), Difference VARCHAR(255), Month VARCHAR(255), Notes VARCHAR(255), UserId INTEGER)")
		self.connection.commit()

	def createBudget(self, category, budget, actual, difference, month, notes, user):
		sql = "INSERT INTO budgets (Category, Budget, Actual, Difference, Month, Notes, UserId) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		vals = (category, budget, actual, difference, month, notes, user)
		self.cursor.execute(sql, vals)
		self.connection.commit()
		return self.cursor.lastrowid

	def updateBudget(self, id, category, budget, actual, difference, month, notes, user):
		sql = "UPDATE budgets SET Category = %s, Budget = %s, Actual = %s, Difference = %s, Month = %s, Notes = %s, UserId = %s WHERE id = %s"
		vals = (category, budget, actual, difference, month, notes, user, id)
		self.cursor.execute(sql, vals)
		self.connection.commit()
		return

	def getBudgets(self, user):
		sql = "SELECT * FROM budgets WHERE UserId = %s"
		self.cursor.execute(sql,(user,))
		rows = self.cursor.fetchall()
		return rows

	def getBudget(self, id, user):
		sql = "SELECT * FROM budgets WHERE budgets.id = %s AND UserId = %s"
		vals = (id, user)
		self.cursor.execute(sql, vals)
		rows = self.cursor.fetchall()
		return rows

	def deleteBudget(self, id, user):
		sql = "DELETE FROM budgets WHERE budgets.id = %s AND UserId = %s"
		vals = (id, user)
		self.cursor.execute(sql, vals)
		self.connection.commit()
		return