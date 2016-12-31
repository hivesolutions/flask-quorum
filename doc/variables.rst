Configuration Variables
=======================

Global
------

.. rst:directive:: .. NAME:: string (default = None)

    String that is going to be used to identify the app
    for the internal structures a fallback value should
    be defined by the developer of the app.

.. rst:directive:: .. INSTANCE:: string (default = None)

    The descriptive value of the instance that is going
    to be executed. This value should provide the required
    mechanisms to correctly separate to virtually different
    running instance (eg: databases, log files, etc.).

.. rst:directive:: .. LEVEL:: string (default = "INFO")

    Defines the verbosity level that is going to be used while
    running the application's logger. It also provides a way of
    defining if the application is running for production where
    production is `INFO` or more verbose levels.

.. rst:directive:: .. DEBUG:: boolean (default = False)

    If the application should be ran under the run mode.

    .. note::

        This variable is considered to be deprecated and the
        :rst:dir:`LEVEL` variable should be used instead with
        the DEBUG level set.

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

Mail / SMTP
-----------

.. rst:directive:: .. SMTP_HOST:: string

    Hostname or IP address of the server to be used as gateway
    for sending smtp messages (e-mails) under quorum.

    This value may contain an optional port value separated by
    a **':'** character.

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

    The URL that described the connection to be used with the REDIS
    key value database, this URL is going to be used under the
    redis-py infra-structure.

    .. note::

        An example url for rabbit would be something like
        **redis://root:root@db.hive**.


RabbitMQ / AMQP
---------------

.. rst:directive:: .. AMQP_URL:: string

    URL used by the AMQP library (pika) to create the connection with
    the server that is going to be used in the session. It should contain
    both authentication and location information.

    .. note::

        An example url for amqp would be something like
        **amqp://root:root@amqp.hive**.

Amazon Web Services
-------------------

.. rst:directive:: .. AMAZON_ID:: string

    Identifier of the Amazon S3 account to be sued for the connection, this
    should comply with the expected string values.

.. rst:directive:: .. AMAZON_SECRET:: string

    The secret value of the account to be used, this value should be kept
    secret from any external person to avoid security problems.

.. rst:directive:: .. AMAZON_BUCKET:: string

    The name of the bucket where file of the current application are going
    to be stored. Currently there's no support for multiple buckets per one
    application scope.

Pusher
-------------------

.. rst:directive:: .. PUSHER_APP_ID:: string

    TODO

.. rst:directive:: .. PUSHER_KEY:: string

    TODO

.. rst:directive:: .. PUSHER_SECRET:: string

    TODO
