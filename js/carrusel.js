/* ===========================================================================
   AIA Uniandes — Carrusel de equipos
   En escritorio las tarjetas se reparten en perspectiva alrededor de la del
   frente; bajo 900 px el CSS las apila y solo se ve la del frente. La misma
   lógica sirve a los dos casos: cambia qué tarjeta está al frente.
   =========================================================================== */
(function () {
  'use strict';

  document.querySelectorAll('[data-carrusel]').forEach(function (carrusel) {
    var cartas = Array.prototype.slice.call(carrusel.querySelectorAll('[data-carta]'));
    if (!cartas.length) return;

    var mandos = document.querySelector(carrusel.dataset.mandos);
    var puntos = mandos ? Array.prototype.slice.call(mandos.querySelectorAll('[data-ir-a]')) : [];
    var contador = mandos ? mandos.querySelector('[data-contador]') : null;
    var actual = Math.floor(cartas.length / 2);

    function pintar() {
      cartas.forEach(function (carta, i) {
        var desvio = i - actual;
        var distancia = Math.abs(desvio);
        var frente = desvio === 0;

        carta.dataset.frente = frente ? 'si' : 'no';
        carta.style.zIndex = String(20 - distancia);
        carta.style.opacity = String(Math.max(0, 1 - distancia * 0.3));
        carta.style.transform =
          'translate(-50%, -50%)' +
          ' translateX(' + desvio * 208 + 'px)' +
          ' translateZ(' + (frente ? 0 : -180 - distancia * 60) + 'px)' +
          ' rotateY(' + desvio * -19 + 'deg)' +
          ' scale(' + (frente ? 1 : 0.94) + ')';
        carta.setAttribute('aria-hidden', String(!frente));
      });

      puntos.forEach(function (punto, i) {
        punto.setAttribute('aria-current', String(i === actual));
      });

      if (contador) {
        contador.textContent = actual + 1 + ' de ' + cartas.length;
      }
    }

    function ir(indice) {
      actual = (indice + cartas.length) % cartas.length;
      pintar();
    }

    cartas.forEach(function (carta, i) {
      carta.addEventListener('click', function () {
        if (i !== actual) ir(i);
      });
    });

    if (mandos) {
      mandos.addEventListener('click', function (evento) {
        var anterior = evento.target.closest('[data-anterior]');
        var siguiente = evento.target.closest('[data-siguiente]');
        var punto = evento.target.closest('[data-ir-a]');
        if (anterior) ir(actual - 1);
        else if (siguiente) ir(actual + 1);
        else if (punto) ir(Number(punto.dataset.irA));
      });
    }

    pintar();
  });
})();
