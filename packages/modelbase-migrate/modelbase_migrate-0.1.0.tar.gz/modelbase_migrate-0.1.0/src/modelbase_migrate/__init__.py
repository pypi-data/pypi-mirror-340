"""Migrate modelbase models to modelbase2."""

from __future__ import annotations

import inspect
from pathlib import Path

from modelbase.ode import Model

from modelbase_migrate.types import Derived, Reaction


def migrate(
    model: Model,
    initial_conditions: dict[str, float],
    out_file: Path,
) -> None:
    variables = initial_conditions
    parameters = model.parameters

    functions: dict[str, str] = {}

    derived: dict[str, Derived] = {}
    for k, v in model.derived_parameters.items():
        fn = v.function
        fn_name = fn.__name__
        functions[fn_name] = inspect.getsource(fn)
        derived[k] = {"fn": fn_name, "args": v.parameters}
    for k, v in model.algebraic_modules.items():
        if len(v.derived_compounds) > 1:
            raise NotImplementedError(f"Only one derived compound is supported for {k}")
        fn = v.function
        fn_name = fn.__name__
        functions[fn_name] = inspect.getsource(fn)

        name = v.derived_compounds[0]
        derived[name] = {"fn": fn_name, "args": v.args}

    derived_source = "\n        ".join(
        f""".add_derived(
            "{name}",
            fn={v["fn"]},
            args={v["args"]},
        )"""
        for name, v in derived.items()
    )

    reactions: dict[str, Reaction] = {}
    for k, v in model.rates.items():
        fn = v.function
        fn_name = fn.__name__
        functions[fn_name] = inspect.getsource(fn)

        reactions[k] = {
            "fn": fn_name,
            "args": v.args,
            "stoichiometry": model.stoichiometries[k],
        }
    reactions_source = "\n        ".join(
        f""".add_reaction(
            "{name}",
            {v["fn"]},
            args={v["args"]},
            stoichiometry={v["stoichiometry"]},
        )"""
        for name, v in reactions.items()
    )

    functions_source = "\n".join(functions.values())

    source = f"""from modelbase2 import Model

{functions_source}

def create_model() -> Model:
    return (
        Model()
        .add_variables({variables})
        .add_parameters({parameters})
        {derived_source}
        {reactions_source}

    )
    """

    with out_file.open("w") as f:
        f.write(source)
