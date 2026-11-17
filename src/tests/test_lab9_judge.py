import pytest

from lab9.judge import calibrate


def test_calibrate_rejects_empty_csv(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("item_id,reply,human,judge\n", encoding="utf-8")

    with pytest.raises(ValueError, match="no labeled rows"):
        calibrate(path)


def test_calibrate_rejects_missing_columns(tmp_path):
    path = tmp_path / "incomplete.csv"
    path.write_text("item_id,human,judge\n1,PASS,PASS\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing columns"):
        calibrate(path)
