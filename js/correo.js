/* ===========================================================================
   AIA Uniandes — Botones de correo
   Un enlace mailto: no hace nada en un navegador sin cliente de correo
   registrado, que es lo normal en un equipo que usa Outlook Web o Gmail en
   una pestaña: se pulsa el botón y no pasa nada.

   Aquí no se cancela la navegación — quien sí tiene cliente de correo sigue
   viéndolo abrirse — pero además se copia la dirección al portapapeles y el
   botón lo dice. Así el botón siempre hace algo visible.
   =========================================================================== */
(function () {
  'use strict';

  var AVISO = 'Correo copiado ✓';
  var ESPERA = 2200;

  function copiar(texto) {
    // El API moderno solo existe en contextos seguros (https). Abriendo el
    // sitio como archivo local no está, de ahí el camino de respaldo.
    try {
      if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(texto).then(function () {
          return true;
        }, function () {
          return intentarRespaldo(texto);
        });
      }
    } catch (e) {
      /* sigue por el respaldo */
    }
    return Promise.resolve(intentarRespaldo(texto));
  }

  function intentarRespaldo(texto) {
    try {
      return respaldo(texto);
    } catch (e) {
      return false;
    }
  }

  function respaldo(texto) {
    var campo = document.createElement('textarea');
    var hecho = false;
    try {
      campo.value = texto;
      campo.setAttribute('readonly', '');
      campo.style.position = 'fixed';
      campo.style.top = '-1000px';
      document.body.appendChild(campo);
      campo.select();
      hecho = document.execCommand('copy');
    } catch (e) {
      hecho = false;
    }
    if (campo.parentNode) campo.parentNode.removeChild(campo);
    return hecho;
  }

  function avisar(boton, mensaje) {
    if (boton.dataset.avisando === 'si') return;
    var original = boton.textContent;
    var ancho = boton.getBoundingClientRect().width;

    boton.dataset.avisando = 'si';
    boton.style.minWidth = Math.ceil(ancho) + 'px';
    boton.textContent = mensaje;

    window.setTimeout(function () {
      boton.textContent = original;
      boton.style.minWidth = '';
      delete boton.dataset.avisando;
    }, ESPERA);
  }

  var botones = document.querySelectorAll('a.boton[href^="mailto:"]');
  if (!botones.length) return;

  // Una sola región para que el lector de pantalla también se entere.
  var region = document.createElement('span');
  region.className = 'oculto-visual';
  region.setAttribute('role', 'status');
  region.setAttribute('aria-live', 'polite');
  document.body.appendChild(region);

  botones.forEach(function (boton) {
    var correo = boton.getAttribute('href').replace(/^mailto:/i, '').split('?')[0];
    boton.title = 'Pulsa para copiar ' + correo;

    boton.addEventListener('click', function () {
      // La respuesta es inmediata y no espera al portapapeles: writeText
      // puede tardar o no resolverse nunca, y mientras tanto el botón
      // parecería muerto. La dirección a la vista ya es útil por sí sola.
      avisar(boton, correo);
      region.textContent = 'Escribe a ' + correo;

      copiar(correo).then(function (bien) {
        if (!bien || boton.dataset.avisando !== 'si') return;
        boton.textContent = AVISO;
        region.textContent = 'Dirección copiada: ' + correo;
      });
    });
  });
})();
