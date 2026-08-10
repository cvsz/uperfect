import json
from pathlib import Path


def test_manifest_uses_canonical_product_directories():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "assets/chatbot/asset-manifest.json").read_text(encoding="utf-8"))
    paths = [item["path"] for item in manifest["items"]]

    assert any(path.startswith("assets/suea_rong_hai_mala_chili_oil/") for path in paths)
    assert any(path.startswith("assets/loe_soap/") for path in paths)
    assert all("น้ำพริกเสือร้องไห้" not in path for path in paths)
    assert all(path.split("/", 2)[1].isascii() and " " not in path.split("/", 2)[1] for path in paths)
    assert all((root / path).is_file() for path in paths)


def test_reference_documents_exist_for_canonical_products():
    root = Path(__file__).resolve().parents[1]

    assert (root / "assets/loe_soap/LOE_Charcoal_Mud_Soap_TH.md").is_file()
    assert (root / "assets/loe_soap/LOE_Charcoal_Mud_Soap_EN.md").is_file()
    assert (root / "assets/suea_rong_hai_mala_chili_oil/Suea_Rong_Hai_Mala_Chili_Oil_TH.md").is_file()
    assert (root / "assets/suea_rong_hai_mala_chili_oil/Suea_Rong_Hai_Mala_Chili_Oil_EN.md").is_file()
