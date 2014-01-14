$(document).ready(function() {

$("form").submit(function(event) {

 //Get and format the "Seed" URL
 seedURL = $("#formText").val();
 if (!seedURL) {
  showRibbon("Enter a web address!", "red", "body");
  return false;
 } else if (!(seedURL.substr(0,7)=="http://" || seedURL.substr(0,7)=="https://")) {
  seedURL = "http://"+seedURL;
 } 

 //Apply any changes to the form that were made.
 $("#formText").val(seedURL);

 //Test if the URL actually exists on the client-side.
 showRibbon("Loading!", "orange", "body", false);

});

});
