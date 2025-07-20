Introduction
============

Goals and Focus
***************

The focus of this project was to create a lightweight yet powerful helper layer on top of Flask that stream-lines everyday web-development tasks. It provides sensible defaults and a familiar, Pythonic API so that developers can focus on implementing business logic instead of boiler-plate.

Overview
********

`Flask-Quorum` (usually imported as ``quorum``) bundles a collection of utilities, conventions and thin wrappers that we use in production every day at Hive Solutions.  Among other things, it offers:

* Project boot-strapping helpers (``quorum.load`` / ``quorum.run``)
* Declarative routing that mirrors Flask’s decorator style
* Seamless model integration with MongoDB, Redis and SQL stores
* Background task scheduling with a dead-simple decorator (see below)
* Common helpers for configuration, logging, mailing and more

If you enjoy Flask’s simplicity but keep re-writing the same glue code across projects, `Flask-Quorum` is for you.

Installation
************

The package is published to PyPI, so installation is as straightforward as:

.. code-block:: console

   $ pip install quorum

Alternatively, you may install directly from the repository for the latest (possibly unstable) version:

.. code-block:: console

   $ pip install git+https://github.com/hivesolutions/flask-quorum.git@master

Quick-Start Example
*******************

Below is the canonical "hello, world" example using `quorum.load` and `quorum.run`.  Save it as ``app.py`` and execute ``python app.py``::

    import flask
    import quorum

    app = quorum.load(name=__name__)

    @app.route("/", methods=("GET",))
    def index():
        return flask.render_template("index.html.tpl")

    if __name__ == "__main__":
        quorum.run()

Background Tasks
****************

Need a simple scheduler?  Any function decorated with :pyfunc:`quorum.background` will execute every *n* seconds in a dedicated thread::

    @quorum.background(timeout=1.0)
    def hello_recursive():
        print("hello world")

This is perfect for cache warm-ups, periodic clean-ups and other lightweight jobs that do not justify a full-blown task queue.

Building the Documentation
**************************

The documentation sources live in the ``doc/`` directory and use Sphinx.  To build the HTML version locally run:

.. code-block:: console

   $ sphinx-build -b html doc doc/_build

The rendered docs will be available under ``doc/_build/index.html``.

Additional Resources
********************

* Source Code: https://github.com/hivesolutions/flask-quorum
* PyPI: https://pypi.org/project/quorum/
* Full Documentation: https://quorum.readthedocs.io

License
*******

`Flask-Quorum` is licensed under the `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.  See the ``LICENSE`` file for full details.
