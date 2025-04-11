Setting Up The Developer Environment
====================================

.. _getting-started-dev:

Getting development started
---------------------------

Solidipes is a project that is currently developed and tested on Linux. For this reason we recommend using Linux, or WSL on Windows (`Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_).  For this reason, the installation instructions below are only for Linux.


Creating a development Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To separate this project from other ones you may have on your computer and avoid package conflicts, it is best to create a Python virtual environment, using for example Anaconda or the Built-in Python venv module.

- :ref:`create-conda-environment`

- :ref:`venv-env`


Once you have created your environment, you can proceed to install Solidipes.


Installing `solidipes` for development
--------------------------------------

Dependencies
~~~~~~~~~~~~

* Python (3.8 minimum)
* make

If you want to add Python dependencies, you also need:

* `Poetry <https://python-poetry.org/docs/#installation>`_


Installation
~~~~~~~~~~~~

.. code-block:: bash

   git clone https://gitlab.com/solidipes/solidipes.git
   cd solidipes
   make install

This will install Solidipes as well as all the Python development dependencies. It will also fetch Solidipes plugins in the ``plugins`` directory.


Verifying the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the ``solidipes`` command to ensure it's installed and working correctly::

      solidipes --help


Enable auto-completion
~~~~~~~~~~~~~~~~~~~~~~

If you are using *bash* or *zsh* as your shell, you can enable TAB completion for the ``solidipes`` command by running::

    activate-global-python-argcomplete

You may need to run this command as ``sudo`` or with the ``--user`` flag.
::

    activate-global-python-argcomplete --user
    #or
    sudo activate-global-python-argcomplete
