Configuration Variables
=======================

Global
------

.. rst:directive:: .. DEBUG:: boolean (default = False)

    If the application should be ran under the run mode.

.. rst:directive:: .. PORT:: integer (default = 5000)

    The port to be used by the default http server when
    binding to the socket.

    .. note::

        The :rst:dir:`PORT` value is not used when running in contained **WSGI**.

.. rst:directive:: .. HOST:: string (default = "127.0.0.1")

    The port to be used by the default http server when
    binding to the socket. This value may be `0.0.0.0`
    in case the user want to bind to every interface on
    the system (may be insecure).

    .. note::

        The :rst:dir:`HOST` value is not used when running in contained **WSGI**.

E-mail / SMTP
-------------

.. rst:directive:: .. SMTP_HOST:: string

    Hostname or IP address of the server to be used as gateway
    for sending smtp messages (e-mails) under quorum.

    This value may contain an optional port value separated by
    a **:** character.

.. rst:directive:: .. SMTP_USER:: string

    Username to be used in the authentication process on the SMTP
    connections used for sending email messages.

    .. note::

        Most of the times the username is an email address and as such
        it's also used as the default fallback value for the sender
        value for outgoing emails.

.. rst:directive:: .. SMTP_PASSWORD:: string

    Password to be used in the authentication process on the SMTP
    connections used for sending email messages.

MongoDB
-------

.. rst:directive:: .. MONGOHQ_URL:: string

    The url to be used for the establishment of connection to the
    MongoDB server. It must contain authentication information, host,
    port and optionally the default database to be used.

    .. note::

        An example url for mongo would be something like
        **mongodb://root:root@db.hive:27017**.

Redis
-----

.. rst:directive:: .. REDISTOGO_URL:: string

    TODO

RabbitMQ / AMQP
---------------

.. rst:directive:: .. CLOUDAMQP_URL:: string

    TODO

Amazon Web Services
-------------------

.. rst:directive:: .. AMAZON_ID:: string

    TODO

.. rst:directive:: .. AMAZON_SECRET:: string

    TODO

.. rst:directive:: .. AMAZON_BUCKET:: string

    TODO
