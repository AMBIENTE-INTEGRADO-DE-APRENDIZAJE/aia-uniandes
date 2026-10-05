/* ===========================================================================
   AIA Uniandes — Filtros por categoría
   Genérico: cualquier [data-filtros] gobierna la lista que nombre su
   atributo data-objetivo. Los elementos filtrados siguen en el HTML —
   se ocultan con CSS, no se borran, para que el buscador los siga leyendo.
   =========================================================================== */
(function () {
  'use strict';

  document.querySelectorAll('[data-filtros]').forEach(function (grupo) {
    var lista = document.querySelector(grupo.dataset.objetivo);
    if (!lista) return;

    var elementos = Array.prototype.slice.call(lista.querySelectorAll('[data-categoria]'));
    var contador = grupo.dataset.contador ? document.querySelector(grupo.dataset.contador) : null;
    var total = elementos.length;

    function filtrar(categoria) {
      var visibles = 0;

      elementos.forEach(function (elemento) {
        var coincide = categoria === 'todos' || elemento.dataset.categoria === categoria;
        elemento.hidden = !coincide;
        if (coincide) visibles++;
      });

      grupo.querySelectorAll('[data-categoria-filtro]').forEach(function (boton) {
        boton.setAttribute('aria-pressed', String(boton.dataset.categoriaFiltro === categoria));
      });

      if (contador) {
        contador.textContent = visibles + ' de ' + total;
      }
    }

    grupo.addEventListener('click', function (evento) {
      var boton = evento.target.closest('[data-categoria-filtro]');
      if (boton) filtrar(boton.dataset.categoriaFiltro);
    });

    filtrar('todos');
  });
})();
