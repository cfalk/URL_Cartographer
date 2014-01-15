//############   Ribbons:   #############################################
window.showRibbon = function(message, color, frame, timeout) {
 //Assume that the ribbon should time out if not specified.
 timeout = timeout !== undefined ? timeout : true

 //Remove any ribbons that currently exist.
 $(".ribbonMessage").remove();

 $(frame).append(
  "<div class=\"ribbonMessage\" style=\"background-color:" + color +
   ";\">" + message + "</div>"
 );
 if (timeout==true) {
  setTimeout(function() {
   $(frame).children(".ribbonMessage").fadeOut(1000, function()
   {
    $(".ribbonMessage").remove();
   });

  },500+18*message.length);
 }
}

