#!/usr/bin/env bash
# Publica sitio/ en https://zamna.softvibes.art (VPS rovicrm). Respaldo previo en el servidor.
set -euo pipefail
cd "$(dirname "$0")/.."
VPS=root@31.220.63.211
KEY=~/.ssh/rovi_vps_deploy
TS=$(date +%Y%m%d-%H%M%S)
ssh -i "$KEY" "$VPS" "mkdir -p /var/www/zamna /var/backups/zamna-web && cp -a /var/www/zamna /var/backups/zamna-web/$TS"
rsync -az --delete --exclude '.*' -e "ssh -i $KEY" sitio/ "$VPS:/var/www/zamna/"
ssh -i "$KEY" "$VPS" "find /var/www/zamna -type d -exec chmod 755 {} + && find /var/www/zamna -type f -exec chmod 644 {} +"
echo "$TS publicado" >> deploy/DESPLIEGUES.log
echo "ok → https://zamna.softvibes.art (respaldo /var/backups/zamna-web/$TS)"
