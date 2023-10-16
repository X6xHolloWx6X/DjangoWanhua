// Variables para rastrear el estado de edición y eliminación
let clienteIdEditar = null;
let clienteIdEliminar = null;

// Función para mostrar el formulario de cliente
function mostrarFormulario(accion) {
  if (accion === 'crear') {
    // Mostrar el formulario de creación
    document.getElementById('formularioCrearCliente').style.display = 'block';
    document.getElementById('formularioEditarCliente').style.display = 'none';
  } else if (accion === 'editar') {
    // Mostrar el formulario de edición
    document.getElementById('formularioCrearCliente').style.display = 'none';
    document.getElementById('formularioEditarCliente').style.display = 'block';
  }

  // Restablecer campos del formulario
  document.getElementById('crearClienteForm').reset();
  document.getElementById('editarClienteForm').reset();

  // Ocultar alerta de eliminación
  document.getElementById('alertaEliminar').style.display = 'none';
  clienteIdEditar = null;
  clienteIdEliminar = null;
}

// Función para iniciar edición de un cliente
function editarCliente(clienteId) {
  // Aquí puedes realizar una petición AJAX para obtener la información del cliente usando el `clienteId`
  // Después de obtener los datos del cliente, puedes llenar los campos del formulario de edición y mostrar el formulario:
  // ejemplo:
  // document.getElementById('campoDelFormulario').value = datosDelCliente.campo;
  
  // Por ahora simplemente mostraremos el formulario de edición:
  mostrarFormulario('editar');

  // Guardar el clienteId en la variable global para saber cuál cliente estamos editando
  clienteIdEditar = clienteId;
}

// Función para iniciar la eliminación de un cliente
function eliminarCliente(clienteId) {
  // Mostrar una alerta de confirmación antes de eliminar
  const confirmacion = confirm("¿Estás seguro de que quieres eliminar este cliente?");
  if (confirmacion) {
    // Aquí puedes realizar una petición AJAX para eliminar el cliente usando el `clienteId`
    // Después de eliminar el cliente puedes actualizar la lista/tabla de clientes o mostrar una notificación

    // Por ahora simplemente mostraremos un mensaje en la consola:
    console.log("Cliente eliminado:", clienteId);
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Nombre de la cookie es 'csrftoken'
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Función para enviar el formulario de creación o edición de cliente
function enviarFormulario(accion) {
  // Obtener el token CSRF para la petición AJAX
  const csrfToken = getCookie('csrftoken');

  let url = "/ruta/api/crear-cliente/";  // Cambia esta URL a la adecuada para tu API de Django
  let metodo = "POST";
  let formularioId = "crearClienteForm";

  if (accion === 'editar') {
    url = "/ruta/api/editar-cliente/" + clienteIdEditar + "/";  // Cambia esta URL a la adecuada y agrega el ID del cliente
    metodo = "PUT";
    formularioId = "editarClienteForm";
  }

  const datosFormulario = new FormData(document.getElementById(formularioId));

  fetch(url, {
    method: metodo,
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: datosFormulario
  })
  .then(response => response.json())
  .then(data => {
    // Aquí puedes procesar la respuesta de tu API, como mostrar una notificación o actualizar la lista/tabla de clientes

    console.log("Respuesta de la API:", data);
  })
  .catch(error => {
    console.error("Error al enviar el formulario:", error);
  });
}
