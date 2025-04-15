"""
clean_notifications for :mod:`django_notifications.management.commands` application.

:creationdate:  14/04/2025 13:35
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_notifications.management.commands.clean_notifications
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from django_notifications import models

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command to remove older notifications."""

    help = "Remove older notifications."  # noqa: A003

    def add_arguments(self, parser) -> None:
        """Add arguments to the parser."""
        parser.add_argument(
            "--dry-run",
            "-n",
            action="store_true",
            default=False,
            help="Do not perform deletions",
        )
        parser.add_argument(
            "--days",
            "-d",
            type=int,
            default=30,
            help="Delete notifications older already sent since <days> days.",
        )

    def handle(self, *args, **options) -> str | None:
        """Handle the command."""
        notifications = models.Notification.objects.filter(
            sent_at__lte=timezone.now() - timedelta(days=options["days"])
        )
        attachments = models.Attachment.objects.filter(notification__in=notifications)
        _notifs_count = notifications.count()
        _attachments_count = attachments.count()
        print(  # noqa: T201
            f"{_notifs_count} notifications and {_attachments_count} are about to be deleted.",
            file=self.stderr,
        )
        if not options["dry_run"]:
            notifications.delete()
            print(  # noqa: T201
                f"{_notifs_count} notifications and {_attachments_count} attachments are DELETED.",
                file=self.stderr,
            )
