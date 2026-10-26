# Inventario previo · Grupo Zamna (25-oct-2026)

Versión exprés del inventario (skill `landing-inventory-first`). Parte de la tabla de
`los-hdp-podcast/docs/inventario-previo.md` (24-oct-2026, <30 días). Desde esa fecha no se
agregaron carpetas inmobiliarias nuevas al workspace.

## Nicho del encargo

- **Nicho:** inmobiliario, Riviera Maya (Playa del Carmen, Ciudad Mayakoba, Tulum, Cancún).
- **Subnicho:** inmobiliaria boutique con master broker de un desarrollo propio (Prana Towers),
  catálogo de reventa/renta y unidades de negocio satélite (Network, Interiors, Property Management).
- **Conversión principal:** conversación de WhatsApp calificada (comprar / rentar / invertir / vender).

## Proyectos del mismo nicho en el workspace

| Proyecto | Ruta | Comparación | Uso |
|---|---|---|---|
| Ocean Caribbean Playacar | `ocean-caribbean-playacar/index.html` | **Mismo nicho** (premium, Playa del Carmen, bilingüe) | **Base estructural**: hero con tarjeta de precio, banda de datos, galería, ubicación, toggle ES/EN. |
| Laura Luna Broker | `laura-luna-broker/index.html` | Mismo nicho (marca personal) | Patrón de formulario que arma el mensaje de WhatsApp sin guardar datos. |
| Mónica Arteaga × DK del Karibe | `monica-arteaga-dkdelkaribe/` | Mismo nicho | Patrón `data-wa` + eventos en `dataLayer`. |
| KLH Hub de rentas | `klh-hub-rentas/` | Mismo nicho (rentas) | Fichas con WhatsApp contextual. |
| Vivemar / Ivy Loya / plantilla Astro CMS | varios | Mismo nicho (Astro) | Descartados: requieren build; el demo debe ser HTML estático. |

## Decisión

**Nicho existente → no se consulta Envato.** Se adapta la estructura de Ocean Caribbean
(hero + datos + galería + bilingüe) a una agencia con desarrollo destacado. Se reescribió todo:
identidad, textos, fotos, teléfonos y metadatos son de Grupo Zamna (fuentes públicas en
`../fuentes/`). No se copió ningún dato, foto o contacto de otro cliente.
