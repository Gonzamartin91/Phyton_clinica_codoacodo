
//Disponibilidad de turnos definido en el array dates
$(function() {
    var dates = ["2021-05-15", "2021-05-16", "2021-05-17", "2021-05-18", "2021-05-19"]; // Días de los turnos disponibles
   
    $("#datepicker").datepicker({
       dateFormat: 'yy-mm-dd',
       beforeShowDay: function(date) {
         var dateStr = jQuery.datepicker.formatDate('yy-mm-dd', date);
         return [dates.indexOf(dateStr) === -1]; // Disponibilidad de los turnos
       }
    });
   });