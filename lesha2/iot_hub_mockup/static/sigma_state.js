

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

function registerVirtualHouse() {
    $.ajax({
  url: "/smarthouse/v1/houses",
  type: "POST",
  contentType: "application/json",
  data: JSON.stringify({
    unique_id: "TBD",
    ip_address: "TBD",
    state: {
      alarm: true,
      led: {
        active: true,
        timestamp: 1622240800
      },
      wall_msg: "Hello, world!"
    }
  }),
  success: function(result) {
    // Handle the success response
    console.log('success')
		   if (result.already) {
			   alert('IP ' + result.already + ' already registered!')
		   } else {
			   var newClient = $('<tr><td>' + result.ip_address + '</td>' +
				'<td>' + result.timestamp + '</td>' +
				'<td><button class="edit-btn">Edit</button></td></tr>');
				$("#ip_container").append(newClient);
		   }
  },
  error: function(xhr, textStatus, errorThrown) {
    // Handle the error response
    console.error(xhr.responseJSON.detail);
  }
});
}

function updateHousesEmpty() {

}

function updateHouses() {
//{'unique_id': 'C8F09EB60250',
//'ip_address': '192.168.0.100',
//'state': {'led': {'timestamp': 0, 'active': False},
//'wall_msg': 'ID:C8F09EB60250', 'alarm': True, 'motion': {'motion_alarm': True}}, 'alarm': True}

	$.ajax({
	  url: "/smarthouse/v1/houses",
	  type: "GET",
	  dataType: "json",
	   success: function(result) {
		   $("#house_container").html('');
		   for (i = 0; i < result.length; i++) {
               var motion = result[i].state && result[i].state.motion && result[i].state.motion.motion_alarm ? 'Motion Alarm' : 'Off'
               var alarmClass = motion != 'Off' ? 'red' : 'green'
               var newRow = '<tr id="' + result[i].unique_id + '">'
                            + '<td>' + result[i].unique_id + '</td>'
                            + '<td class="' + alarmClass+ '">'  + motion + '</td>'
                            + '<td>'  + 'Off' +  '</td>'
                            + '<td>'  + 'Off' +  '</td>'
                            + '<td><button class="edit-btn" onclick="updateHouse(\''+result[i].unique_id+'\');">Edit</button></td></tr>';
    /*				var newRow = $('<tr id="' + result[i].unique_id + '"><td>' + result[i].unique_id + '</td>' +
                    '<td class=' + result[i].display_alarm + '>' + result[i].timestamp + '</td>' +
                    '<td><button class="edit-btn" onclick="updateHouse(\''+result[i].unique_id+'\');">Edit</button></td></tr>');*/
                    $("#house_container").append(newRow);
		   }
		}
	});
}

function updateHouse(unique_id) {
   $.ajax({
      url: "/smarthouse/v1/houses/" + unique_id ,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify({
        unique_id: unique_id,
        ip_address: "TBD",
        state: {
          alarm: true,
          led: {
            active: true,
            timestamp: 1622240800
          },
          wall_msg: "Hello, world!"
        }
      }),
      success: function(result) {
        // Handle the success response
        console.log('success')
            $("#" + result.unique_id).html('<td>' + result.unique_id + '</td>' +
				'<td class=' + result.display_alarm + '>' + result.timestamp + '</td>' +
				'<td><button class="edit-btn" onclick="updateHouse('+result.unique_id+');">Edit</button></td>')
      },
      error: function(xhr, textStatus, errorThrown) {
        // Handle the error response
        console.error(xhr.responseJSON.detail);
      }
    });
}


