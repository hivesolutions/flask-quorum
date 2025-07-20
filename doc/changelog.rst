Changelog
=========

List the complete set of changes to the quorum project since it's creation.

Current Versions
----------------

0.8.6
^^^^^

    * Logging methods better handle conditional formatting

0.8.5
^^^^^

    * Support for `description` in task creation

0.8.4
^^^^^

    * Support for loading of `.env` files
    * Support for `save()` and `open()` methods in `File` class
    * Fixed warning on regex compilation
    * Fixed jinja2 compatibility issues

0.8.3
^^^^^

    * Made code compliant with `black`

0.8.2
^^^^^

    * Support for multiple items in the `sort` field
    * Support for `id` as a fallback secondary sorter
    * Changed structure of the ReadTheDocs configuration

0.8.1
^^^^^

    * Fixed Incompatibilities with Flask 2.3+

0.8.0
^^^^^

    * Support for the `basic_auth()` method
    * Support for the `date.py` module and the `format_delta` function
    * Renamed repository to `flask-quorum`

0.7.0
^^^^^

    * Safer check for integer value in Excel

0.6.4
^^^^^

    * Fixed support for `count_documents` in `PyMongo>=4`

0.6.3
^^^^^

    * Fixed issue related with PyMongo version parsing

0.6.2
^^^^^

    * Made client side sessions more stable, by patching some global session related configurations

0.6.1
^^^^^

    * Support for version printing at startup

0.6.0
^^^^^

    * Major 0.6.0 release
    * Fixed critical issues with deep nested relations

0.5.36
^^^^^^

    * Fixed issue with pypy

0.5.35
^^^^^^

    * Added compatibility with TinyDB 4

0.5.34
^^^^^^

    * Dynamic template loading for SMTP

0.5.33
^^^^^^

    * Small improvements

0.5.32
^^^^^^

    * Improved pyMongo integration
    * Support for context in configuration
    * Better `verify` functions

0.5.31
^^^^^^

    * Support for the default field in the to_locale method

0.5.30
^^^^^^

    * Small set of fixes

0.5.29
^^^^^^

    * New |unset filter

0.5.28
^^^^^^

    * Bug fixes

0.5.27
^^^^^^

    * Improved quality of the HTTP client
    * Generators as input for HTTP requests
    * Support for Flask 1.0.x
    * Bug fixes

0.5.26
^^^^^^

    * Support for secure headers
    * Bug fixes

0.5.25
^^^^^^

    * Support for clusters in Pusher

0.5.24
^^^^^^

    * Fixed some bugs related with data structures

0.5.23
^^^^^^

    * Fixed some bugs

0.5.22
^^^^^^

    * Fixed some bugs, related with HTTP client

0.5.21
^^^^^^

    * Fixed some bugs

0.5.20
^^^^^^

    * Fixed some bugs
    * Support for better OrderedDict structure

0.5.19
^^^^^^

    * Fixed problem with the SERVER_NAME config value generation

0.5.18
^^^^^^

    * Fixed issue with default port and URL generation

0.5.17
^^^^^^

    * Support for BASE_URL and _external URL generation

0.5.16
^^^^^^

    * Small context ensure fixes

0.5.15
^^^^^^

    * Simplified ensure_context decorator

0.5.14
^^^^^^

    * New support for minute and hour based work

0.5.13
^^^^^^

    * New ensure_context() function

0.5.12
^^^^^^

    * Fixed AMQP issues

0.5.11
^^^^^^

    * Small legacy fixes

0.5.10
^^^^^^

    * Small fixes in form loading

0.5.9
^^^^^

    * Better ACL structure

0.5.8
^^^^^

    * ACL security fix

0.5.7
^^^^^

    * Small Mime bug fixes

0.5.6
^^^^^

    * Some ACL bug fixes

0.5.5
^^^^^

    * New namespace based ACL

0.5.4
^^^^^

    * New compatibility layer with models

0.5.3
^^^^^

    * Fixed issue with new version of Jinja 2

0.5.2
^^^^^

    * Support for multiple indexes

0.5.1
^^^^^

    * Some bug fixes for indexes

0.5.0
^^^^^

    * Improved overall stability
    * Added support for more indexes in Mongo

0.4.15
^^^^^^

    * Small set of fixes

0.4.14
^^^^^^

    * Small set of fixes in RabbitMQ to AMQP migration

0.4.13
^^^^^^

    * Renamed RabbitMQ to AMQP

0.4.12
^^^^^^

    * Removed extra print statements

0.4.11
^^^^^^

    * New model structure
    * Fixed issues with locales

0.4.10
^^^^^^

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
^^^^^^

    * Fixed major issue

0.3.21
^^^^^^

    * Major changes in data layer

0.3.20
^^^^^^

    * Fixed memory leak

0.3.19
^^^^^^

    * Fixed issue in xls conversion

0.3.18
^^^^^^

    * Better xls conversion
    * Minor bug fixes

0.3.17
^^^^^^

    * Better persistence model
    * Minor bug fixes

0.3.16
^^^^^^

    * New map like access support for models

0.3.15
^^^^^^

    * Fixed issue with filtering

0.3.14
^^^^^^

    * New support for travis

0.3.13
^^^^^^

    * Fixed bug related with http client

0.3.12
^^^^^^

    * Fixed bug related with email sending

0.3.11
^^^^^^

    * Bug fix related with async based redirection

0.3.10
^^^^^^

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
