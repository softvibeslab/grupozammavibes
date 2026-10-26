#!/usr/bin/env bash
# Instala (o actualiza) el puente ZÍA en el VPS. Correr desde tu Mac: ./deploy/instalar.sh
set -euo pipefail
cd "$(dirname "$0")/.."
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
rsync -az --delete --exclude 'tests' --exclude 'deploy' --exclude '__pycache__' --exclude '.*' -e "ssh -i $KEY" ./ "$VPS:/opt/zia-zamna/"
scp -i "$KEY" deploy/zia-zamna.service deploy/conectar-perfil.sh deploy/zia-zamna.env.example "$VPS:/tmp/"
ssh -i "$KEY" "$VPS" 'set -e
  id ziazamna >/dev/null 2>&1 || useradd --system --home /var/lib/zia-zamna --shell /usr/sbin/nologin ziazamna
  install -d -o ziazamna -g ziazamna -m 0750 /var/lib/zia-zamna /var/lib/zia-zamna/.hermes
  [ -f /var/lib/zia-zamna/service.env ] || install -o ziazamna -g ziazamna -m 0600 /tmp/zia-zamna.env.example /var/lib/zia-zamna/service.env
  install -m 0755 /tmp/conectar-perfil.sh /opt/zia-zamna/conectar-perfil.sh
  chown -R root:ziazamna /opt/zia-zamna && chmod -R g+rX,o-rwx /opt/zia-zamna
  install -m 0644 /tmp/zia-zamna.service /etc/systemd/system/zia-zamna.service
  systemctl daemon-reload && systemctl enable zia-zamna >/dev/null
  echo "Instalado. Falta: OPENROUTER_API_KEY en /var/lib/zia-zamna/service.env, nginx y conectar-perfil.sh"'
