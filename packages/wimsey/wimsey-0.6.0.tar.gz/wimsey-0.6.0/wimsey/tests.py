from functools import partial
from typing import Any, Callable
from dataclasses import dataclass


import narwhals.stable.v1 as nw


@dataclass
class Result:
    name: str
    success: bool
    unexpected: Any = None


def _range_check(metric: str) -> Callable:
    """
    Factory function for generated tests of the form "x should be within range"

    Tests are also factories in themselves, they'll generate functions to take
    only a "describe" object.
    """

    def should(
        describe: dict[str, Any],
        column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
    ) -> Result:
        """Test that column metric is within designated range"""
        checks: list[bool] = []
        value: Any = describe[f"{metric}_{column}"]
        if be_exactly is not None:
            checks.append(value == be_exactly)
        if be_less_than is not None:
            checks.append(value < be_less_than)
        if be_greater_than is not None:
            checks.append(value > be_greater_than)
        if be_less_than_or_equal_to is not None:
            checks.append(value <= be_less_than_or_equal_to)
        if be_greater_than_or_equal_to is not None:
            checks.append(value >= be_greater_than_or_equal_to)
        return Result(
            name=f"{metric}-of-{column}",
            success=all(checks),
            unexpected=value if not all(checks) else None,
        )

    def should_be_partial(
        column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> Callable:
        """Test that column {metric} is within designated range"""
        return_partial = partial(
            should,
            column=column,
            be_exactly=be_exactly,
            be_less_than=be_less_than,
            be_less_than_or_equal_to=be_less_than_or_equal_to,
            be_greater_than=be_greater_than,
            be_greater_than_or_equal_to=be_greater_than_or_equal_to,
        )
        return_partial.required_metrics = [metric]
        return return_partial

    should_be_partial.__doc__ = should_be_partial.__doc__.replace("{metric}", metric)
    return should_be_partial


def row_count_should(
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    be_exactly: float | int | None = None,
    **kwargs,
) -> Callable:
    """Test that dataframe row count is within designated range"""

    def row_count_should_be(
        description: dict,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
        be_exactly: float | int | None = None,
    ) -> Result:
        """Test that dataframe row count is within designated range"""
        checks: list[bool] = []
        value: float | int = description["length"]
        if be_exactly is not None:
            checks.append(value == be_exactly)
        if be_less_than is not None:
            checks.append(value < be_less_than)
        if be_greater_than is not None:
            checks.append(value > be_greater_than)
        if be_less_than_or_equal_to is not None:
            checks.append(value <= be_less_than_or_equal_to)
        if be_greater_than_or_equal_to is not None:
            checks.append(value >= be_greater_than_or_equal_to)
        return Result(
            name="row-count",
            success=all(checks),
            unexpected=value if not all(checks) else None,
        )

    should_be_partial = partial(
        row_count_should_be,
        be_less_than=be_less_than,
        be_less_than_or_equal_to=be_less_than_or_equal_to,
        be_greater_than=be_greater_than,
        be_greater_than_or_equal_to=be_greater_than_or_equal_to,
        be_exactly=be_exactly,
    )
    should_be_partial.required_metrics = ["length"]
    return should_be_partial


def columns_should(
    have: list[str] | str | None = None,
    not_have: list[str] | str | None = None,
    be: list[str] | str | None = None,
    **kwargs,
) -> Callable:
    """Test column names match up with expected values"""

    def should_have(
        description: dict,
        have: list[str] | str | None = None,
        not_have: list[str] | str | None = None,
        be: list[str] | str | None = None,
        **kwargs,
    ) -> Result:
        """Test column names match up with expected values"""
        have = list(have) if isinstance(have, str) else have
        not_have = list(not_have) if isinstance(not_have, str) else not_have
        be = list(be) if isinstance(be, str) else be
        checks: list[bool] = []
        present_columns = description["columns"].split("_^&^_")
        if have is not None:
            for col in have:
                checks.append(col in present_columns)
        if not_have is not None:
            for col in not_have:
                checks.append(col not in present_columns)
        if be is not None:
            checks.append(set(present_columns) == set(be))
            checks.append(len(present_columns) == len(be))
        return Result(
            name="columns",
            success=all(checks),
            unexpected=present_columns if not all(checks) else None,
        )

    should_have_partial = partial(should_have, have=have, not_have=not_have, be=be)
    should_have_partial.required_metrics = []
    return should_have_partial


def type_should(
    column: str,
    be: str | None = None,
    not_be: str | None = None,
    be_one_of: list[str] | None = None,
    **kwargs,
) -> Callable:
    """
    Test column type matches up with expected value.

    Note that this will expect *polars* style types, although does not require
    that they be case sensitive. For example, if testing a pandas dataframe for
    integer type, specify "int64" rather than, say, "int64[pyarrow]" or otherwise.
    """

    def should_be(
        description: dict,
        column: str,
        be: str | None,
        not_be: str | None,
        be_one_of: str | None,
        **kwargs,
    ) -> Result:
        """
        Test column type matches up with expected value.

        Note that this will expect *polars* style types, although does not require
        that they be case sensitive. For example, if testing a pandas dataframe for
        integer type, specify "int64" rather than, say, "int64[pyarrow]" or otherwise.
        """
        checks: list[bool] = []
        col_type = description[f"type_{column}"]
        if be is not None:
            checks.append(be.lower() == col_type.lower())
        if not_be is not None:
            checks.append(not_be.lower() != col_type.lower())
        if be_one_of is not None:
            checks.append(col_type.lower() in [i.lower() for i in be_one_of])
        return Result(
            name=f"type-of-{column}",
            success=all(checks),
            unexpected=col_type if not all(checks) else None,
        )

    should_be_partial = partial(
        should_be,
        column=column,
        be=be,
        not_be=not_be,
        be_one_of=be_one_of,
    )
    should_be_partial.required_metrics = ["type"]
    return should_be_partial


def average_difference_from_other_column_should(
    column: str,
    other_column: str,
    be_exactly: float | int | None = None,
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    **kwargs,
) -> Callable:
    """
    Test that the average difference between column and other column are
    within designated bounds.
    """

    def should(
        description: dict,
        column: str,
        other_column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> Result:
        """
        Test that the average difference between column and other column are
        within designated bounds.
        """
        checks: list[bool] = []
        difference = description[f"mean_{column}"] - description[f"mean_{other_column}"]
        if be_exactly is not None:
            checks.append(difference == be_exactly)
        if be_less_than is not None:
            checks.append(difference < be_less_than)
        if be_less_than_or_equal_to is not None:
            checks.append(difference <= be_less_than_or_equal_to)
        if be_greater_than is not None:
            checks.append(difference > be_greater_than)
        if be_greater_than_or_equal_to is not None:
            checks.append(difference >= be_greater_than_or_equal_to)
        return Result(
            name=f"average-difference-from-{column}-to-{other_column}",
            success=all(checks),
            unexpected=difference if not all(checks) else None,
        )

    should_partial = partial(
        should,
        column=column,
        other_column=other_column,
        be_exactly=be_exactly,
        be_less_than=be_less_than,
        be_less_than_or_equal_to=be_less_than_or_equal_to,
        be_greater_than=be_greater_than,
        be_greater_than_or_equal_to=be_greater_than_or_equal_to,
    )
    should_partial.required_metrics = ["mean"]
    return should_partial


def average_ratio_to_other_column_should(
    column: str,
    other_column: str,
    be_exactly: float | int | None = None,
    be_less_than: float | int | None = None,
    be_less_than_or_equal_to: float | int | None = None,
    be_greater_than: float | int | None = None,
    be_greater_than_or_equal_to: float | int | None = None,
    **kwargs,
) -> Callable:
    """
    Test that the average ratio between column and other column are
    within designated bounds (for instance, a value of 1 has a ratio
    of 0.1 to a value of 10)
    """

    def should(
        description: dict,
        column: str,
        other_column: str,
        be_exactly: float | int | None = None,
        be_less_than: float | int | None = None,
        be_less_than_or_equal_to: float | int | None = None,
        be_greater_than: float | int | None = None,
        be_greater_than_or_equal_to: float | int | None = None,
        **kwargs,
    ) -> Result:
        """
        Test that the average ratio between column and other column are
        within designated bounds (for instance, a value of 1 has a ratio
        of 0.1 to a value of 10)
        """
        checks: list[bool] = []
        ratio = description[f"mean_{column}"] / description[f"mean_{other_column}"]
        if be_exactly is not None:
            checks.append(ratio == be_exactly)
        if be_less_than is not None:
            checks.append(ratio < be_less_than)
        if be_less_than_or_equal_to is not None:
            checks.append(ratio <= be_less_than_or_equal_to)
        if be_greater_than is not None:
            checks.append(ratio > be_greater_than)
        if be_greater_than_or_equal_to is not None:
            checks.append(ratio >= be_greater_than_or_equal_to)
        return Result(
            name=f"average-ratio-between-{column}-and-{other_column}",
            success=all(checks),
            unexpected=ratio if not all(checks) else None,
        )

    should_partial = partial(
        should,
        column=column,
        other_column=other_column,
        be_exactly=be_exactly,
        be_less_than=be_less_than,
        be_less_than_or_equal_to=be_less_than_or_equal_to,
        be_greater_than=be_greater_than,
        be_greater_than_or_equal_to=be_greater_than_or_equal_to,
    )
    should_partial.required_metrics = ["mean"]
    return should_partial


def max_string_length_should(
    column: str,
    be_less_than: int | float | None = None,
    be_greater_than: int | float | None = None,
    be_exactly: int | float | None = None,
    **kwargs,
) -> Callable:
    def should(
        description: dict,
        column: str,
        **kwargs,
    ) -> Result:
        success = description[f"max_string_length_of_{column}"]
        return Result(
            name=f"max-string-length-of-{column}",
            success=success,
            unexpected=None
            if success
            else "Length of column values did not meet bounds",
        )

    expressions: list[nw.Expr] = []
    if be_less_than:
        expr: nw.Expr = nw.col(column).str.len_chars().max() < nw.lit(be_less_than)
        expressions.append(expr)
    if be_greater_than:
        expr: nw.Expr = nw.col(column).str.len_chars().max() > nw.lit(be_greater_than)
        expressions.append(expr)
    if be_exactly:
        expr: nw.Expr = nw.col(column).str.len_chars().max() == nw.lit(be_exactly)
        expressions.append(expr)
    partial_should = partial(should, column=column)
    partial_should.required_metrics = [
        nw.all_horizontal(*expressions).alias(f"max_string_length_of_{column}")
    ]
    return partial_should


def all_values_should(
    column: str,
    be_one_of: list[str] | None = None,
    not_be_one_of: list[str] | None = None,
    match_regex: str | None = None,
    **kwargs,
) -> None:
    def should(
        description: dict,
        **kwargs,
    ) -> Result:
        success = description[f"all_values_of_{column}"]
        return Result(
            name=f"all-values-of-{column}",
            success=success,
            unexpected=None if success else "Values did not meet given conditions",
        )

    expressions: list[nw.Expr] = []
    if be_one_of:
        expressions.append(nw.col(column).is_in(be_one_of).min())
    if not_be_one_of:
        expressions.append(~(nw.col(column).is_in(not_be_one_of)).max())
    if match_regex:
        expressions.append(nw.col(column).str.contains(match_regex))
    partial_should = partial(should)
    partial_should.required_metrics = [
        nw.all_horizontal(*expressions).alias(f"all_values_of_{column}")
    ]
    return partial_should


possible_tests: dict[str, Callable] = {
    "mean_should": (mean_should := _range_check("mean")),
    "min_should": (min_should := _range_check("min")),
    "max_should": (max_should := _range_check("max")),
    "std_should": (std_should := _range_check("std")),
    "null_count_should": (null_count_should := _range_check("null_count")),
    "count_should": (count_should := _range_check("count")),
    "null_percentage_should": (
        null_percentage_should := _range_check("null_percentage")
    ),
    "columns_should": columns_should,
    "type_should": type_should,
    "row_count_should": row_count_should,
    "average_difference_from_other_column_should": average_difference_from_other_column_should,
    "average_ratio_to_other_column_should": average_ratio_to_other_column_should,
    "max_string_length_should": max_string_length_should,
    "all_values_should": all_values_should,
}
