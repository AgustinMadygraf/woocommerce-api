// interface_adapters/gateway/SheetApiGateway.js

export default class SheetApiGateway {
  async fetchSheetValues() {
    const res = await fetch('/api/sheet-values');
    if (!res.ok) {
      let errorMsg = 'Error al cargar los datos.';
      try {
        const errJson = await res.json();
        if (errJson && errJson.error) errorMsg = errJson.error;
      } catch (e) {
        errorMsg = `Error ${res.status}: ${res.statusText}`;
      }
      throw new Error(errorMsg);
    }
    return res.json();
  }
}
