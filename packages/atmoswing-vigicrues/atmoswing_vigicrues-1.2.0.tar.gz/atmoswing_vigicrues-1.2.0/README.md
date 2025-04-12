# atmoswing-vigicrues

[![GitHub release](https://img.shields.io/github/v/release/atmoswing/atmoswing-vigicrues)](https://github.com/atmoswing/atmoswing-vigicrues)
[![PyPI](https://img.shields.io/pypi/v/atmoswing-vigicrues)](https://pypi.org/project/atmoswing-vigicrues/)
[![Docker Image Version](https://img.shields.io/docker/v/atmoswing/atmoswing-vigicrues)](https://hub.docker.com/r/atmoswing/atmoswing-vigicrues)
![Static Badge](https://img.shields.io/badge/python-%3E%3D3.7-blue)
   
Module Python pour l'intégration d'AtmoSwing dans le réseau Vigicrues.

Documentation API: http://atmoswing.org/atmoswing-vigicrues


Objectif
--------

Le module a pour but la gestion du flux de la prévision par AtmoSwing. Il permet :

* de télécharger les fichiers de sortie de modèles météo (p. ex. GFS),
* de transformer de tels fichiers en un format netCDF générique,
* d'exécuter les prévisions par AtmoSwing,
* d'extraire les résultats en d'autres formats (p.ex. json),
* et de diffuser ces fichiers par SFTP.


Installation
------------

Pour utiliser le module atmoswing-vigicrues, il faut installer :

* Python >= 3.7
* AtmoSwing Forecaster (de préférence la version serveur)
* Le module atmoswing-vigicrues (``pip install atmoswing-vigicrues`` ou l'image docker ``docker pull atmoswing/atmoswing-vigicrues``)

Utilisation
-----------

Le paquet est constitué de plusieurs modules qui peuvent être activés et configurés dans un fichier de configuration. Plusieurs flux de prévision peuvent être configurés sur un serveur / PC par la création de différents fichiers de configuration. Il n’y a pas de paramètres codés en dur dans le code. L’exécution d’un flux de prévision est effectuée par la commande :

```
python -m atmoswing_vigicrues --config-file="chemin/vers/fichier/config.yaml
```

Le fichier de configuration définit :

* Les propriétés de la prévision par AtmoSwing
* Les pré-actions : les actions à effectuer préalablement à la prévision par AtmoSwing
* Les post-actions : les actions à effectuer après la prévision par AtmoSwing
* Les disséminations : les actions de transfert des résultats

Le flux de la prévision est le suivant :

1. pré-actions
2. prévision par AtmoSwing
3. post-actions
4. diffusion

Documentation API: http://atmoswing.org/atmoswing-vigicrues
