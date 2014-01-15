$(document).ready(function() {
//Variable Setup.
var errorColor = "#FF9F80";
var waitColor = "#FFDF80";
var successColor = "#9FFF80";


$("form").submit(function(event) {

 //Get and format the "Seed" URL
 seedURL = $("#formText").val();
 if (!seedURL) {
  showRibbon("Enter a web address!", errorColor, "body");
  return false;
 } else if (!(seedURL.substr(0,7)=="http://" || seedURL.substr(0,7)=="https://")) {
  seedURL = "http://"+seedURL;
 } 

 //Apply any changes to the form that were made.
 $("#formText").val(seedURL);

 //Test if the URL actually exists on the client-side.
 showRibbon("Loading!", waitColor, "body", false);
 $("#formLoadingWheel").show()
 $("#formSubmit").remove()

});

//Setup for Tooltips.
$(".formField").hover(
 function() {
  $("#formTitleContainer").html($(this).attr("title"));
  $(this).attr("title","");
 }, function() {
  $(this).attr("title", $("#formTitleContainer").html());
  $("#formTitleContainer").empty();
 }
);

});
