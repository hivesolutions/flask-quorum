Quorum Extensions for Flask
===========================

A small extension framework for Flask to easy a series of simple tasks.

.. toctree::
   :maxdepth: 2

   introduction
   changelog
   api/api
   glosary

Installation
============

Install using setuptools, e.g. (within a virtualenv)::

  $ easy_install quorum

Example
=======

.. code-block:: python

    import flask
    import quorum

    app = quorum.load(
        name = __name__
    )

    @app.route("/", methods = ("GET",))
    def index():
        return flask.render_template("index.html.tpl")

    if __name__ == "__main__":
        quorum.run()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
