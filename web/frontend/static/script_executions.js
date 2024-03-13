function loadExecutions() {
    fetch('/p3co/cards')
        .then(response => response.json())
        .then(data => {
            var loadingElement = document.getElementById('loading');
            if (loadingElement) {
                loadingElement.remove();
            }

            container = document.getElementById('cards-container')
            container.innerHTML = data['cards'];

        })
        .catch(error => {
            console.error('Error al obtener el formulario:', error);
        });
}

document.addEventListener('DOMContentLoaded', loadExecutions);
setInterval(loadExecutions, 60000);