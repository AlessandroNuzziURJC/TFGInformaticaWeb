document.addEventListener('DOMContentLoaded', function () {
    fetch('/testsystem/index_form/')
        .then(response => response.json())
        .then(data => {
            console.log(data.form);

            var formContainer = document.getElementById('form-container');
            //formContainer.innerHTML = '<p>Prueba de HTML</p>';
            formContainer.innerHTML = data.form;

            var loadingElement = document.getElementById('form-loading');
            if (loadingElement) {
                loadingElement.remove();
            }

            var formulario = document.getElementById('formulario');
            var btnEnviar = document.getElementById('btnEnviar');
            btnEnviar.addEventListener('click', function (event) {
                event.preventDefault();
                formulario.submit();
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