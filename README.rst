Pelix Web Console
#################

This project provides a Web UI to manage and monitor an instance of a
`Pelix/iPOPO <https://ipopo.coderxpress.net/>`_ framework.


How to use it
=============

#. Install Pelix:
   ``pip install iPOPO``
#. Clone this repository
#. In the top directory, run the Pelix Shell using the ``run.txt``
   initialization file:
   ``python -m pelix.shell --init run.txt``
#. Go to http://localhost:8080/


Dependencies
============

Python
------

* `iPOPO <https://ipopo.coderxpress.net/>`_


JavaScript
----------

The JavaScript part is compiled from a TypeScript file, ``app.ts``.

* `Bootstrap <http://getbootstrap.com/>`_

  * The whole interface is based on the
    `Dashboard <http://getbootstrap.com/examples/dashboard/>`_ example.

* `jQuery <http://jquery.com/>`_
* `jQuery Table Sorter <http://mottie.github.io/tablesorter/docs/index.html>`_
