Changelog
=========

List the complete set of changes to the quorum project since it's creation.

Current Versions
----------------

0.5.1
^^^^^

    * Some bug fixes for indexes

0.5.0
^^^^^

    * Improved overall stability
    * Added support for more indexes in Mongo

0.4.15
^^^^^

    * Small set of fixes

0.4.14
^^^^^

    * Small set of fixes in RabbitMQ to AMQP migration

0.4.13
^^^^^

    * Renamed RabbitMQ to AMQP

0.4.12
^^^^^

    * Removed extra print statements

0.4.11
^^^^^

    * New model structure
    * Fixed issues with locales

0.4.10
^^^^^

    * New configuration infra-structure

0.4.9
^^^^^

    * Fixed another build issue

0.4.8
^^^^^

    * Fixed issue with deployment

0.4.7
^^^^^

    * New dump all support in typesf

0.4.6
^^^^^

    * Fixed issue related with locales

0.4.5
^^^^^

    * Support for locales in exceptions

0.4.4
^^^^^

    * Fixed major bug with file type

0.4.3
^^^^^

    * Lots of bug fixes
    * Better export of database

0.4.2
^^^^^

    * Better structure for map based models

0.4.1
^^^^^

    * Better resolution of models

0.4.0
^^^^^

    * Small set of issue fixes

0.3.22
^^^^^

    * Fixed major issue

0.3.21
^^^^^

    * Major changes in data layer

0.3.20
^^^^^

    * Fixed memory leak

0.3.19
^^^^^

    * Fixed issue in xls conversion

0.3.18
^^^^^

    * Better xls conversion
    * Minor bug fixes

0.3.17
^^^^^

    * Better persistence model
    * Minor bug fixes

0.3.16
^^^^^

    * New map like access support for models

0.3.15
^^^^^

    * Fixed issue with filtering

0.3.14
^^^^^

    * New support for travis

0.3.13
^^^^^

    * Fixed bug related with http client

0.3.12
^^^^^

    * Fixed bug related with email sending

0.3.11
^^^^^

    * Bug fix related with async based redirection

0.3.10
^^^^^

    * Compatibility fixes

0.3.9
^^^^^

    * Compatibility fixes
    * Support for new pymongo interface

0.3.8
^^^^^

    * Better email address support with format


0.3.7
^^^^^

    * Support for model duplicate attribute validation


0.3.6
^^^^^

    * New support for session file path definition

0.3.5
^^^^^

    * Better configuration overriding

0.3.4
^^^^^

    * Fixed problem in http naming collision

0.3.3
^^^^^

    * New handler retrieval function

0.3.2
^^^^^

    * Refactor of the configuration infra-structure

0.3.1
^^^^^

    * Fix in legacy support

0.3.0
^^^^^

    * Major code re-structure
    * New Apache based license

0.2.6
^^^^^

    * New set of bug fixes
    * Fixed issue in memory based log

0.2.5
^^^^^

    * Support for new HTTP client

0.2.4
^^^^^

    * Major bug fix with ``count`` fixed

0.2.3
^^^^^

    * Improved overall stability of the system


0.2.2
^^^^^

    * Improved the email structure

0.2.1
^^^^^

    * Minimal stability improvements

0.2.0
^^^^^

    * Initial support for ``Python 3.0+``
    * More stability in the infra-structure

0.1.8
^^^^^

    * New support for :func:`quorum.exists_amazon_key` and :func:`quorum.clear_amazon_bucket` calls
    * Better unit testing for ``amazon.py``
    * Support for the SERVER_* environment variables

0.1.7
^^^^^

    * Better signature for :func:`quorum.send_mail`
    * Improved asynchronous mode under :func:`quorum.send_mail_a`
    * New support for :func:`quorum.delete_amazon_key` calls

0.1.6
^^^^^

    * Support for Amazon S3 using `boto <http://docs.pythonboto.org/>`_
    * Experimental documentation

Older Versions
--------------

0.1.5
^^^^^

    * Initial support for ``mongodb``

0.1.4
^^^^^

    * Legacy support values

0.1.3
^^^^^

    * Legacy support values

0.1.1
^^^^^

    * Legacy support values

0.1.0
^^^^^

    * Initial release
    * First specification of the framework
