/*
Path: static/js/main.js
*/

fetch('/api/sheet-values')
  .then(async res => {
    if (!res.ok) {
      // Intenta extraer el mensaje de error del backend
      let errorMsg = 'Error al cargar los datos.';
      try {
        const errJson = await res.json();
        if (errJson && errJson.error) errorMsg = errJson.error;
      } catch (e) {
        // No es JSON, usa el status
        errorMsg = `Error ${res.status}: ${res.statusText}`;
      }
      throw new Error(errorMsg);
    }
    return res.json();
  })
  .then(data => {
    if (!data || data.length === 0) {
      document.getElementById('sheet-table-container').innerHTML = '<div class="alert alert-warning">No hay datos para mostrar.</div>';
      return;
    }
    let html = '<table class="table table-bordered table-striped">';
    // Encabezados
    html += '<thead><tr>';
    data[0].forEach(cell => html += `<th>${cell}</th>`);
    html += '</tr></thead><tbody>';
    // Filas
    for (let i = 1; i < data.length; i++) {
      html += '<tr>';
      data[i].forEach(cell => html += `<td>${cell}</td>`);
      html += '</tr>';
    }
    html += '</tbody></table>';
    document.getElementById('sheet-table-container').innerHTML = html;
  })
  .catch(err => {
    document.getElementById('sheet-table-container').innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    console.error('[API ERROR]', err);
  });
