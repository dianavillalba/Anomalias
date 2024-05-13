function confirmarSeleccion() {
    if (sentimientoSeleccionado) {
     
      enviarDatosAPI(sentimientoSeleccionado);

      window.location.href = '/genero';
    } else {
      alert('Selecciona un sentimiento antes de confirmar.');
    }
  }
  
function enviarDatosAPI(sentimiento) {
    // URL de la REST API donde enviar el sentimiento
    var urlAPI = 'http://52.3.220.233:5000/api/enviar-sentimiento';
  
    // Objeto de opciones para la solicitud
    var opciones = {
      method: 'POST', // Método HTTP para enviar datos
      headers: {
        'Content-Type': 'application/json', // Tipo de contenido JSON
      },
      body: JSON.stringify({ sentimiento: sentimiento }), // Convertir a JSON y enviar en el cuerpo
    };
  
    // Realizar la solicitud HTTP
    fetch(urlAPI, opciones)
      .then(function (respuesta) {
        if (!respuesta.ok) {
          throw new Error('Error en la solicitud.');
        }
        return respuesta.json();
      })
      .then(function (datos) {
        // Aquí puedes manejar la respuesta de la API si es necesario
        console.log('Respuesta de la API:', datos);
      })
      .catch(function (error) {
        console.error('Error al enviar el sentimiento:', error);
      });
}