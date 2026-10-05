/* ===========================================================================
   AIA Uniandes — Menú móvil
   Despliega la barra de pestañas bajo el encabezado. La navegación existe
   en el HTML siempre: este guion solo la muestra u oculta.
   =========================================================================== */
(function () {
  'use strict';

  var boton = document.querySelector('[data-menu-boton]');
  var panel = document.querySelector('[data-menu-panel]');
  if (!boton || !panel) return;

  boton.addEventListener('click', function () {
    var abierto = panel.getAttribute('data-abierto') === 'si';
    panel.setAttribute('data-abierto', abierto ? 'no' : 'si');
    boton.setAttribute('aria-expanded', String(!abierto));
  });

  document.addEventListener('keydown', function (evento) {
    if (evento.key === 'Escape' && panel.getAttribute('data-abierto') === 'si') {
      panel.setAttribute('data-abierto', 'no');
      boton.setAttribute('aria-expanded', 'false');
      boton.focus();
    }
  });
})();
