/* ===========================================================================
   AIA Uniandes — Carrusel de equipos
   En escritorio las tarjetas se reparten en perspectiva alrededor de la del
   frente; bajo 900 px el CSS las apila y solo se ve la del frente. La misma
   lógica sirve a los dos casos: cambia qué tarjeta está al frente.

   Los filtros ocultan cartas con [hidden]. La baraja reparte únicamente las
   que siguen a la vista, así que `actual` es un índice dentro de esa lista —
   nunca dentro de la lista completa.
   =========================================================================== */
(function () {
  'use strict';

  document.querySelectorAll('[data-carrusel]').forEach(function (carrusel) {
    var cartas = Array.prototype.slice.call(carrusel.querySelectorAll('[data-carta]'));
    if (!cartas.length) return;

    var mandos = document.querySelector(carrusel.dataset.mandos);
    var puntos = mandos ? Array.prototype.slice.call(mandos.querySelectorAll('[data-ir-a]')) : [];
    var contador = mandos ? mandos.querySelector('[data-contador]') : null;
    var actual = 0;

    function aLaVista() {
      return cartas.filter(function (carta) {
        return !carta.hidden;
      });
    }

    function centrar() {
      actual = Math.floor(aLaVista().length / 2);
    }

    function pintar() {
      var lista = aLaVista();

      if (actual > lista.length - 1) actual = Math.max(0, lista.length - 1);

      lista.forEach(function (carta, i) {
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

      // Un punto por carta visible: con el filtro puesto sobran los demás.
      puntos.forEach(function (punto, i) {
        punto.hidden = i >= lista.length;
        punto.setAttribute('aria-current', String(i === actual));
      });

      if (contador) {
        contador.textContent = lista.length
          ? actual + 1 + ' de ' + lista.length
          : 'Sin equipos en esta categoría';
      }
    }

    function ir(indice) {
      var total = aLaVista().length;
      if (!total) return;
      actual = (indice + total) % total;
      pintar();
    }

    cartas.forEach(function (carta) {
      carta.addEventListener('click', function () {
        var i = aLaVista().indexOf(carta);
        if (i !== -1 && i !== actual) ir(i);
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

    // Al filtrar, la baraja vuelve a repartirse con las cartas que quedan.
    carrusel.addEventListener('filtrado', function () {
      centrar();
      pintar();
    });

    centrar();
    pintar();
  });
})();
