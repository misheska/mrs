#!/bin/bash
set -eu
export RESTIC_PASSWORD_FILE={{ home }}/.restic_password
set -x
export RESTIC_REPOSITORY={{ lookup('env', 'RESTIC_REPOSITORY') or home + '/restic' }}

pushd {{ home }}
if [ ! -d $RESTIC_REPOSITORY ]; then
    echo 'Repository not found ! geting from ftp'
    lftp -c 'set ssl:check-hostname false;connect {{ lookup("env", "LFTP_DSN") }}; mirror -v {{ home.split("/")[-1] }}/restic {{ home }}/restic'
fi
if [ -z "${1-}" ]; then
    restic snapshots
    exit 0
fi
restic restore $1 --target $restore
docker-compose down --remove-orphans -v
docker-compose start postgres
until test -S {{ home }}/postgres/run/.s.PGSQL.5432; do
    sleep 1
done
sleep 3 # ugly wait until db starts up, socket waiting aint enough
mv $restore/data.dump /home/mrs-production/postgres/data/data.dump
docker exec mrs-production-postgres psql -d mrs-production -U django -f /var/lib/postgresql/data/data.dump
echo Restore happy, clearing $postgres_current and $restore/data.dump
rm -rf $postgres_current $restore/data.dump
# playlabs/plugins/uwsgi/restore.post.sh: start
# playlabs/plugins/django/restore.post.sh: start
mv $restore/media media
# playlabs/plugins/sentry/restore.post.sh: start
# last plugin end: sentry
mv $restore/docker-run.sh .
bash -eux /home/mrs-production/docker-run.sh
docker-compose up -d
retcode=$?
docker-compose logs -f &
logspid=$!
[ $retcode = 0 ] || sleep 30
kill $logspid
exit $retcode
