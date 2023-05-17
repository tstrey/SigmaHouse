

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
				'<td>' + result[i].timestamp + '</td>' +
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
				'<td>' + result.timestamp + '</td>' +
				'<td><button class="edit-btn">Edit</button></td></tr>');
				$("#ip_container").append(newClient);
		   }
			   

		} ,
		  error: function(jqXHR, textStatus, errorThrown) {
			console.error('problem'); // handle the error
		  }
	});
}

function updateHouses() {
	$.ajax({
	  url: "/updateHouses",
	  type: "GET",
	  dataType: "json",
	   success: function(result) {
		   $("#house_container").html('');
		   for (i = 0; i < result.length; i++) {
				var newRow = $('<tr><td>' + result[i].ip + '</td>' +
				'<td class=' + result[i].display_alarm + '>' + result[i].timestamp + '</td>' +
				'<td><button class="edit-btn">Edit</button></td></tr>');
				$("#house_container").append(newRow);
		   }
		}
	});
}


