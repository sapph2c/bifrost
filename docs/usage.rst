Usage
=====

.. _installation:

Installation
------------

To use Bifrost, first install the python dependencies using pip:

.. code-block:: console

   (.venv) $ pip install -r requirements.txt

.. note::

   Docker and docker-compose are used to run the webserver and reverse proxy,
   so make sure you have both installed before you continue.

Launching the server
--------------------

Make sure the docker service is running

.. code:: bash

   sudo systemctl restart docker.service

Start the nginx reverse proxy and Flask app containers

.. code:: bash

   sudo docker-compose up

Navigate to the local signup endpoint

::

  https://127.0.0.1:5000/signup

Register a user and login to go to the dashboard

Running an agent
----------------

Nagivate from the project root to src/agent and execute the binary

.. code:: bash
   
  ./agent
