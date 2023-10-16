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

// Función para ocultar el formulario de cliente
function cancelarFormulario(accion) {
  if (accion === 'crear') {
    document.getElementById('formularioCrearCliente').style.display = 'none';
  } else if (accion === 'editar') {
    document.getElementById('formularioEditarCliente').style.display = 'none';
  }

  clienteIdEditar = null;
  clienteIdEliminar = null;
}

// Función para mostrar/ocultar datos del garante según el tipo de cliente
function toggleGarante() {
  const tipoCliente = document.getElementById('tipo_cliente').value;
  if (tipoCliente === 'inquilino') {
    document.getElementById('garanteDatos').style.display = 'block';
  } else {
    document.getElementById('garanteDatos').style.display = 'none';
  }
}

// Función para mostrar/ocultar datos del garante en el formulario de edición según el tipo de cliente
function toggleGaranteEditar() {
  const tipoCliente = document.getElementById('tipo_clienteEditar').value;
  if (tipoCliente === 'inquilino') {
    document.getElementById('garanteDatosEditar').style.display = 'block';
  } else {
    document.getElementById('garanteDatosEditar').style.display = 'none';
  }
}

// Llamar a toggleGarante cuando cambie la selección de tipo de cliente
document.getElementById('tipo_cliente').addEventListener('change', toggleGarante);
document.getElementById('tipo_clienteEditar').addEventListener('change', toggleGaranteEditar);

// Restablecer campos del formulario de edición cuando se cancela la edición
document.getElementById('formularioEditarCliente').addEventListener('reset', () => {
  clienteIdEditar = null;
});

function guardarCliente(accion) {
  const form = accion === 'crear' ? document.getElementById('crearClienteForm') : document.getElementById('editarClienteForm');
  const formData = new FormData(form);
  fetch(accion === 'crear' ? '/clientes/agregar/' : `/clientes/editar/${clienteIdEditar}/`, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.message) {
      document.getElementById('messages').innerHTML = `<div class="alert alert-success">${data.message}</div>`;
      form.reset();
      // Actualizar la lista de clientes si es necesario
      // Puedes implementar la lógica aquí
    } else if (data.error) {
      document.getElementById('messages').innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
    }
    // Ocultar el formulario después de guardar
    if (accion === 'crear') {
      document.getElementById('formularioCrearCliente').style.display = 'none';
    } else if (accion === 'editar') {
      document.getElementById('formularioEditarCliente').style.display = 'none';
    }
    clienteIdEditar = null;
  })
  .catch(error => {
    console.error(error);
  });
}

function editarCliente(clienteId) {
  if (clienteIdEliminar) {
    // Evitar editar si hay una eliminación en curso
    return;
  }
  const url = `/clientes/editar/${clienteId}/`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Llenar el formulario de edición con los datos del cliente
      document.getElementById('clienteIdEditar').value = data.id_cliente;
      document.getElementById('nombreEditar').value = data.nombre;
      document.getElementById('apellidoEditar').value = data.apellido;
      document.getElementById('dniEditar').value = data.dni;
      document.getElementById('fecha_nacimientoEditar').value = data.fecha_nacimiento;
      document.getElementById('tipo_clienteEditar').value = data.tipo_cliente;

      // Mostrar el formulario de edición
      document.getElementById('formularioEditarCliente').style.display = 'block';

      // Mostrar u ocultar datos del garante en el formulario de edición según el tipo de cliente
      toggleGaranteEditar();
      clienteIdEditar = clienteId;
    })
    .catch(error => {
      console.error(error);
    });
}

function mostrarConfirmacion(clienteId) {
  if (clienteIdEditar) {
    // Evitar eliminación si hay una edición en curso
    return;
  }
  // Mostrar alerta de eliminación
  document.getElementById('alertaEliminar').style.display = 'block';
  clienteIdEliminar = clienteId;
}

function cancelarEliminar() {
  // Ocultar alerta de eliminación
  document.getElementById('alertaEliminar').style.display = 'none';
  clienteIdEliminar = null;
}

function eliminarCliente() {
  if (clienteIdEliminar) {
    fetch(`/clientes/eliminar/${clienteIdEliminar}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        document.getElementById('messages').innerHTML = `<div class="alert alert-success">${data.message}</div>`;
        // Actualizar la lista de clientes si es necesario
        // Puedes implementar la lógica aquí
      } else if (data.error) {
        document.getElementById('messages').innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
      }
      // Ocultar alerta de eliminación
      document.getElementById('alertaEliminar').style.display = 'none';
      clienteIdEliminar = null;
    })
    .catch(error => {
      console.error(error);
    });
  }
}

// Función para ver la información del cliente
function verInformacion(clienteId) {
// Realizar una solicitud para obtener los datos del cliente por su ID
fetch(`/clientes/obtener/${clienteId}/`)
.then(response => response.json())
.then(data => {
  if (data.cliente) {
    const cliente = data.cliente;
    // Llenar los campos del menú flotante con los datos del cliente
    document.getElementById('infoId').textContent = cliente.id_cliente;
    document.getElementById('infoNombre').textContent = cliente.nombre;
    document.getElementById('infoApellido').textContent = cliente.apellido;
    document.getElementById('infoDni').textContent = cliente.dni;
    document.getElementById('infoFechaNacimiento').textContent = cliente.fecha_nacimiento;
    document.getElementById('infoTipoCliente').textContent = cliente.tipo_cliente;
    document.getElementById('infoGaranteNombre').textContent = cliente.garante_nombre || '-';
    document.getElementById('infoGaranteApellido').textContent = cliente.garante_apellido || '-';
    document.getElementById('infoGaranteDni').textContent = cliente.garante_dni || '-';
    // Mostrar el menú flotante
    document.getElementById('menuFlotante').style.display = 'block';
  } else {
    console.error('Cliente no encontrado');
  }
});
}
// Función para cerrar el menú flotante
function cerrarMenuFlotante() {
// Ocultar el menú flotante
document.getElementById('menuFlotante').style.display = 'none';
}

// Función para obtener el valor de la cookie CSRFToken
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