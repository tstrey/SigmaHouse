
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


function listHouses() {

  var houses = document.getElementById("houses");
 
 $.ajax({
   type: "GET",
   url: "/list_houses",
   contentType: "application/json",
   dataType: 'json',
   success: function(result) {
     houses.innerHTML = result; 
   } 
 });
}

