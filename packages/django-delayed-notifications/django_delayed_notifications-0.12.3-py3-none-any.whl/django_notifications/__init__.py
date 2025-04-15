"""
Application to manage notifications.

.. note::
  This application allow to create notification emails

.. image:: _images/models.png
   :width: 100%
   :align: center

:copyright: (c) 2022 by François GUÉRIN
:license: mit, see LICENSE for more details.
:creationdate: 06/01/2022 11:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications

"""

from .__about__ import __version__

VERSION = __version__


__all__ = [
    "__version__",
    "VERSION",
]
