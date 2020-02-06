Opérations
~~~~~~~~~~

Ce chapitre vise les DevOps en vue de maintenir un deploiement de MRS
automatisé, comme c'est le cas pour la production, staging, ecole, ainsi que
pour les deploiements de dev ephemeres faits a partir des branches.

Ce chapitre a donc vocation d'expliquer tous les types de déploiements
possibles ainsi que les opérations courantes.

Architecture compose
====================

Docker-compose prefixe les containers et volume d'une installation a partir
d'un prefixe. Soit ce prefixe est l'argument passé a compose avec
``--project-name``, soit c'est le nom du dossier qui contient le fichier
compose.

La difference entre un deploiement persistent et un deploiement de dev reside
principalement la:

- pour un env persistent (prod, staging ...), on passe un
  ``home=/home/mrs-production`` et on fusionne ``docker-compose.yml`` avec
  ``docker-compose.persist.yml``,
- pour un env ephèmere (branche dev), on passe ``project=test-$BRANCHNAME``

Dans tous les cas, si le serveur a un load-balancer fonctionnel (deployable
avec ``bigsudo yourlabs.traefik`` ou manuellement), alors on veut aussi
fusionner ``docker-compose.traefik.yml``.

Enfin, utile pour les envs de dev et staging, on peut aussi fusionner
``docker-compose.maildev.yml`` pour avoir un serveur de mail de test.

Operations courantes
====================

Il faut un acces sudo sans mot de passe sur l'un des serveurs pour pouvoir
effectuer l'une de ces operations.

Ajouter un utilisateur sudo
---------------------------

Pour ajouter un utilisateur en sudo sans mot de passe, avec son nom
d'utilisateur github, et la clef ssh publique correspondante a cet utilisateur
sur github::

    bigsudo yourlabs.ssh adduser usergroups=sudo username=github_username @mrs.beta.gouv.fr @staging.mrs.beta.gouv.fr

Pour choisir un nom d'utilisateur ou clef qui n'est pas sur github::

    bigsudo yourlabs.ssh adduser usergroups=sudo username=your_username key=https://gitlab.com/your_gitlab_username.keys @mrs.beta.gouv.fr @staging.mrs.beta.gouv.fr

Après vous pouvez bien entendu le faire manuellement a l'ancienne, mais perso
je trouve cette maniere plus rapide car elle encapsule des operations autrement
repetitives.

Copier les données de prod en staging
-------------------------------------

Cette opération se passe en deux temps:

- la copie des données d'une base de données à l'autre à travers ssh
- l'execution du script d'anonymisation des données, car staging n'a pas
  vocation d'etre particulierement protegée

::

    ssh -A staging.mrs.beta.gouv.fr

Envoyer un mail de test
-----------------------

Typiquement pour tester la configuration du serveur de mail::

    docker-compose exec django mrs sendtestemail

Exemples
========

Developpement local
-------------------

Pour executer la meme operation de deploiement et d'installation de prod en
local, en vue de la bidouiller, sans le load-balancer.

Du coup, on va pas mal tordre l'execution qui est faite en CI dans cet
objectif::

    export LFTP_DSN=ftp://localhost
    export RESTIC_PASSWORD=lol
    export RESTIC_REPOSITORY=/tmp/backup/mrs-production-restic
    export POSTGRES_BACKUP=/tmp/backup/mrs-production-postgres
    export SECRET_KEY=notsecret
    export BASICAUTH_DISABLE=1
    export HOST=localhost:8000
    export ALLOWED_HOSTS=127.0.0.1,localhost
    bigsudo ansible/deploy.yml home=/tmp/testmrs compose_django_ports='["8000:8000"]' compose_django_build= compose_django_image=betagouv/mrs:master compose=docker-compose.yml,docker-compose.persist.yml

``LFTP_DSN``
    Le DSN de connection a passer a LFTP pour qu'il upload les backups chiffrées

``RESTIC_PASSWORD``
    Le mot de passe de chiffrement de backups

``RESTIC_REPOSITORY``
    Le chemin vers le repo de backups

``POSTGRES_BACKUP``
    Le chemin dans lequel postgres doit dumper ses data

``SECRET_KEY``
    La clef secrete avec laquelle les mots de passes sont chiffrés

``ALLOWED_HOSTS``
    La liste des hostnames que le serveur est censé accepter. Toute requete
    recue par le serveur dont le host name ne correspond pas prendra direct une
    403.

``HOST``
    Le host que le healthcheck doit verifier.

``BASICAUTH_DISABLE``
    Desactiver le HTTP Basic Auth sur ce deploiement, a noter que le Basic Auth
    se base sur les utilisateurs en base de données.

``bigsudo``
    Le generateur de ligne de commandes Ansible, a installer avec pip

``ansible/deploy.yml``
    C'est le script de deploiement en ansible

``home=/tmp/testmrs``
    Que le deploiement persiste dans ce dossier (en prod: /home/mrs-production)

``compose_django_ports='["8000:8000"]'``
    Cela permet au deploiement d'etre utilisable sans load balancer en
    l'exposant sur le port 8000 de localhost

``compose_django_build=``
    Annule la configuration de build: on ne veut pas qu'il essaye de builder en production

``compose_django_image=betagouv/mrs:master``
    Image a deployer: vu qu'on ne veut pas la builder en prod

``compose=docker-compose.yml,docker-compose.persist.yml``
    Liste des fichiers compose a fusionner pour la configuration finale de ce deploiement
