Tweet Lamp
==========

During the Curso de Arduino UFRJ (an [Arduino course](http://www.CursoDeArduino.com.br/) at Universidade Federal do Rio de Janeiro the students had the idea to control an AC light bulb using Twitter, so we developed this little projects in near 1 hour!



Archietcture
------------

The project have a simple architecture as follows:

    [PC with Python program] <--- USB ---> Arduino <--- relay module ---> AC lamp


PC code (in Python)
-------------------

This software does a search in Twitter and, based on the last tweet it find, send a message to Arduino via USB with what should be the state of the lamp.


Arduino Code
============

Just receives the command from Python software and turn HIGH or LOW the digital port 13.


The circuit
===========

You could attach everything to the Arduino that can be controlled by Twitter. In our experiment we attached a relay module to the digital port 13. Then, the relay module activates or deactivates the AC lamp.
