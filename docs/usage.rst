Usage
=====

.. _installation:

Installation
------------

.. note::

   Pip is required in this step and it's recommended to run within a virtual environment.

To use Bifrost, first install the python dependencies:

.. code-block:: console

   (.venv) $ make init

Launching the server
--------------------

.. note::

   Docker and docker-compose are used to run the webserver and reverse proxy,
   so make sure you have both installed before you continue.

Start the nginx reverse proxy and Flask app containers:

.. code-block:: console

   (venv) $ make deploy


Navigate to the local signup endpoint

::

  https://127.0.0.1:5000/signup

Register a user and login to go to the dashboard

Running an agent
----------------

Nagivate from the project root to src/agent and execute the binary

.. code:: bash
   
  ./agent
