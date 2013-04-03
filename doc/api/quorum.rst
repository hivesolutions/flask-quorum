quorum
======

.. autodata:: quorum.APP

    The reference to the top level application object
    that is being handled by quorum. This value is used
    across the quorum infra-structure to access flask
    data and capabilities.

    .. note::

        Changing this value directly should be done with
        care as it may create undesired results. To set/start
        this value use the :func:`quorum.load` function instead.

.. autofunction:: quorum.load

.. autofunction:: quorum.unload

.. autofunction:: quorum.send_mail

.. autofunction:: quorum.send_mail_a

.. py:function:: enumerate(sequence[, start=0])

    Return an iterator that yields tuples of an index and an item of the
