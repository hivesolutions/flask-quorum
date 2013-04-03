Configuration Variables
=======================

Global
------

.. rst:directive:: .. DEBUG:: boolean

    If the application should be ran under the run mode.

.. rst:directive:: .. PORT:: integer

    The port to be used by the default http server when
    binding to the socket.

    .. note::

        This :rst:dir:`PORT` value is not used when running in contained WSGI.

.. rst:directive:: .. HOST:: string

    The port to be used by the default http server when
    binding to the socket. This value may be `0.0.0.0`
    in case the user want to bind to every interface on
    the system (may be insecure).

    .. note::

        This :rst:dir:`HOST` value is not used when running in contained WSGI.

E-mail / SMTP
-------------

.. rst:directive:: .. SMTP_HOST:: string

    Hostname or IP address of the server to be used as gateway
    for sending smtp messages (e-mails) under quorum.

    This value may contain an optional port value separated by
    a **:** character.

.. rst:directive:: .. SMTP_USER:: string

    Username to be used in the authentication process on the SMTP
    connections used for sending emails.

.. rst:directive:: .. SMTP_PASSWORD:: string

    TODO

MongoDB
-------

.. rst:directive:: .. MONGOHQ_URL:: string

    TODO

    .. note::

        An example url for mongo would be something like
        **mongodb://root:root@db.hive:27017**.
