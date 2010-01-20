================
django_live_edit
================

I found Christian Hellsten's jquery-in-place-edit_ library and I meant to write an integration demo with Django many, many moons ago.  After randomly stumbling on it again today, I still needed to scratch this itch.  The templates included are a slightly modified version of Christian's examples.

The ``app`` project is just a starter project to test the demo.  Nothing more, nothing less.


TODO
====

- consider making a reusable app
- check that user submitting content owns the item
- create an app/model access list to keep people from guessing apps/models/fields to post random data to
- better error checking
- detect success or fail in the json post and handle that
- better working examples
- tests


License
=======

django_live_edit is released under the new-style BSD license.


.. _jquery-in-place-edit: http://github.com/christianhellsten/jquery-in-place-edit

