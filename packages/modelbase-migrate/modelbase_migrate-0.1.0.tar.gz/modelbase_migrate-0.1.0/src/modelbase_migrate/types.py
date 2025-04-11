"""Types for the modelbase_migrate module."""

from typing import TypedDict


class Derived(TypedDict):
    fn: str
    args: list[str]


class Reaction(TypedDict):
    fn: str
    args: list[str]
    stoichiometry: dict[str, float]
