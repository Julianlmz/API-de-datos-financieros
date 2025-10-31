document.addEventListener('DOMContentLoaded', () => {
    
    const monedaBaseSelect = document.getElementById('moneda-base');
    const monedaDestinoSelect = document.getElementById('moneda-destino');
    const btnConsultar = document.getElementById('btn-consultar');
    const resultadoDiv = document.getElementById('resultado');

    btnConsultar.addEventListener('click', () => {
        const monedaBase = monedaBaseSelect.value;
        const monedaDestino = monedaDestinoSelect.value;

        if (monedaBase === monedaDestino) {
            mostrarError("Por favor, selecciona dos monedas diferentes.");
            return;
        }
        
        obtenerTasaDeCambio(monedaBase, monedaDestino);
    });

    async function obtenerTasaDeCambio(base, destino) {
        resultadoDiv.innerHTML = "<p>Consultando tasa...</p>";

        const url = `http://127.0.0.1:8000/api/tasa-cambio?moneda_base=${base}&moneda_destino=${destino}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Error en la respuesta del servidor');
            }
            mostrarResultado(data.moneda_base, data.moneda_destino, data.tasa);

        } catch (error) {
            console.error('Error al consultar el backend:', error);
            mostrarError(error.message);
        }
    }

    function mostrarResultado(base, destino, tasa) {
        resultadoDiv.innerHTML = `
            <p>1 ${base} equivale a:</p>
            <p class="tasa-final">${tasa.toFixed(4)} ${destino}</p>
        `;
    }

    function mostrarError(mensaje) {
        resultadoDiv.innerHTML = `<p style="color: red;">${mensaje}</p>`;
    }
});