"""
Manipulation of the index of data
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, TypeVar

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    P = TypeVar("P", pd.DataFrame, pd.Series[Any])

    import pandas.core.indexes.frozen


def convert_index_to_category_index(pandas_obj: P) -> P:
    """
    Convert the index's values to categories

    This can save a lot of memory and improve the speed of processing.
    However, it comes with some pitfalls.
    For a nice discussion of some of them,
    see [this article](https://towardsdatascience.com/staying-sane-while-adopting-pandas-categorical-datatypes-78dbd19dcd8a/).

    Parameters
    ----------
    pandas_obj
        Object whose index we want to change to categorical.

    Returns
    -------
    :
        A new object with the same data as `pandas_obj`
        but a category type index.
    """
    new_index = pd.MultiIndex.from_frame(
        pandas_obj.index.to_frame(index=False).astype("category")
    )

    if hasattr(pandas_obj, "columns"):
        return type(pandas_obj)(  # type: ignore # confusing mypy here
            pandas_obj.values,
            index=new_index,
            columns=pandas_obj.columns,
        )

    return type(pandas_obj)(
        pandas_obj.values,
        index=new_index,
    )


def unify_index_levels(
    left: pd.MultiIndex, right: pd.MultiIndex
) -> tuple[pd.MultiIndex, pd.MultiIndex]:
    """
    Unify the levels on two indexes

    The levels are unified by simply adding NaN to any level in either `left` or `right`
    that is not in the level of the other index.

    This is differnt to [pd.DataFrame.align][pandas.DataFrame.align].
    [pd.DataFrame.align][pandas.DataFrame.align]
    will fill missing values with values from the other index if it can.
    We don't want that here.
    We want any non-aligned levels to be filled with NaN.

    The implementation also allows this to be performed on indexes directly
    (avoiding casting to a DataFrame
    and avoiding paying the price of aligning everything else
    or creating a bunch of NaN that we just drop straight away).

    The indexes are returned with the levels from `left` first,
    then the levels from `right`.

    Parameters
    ----------
    left
        First index to unify

    right
        Second index to unify

    Returns
    -------
    left_aligned :
        Left after alignment

    right_aligned :
        Right after alignment

    Examples
    --------
    >>> import pandas as pd
    >>>
    >>> idx_a = pd.MultiIndex.from_tuples(
    ...     [
    ...         (1, 2, 3),
    ...         (4, 5, 6),
    ...     ],
    ...     names=["a", "b", "c"],
    ... )
    >>> idx_b = pd.MultiIndex.from_tuples(
    ...     [
    ...         (7, 8),
    ...         (10, 11),
    ...     ],
    ...     names=["a", "b"],
    ... )
    >>> unified_a, unified_b = unify_index_levels(idx_a, idx_b)
    >>> unified_a
    MultiIndex([(1, 2, 3),
                (4, 5, 6)],
               names=['a', 'b', 'c'])

    >>> unified_b
    MultiIndex([( 7,  8, nan),
                (10, 11, nan)],
               names=['a', 'b', 'c'])

    >>> # Also fine if b has swapped levels
    >>> idx_b = pd.MultiIndex.from_tuples(
    ...     [
    ...         (7, 8),
    ...         (10, 11),
    ...     ],
    ...     names=["b", "a"],
    ... )
    >>> unified_a, unified_b = unify_index_levels(idx_a, idx_b)
    >>> unified_a
    MultiIndex([(1, 2, 3),
                (4, 5, 6)],
               names=['a', 'b', 'c'])

    >>> unified_b
    MultiIndex([( 8,  7, nan),
                (11, 10, nan)],
               names=['a', 'b', 'c'])

    >>> # Also works if a is 'inside' b
    >>> idx_a = pd.MultiIndex.from_tuples(
    ...     [
    ...         (7, 8),
    ...         (10, 11),
    ...     ],
    ...     names=["a", "b"],
    ... )
    >>> idx_b = pd.MultiIndex.from_tuples(
    ...     [
    ...         (1, 2, 3),
    ...         (4, 5, 6),
    ...     ],
    ...     names=["a", "b", "c"],
    ... )
    >>> unified_a, unified_b = unify_index_levels(idx_a, idx_b)
    >>> unified_a
    MultiIndex([( 7,  8, nan),
                (10, 11, nan)],
               names=['a', 'b', 'c'])

    >>> unified_b
    MultiIndex([(1, 2, 3),
                (4, 5, 6)],
               names=['a', 'b', 'c'])

    >>> # But, be a bit careful, this is now sensitive to a's column order
    >>> idx_a = pd.MultiIndex.from_tuples(
    ...     [
    ...         (7, 8),
    ...         (10, 11),
    ...     ],
    ...     names=["b", "a"],
    ... )
    >>> idx_b = pd.MultiIndex.from_tuples(
    ...     [
    ...         (1, 2, 3),
    ...         (4, 5, 6),
    ...     ],
    ...     names=["a", "b", "c"],
    ... )
    >>> unified_a, unified_b = unify_index_levels(idx_a, idx_b)
    >>> # Note that the names are `['b', 'a', 'c']` in the output
    >>> unified_a
    MultiIndex([( 7,  8, nan),
                (10, 11, nan)],
               names=['b', 'a', 'c'])

    >>> unified_b
    MultiIndex([(2, 1, 3),
                (5, 4, 6)],
               names=['b', 'a', 'c'])
    """
    if left.names == right.names:
        return left, right

    if (not left.names.difference(right.names)) and (  # type: ignore # pandas-stubs confused
        not right.names.difference(left.names)  # type: ignore # pandas-stubs confused
    ):
        return left, right.reorder_levels(left.names)  # type: ignore # pandas-stubs missing reorder_levels

    out_names = [*left.names, *[v for v in right.names if v not in left.names]]
    out_names_s = set(out_names)
    left_to_add = out_names_s.difference(left.names)
    right_to_add = out_names_s.difference(right.names)

    left_unified = pd.MultiIndex(  # type: ignore # pandas-stubs missing reorder_levels
        levels=[
            *left.levels,
            *[np.array([], dtype=right.get_level_values(c).dtype) for c in left_to_add],  # type: ignore # pandas-stubs confused
        ],
        codes=[
            *left.codes,
            *([np.full(left.shape[0], -1)] * len(left_to_add)),
        ],
        names=[
            *left.names,
            *left_to_add,
        ],
    ).reorder_levels(out_names)

    right_unified = pd.MultiIndex(  # type: ignore # pandas-stubs missing reorder_levels
        levels=[
            *[np.array([], dtype=left.get_level_values(c).dtype) for c in right_to_add],  # type: ignore # pandas-stubs confused
            *right.levels,
        ],
        codes=[
            *([np.full(right.shape[0], -1)] * len(right_to_add)),
            *right.codes,
        ],
        names=[
            *right_to_add,
            *right.names,
        ],
    ).reorder_levels(out_names)

    return left_unified, right_unified


def unify_index_levels_check_index_types(
    left: pd.Index[Any], right: pd.Index[Any]
) -> tuple[pd.MultiIndex, pd.MultiIndex]:
    """
    Unify the levels on two indexes

    This is just a thin wrapper around [unify_index_levels][(m).]
    that checks the the inputs are both [pd.MultiIndex][pandas.MultiIndex]
    before unifying the indices.

    Parameters
    ----------
    left
        First index to unify

    right
        Second index to unify

    Returns
    -------
    left_aligned :
        Left after alignment

    right_aligned :
        Right after alignment
    """
    if not isinstance(left, pd.MultiIndex):
        raise TypeError(left)

    if not isinstance(right, pd.MultiIndex):
        raise TypeError(right)

    return unify_index_levels(left, right)


def update_index_from_candidates(
    indf: pd.DataFrame, candidates: pandas.core.indexes.frozen.FrozenList
) -> pd.DataFrame:
    """
    Update the index of data to align with the candidate columns as much as possible

    Parameters
    ----------
    indf
        Data of which to update the index

    candidates
        Candidate columns to use to create the updated index

    Returns
    -------
    :
        `indf` with its updated index.

        All columns of `indf` that are in `candidates`
        are used to create the index of the result.

    Notes
    -----
    This overwrites any existing index of `indf`
    so you will only want to use this function
    when you're sure that there isn't anything of interest
    already in the index of `indf`.
    """
    set_to_index = [v for v in candidates if v in indf.columns]
    res = indf.set_index(set_to_index)

    return res


def update_index_levels_func(
    df: pd.DataFrame,
    updates: dict[Any, Callable[[Any], Any]],
    copy: bool = True,
    remove_unused_levels: bool = True,
) -> pd.DataFrame:
    """
    Update the index levels of a [pd.DataFrame][pandas.DataFrame]

    Parameters
    ----------
    df
        [pd.DataFrame][pandas.DataFrame] to update

    updates
        Updates to apply to `df`'s index

        Each key is the index level to which the updates will be applied.
        Each value is a function which updates the levels to their new values.

    copy
        Should `df` be copied before returning?

    remove_unused_levels
        Call `df.index.remove_unused_levels` before updating the levels

        This avoids trying to update levels that aren't being used.

    Returns
    -------
    :
        `df` with updates applied to its index
    """
    if copy:
        df = df.copy()

    if not isinstance(df.index, pd.MultiIndex):
        msg = (
            "This function is only intended to be used "
            "when `df`'s index is an instance of `MultiIndex`. "
            f"Received {type(df.index)=}"
        )
        raise TypeError(msg)

    df.index = update_levels(
        df.index, updates=updates, remove_unused_levels=remove_unused_levels
    )

    return df


def update_levels(
    ini: pd.MultiIndex,
    updates: dict[Any, Callable[[Any], Any]],
    remove_unused_levels: bool = True,
) -> pd.MultiIndex:
    """
    Update the levels of a [pd.MultiIndex][pandas.MultiIndex]

    Parameters
    ----------
    ini
        Input index

    updates
        Updates to apply

        Each key is the level to which the updates will be applied.
        Each value is a function which updates the levels to their new values.

    remove_unused_levels
        Call `ini.remove_unused_levels` before updating the levels

        This avoids trying to update levels that aren't being used.

    Returns
    -------
    :
        `ini` with updates applied

    Raises
    ------
    KeyError
        A level in `updates` is not a level in `ini`
    """
    if remove_unused_levels:
        ini = ini.remove_unused_levels()  # type: ignore

    levels: list[pd.Index[Any]] = list(ini.levels)
    codes: list[list[int]] = list(ini.codes)

    for level, updater in updates.items():
        if level not in ini.names:
            msg = (
                f"{level} is not available in the index. Available levels: {ini.names}"
            )
            raise KeyError(msg)

        level_idx = ini.names.index(level)
        new_level = levels[level_idx].map(updater)
        if not new_level.has_duplicates:
            # Fast route: no clashes so no need to update the codes
            levels[level_idx] = new_level

        else:
            # Slow route: have to update the codes too
            dup_level = ini.get_level_values(level).map(updater)
            new_level = new_level.unique()
            new_codes = new_level.get_indexer(dup_level)  # type: ignore
            levels[level_idx] = new_level
            codes[level_idx] = new_codes

    res = pd.MultiIndex(
        levels=levels,
        codes=codes,
        names=ini.names,
    )

    return res
