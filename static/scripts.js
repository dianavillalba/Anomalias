var site = {
    init: function() {
        // Define isValidDateFormat and other functions here
        function isValidDateFormat(dateString) {
            // Regular expression to match the format "YYYY/mm/dd"
            var regex = /^\d{4}\/\d{2}\/\d{2}$/;
            return regex.test(dateString);
        }

        function isValidPositiveInteger(input) {
            // Check if the input is a non-empty string
            if (typeof input !== 'string' || input.trim() === '') {
                return false;
            }
        
            // Use parseInt() to attempt conversion to an integer
            // If parseInt() returns NaN or if the input contains non-numeric characters, it's not a valid integer
            var integerValue = parseInt(input);
            if (isNaN(integerValue) || !isFinite(input)) {
                return false;
            }
        
            // Check if the integer value is greater than zero
            return integerValue > 0;
        }



        // Form submission handler
        $('#form').submit(function(event) {
            // Clear previous error messages
            $('.error').html('');
            // alert("hello");

            // Perform validation
            var fecha_inicial = $('#fecha_inicial').val().trim();
            if (fecha_inicial !== '' && !isValidDateFormat(fecha_inicial)) {
                $('.error').html('Fecha Inicial debe estar en formato YYYY/MM/DD');
                event.preventDefault();
                return false;
            }

            var fecha_final = $('#fecha_final').val().trim();
            if (fecha_final !== '' && !isValidDateFormat(fecha_final)) {
                $('.error').html('Fecha Final debe estar en formato YYYY/MM/DD');
                event.preventDefault();
                return false;
            }

            // Validate date range only if both dates are not empty and valid
            if (fecha_inicial!== '' && fecha_final!== '') {
                var fecha_inicial_number = parseFloat(fecha_inicial.replace(/\//g, ''));
                var fecha_final_number = parseFloat(fecha_final.replace(/\//g, ''));
                if (fecha_final_number < fecha_inicial_number) {
                    $('.error').html('Fecha Final debe ser mayor que la fecha inicial');
                    event.preventDefault();
                    return false;
                }
            }
            else {
                $('.error').html('Las fechas son requeridas');
                    event.preventDefault();
                    return false;
            }

            
        });
    }
};

$(document).ready(function() {
    site.init(); // Initialize scripts
});
