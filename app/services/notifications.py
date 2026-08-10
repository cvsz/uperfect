"""Retryable LINE notification outbox with no client-side secret handling."""

from __future__ import annotations

from collections.abc import Callable

from app.repositories import Repository
from app.schemas import DeliverySummary


NotificationSender = Callable[[str, str], None]


class NotificationService:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def enqueue(self, destination: str, body: str, event_type: str = "generic") -> str:
        return self.repository.add_notification(event_type, destination, body)

    def deliver_pending(self, sender: NotificationSender) -> DeliverySummary:
        sent = 0
        failed = 0
        for event in self.repository.pending_notifications(limit=20):
            try:
                sender(event["destination"], event["body"])
            except Exception as error:  # noqa: BLE001 - failure must remain retryable
                self.repository.record_notification_failure(event["id"], str(error))
                failed += 1
            else:
                self.repository.mark_notification_sent(event["id"])
                sent += 1
        return DeliverySummary(sent=sent, failed=failed, remaining=self.pending_count())

    def pending_count(self) -> int:
        return self.repository.pending_notification_count()

    def list_pending(self) -> list[dict[str, object]]:
        return self.repository.pending_notifications()
