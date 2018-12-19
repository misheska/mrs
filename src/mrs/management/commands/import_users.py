from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from mrsuser.models import User
from caisse.models import Caisse
import csv


def add_user(row):
    agent_nb = row[2].strip()
    last_name = row[0].strip().upper()
    username = "{}_{}".format(last_name, agent_nb)
    password = agent_nb

    user, created = User.objects.get_or_create(
        last_name=last_name,
        first_name=row[1].strip(),
        email=row[-1].strip(),
        username=username,
    )
    if created:
        print("created: {}".format(username))
    else:
        print("already exists: {}".format(username))

    user.set_password(password)
    user.save()

    groups = row[3].split(',')
    user.add_groups(groups)

    caisses_ids = row[4].split(',')
    caisses = []
    for id in caisses_ids:
        try:
            caisses.append(Caisse.objects.get(number=id))
        except ObjectDoesNotExist:
            print("could not find caisse number {}."
                  .format(id))

    if caisses:
        user.caisses.add(*caisses)

    return user


class Command(BaseCommand):
    help = """Import users and set permissions from a csv file.

    Columns are:
    NOM	PRENOM	NUMERO AGENT	PROFIL	NUMERO ORGANISME	MAIL
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            dest='file',
            help='csv file',
        )

    def handle(self, *args, **options):
        if not options.get('file'):
            print("usage: mrs import_users -f file.csv")
            exit(1)

        with open(options.get('file'), newline='') as f:
            reader = csv.reader(f, delimiter='\t')  # watch delimiter
            # DictReader ? clunky.
            for row in reader:
                if row:
                    if not row[0]:
                        continue
                    elif row[0] == 'NOM' and row[1] == 'PRENOM':
                        continue

                    print(row)
                    add_user(row)
