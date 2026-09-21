"""Safe ML training gate for AgriFlood-PK.

This module validates whether the agricultural-impact dataset is
eligible for future model training.

It intentionally does NOT train a model yet.

Training must remain blocked until:
1. All required predictor features are available.
2. Independent agricultural-impact ground-truth labels are available.
3. Label provenance is documented.
"""

import argparse
from pathlib import Path

import pandas as pd

from ml.features import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    IMPACT_CLASSES,
    validate_feature_columns,
)


REQUIRED_PROVENANCE_COLUMNS = [
    "label_source",
    "label_method",
]

UNASSIGNED_PROVENANCE_VALUES = {
    "",
    "unlabeled",
    "not_assigned",
    "unknown",
    "none",
    "nan",
}


def validate_training_dataset(
    dataframe: pd.DataFrame,
) -> list[str]:
    """Return all blockers that prevent safe ML training."""

    blockers = []

    # Check predictor features.
    missing_features = validate_feature_columns(
        dataframe.columns
    )

    if missing_features:
        blockers.append(
            "Missing required model features: "
            + ", ".join(missing_features)
        )

    # Check target column.
    if TARGET_COLUMN not in dataframe.columns:
        blockers.append(
            f"Missing target column: {TARGET_COLUMN}. "
            "Independent agricultural-impact ground truth "
            "has not been assigned."
        )

    # Check provenance columns.
    missing_provenance = [
        column
        for column in REQUIRED_PROVENANCE_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_provenance:
        blockers.append(
            "Missing label provenance columns: "
            + ", ".join(missing_provenance)
        )

    # Only perform detailed label checks if target exists.
    if TARGET_COLUMN in dataframe.columns:

        target = pd.to_numeric(
            dataframe[TARGET_COLUMN],
            errors="coerce",
        )

        if target.isna().any():
            blockers.append(
                f"{TARGET_COLUMN} contains missing or "
                "non-numeric labels."
            )
        else:
            observed_classes = set(target.unique())
            valid_classes = set(IMPACT_CLASSES.keys())

            invalid_classes = (
                observed_classes - valid_classes
            )

            if invalid_classes:
                blockers.append(
                    "Invalid impact_class values: "
                    + ", ".join(
                        str(value)
                        for value in sorted(
                            invalid_classes
                        )
                    )
                )

            missing_classes = (
                valid_classes - observed_classes
            )

            if missing_classes:
                blockers.append(
                    "Training dataset does not contain "
                    "all intended impact classes. Missing: "
                    + ", ".join(
                        str(value)
                        for value in sorted(
                            missing_classes
                        )
                    )
                )

    # Check label provenance values.
    for column in REQUIRED_PROVENANCE_COLUMNS:

        if column not in dataframe.columns:
            continue

        values = (
            dataframe[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        invalid = values.isin(
            UNASSIGNED_PROVENANCE_VALUES
        )

        if invalid.any():
            blockers.append(
                f"{column} contains unassigned "
                "label provenance."
            )

    # Check missing predictor values only when
    # all predictor columns are present.
    if not missing_features:

        if dataframe[FEATURE_COLUMNS].isna().any().any():
            blockers.append(
                "One or more predictor features "
                "contain missing values."
            )

    return blockers


def main() -> None:
    """Validate a dataset without training a model."""

    parser = argparse.ArgumentParser(
        description=(
            "Validate AgriFlood-PK agricultural-impact "
            "training data."
        )
    )

    parser.add_argument(
        "--input",
        default="data/ml/khairpur_features_2022.csv",
        help="Path to the candidate training CSV.",
    )

    args = parser.parse_args()

    dataset_path = Path(args.input)

    if not dataset_path.exists():
        print("ML TRAINING: BLOCKED")
        print(
            f"- Dataset not found: {dataset_path}"
        )
        print("\nNo model was trained.")
        raise SystemExit(2)

    dataframe = pd.read_csv(dataset_path)

    blockers = validate_training_dataset(dataframe)

    if blockers:
        print("ML TRAINING: BLOCKED")

        for blocker in blockers:
            print(f"- {blocker}")

        print(
            "\nNo model was trained. "
            "Do not create synthetic impact_class labels "
            "to bypass these checks."
        )

        raise SystemExit(2)

    print("ML TRAINING DATASET: ELIGIBLE FOR REVIEW")
    print(f"Rows: {len(dataframe)}")
    print(
        "All required predictors, target classes, "
        "and label provenance fields are present."
    )
    print(
        "\nNo model was trained. Independent label "
        "quality and scientific suitability must still "
        "be reviewed before training."
    )


if __name__ == "__main__":
    main()