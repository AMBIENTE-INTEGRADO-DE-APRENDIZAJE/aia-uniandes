/* ===========================================================================
   AIA Uniandes — Interruptor de tema
   El <head> de cada página estampa data-tema antes de pintar (guion en línea),
   así que aquí solo se conecta el control y se recuerda la elección.
   =========================================================================== */
(function () {
  'use strict';

  var raiz = document.documentElement;
  var LLAVE = 'aia-tema';

  function aplicar(tema) {
    raiz.setAttribute('data-tema', tema);
    try {
      localStorage.setItem(LLAVE, tema);
    } catch (e) {
      /* navegación privada o almacenamiento bloqueado: el tema vale solo
         para esta visita, que es un resultado aceptable. */
    }
    document.querySelectorAll('[data-poner-tema]').forEach(function (boton) {
      boton.setAttribute('aria-pressed', String(boton.dataset.ponerTema === tema));
    });
  }

  document.querySelectorAll('[data-poner-tema]').forEach(function (boton) {
    boton.addEventListener('click', function () {
      aplicar(boton.dataset.ponerTema);
    });
  });

  aplicar(raiz.getAttribute('data-tema') || 'claro');
})();
