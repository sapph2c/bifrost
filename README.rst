.. figure:: docs/img/Bifrost.png
   :alt: Bifrost

   Bifrost

|GitHub license|\ |GitHub stars|\ |Test coverage| 

Getting Started
===============

Basic Overview
**Bifrost** is a Flask app that allows communication between implants
and a centralized command and control server.

Server side:
============

Clone the repo

.. code:: bash

   git clone https://github.com/AshleyNikr/Bifrost.git

Change into the server directory

.. code:: bash

   cd Bifrost/server

Make sure the docker service is running

.. code:: bash

   sudo systemctl restart docker.service

Start the docker container

.. code:: bash

   sudo docker-compose up --force-recreate --build

Naviage to the local signup endpoint

::

   https://127.0.0.1:5000/signup

Client side:
============

Run the implant on the agent

::

   sudo ./implant

Planned Features:
=================

-  Modularity
-  Documentation
-  Group commands

.. |GitHub license| image:: https://img.shields.io/github/license/AshleyNikr/Bifrost
   :target: https://github.com/AshleyNikr/Bifrost/blob/master/LICENSE
.. |GitHub stars| image:: https://img.shields.io/github/stars/AshleyNikr/Bifrost
   :target: https://github.com/AshleyNikr/Bifrost/stargazers
.. |Test coverage| image:: docs/img/coverage.svg
