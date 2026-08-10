from decimal import Decimal

import pytest

from app.database import Database
from app.repositories import Repository


@pytest.fixture()
def repository(tmp_path):
    database = Database(str(tmp_path / "repository.db"))
    database.initialize()
    return Repository(database)


def test_product_keyword_lookup_returns_seeded_product(repository):
    matches = repository.find_keyword_matches("วิตซีโลเอ้")

    assert matches[0].id == "LOE_VITC_SERUM"
    assert matches[0].matched_alias == "วิตซีโลเอ้"


def test_conversation_creation_is_unique_for_platform_and_customer(repository):
    first = repository.get_or_create_conversation("facebook", "customer-1")
    second = repository.get_or_create_conversation("facebook", "customer-1")

    assert first.id == second.id


def test_webhook_claim_is_idempotent(repository):
    assert repository.claim_webhook("facebook", "event-1") is True
    assert repository.claim_webhook("facebook", "event-1") is False


def test_notification_failure_can_be_marked_sent(repository):
    notification_id = repository.add_notification("test", "admin-line", "body")

    repository.record_notification_failure(notification_id, "offline")
    assert repository.pending_notification_count() == 1

    repository.mark_notification_sent(notification_id)
    assert repository.pending_notification_count() == 0


def test_inventory_reservation_rejects_quantity_above_available_stock(repository):
    with pytest.raises(ValueError, match="OUT_OF_STOCK"):
        repository.reserve_inventory("LOE_VITC_SERUM", 501)


def test_order_round_trip_preserves_currency_and_item(repository):
    order = repository.create_order(
        customer_name="Mali",
        status="awaiting_payment",
        total_thb=Decimal("169.00"),
        product_id="LOE_VITC_SERUM",
        quantity=2,
        unit_price_thb=Decimal("98.00"),
        conversation_id=None,
    )

    loaded = repository.get_order(order.id)

    assert loaded.id == order.id
    assert loaded.product_id == "LOE_VITC_SERUM"
    assert loaded.quantity == 2
    assert loaded.total_thb == Decimal("169.00")


def test_workspace_settings_round_trip_returns_timestamp(repository):
    repository.save_workspace_settings({"store_name": "Test Store"})

    values, updated_at = repository.load_workspace_settings()

    assert values["store_name"] == "Test Store"
    assert updated_at
