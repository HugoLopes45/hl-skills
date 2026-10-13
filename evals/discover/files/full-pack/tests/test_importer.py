from app import importer


def test_import_counts_rows(tmp_path, monkeypatch):
    saved = []
    monkeypatch.setattr(importer, "save_rows", saved.extend)
    path = tmp_path / "bank.csv"
    path.write_text("date,amount\n2024-01-03,12.5\n")
    assert importer.import_csv(path) == 1
    assert saved == [{"month": "2024-01", "amount": 12.5}]
