#!/usr/bin/env bash
# Conecta ZÍA con un perfil de Hermes: copia su SOUL.md (solo lectura) al servicio y reinicia.
# Uso (en el VPS, como root):  ./conectar-perfil.sh <perfil>     ej. ./conectar-perfil.sh zamna-zia
set -euo pipefail
P="${1:?Uso: $0 <perfil-de-hermes>}"
SRC="/root/.hermes/profiles/$P/SOUL.md"
[ -f "$SRC" ] || { echo "No existe $SRC (perfiles: $(ls /root/.hermes/profiles | tr '\n' ' '))"; exit 1; }
install -d -o ziazamna -g ziazamna -m 0750 /var/lib/zia-zamna/perfil
install -o ziazamna -g ziazamna -m 0640 "$SRC" /var/lib/zia-zamna/perfil/SOUL.md
ENV=/var/lib/zia-zamna/service.env
sed -i "s|^ZIA_PROFILE_NAME=.*|ZIA_PROFILE_NAME=$P|" "$ENV"
systemctl restart zia-zamna
sleep 1
curl -s http://127.0.0.1:4661/health; echo
echo "Conectado al perfil «$P». Si editas su SOUL.md, vuelve a correr este script."
