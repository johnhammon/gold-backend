"use strict";



var app = {


	init: function(initMessage){
		var self = this;

		if(initMessage)
			alert(initMessage);

		fetch('https://budgeter-app-by-cj.herokuapp.com/budgets', {credentials: 'include'}).then(function(response) {
		  return response.text().then(text => {
        return {
          data: text,
          status: response.status  
        }
    	}) 
		}).then(function(response) {
			if(response.status == 200) {
				let budget = JSON.parse(response.data.replace(/'/g, '"'));
				console.log(budget);
				document.querySelector("#budgetItemHldr").style.display = "";
				document.querySelector("#createBudgetItemContainer").style.display = "";
				self.createBudgetItem(budget);
			} else {
				var loginRegisterContainerEl = document.querySelector("#loginRegisterContainer");
				console.log(response.data);
				loginRegisterContainerEl.style.display = "";
				if(!initMessage) {
					loginRegisterContainerEl.querySelector("#loginButton").addEventListener("click", self.loginWasClicked);
					loginRegisterContainerEl.querySelector("#createUserButton").addEventListener("click", self.registerWasClicked);
				}
			}
		});

		if(!initMessage)
			document.querySelector("#createBudgetItem").addEventListener("click", self.initNewBudgetItem);

	},

	loginWasClicked: function(e) {
		self = this;
		var emailEl, passwordEl;
		emailEl = document.querySelector("#emailLogin");
		passwordEl = document.querySelector("#passwordLogin");
		if(emailEl.value && passwordEl.value) {
			fetch('https://budgeter-app-by-cj.herokuapp.com/sessions', {
				method: "POST",
				body: encodeURI("Email=" + emailEl.value + "&Password=" + passwordEl.value),
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				credentials: 'include'
			}).then(function(response) {
			  	return response.text().then(text => {
		        return {
		          data: text,
		          status: response.status  
		        }
		    	}) 
			}).then(function(response) {
				if(response.status == 200) {
					e.target.closest("#loginRegisterContainer").style.display = "none";
					window.app.init(response.data);
				} else {
					alert(response.data)
				}
			});
		} else {
			alert("Please fill out all fields before submitting.")
		}
	},

	registerWasClicked: function(e) {
		var self = this;
		var firstNameEl, lastNameEl, emailEl, passwordEl;
		firstNameEl = document.querySelector("#firstName");
		lastNameEl = document.querySelector("#lastName");
		emailEl = document.querySelector("#emailRegister");
		passwordEl = document.querySelector("#passwordRegister");
		if(emailEl.value && passwordEl.value && firstNameEl.value && lastNameEl.value) {
			fetch('https://budgeter-app-by-cj.herokuapp.com/users', {
				method: "POST",
				body: encodeURI("Email=" + emailEl.value + "&Password=" + passwordEl.value +
												"&FirstName=" + firstNameEl.value + "&LastName=" + lastNameEl.value),
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				credentials: 'include'
			}).then(function(response) {
			  	return response.text().then(text => {
		        return {
		          data: text,
		          status: response.status  
		        }
		    	}) 
			}).then(function(response) {
				if(response.status == 201) {
					e.target.closest("#loginRegisterContainer").style.display = "none";
					window.app.init(response.data);
				} else {
					alert(response.data);
				}
			});
		} else {
			alert("Please fill out all fields before submitting.")
		}
	},

	initNewBudgetItem: function(e) {
		var self = window.app;
		console.log("hello");
		var category, budget, actual, difference, notes, month, categoryEl, budgetEl, actualEl, differenceEl, notesEl, monthEl;
		categoryEl = document.querySelector("#category");
		budgetEl = document.querySelector("#budget");
		actualEl = document.querySelector("#actual");
		differenceEl = document.querySelector("#difference");
		notesEl = document.querySelector("#notes");
		monthEl = document.querySelector("#month");

		category = categoryEl.value;
		categoryEl.value = "";

		budget = budgetEl.value;
		budgetEl.value = "";

		actual = actualEl.value;
		actualEl.value = "";

		difference = differenceEl.value;
		differenceEl.value = "";

		notes = notesEl.value;
		notesEl.value = "";

		month = monthEl.value;
		monthEl.value = "";

		fetch('https://budgeter-app-by-cj.herokuapp.com/budgets', {
			method: "POST",
			body: encodeURI("Category=" + category + "&Budget=" + budget +
			  				"&Actual=" + actual + "&Difference=" + difference + "&Notes=" + notes
			  				 + "&Month=" + month),
			headers: {
				"Content-Type": "application/x-www-form-urlencoded"
			},
			credentials: 'include'
		}).then(function(response) {
		  	return response.text().then(text => {
	        return {
	          data: text,
	          status: response.status  
	        }
	    	})
		}).then(function(response) {
			console.log(response.data);
			if(response.status == 201) {
				self.createBudgetItem([{
					id: response.data,
					Category: category,
					Budget: budget,
					Actual: actual,
					Difference: difference,
					Month: month,
					Notes: notes
				}]);
			} else {
				alert(response.data);
			}
		});
	},

	editBudgetRow: function(e) {
		var budgetId, category, budget, actual, difference, notes, month, categoryEl, budgetEl, actualEl, differenceEl, notesEl, monthEl, saveButton, tableRow, tableRowChildren, tempInput;

		tableRow = e.target.closest(".tableRow");

		budgetId = tableRow.attributes["data-id"].value

		tableRowChildren = tableRow.querySelectorAll(".tableCell");

		categoryEl = document.createElement("input");
		categoryEl.value = tableRowChildren[0].innerText;

		budgetEl = document.createElement("input");
		budgetEl.value = tableRowChildren[1].innerText;

		actualEl = document.createElement("input");
		actualEl.value = tableRowChildren[2].innerText;

		differenceEl = document.createElement("input");
		differenceEl.value = tableRowChildren[3].innerText;

		monthEl = document.createElement("input");
		monthEl.value = tableRowChildren[4].innerText;

		notesEl = document.createElement("input");
		notesEl.value = tableRowChildren[5].innerText;

		console.dir(tableRowChildren);
		for (var i =  0; i < tableRowChildren.length - 1; i++)
			tableRowChildren[i].innerHTML = "";

		console.dir(tableRowChildren);

		tableRowChildren[0].appendChild(categoryEl);
		tableRowChildren[1].appendChild(budgetEl);
		tableRowChildren[2].appendChild(actualEl);
		tableRowChildren[3].appendChild(differenceEl);
		tableRowChildren[4].appendChild(monthEl);
		tableRowChildren[5].appendChild(notesEl);
		tableRowChildren[6].children[0].style.display = "none";
		tableRowChildren[6].children[1].style.display = "none";
		tableRow.querySelector(".fa-floppy-o").style.display = "inline";

		function saveButtonWasClicked(e) {
			category = categoryEl.value;
			budget = budgetEl.value;
			actual = actualEl.value;
			difference = differenceEl.value;
			notes = notesEl.value;
			month = monthEl.value;

			fetch('https://budgeter-app-by-cj.herokuapp.com/budgets/' + budgetId, {
				method: "PUT",
				body: encodeURI("Category=" + category + "&Budget=" + budget +
					  				"&Actual=" + actual + "&Difference=" + difference + "&Notes=" + notes
					  				 + "&Month=" + month),
				headers: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				credentials: 'include'
			}).then(function(response) {
				return response.text().then(text => {
	        return {
	          data: text,
	          status: response.status  
	        }
	    	})
			}).then(function(response) {
				console.log(response.data);
				if(response.status == 200) {
					tableRowChildren[0].innerHTML = categoryEl.value;
					tableRowChildren[1].innerHTML = budgetEl.value;
					tableRowChildren[2].innerHTML = actualEl.value;
					tableRowChildren[3].innerHTML = differenceEl.value;
					tableRowChildren[4].innerHTML = monthEl.value;
					tableRowChildren[5].innerHTML = notesEl.value;
					tableRowChildren[6].children[0].style.display = "inline";
					tableRowChildren[6].children[1].style.display = "inline";
					tableRow.querySelector(".fa-floppy-o").style.display = "none";
				} else {
					alert(response.data);
				}
			});
		}
		tableRow.querySelector(".fa-floppy-o").outerHTML = tableRow.querySelector(".fa-floppy-o").outerHTML;
		tableRow.querySelector(".fa-floppy-o").addEventListener("click", saveButtonWasClicked);

	},

	deleteBudgetRow: function(e) {
		var budgetId, tableRow;

		tableRow = e.target.closest(".tableRow");

		budgetId = tableRow.attributes["data-id"].value

		if(confirm("Are you sure you want to delete this budget item?")) {
			fetch('https://budgeter-app-by-cj.herokuapp.com/budgets/' + budgetId, {
				method: "DELETE",
				credentials: 'include'
			}).then(function(response) {
				return response.text().then(text => {
	        return {
	          data: text,
	          status: response.status  
	        }
	    	})
			}).then(function(response) {
				if(response.status == 200) {
					console.log(response.data);
				} else {
					alert(response.data);
				}
			});
			tableRow.parentElement.removeChild(tableRow);
		}
	},

	createBudgetItem: function(budgetData) {
		var self = this;
		var budgetItemHldr, tableRow, tempTableRow, tableCell, tempTableCell, pencil, trash, tempPencil, tempTrash, save, tempSave;
		budgetItemHldr = document.querySelector("#budgetItemHldr");
		tableRow = document.createElement("div");
		tableRow.className = "tableRow";
		tableCell = document.createElement("div");
		tableCell.className = "tableCell";
		pencil = document.createElement("i");
		pencil.className = "fa fa-pencil";
		trash = document.createElement("i");
		trash.className = "fa fa-trash-o";
		save = document.createElement("i");
		save.className = "fa fa-floppy-o";
		save.style.display = "none";
		for (var i = budgetData.length - 1; i >= 0; i--) {
			tempTableRow = tableRow.cloneNode(true);
			tempTableCell = tableCell.cloneNode(true);
			tempPencil = pencil.cloneNode(true);
			tempTrash = trash.cloneNode(true);
			tempSave = save.cloneNode(true);
			tempPencil.addEventListener("click", self.editBudgetRow);
			tempTrash.addEventListener("click", self.deleteBudgetRow);
			tempPencil.style.marginRight = "3px";
			tempTableCell.appendChild(tempPencil);
			tempTableCell.appendChild(tempTrash);
			tempTableCell.appendChild(tempSave);
			tempTableRow.setAttribute("data-id", budgetData[i].id)
			tempTableRow.innerHTML = "<div class='tableCell'>" + budgetData[i].Category + "</div>" +
			"<div class='tableCell'>" + budgetData[i].Budget + "</div>" +
			"<div class='tableCell'>" + budgetData[i].Actual + "</div>" +
			"<div class='tableCell'>" + budgetData[i].Difference + "</div>" +
			"<div class='tableCell'>" + budgetData[i].Month + "</div>" +
			"<div class='tableCell'>" + budgetData[i].Notes + "</div>";
			;
			tempTableRow.appendChild(tempTableCell);
			budgetItemHldr.appendChild(tempTableRow);
		}
	}

}

// Initiate app
app.init();