#!/bin/bash -eux
if [ -z "${BACKUP_FORCE-}" ]; then
  echo This script is not safe to run multiple instances at the same time
  echo Starting through systemctl and forwarding journalctl
  set -eux
  journalctl -fu {{ home.split("/")[-1] }}-backup &
  journalpid="$!"
  systemctl start --wait {{ home.split("/")[-1] }}-backup
  retcode="$?"
  kill $journalpid
  exit $retcode
fi

cd {{ home }}

set -eu
export RESTIC_PASSWORD_FILE={{ home }}/.restic_password
set -x
export RESTIC_REPOSITORY={{ lookup('env', 'RESTIC_REPOSITORY') or home + '/restic' }}

backup=""

getcommit="docker-compose exec django env | grep -o 'GIT_COMMIT=[a-z0-9]*'"
if $getcommit; then
  export $($getcommit)
  backup="$backup --tag $GIT_COMMIT"
fi

docker-compose start postgres
docker-compose exec postgres pg_dumpall -U django -c -f /dump/data.dump

docker-compose logs &> log/docker.log || echo "Couldn't get logs from instance"

restic backup $backup docker-compose.yml log mrsattachments {{ lookup('env', 'POSTGRES_BACKUP') }}/data.dump

{% if lookup('env', 'LFTP_DSN') %}
lftp -c 'set ssl:check-hostname false;connect {{ lookup("env", "LFTP_DSN") }}; mkdir -p {{ home.split("/")[-1] }}; mirror -Rv {{ home }}/restic {{ home.split("/")[-1] }}/restic'
{% endif %}

rm -rf postgres/data/data.dump
