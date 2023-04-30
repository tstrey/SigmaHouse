
function registerHouse() {
  var prolonged;
  var sex = document.getElementsByName("sex");
  var qtcResult = document.getElementById("qtc");
  var prolongedResult = document.getElementById("prolonged");
  var resultsContainer = document.getElementById("qtc-results");
  var numRows = document.getElementById("num-rows");
  
  resultsContainer.style.display = "block";

 
  qtcResult.innerHTML = 'Initial setup';

 var server_data = [
  {"House_name": $('#house_id').val()},
  {"Sex": $('input[name="type"]:checked').val()}
 ];
 
 $.ajax({
   type: "POST",
   url: "/process_house",
   data: JSON.stringify(server_data),
   contentType: "application/json",
   dataType: 'json',
   success: function(result) {
     numRows.innerHTML = result.rows; 
   } 
 });
}

function clearIps() {
	$.ajax({
	  url: "/clearIps",
	  type: "GET",
	  dataType: "json",
	   success: function(result) {
		   console.log('clear')
			$("#ip_container").html('');
		}
	});
}

function updateIps() {
	$.ajax({
	  url: "/updateIps",
	  type: "GET",
	  dataType: "json",
	   success: function(result) {
		   $("#ip_container").html('');
		   for (i = 0; i < result.length; i++) { 
		   
				var newRow = $('<tr><td>' + result[i].ip + '</td>' +
				'<td></td>' +
				'<td><button class="edit-btn">Edit</button></td></tr>');
				$("#ip_container").append(newRow);
		   }
		}
	});
}


function registerIp() {
	$.ajax({
	  url: "/register",
	  type: "GET",
	  dataType: "json",
	   success: function(result) {
		   console.log('success')
		   if (result.already) {
			   alert('IP ' + result.already + ' already registered!')
		   } else {
			   var newClient = $('<tr><td>' + result.ip + '</td>' +
				'<td></td>' +
				'<td><button class="edit-btn">Edit</button></td></tr>');
				$("#ip_container").append(newClient);
		   }
			   

		} ,
		  error: function(jqXHR, textStatus, errorThrown) {
			console.error('problem'); // handle the error
		  }
	});
}


function listHouses() {

  var houses = document.getElementById("houses");
 
	 $.ajax({
	   type: "GET",
	   url: "/list_houses",
	   contentType: "application/json",
	   dataType: 'json',
	   success: function(result) {
		   var newClient = $('<tr><td>' + result.ip + '</td>' +
          '<td></td>' +
          '<td><button class="edit-btn">Edit</button></td></tr>');
			$("#ip_container").append(newClient);
		} 
	 });
}

