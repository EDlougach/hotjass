"""Physics regression test: solves the operating point of a few reference
cases (tests/cases.json: ITER, JET, MAST-U, TCV inputs from the HOT-Jass web
presets, both profile modes, delayed orbit loss off and on) and compares the
key results with tests/reference.json.

    pytest tests                                  # or:
    python tests/test_regression.py               # check
    python tests/test_regression.py --update      # store the current results

After an intended physics change, review the differences, run --update and
commit the new reference together with the change.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))      # the checkout, also without `pip install`

from hotjass.core import BeamParams, HotJassModel, PlasmaParams  # noqa: E402

CASES = json.loads((HERE / "cases.json").read_text())
REFERENCE = HERE / "reference.json"
REL_TOL = 1e-6


def solve_case(case: dict) -> dict:
    model = HotJassModel(PlasmaParams(**case["plasma"]), [BeamParams(**b) for b in case["beams"]])
    op = model.operating_point()
    assert op.feasible, op.infeasible_reason
    cd = model.current_drive(op)
    out = {
        "Te_keV": op.Te_keV, "Ti_keV": op.Ti_keV, "nb0_m3": op.nb0_m3, "n_thermal_m3": op.n_thermal_m3,
        "P_e_w": op.P_e_w, "P_i_w": op.P_i_w, "P_delayed_loss_w": op.P_delayed_loss_w,
        "pf_total_w": op.pf_total_w, "neutron_rate_s": op.neutron_rate_s, "beta_t": op.beta_t,
    }
    if cd is not None:
        out.update(I_nb_A=cd.I_nb_A, I_bs_A=cd.I_bs_A)
    return out


def compare(name: str, res: dict, ref: dict) -> list[str]:
    return [f"{name}: {key} {ref.get(key)!r} -> {val!r}" for key, val in res.items()
            if ref.get(key) is None or abs(val - ref[key]) > REL_TOL * max(abs(ref[key]), 1e-30)]


def test_reference_cases():
    reference = json.loads(REFERENCE.read_text())
    diffs = []
    for name, case in CASES.items():
        diffs += compare(name, solve_case(case), reference[name])
    assert not diffs, "\n".join(diffs)


if __name__ == "__main__":
    results = {name: solve_case(case) for name, case in CASES.items()}
    if "--update" in sys.argv[1:]:
        REFERENCE.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
        print(f"reference updated ({len(results)} cases)")
        sys.exit(0)
    reference = json.loads(REFERENCE.read_text())
    diffs = [d for name, res in results.items() for d in compare(name, res, reference[name])]
    print("\n".join(diffs) if diffs else f"all {len(results)} cases match the reference")
    sys.exit(1 if diffs else 0)
