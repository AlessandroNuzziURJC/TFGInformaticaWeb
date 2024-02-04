function validate() {
    var output = true;
    var id_name = document.getElementById('id_name');
    if (id_name.value.trim() === '') {
        id_name.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        id_name.focus();
        id_name.scrollIntoView();
        output = false;
    }

    var id_reps = document.getElementById('id_reps');
    if (id_reps.value.trim() === '') {
        id_reps.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        id_reps.focus();
        id_reps.scrollIntoView();
        output = false;
    }

    var id_email = document.getElementById('id_email');
    if (id_email.value.trim() === '') {
        id_email.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        id_email.focus();
        id_email.scrollIntoView();
        output = false;
    }

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var isChecked = false;

    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            isChecked = true;
        }
    });

    if (!isChecked) {
        for (numero = 0; numero < 3; numero ++) {
            var label = document.querySelector('label[for="id_lib_' + numero + '"]');
            label.style.color = 'red';

        }
        output = false;
    }

    var id_program = document.getElementById('id_program');
    if (id_program.value.trim() === '') {
        id_program.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        id_program.focus();
        id_program.scrollIntoView();
        output = false;
    }

    return output;
}

document.addEventListener('DOMContentLoaded', function () {
    fetch('/testsystem/index_form/')
        .then(response => response.json())
        .then(data => {
            console.log(data.form);

            var formContainer = document.getElementById('form-container');
            formContainer.innerHTML = data.form;

            var loadingElement = document.getElementById('form-loading');
            if (loadingElement) {
                loadingElement.remove();
            }

            var form = document.getElementById('formulario');
            var btnEnviar = document.getElementById('btnEnviar');
            btnEnviar.addEventListener('click', function (event) {
                event.preventDefault();
                if (validate()) {
                    form.submit();
                } else {
                    alert('Error en el formulario. Revisar valores de los campos.');
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener el formulario:', error);
        });

});

function loadQueue() {
    fetch('/testsystem/queue/')
        .then(response => response.json())
        .then(data => {
            console.log(data.executions);

            var queueContainer = document.getElementById('queue-container');
            queueContainer.innerHTML = data.executions;

            var loadingElement = document.getElementById('queue-loading');
            if (loadingElement) {
                loadingElement.remove();
            }
        })
        .catch(error => {
            console.error('Error al obtener la cola:', error);
        });
}

document.addEventListener('DOMContentLoaded', loadQueue);
setInterval(loadQueue, 1000);