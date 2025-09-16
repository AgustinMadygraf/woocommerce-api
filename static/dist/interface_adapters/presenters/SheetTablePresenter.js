/*
Path: static/src/interface_adapters/presenters/SheetTablePresenter.ts
*/
/**
 * Presents sheet data as an HTML table
 */
export default class SheetTablePresenter {
    present(data) {
        if (!data || data.length === 0) {
            return '<div class="alert alert-warning">No hay datos para mostrar.</div>';
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
