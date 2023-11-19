
//Disponibilidad de turnos definido en el array dates
$(function() {
    var dates = ["2023-11-20", "2023-11-21", "2023-11-22"]; // Días de los turnos disponibles
   
    $("#datepicker").datepicker({
       dateFormat: 'yy-mm-dd',
       beforeShowDay: function(date) {
         var dateStr = jQuery.datepicker.formatDate('yy-mm-dd', date);
         return [dates.indexOf(dateStr) === -1]; // Disponibilidad de los turnos
       }
    });
   });