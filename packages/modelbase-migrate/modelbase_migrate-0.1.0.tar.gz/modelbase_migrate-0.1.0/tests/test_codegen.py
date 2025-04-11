from pathlib import Path

from modelbase.ode import Model
from modelbase.ode.utils import ratefunctions as rf

from modelbase_migrate import migrate


def example1() -> Model:
    return (
        Model()
        .add_compounds(["x1"])
        .add_parameter("k1", 1.0)
        .add_derived_parameter("dk1", rf.constant, ["k1"])
        .add_derived_compound("dx1", rf.constant, ["x1"])
        .add_reaction_from_args(
            "v1",
            rf.mass_action_1,
            args=["x1", "k1"],
            stoichiometry={"x1": -1},
        )
    )


def upper_glycolysis() -> Model:
    # Instantiate model
    m = Model(
        {
            "k1": 0.25,
            "k2": 1,
            "k3": 1,
            "k3m": 1,
            "k4": 1,
            "k5": 1,
            "k6": 1,
            "k7": 2.5,
        }
    )
    m.add_compounds(["GLC", "G6P", "F6P", "FBP", "ATP", "ADP"])

    m.add_reaction(
        rate_name="v1",
        function=rf.constant,
        stoichiometry={"GLC": 1},
        parameters=["k1"],
    )
    m.add_reaction(
        rate_name="v2",
        function=rf.mass_action_2,
        stoichiometry={"GLC": -1, "ATP": -1, "G6P": 1, "ADP": 1},
        parameters=["k2"],
    )
    m.add_reaction(
        rate_name="v3",
        function=rf.reversible_mass_action_1_1,
        stoichiometry={"G6P": -1, "F6P": 1},
        parameters=["k3", "k3m"],
        reversible=True,
    )
    m.add_reaction(
        rate_name="v4",
        function=rf.mass_action_2,
        stoichiometry={"F6P": -1, "ATP": -1, "ADP": 1, "FBP": 1},
        parameters=["k4"],
    )
    m.add_reaction(
        rate_name="v5",
        function=rf.mass_action_1,
        stoichiometry={"FBP": -1, "F6P": 1},
        parameters=["k5"],
    )
    m.add_reaction(
        rate_name="v6",
        function=rf.mass_action_1,
        stoichiometry={"FBP": -1},
        parameters=["k6"],
    )
    m.add_reaction(
        rate_name="v7",
        function=rf.mass_action_1,
        stoichiometry={"ADP": -1, "ATP": 1},
        parameters=["k7"],
    )

    return m


def test_migrate() -> None:
    (out := Path(__file__).parent / "tmp").mkdir(exist_ok=True)

    migrate(
        example1(),
        initial_conditions={"x1": 1.0},
        out_file=out / "example1.py",
    )

    migrate(
        upper_glycolysis(),
        initial_conditions={
            "GLC": 0,
            "G6P": 0,
            "F6P": 0,
            "FBP": 0,
            "ATP": 0.5,
            "ADP": 0.5,
        },
        out_file=out / "upper_glycolysis.py",
    )
    assert True
