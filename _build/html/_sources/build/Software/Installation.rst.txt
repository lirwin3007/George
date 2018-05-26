Installation
============

George's software is designed to be installed on a raspberry pi 3.

It is recommended to install George's software within a python virtual environment. If you do not wish to do this, skip this first section.

Virtual Environment Setup
-------------------------

Firstly, ensure dependencies are installed for using virtual environments

.. code-block:: console

   sudo pip install virtualenv virtualenvwrapper
   
Create a virtual environment, any name can be used instead of 'George', however 'George' will be consistently used throughout this documentation.

.. code-block:: console

   mkvirtualenv George
   workon George
   
Installing the Software
-----------------------

The software will be installed in the folder 'George' stored in the home directory, so create this:

.. code-block:: console

   cd ~
   mkdir George
   cd George

Then clone the GitHub repo:

.. code-block:: console

   git clone https://github.com/lirwin3007/George
   
And finally install the required dependencies:

.. code-block:: console

   pip install -r requirements.txt
   
Next Steps
----------

More detail about George's software can be found on the software documentation: http://bipedal-george.readthedocs.io/en/latest/index.html