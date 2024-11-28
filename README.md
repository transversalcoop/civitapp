Civitapp
========

Civitapp és una plataforma web per a l'acompanyament de processos de dinamització
comunitària. La plataforma planteja una sèrie de preguntes amb respostes tancades de tipus
ABCD, agrupades per diverses temàtiques, i per a cada resposta dóna consells sobre com dur
a terme el procés de dinamització.

Una propietat fonamental de la plataforma és que és _adaptable_ a altres realitats. És a
dir, la plataforma parteix d'uns temes, preguntes i respostes bàsics, però que es poden
adaptar a altres realitats. Això es pot fer gràcies a que el projecte està publicat com a
programari lliure, i també al fet que el contingut en si es pot editar.

Per adaptar la plataforma a una altra realitat, cal seguir a grans trets els següents
passos, que es desenvolupen posteriorment:

1. Crear un _fork_ d'aquest repositori de Github.
2. Editar el contingut de l'aplicació
3. Crear la imatge de Docker de l'aplicació
4. Configurar el domini
5. Executar la imatge de Docker


Crear un _fork_
---------------

El primer pas és crear un _fork_ o, dit d'altra manera, duplicar aquest repositori. La
plataforma Github permet fer-ho de manera senzilla sempre que es dispose d'un usuari,
simplement polsant al menú de «Fork» dalt a la dreta de la pàgina i després polsant
«Create a new fork». El propi Github demanarà alguns detalls més, després del qual ja es
disposarà d'un repositori propi. Per més detalls, es pot consultar [aquest
document](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).


Editar el contingut
-------------------

El centre de Civitapp es troba en l'arxiu `populate_content.py`, dins de la carpeta
`civitapp/management/commands`. En aquest arxiu es poden trobar tots els temes,
preguntes, respostes, i consells. Aquests es poden editar per canviar el redactat, i
també es poden eliminar o afegir-ne de nous. Per fer-ho només cal un editor de text.


Crear la imatge de Docker
-------------------------

Civitapp està completament preparat per a funcionar dins d'un contenidor de Docker. Per
fer-ho, primer cal crear-ne una imatge. Després d'haver modificat el contingut de
`populate_content.py` i qualsevol altra cosa que es considere oportú, només cal generar la
imatge com és habitual, executant:

    docker build . -t civitapp


Configurar el domini
--------------------

Per fer funcionar l'aplicació en una web pròpia és necessari comprar i configurar un
domini. Això es pot fer en múltiples proveïdors d'internet, en els quals es pot comprar el
nom de domini que es considere, i que després proveïrà una manera de configurar-lo.

Una vegada comprat el domini cal configurar-lo perquè «apunte» a la direcció IP des d'on
se servirà la web. Hi ha principalment dos maneres de fer-ho.

En la primera manera, es disposa d'un servidor propi on executar l'aplicació. En aquest
cas, cal afegir un registre A a la zona DNS del domini amb la IP del servidor. Una vegada
fet, en el servidor cal configurar un servidor web, com per exemple Nginx, per gestionar
les peticions rebudes al domini. A més, cal crear i configurar un certificat per poder
servir la web a través d'una connexió segura HTTPS. Per fer-ho es pot fer servir el
programa [certbot](https://certbot.eff.org/), que simplifica molt el procés. Aquest
servidor web només ha de redirigir totes les peticions al port on es configure el docker,
com s'explica en el punt següent.

En la segona, es fa servir un proveïdor de tipus _Platform As A Service_ (PAAS), com per
exemple Heroku. Cada proveïdor disposa de les seues pròpies instruccions sobre com
configurar els dominis.


Executar la imatge de Docker
----------------------------

Aquest pas es pot fer principalment de dos maneres diferents, a l'igual que el pas
anterior de configuració del domini. En la primera, en cas de disposar d'un servidor,
només cal pujar la imatge al servidor i executar-la fent servir `docker compose`. A
continuació s'ofereix un exemple d'arxiu `docker-compose.yml` que es podria fer servir per
fer funcionar l'aplicació:

    {
      "services": {
        "civitapp": {
          "image": "${CIVITAPP_IMAGE}",
          "command": "bash -c 'python /code/manage.py migrate && gunicorn config.wsgi -b 0.0.0.0 --workers=1 --threads=1'",
          "volumes": [
            "civitapp_data:/code/database/"
          ],
          "ports": [
            "127.0.0.1:${CIVITAPP_PORT}:8000"
          ],
          "environment": [
            "PYTHONDONTWRITEBYTECODE=true",
            "WEB_RELOAD=false",
            "DJANGO_SECRET_KEY=${CIVITAPP_KEY}",
            "DJANGO_DEBUG=false",
            "DJANGO_BASE_URL=https://${CIVITAPP_DOMAIN}",
            "DJANGO_ALLOWED_HOSTS=${CIVITAPP_DOMAIN}",
            "DJANGO_ALLOWED_CSRF=https://${CIVITAPP_DOMAIN}",
            "DJANGO_CONN_MAX_AGE=60",
            "DJANGO_ADMINS=${CIVITAPP_ADMIN}",
            "DJANGO_MANAGERS=${CIVITAPP_ADMIN}",
          ]
        }
      },
      "volumes": {
        "civitapp_data": {}
      }
    }

Com es pot veure, en l'arxiu es fa referència a diverses variables d'entorn, que poden
estar configurades en l'entorn des d'on s'executa o en un arxiu `.env`. Les variables que
cal configurar son les següents:

- `CIVITAPP_IMAGE`: el nom que se li haja donat a la imatge de docker creada anteriorment,
  per exemple, civitapp.
- `CIVITAPP_PORT`: el port que es vulga fer servir i que s'haja configurat al servidor web,
  per exemple, el 8000.
- `CIVITAPP_KEY`: una cadena de caràcters aleatòria i llarga (mínim 40 caràcters). Pot ser
  qualsevol cosa, sempre que siga realment aleatòria i es guarde com un secret.
- `CIVITAPP_DOMAIN`: el domini que s'haja comprat i configurat; civitapp.social podria ser
  un bon domini.
- `CIVITAPP_ADMIN`: el correu electrònic de la persona que haja d'estar pendent de que
  l'aplicació funcione.

En la segona manera, en cas de fer servir un proveïdor PAAS, cada proveïdor ofereix unes
instruccions de com executar una imatge de Docker, però que en general és similar a
l'explicada per al servidor, és a dir, enviar la imatge de Docker i configurar les
variables d'entorn necessàries, que serien les mateixes que s'acaben d'explicar.

