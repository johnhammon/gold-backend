import base64, os

class SessionStore:

	def __init__(self):
		self.sessionStore = {}
		return

	def generateSessionId(self):
		randNum = os.urandom(32)
		randString = base64.b64encode(randNum).decode("utf-8")
		return randString

	def createSession(self):
		sessionId = self.generateSessionId()
		self.sessionStore[sessionId] = {}
		return sessionId

	def getSession(self, sessionId):
		if sessionId in self.sessionStore:
			return self.sessionStore[sessionId]
		else:
			return None