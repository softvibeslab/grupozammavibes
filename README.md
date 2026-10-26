# Grupo Zamna · landing de campaña + análisis (/chamba)

Prospecto: **Grupo Zamna** (Real Estate · Technology · Interiors), inmobiliaria boutique de Playa del
Carmen y master broker de Prana Towers. Contactos: Eduardo Zamna y Alejandra Enríquez.

## URLs vivas (VPS rovicrm, publicado el 25-oct-2026)

- Landing: https://zamna.softvibes.art/
- Análisis: https://zamna.softvibes.art/analisis/
- Links (bio de IG): https://zamna.softvibes.art/links/

Todo con `noindex` (meta + cabecera `X-Robots-Tag` + robots.txt).

## Estructura

| Ruta | Qué es |
|---|---|
| `sitio/index.html` | Landing bilingüe ES/EN: Prana Towers, calculadora de rendimiento, 4 fichas reales, ecosistema, equipo, blog, FAQ y formulario → WhatsApp |
| `sitio/links/` | Reemplazo de link-in-bio con WhatsApp por intención |
| `sitio/analisis/` | Análisis interactivo: 8 fugas, antes/ahora con iframe, benchmark y 3 tiers (2,500 / 4,900 / 8,900 MXN) |
| `fuentes/` | Capturas, HTML del sitio, `redes-sociales.md` (19 presencias), `benchmark.md` (8 competidores) |
| `outreach/` | `mensajes.md` (WA 3 burbujas, cadencia 14 días) y `email.html`. **Borradores: no enviados** |
| `docs/` | `inventario-previo.md` (base: Ocean Caribbean Playacar) y capturas de QA |
| `deploy/` | vhost nginx y `publicar.sh` (respaldo previo en `/var/backups/zamna-web/`) |
| `cliente.config.json` | Cifras, hallazgos, paleta y pendientes |

## Publicar cambios

```bash
./deploy/publicar.sh
```

## Pendientes

- Link de pago del tier Cimiento (`PAY_URL` en `sitio/analisis/index.html`; hoy abre WhatsApp de Softvibes).
- Confirmar el teléfono oficial de Zamna (se usa 984 136 2816, el del sitio).
- Citas textuales de opiniones de Facebook (requieren ver la página).
- Fotos en alta de Prana Towers.
- Enviar WA-1 (borrador en `outreach/mensajes.md`).

## Verificación mínima

```bash
for p in / /analisis/ /links/ /img/prana-pool.jpg /img/lagunas-e302.jpg; do curl -s -o /dev/null -w "%{http_code} $p\n" https://zamna.softvibes.art$p; done
```
