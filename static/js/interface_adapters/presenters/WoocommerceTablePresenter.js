// interface_adapters/presenters/WoocommerceTablePresenter.js

export default class WoocommerceTablePresenter {
  present(data) {
    if (!data || data.length === 0) {
      return '<div class="alert alert-warning">No hay productos WooCommerce para mostrar.</div>';
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
    return html;
  }
}
