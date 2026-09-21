from ml.features import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    IMPACT_CLASSES,
    validate_feature_columns,
)


def test_feature_schema():
    assert len(FEATURE_COLUMNS) == 11
    assert len(set(FEATURE_COLUMNS)) == len(FEATURE_COLUMNS)

    assert TARGET_COLUMN == "impact_class"

    assert IMPACT_CLASSES == {
        0: "Low",
        1: "Moderate",
        2: "Severe",
    }


def test_validate_feature_columns_complete():
    missing = validate_feature_columns(FEATURE_COLUMNS)
    assert missing == []


def test_validate_feature_columns_detects_missing():
    incomplete = [
        feature
        for feature in FEATURE_COLUMNS
        if feature != "rainfall_mm"
    ]

    missing = validate_feature_columns(incomplete)

    assert missing == ["rainfall_mm"]