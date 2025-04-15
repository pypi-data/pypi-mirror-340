"""
signals for :mod:`django_notifications` application.

:creationdate:  14/04/2025 14:17
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.signals
"""

import logging
from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django_notifications import models

logger = logging.getLogger(__name__)
__author__ = "fguerin"


@receiver(post_delete, sender=models.Attachment)
def delete_attachments(sender, instance: models.Attachment, **kwargs):
    """Delete attachment file on :class:`django_notifications.models.Attachment` deletion."""
    _path = Path(instance.attachment_file.path)
    if _path.exists():
        _path.unlink()
        logger.info("delete_attachment(%s) File '%s' deleted.", instance, _path)
