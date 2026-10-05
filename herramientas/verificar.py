# -*- coding: utf-8 -*-
"""Revisa que todo enlace y recurso local del sitio apunte a un archivo real,
y que cada pagina traiga lo minimo de SEO."""
import io
import os
import re
import sys
from html.parser import HTMLParser

import os

# La raiz del sitio es la carpeta que contiene a herramientas/.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGINAS = [
    "index.html",
    "pages/laboratorio.html", "pages/equipos.html",
    "pages/investigacion.html", "pages/eventos.html",
    "pages/eventos/escape-room-espacial.html",
    "pages/eventos/colegio-himalaya-fusagasuga.html",
    "pages/eventos/colegio-tecnico-zipaquira.html",
]


class Recolector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.recursos = []
        self.pila = []
        self.desbalance = []
        self.ids = set()
        self.anclas = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        for att in ("href", "src"):
            v = d.get(att)
            if not v:
                continue
            if v.startswith("#"):
                self.anclas.append(v[1:])
            elif not re.match(r"^(https?:|mailto:|data:|//)", v):
                self.recursos.append(v.split("#")[0].split("?")[0])
        if tag not in ("meta", "link", "img", "br", "hr", "input", "source", "path",
                       "circle", "rect", "use", "area", "col", "embed", "param", "track", "wbr"):
            self.pila.append(tag)

    def handle_startendtag(self, tag, attrs):
        # <path .../> y demas autocerradas: abren y cierran en el mismo sitio,
        # no entran en la pila.
        self.handle_starttag(tag, attrs)
        if self.pila and self.pila[-1] == tag:
            self.pila.pop()

    def handle_endtag(self, tag):
        if tag in ("meta", "link", "img", "br", "hr", "input", "source"):
            return
        if self.pila and self.pila[-1] == tag:
            self.pila.pop()
        elif tag in self.pila:
            while self.pila and self.pila.pop() != tag:
                pass
        else:
            self.desbalance.append(tag)


fallos = 0
for pagina in PAGINAS:
    ruta = os.path.join(RAIZ, pagina)
    if not os.path.exists(ruta):
        print("FALTA LA PAGINA %s" % pagina)
        fallos += 1
        continue

    texto = io.open(ruta, encoding="utf-8").read()
    r = Recolector()
    r.feed(texto)

    carpeta = os.path.dirname(ruta)
    rotos = []
    for recurso in sorted(set(r.recursos)):
        destino = os.path.normpath(os.path.join(carpeta, recurso))
        if not os.path.exists(destino):
            rotos.append(recurso)

    anclas_rotas = sorted(set(a for a in r.anclas if a and a not in r.ids))

    seo = []
    if '<meta name="description"' not in texto:
        seo.append("sin description")
    if '<link rel="canonical"' not in texto:
        seo.append("sin canonical")
    if texto.count("<h1") != 1:
        seo.append("%d etiquetas h1" % texto.count("<h1"))
    if 'lang="es"' not in texto:
        seo.append("sin lang")
    if 'property="og:title"' not in texto:
        seo.append("sin Open Graph")

    estado = "OK"
    if rotos or anclas_rotas or r.desbalance or seo:
        estado = "REVISAR"
        fallos += 1

    print("%-46s %s" % (pagina, estado))
    for x in rotos:
        print("      recurso inexistente: %s" % x)
    for x in anclas_rotas:
        print("      ancla sin destino:   #%s" % x)
    for x in set(r.desbalance):
        print("      cierre sin apertura: </%s>" % x)
    for x in seo:
        print("      SEO: %s" % x)

print()
print("paginas con algo que revisar: %d de %d" % (fallos, len(PAGINAS)))
sys.exit(0)
