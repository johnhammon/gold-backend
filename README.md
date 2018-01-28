# Resource: budgets

# Attributes:

Attribute | Description
------------ | -------------
id | Primary key.
Category | Category of the budget item.
Budget | How much the user wants to spend.
Actual | How much the user actually spends.
Difference | Difference between how much the user wanted to spend and how much they spent.
Month | Which month the budget was for.
Notes | Notes about the budget item.
UserId | Foreign key to users.

# Schema:

CREATE TABLE budgets (id INTEGER PRIMARY KEY, Category varchar(255), Budget varchar(255), Actual varchar(255), Difference varchar(255), Month varchar(255), Notes varchar(255), UserId INTEGER);

# Resource: users

# Attributes:

Attribute | Description
------------ | -------------
id | Primary key.
FirstName | First name of the user.
LastName | Last Name of the user.
Email | Email of the user, used as username.
Password | Hashed password of user.

# Schema:

CREATE TABLE users (id INTEGER PRIMARY KEY, FirstName varchar(255), LastName varchar(255), Email varchar(255), Password varchar(255));

# REST endpoints:

Name | HTTP Method | Path
------------ | ------------- | -------------
List | GET | /budgets
Retrieve | GET | /budgets/budgetId
Create | POST | /budgets
Replace | PUT | /budgets/budgetId
Delete | DELETE | /budgets/budgetId
Create | POST | /users
Create | POST | /sessions

# Hashing
Uses Python BCrypt module to hash the passwords before storing them in the database and then uses the "verify" method provided by BCrypt to validate passwords in order to authenticate users and allow them access to their specific user data.
