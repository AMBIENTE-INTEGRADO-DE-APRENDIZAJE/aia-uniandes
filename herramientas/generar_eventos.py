# -*- coding: utf-8 -*-
"""Genera las páginas de evento desde una plantilla común.

El resultado son archivos HTML normales: se editan a mano como cualquier otro.
Para agregar un evento nuevo, añade su entrada a EVENTOS y vuelve a correr
este guion, o copia una página existente y cambia el contenido — las dos
formas son válidas.
"""
import io
import json
import os

BASE = "https://ambiente-integrado-de-aprendizaje.github.io/aia-uniandes"
import os

# La raiz del sitio es la carpeta que contiene a herramientas/.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "../"   # eventos/ -> raiz del sitio

EVENTOS = [
    {
        "slug": "escape-room-espacial",
        "titulo": "Escape Room 202610: Escape Espacial",
        "tag": "Ingeniería Industrial",
        "fecha_iso": "2026-05-20",
        "fecha_texto": "20 de mayo de 2026",
        "resumen": "Durante el Family Fest transformamos el laboratorio en una misión espacial donde los equipos resolvieron retos de ingeniería aplicada antes de agotar el tiempo.",
        "foto": None,
        "foto_alt": "",
        "cuerpo": [
            "Cada semestre, el <em>Family Fest</em> nos permite acercar la ingeniería a las familias de una manera lúdica y desafiante. En esta edición, la narrativa se trasladó al espacio exterior con nuestro <strong>Escape Room 202610 &mdash; El escape del ingeniero</strong>.",
            "Los participantes se enfrentaron a una misión colaborativa a contrarreloj donde, para lograr descifrar el código enigma, debieron superar acertijos diseñados alrededor de las áreas de núcleo de nuestra disciplina: Diseño, Producción y Logística, Ingeniería Financiera, Investigación de Operaciones, Analítica de Datos y Estrategia Organizacional.",
            "A través de dinámicas inmersivas los participantes exploraron temáticas de ingeniería industrial como la <em>cadena de suministro</em>, la <em>predicción de precio de acciones</em> y la <em>regresión lineal</em>. Demostramos que las habilidades analíticas, el trabajo en equipo y la optimización de recursos son herramientas universales, incluso para misiones en el espacio.",
        ],
    },
    {
        "slug": "colegio-himalaya-fusagasuga",
        "titulo": "Visita del Colegio Himalaya de Fusagasugá",
        "tag": "Investigación de operaciones",
        "fecha_iso": "2026-05-13",
        "fecha_texto": "13 de mayo de 2026",
        "resumen": "Los estudiantes se pusieron al frente de una compañía de food trucks y buscaron las mejores ubicaciones para vender en la ciudad.",
        "foto": None,
        "foto_alt": "",
        "cuerpo": [
            "Los ingenieros industriales terminan desarrollando un papel clave dentro de muchas áreas de las empresas; por ejemplo, las estrategias de ventas.",
            "En esta oportunidad, nuestros invitados se pusieron al frente de las operaciones de una compañía que vende tacos a través de <em>food trucks</em>.",
            "En este reto, los estudiantes debían encontrar las mejores ubicaciones para vender tacos dentro de la ciudad, enfrentando situaciones adversas como fallas en la cadena de suministro o lluvias.",
        ],
    },
    {
        "slug": "colegio-tecnico-zipaquira",
        "titulo": "Visita del colegio técnico rural de Zipaquirá",
        "tag": "Investigación de operaciones",
        "fecha_iso": "2026-04-10",
        "fecha_texto": "10 de abril de 2026",
        "resumen": "Los estudiantes visitantes exploraron la ciencia detrás de las apuestas y cómo los eventos discretos se modelan matemáticamente.",
        "foto": "assets/img/eventos/visita-colegio-zipaquira.jpg",
        "foto_alt": "Estudiantes del colegio técnico rural de Zipaquirá durante su visita al laboratorio AIA",
        "cuerpo": [
            "La <strong>probabilidad y la estadística</strong> tienen aplicaciones mucho más profundas de lo que se cree; incluso los juegos que parecen puramente azarosos pueden ser descifrados mediante el rigor matemático.",
            "En esta ocasión, los estudiantes visitantes exploraron la ciencia detrás de las apuestas, comprendiendo que eventos discretos &mdash;como el azar de una carta o el resultado de un dado&mdash; pueden <strong>modelarse matemáticamente</strong> para entender cómo se establece la ventaja de la casa. Como ingenieros industriales, una de nuestras mayores fortalezas es el análisis de fenómenos reales y su reinterpretación cuantitativa.",
            "Nuestras técnicas de modelado trascienden el ámbito del azar: áreas estratégicas como el <strong>mercadeo, la producción y la logística</strong> representan nuestro principal campo de acción dentro de la ingeniería.",
        ],
    },
]


def tildar(texto):
    """El texto ya viene con sus tildes; se conserva la función para no
    dispersar llamadas por la plantilla."""
    return texto


# destino de cada pestana visto desde pages/eventos/
# destino de cada pestana visto desde eventos/
NAV = [
    ("../", "AIA"),
    ("../laboratorio/", "Laboratorio"),
    ("../equipos/", "Equipos"),
    ("../investigacion/", "Investigación"),
    ("./", "Eventos"),
]


def chrome_nav(activa):
    """Los destinos de NAV ya vienen relativos a pages/eventos/: no se les
    antepone nada mas."""
    enlaces = "\n        ".join(
        '<a class="nav__enlace" href="%s"%s>%s</a>'
        % (h, ' aria-current="page"' if h == activa else "", t)
        for h, t in NAV
    )
    chips = "\n      ".join(
        '<a class="chip" href="%s"%s>%s</a>'
        % (h, ' aria-current="page"' if h == activa else "", t)
        for h, t in NAV
    )
    return enlaces, chips


def pie(p):
    return """<footer class="pie">
  <div class="contenedor">
    <div class="pie__alto">
      <div class="pie__col pie__col--ancha">
        <a class="marca" href="{p}" style="color: #fff;">
          <img src="{p}assets/img/logo-aia-blanco.png" alt="" width="44" height="57">
          <span>
            <span class="marca__nombre">Ambiente Integrado de Aprendizaje</span>
            <span class="marca__sub">Ingeniería Industrial · Uniandes</span>
          </span>
        </a>
        <p class="pie__texto">El laboratorio de Industria 4.0 de Ingeniería Industrial de la Universidad de los Andes. Robótica, manufactura aditiva, realidad aumentada e inteligencia artificial aplicada a operaciones reales.</p>
      </div>
      <nav class="pie__col" aria-label="Pie de página">
        <span class="pie__titulo-col">Navegación</span>
        <a href="{p}">AIA</a>
        <a href="../laboratorio/">El laboratorio</a>
        <a href="../laboratorio/#nuestra-gente">Nuestra gente</a>
        <a href="../equipos/">Equipos</a>
        <a href="../investigacion/">Investigación</a>
        <a href="./">Eventos</a>
      </nav>
      <div class="pie__col">
        <span class="pie__titulo-col">Horario de atención</span>
        <div>
          <div style="font-size: 0.8125rem; color: rgba(255,255,255,0.72);">Lunes a viernes</div>
          <div class="pie__dato-grande">8:00 a.m. – 6:00 p.m.</div>
        </div>
        <p class="pie__aviso">Solo se puede entrar dentro de estas horas, con personal del AIA presente.</p>
        <a href="../laboratorio/#horario" style="color: var(--acento-marca); font-weight: 700; font-size: 0.8125rem;">Ver el horario completo →</a>
      </div>
      <div class="pie__col">
        <span class="pie__titulo-col">Dónde y con quién</span>
        <div>
          <div class="pie__dato-grande">ML 508</div>
          <div style="font-size: 0.8125rem; line-height: 1.55; color: rgba(255,255,255,0.72);">Edificio Mario Laserna, quinto piso<br>Universidad de los Andes, Bogotá</div>
        </div>
        <a href="mailto:aiaindustrial@uniandes.edu.co">aiaindustrial@uniandes.edu.co</a>
        <span style="font-size: 0.8125rem; color: rgba(255,255,255,0.46);">También al equipo por Microsoft Teams</span>
      </div>
    </div>
    <div class="pie__bajo">
      <span>Universidad de los Andes · Facultad de Ingeniería · Departamento de Ingeniería Industrial</span>
      <a href="../equipos/" style="font-weight: 600;">Reservar un equipo</a>
    </div>
  </div>
</footer>""".format(p=p)


PLANTILLA = """<!doctype html>
<html lang="es" data-tema="claro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{titulo} | Eventos AIA Uniandes</title>
<meta name="description" content="{resumen}">
<link rel="canonical" href="{url}">

<meta property="og:type" content="article">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Ambiente Integrado de Aprendizaje — Uniandes">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{resumen}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="article:published_time" content="{fecha_iso}">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="{p}assets/img/logo-aia.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{p}css/tokens.css">
<link rel="stylesheet" href="{p}css/base.css">
<link rel="stylesheet" href="{p}css/layout.css">
<link rel="stylesheet" href="{p}css/componentes.css">

<script>
  (function () {{
    try {{
      var g = localStorage.getItem('aia-tema');
      if (!g) g = matchMedia('(prefers-color-scheme: dark)').matches ? 'oscuro' : 'claro';
      document.documentElement.setAttribute('data-tema', g);
    }} catch (e) {{}}
  }})();
</script>

<script type="application/ld+json">
{jsonld}
</script>
</head>

<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>

<header class="encabezado">
  <div class="contenedor">
    <div class="encabezado__barra">
      <a class="marca" href="{p}">
        <img src="{p}assets/img/logo-aia.png" alt="" width="38" height="49">
        <span>
          <span class="marca__nombre">Ambiente Integrado de Aprendizaje</span>
          <span class="marca__sub">Uniandes / Ing. Industrial / ML&nbsp;508</span>
        </span>
      </a>
      <nav class="nav" aria-label="Principal">
        {enlaces}
        <div class="tema" role="group" aria-label="Tema de color">
          <button class="tema__boton" type="button" data-poner-tema="claro" aria-pressed="true">Claro</button>
          <button class="tema__boton" type="button" data-poner-tema="oscuro" aria-pressed="false">Oscuro</button>
        </div>
        <a class="boton boton--primario boton--compacto" href="../equipos/">Reservar</a>
      </nav>
      <button class="menu-boton" type="button" data-menu-boton aria-expanded="false" aria-controls="menu-movil">
        <span class="oculto-visual">Abrir menú</span>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <div class="nav-movil" id="menu-movil" data-menu-panel data-abierto="no">
    <div class="nav-movil__pista">
      {chips}
    </div>
  </div>
</header>

<main id="contenido">
  <article class="seccion contenedor">
    <nav class="migas" aria-label="Ruta">
      <a href="{p}">Inicio</a>
      <span class="migas__sep" aria-hidden="true">/</span>
      <a href="./">Eventos</a>
      <span class="migas__sep" aria-hidden="true">/</span>
      <span class="migas__actual" aria-current="page">{titulo}</span>
    </nav>

    <div class="articulo">
      <div class="evento__meta" style="margin-bottom: 16px;">
        <span class="evento__tag">{tag}</span>
        <time class="evento__fecha" datetime="{fecha_iso}">{fecha_texto}</time>
      </div>
      <h1 style="margin-bottom: 20px;">{titulo}</h1>
      <p class="entradilla" style="max-width: none; margin-bottom: 28px;">{resumen}</p>
    </div>

    <div class="placa" style="aspect-ratio: 16/9; max-width: 1000px; margin: 0 auto 36px;">
      {media}{nota}
    </div>

    <div class="articulo">
      {cuerpo}
    </div>

    <div class="articulo" style="margin-top: 40px;">
      <div class="aviso" style="border-color: var(--borde); background: var(--panel);">
        <div class="aviso__cuerpo">
          <h3>¿Quieres traer tu colegio o grupo al laboratorio?</h3>
          <p class="apoyo">Recibimos visitas guiadas donde los estudiantes resuelven retos reales de ingeniería industrial con robots, impresión 3D y realidad aumentada.</p>
        </div>
        <a class="boton boton--primario" href="mailto:aiaindustrial@uniandes.edu.co">Escríbenos</a>
      </div>
      <p style="margin-top: 28px;"><a href="./">← Volver a todos los eventos</a></p>
    </div>
  </article>
</main>

{pie}

<script src="{p}js/tema.js" defer></script>
<script src="{p}js/menu.js" defer></script>
</body>
</html>
"""


def main():
    enlaces, chips = chrome_nav("./")
    pie_html = pie(P)

    for ev in EVENTOS:
        titulo = tildar(ev["titulo"])
        tag = tildar(ev["tag"])
        resumen = tildar(ev["resumen"])
        cuerpo_parrafos = [tildar(x) for x in ev["cuerpo"]]
        foto_alt = tildar(ev["foto_alt"])

        url = "%s/eventos/%s.html" % (BASE, ev["slug"])
        og_img = "%s/%s" % (BASE, ev["foto"]) if ev["foto"] else "%s/assets/img/logo-aia.png" % BASE

        if ev["foto"]:
            media = (
                '<img src="%s%s" alt="%s" width="1100" height="619" '
                'style="width:100%%;height:100%%;object-fit:cover;">' % (P, ev["foto"], foto_alt)
            )
            nota = ""
        else:
            media = (
                '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                'stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
                'style="color: rgba(255,255,255,0.4);"><rect x="3" y="5" width="18" height="14" rx="2"/>'
                '<circle cx="12" cy="12" r="3"/></svg>'
            )
            nota = '\n      <span class="placa__nota">Foto pendiente</span>'

        cuerpo = "\n      ".join("<p>%s</p>" % x for x in cuerpo_parrafos)

        jsonld = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "Event",
                "name": titulo,
                "startDate": ev["fecha_iso"],
                "eventStatus": "https://schema.org/EventScheduled",
                "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "description": resumen,
                "url": url,
                "location": {
                    "@type": "Place",
                    "name": "Ambiente Integrado de Aprendizaje — ML 508",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "Edificio Mario Laserna, ML 508, quinto piso",
                        "addressLocality": "Bogotá",
                        "addressCountry": "CO",
                    },
                },
                "organizer": {
                    "@type": "Organization",
                    "name": "Ambiente Integrado de Aprendizaje — Universidad de los Andes",
                    "url": BASE + "/",
                },
            },
            ensure_ascii=False,
            indent=2,
        )

        html = PLANTILLA.format(
            p=P, enlaces=enlaces, chips=chips, pie=pie_html, jsonld=jsonld,
            media=media, nota=nota, cuerpo=cuerpo, url=url, og_img=og_img,
            titulo=titulo, tag=tag, resumen=resumen,
            fecha_iso=ev["fecha_iso"], fecha_texto=ev["fecha_texto"],
        )

        destino = os.path.join(RAIZ, "eventos", ev["slug"] + ".html")
        io.open(destino, "w", encoding="utf-8").write(html)
        print("escrito %-46s %6d bytes" % (destino.split("/")[-1], len(html)))


if __name__ == "__main__":
    main()
