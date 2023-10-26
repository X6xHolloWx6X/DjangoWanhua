document.addEventListener('DOMContentLoaded', function() {
  // Llenar el formulario de edición
  window.setEditarModalValues = function(dni, nombre_cliente, tel_cliente, email_cliente, direccion_cliente) {
      document.getElementById('editDni').value = dni;
      document.getElementById('editNombre').value = nombre_cliente;
      // Completa los demás campos aquí...
      
      document.getElementById('editarForm').action = '/cliente/editar/' + dni + '/';
  }
  
  // Configurar el formulario de eliminación
  window.setEliminarModalValue = function(dni) {
      document.getElementById('deleteDni').value = dni;
      
      document.getElementById('eliminarForm').action = '/cliente/eliminar/' + dni + '/';
  }
  
  // Validación básica del formulario
  let validateForm = function(form) {
      for (let input of form.getElementsByTagName('input')) {
          if (input.value.trim() === '') {
              alert('Por favor, llena todos los campos.');
              return false;
          }
      }
      return true;
  }

  // Validar el formulario antes de enviar
  let forms = document.querySelectorAll('form');
  for (let form of forms) {
      form.addEventListener('submit', function(event) {
          if (!validateForm(form)) {
              event.preventDefault();
          }
      });
  }
  
  // Recargar la página después de enviar el formulario
  let reloadAfterSubmit = function(form) {
      form.addEventListener('submit', function(event) {
          event.preventDefault();

          // Aquí puedes agregar una llamada AJAX si lo prefieres, pero simplemente recargaremos por ahora
          setTimeout(function() {
              location.reload();
          }, 500); // Recargar después de medio segundo para dar tiempo al servidor a procesar la solicitud
      });
  }
  
  for (let form of forms) {
      reloadAfterSubmit(form);
  }
  
  // Función de notificación
  let showNotification = function(message, type = 'info') {
      let notification = document.createElement('div');
      notification.className = `alert alert-${type} fixed-top`;
      notification.innerText = message;

      document.body.appendChild(notification);

      setTimeout(function() {
          notification.remove();
      }, 3000); // La notificación se mostrará durante 3 segundos
  }
  function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for(let cookie of cookies) {
        const [name, value] = cookie.split('=');
        if(name.trim() === 'csrftoken') {
            return value;
        }
    }
    return null;
}

  async function createCliente(data) {
        let formData = new FormData();
        for (let key in data) {
            formData.append(key, data[key]);
        }

        try {
            const response = await fetch('/cliente/nuevo/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()  // Obtiene el token CSRF desde una cookie
                },
                body: formData
            });

            if (response.ok) {
                showNotification('Cliente creado con éxito', 'success');
                setTimeout(function() {
                    location.reload();
                }, 1500);
            } else {
                showNotification('Error al crear cliente', 'danger');
            }
        } catch (error) {
            console.error('Hubo un problema con la solicitud Fetch:', error);
        }
    }
//Escucha el botón "Guardar" y llama a createCliente
let guardarBtn = document.querySelector("#crearClienteModal button[type='submit']");
    guardarBtn.addEventListener('click', function(event) {
        event.preventDefault();
        
        let data = {
            dni: document.querySelector("input[name='dni']").value,
            nombre_cliente: document.querySelector("input[name='nombre_cliente']").value,
            tel_cliente: document.querySelector("input[name='tel_cliente']").value,
            email_cliente: document.querySelector("input[name='email_cliente']").value,
            direccion_cliente: document.querySelector("input[name='direccion_cliente']").value,
        };
        
        createCliente(data);
});


  // Mostrar notificaciones al realizar acciones (opcional y depende de tu flujo de trabajo)
  // Ejemplo:
  // showNotification('Cliente creado con éxito', 'success');

});
