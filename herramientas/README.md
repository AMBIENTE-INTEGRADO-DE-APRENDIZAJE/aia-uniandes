# Herramientas del sitio

Dos guiones de Python, sin dependencias: basta con tener Python instalado.
Ambos calculan solos dónde está la raíz del sitio, así que se pueden correr
desde cualquier carpeta.

---

## `verificar.py` — revisa el sitio antes de publicar

```
python herramientas/verificar.py
```

Recorre las ocho páginas y avisa de:

- enlaces o recursos locales que apuntan a un archivo que no existe
- anclas (`#algo`) sin destino en la página
- etiquetas mal cerradas
- faltantes de SEO: `meta description`, `canonical`, `lang`, Open Graph,
  o un número de `<h1>` distinto de uno

Córrelo **siempre antes de hacer push**. Es barato y atrapa justo los errores
que no se ven al abrir la página en el navegador — un `href` roto se ve igual
de bien hasta que alguien lo pulsa.

Si agregas una página nueva, añádela a la lista `PAGINAS` del guion.

---

## `generar_eventos.py` — crea las páginas de evento

```
python herramientas/generar_eventos.py
```

Escribe los archivos de `pages/eventos/` a partir de la lista `EVENTOS` que
está dentro del mismo guion. Cada entrada lleva:

| campo | para qué sirve |
|---|---|
| `slug` | nombre del archivo y de la URL: `pages/eventos/<slug>.html` |
| `titulo` | el `<h1>`, el `<title>` y el encabezado de la tarjeta |
| `tag` | categoría; debe coincidir con un filtro de `pages/eventos.html` |
| `fecha_iso` | formato `AAAA-MM-DD`; alimenta el `<time>` y los datos estructurados |
| `fecha_texto` | la fecha como se lee en pantalla |
| `resumen` | la `meta description` y la entradilla |
| `foto` | ruta desde la raíz, o `None` para dejar el marcador |
| `foto_alt` | descripción de la foto: esto es lo que lee Google y un lector de pantalla |
| `cuerpo` | lista de párrafos; admite `<strong>` y `<em>` |

**Para agregar un evento:** añade su entrada a `EVENTOS`, corre el guion, y
después agrega a mano su tarjeta en `pages/eventos.html` y su `<url>` en
`sitemap.xml`. Esas dos últimas no las toca el guion a propósito: así decides
tú el orden en que aparecen las tarjetas.

También puedes trabajar sin el guion: copia una página de evento existente y
cámbiale el contenido. Las dos formas son igual de válidas.

---

## Pendientes conocidos

- **La URL base está sin confirmar.** Es
  `https://ambiente-integrado-de-aprendizaje.github.io/aia-uniandes` y aparece
  en los `canonical`, el Open Graph, `sitemap.xml`, `robots.txt` y en
  `generar_eventos.py` (constante `BASE`). Si la dirección real es otra,
  cámbienla en todos esos sitios antes de publicar: un `canonical` que apunta
  a un dominio equivocado hace más daño que no tenerlo.
- **Faltan fotos de los equipos** del laboratorio; las fichas de
  `pages/equipos.html` muestran un marcador mientras tanto.
