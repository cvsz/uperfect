import pytest


def test_settings_update_persists_allowed_values_and_keeps_reference_url(services):
    before = services.workspace_settings.get()

    result = services.workspace_settings.update({"store_name": "Test Store", "assistant_tone": "warm"})

    assert result["store_name"] == "Test Store"
    assert result["assistant_tone"] == "warm"
    assert result["facebook_page_url"] == before["facebook_page_url"]
    assert services.workspace_settings.get()["store_name"] == "Test Store"


def test_settings_reject_unknown_keys_without_persisting_them(services):
    with pytest.raises(ValueError, match="Unsupported workspace setting"):
        services.workspace_settings.update({"FACEBOOK_PAGE_ACCESS_TOKEN": "secret"})
