function validate() {
    var output = true;
    var id_name = document.getElementById('id_exec_name');
    if (id_name.value.trim() === '') {
        id_name.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        id_name.focus();
        id_name.scrollIntoView();
        output = false;
    }

    var checkboxes_div = document.getElementById('id_instance_types');
    var checkboxes = document.querySelectorAll('#id_instance_types input[type="checkbox"]');
    var atLeastOneChecked = Array.prototype.slice.call(checkboxes).some(function(checkbox) {
        return checkbox.checked;
    });
    if (!atLeastOneChecked) {
        checkboxes_div.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';
        checkboxes_div.focus();
        checkboxes_div.scrollIntoView();
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
    fetch('/p3co/index_form/')
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
    fetch('/api/get_queue')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        var loadingElement = document.getElementById('queue-loading');
            if (loadingElement) {
                loadingElement.remove();
            }

        document.getElementById('queue-container').innerHTML = '';

        data['queue'].forEach(execution => {
            const queueElement = document.createElement('div');
            queueElement.classList.add('row');

            const col1 = document.createElement('div');
            col1.classList.add('col-1');
            queueElement.appendChild(col1);

            const col10 = document.createElement('div');
            col10.classList.add('col-10');
            const queueElementInner = document.createElement('div');
            queueElementInner.classList.add('queue-element', execution.status);

            const header = document.createElement('h6');
            header.textContent = execution.exec_name;
            queueElementInner.appendChild(header);

            const paragraph = document.createElement('p');
            paragraph.textContent = execution.timestamp;
            queueElementInner.appendChild(paragraph);

            col10.appendChild(queueElementInner);
            queueElement.appendChild(col10);

            const col2 = document.createElement('div');
            col2.classList.add('col-1');
            queueElement.appendChild(col2);

            document.getElementById('queue-container').appendChild(queueElement);
        });
    })
    .catch(error => console.error('Error al obtener los datos de la cola:', error));
}

document.addEventListener('DOMContentLoaded', loadQueue);
setInterval(loadQueue, 10000);