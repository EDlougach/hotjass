# hotjass

Physics of neutral-beam-driven tokamak plasmas in a fast 0-D / 1-D model:
power and particle balance (H, D, T and impurity), neutral-beam deposition,
shine-through, first-orbit and delayed (pitch-scattering) orbit loss,
charge-exchange loss, fast-ion slowing down, thermal, beam-target and
beam-beam fusion, rotation, NBCD and bootstrap current.

It is the physics engine of the [HOT-Jass web app](https://github.com/EDlougach/HOT-JASS)
and of the HI-Jass desktop app, and is meant to be reused by other tools.
The models, their assumptions and their validation are described in
[User_Manual.md](User_Manual.md) ([PDF](User_Manual.pdf)).

## Install

```bash
pip install "hotjass @ git+https://github.com/EDlougach/hotjass@v0.9.0"
```

Only `numpy` is required. Pin a version tag (as above) in applications, so
that a physics change never changes their results unnoticed.

## Use

```python
from hotjass.core import BeamParams, HotJassModel, PlasmaParams

model = HotJassModel(PlasmaParams(), [BeamParams()])   # default parameters
op = model.operating_point()            # solved 0-D operating point
print(op.Te_keV, op.Ti_keV, op.pf_total_w)
cd = model.current_drive(op)            # NBCD + bootstrap diagnostics
```

`hotjass.physics` holds the individual models, `hotjass.solve` the
operating-point solver, `hotjass.current` the current drive, and
`hotjass.core` the parameter classes and `HotJassModel` used by the apps.
The older top-level module name `hotjass_core` still works as an alias.

## Develop

Work on the physics together with an app by installing your checkout in the
app's environment in editable mode -- the app then uses your working copy:

```bash
git clone https://github.com/EDlougach/hotjass
cd <your app> && .venv/bin/pip install -e ../hotjass
```

Run the regression test after every change:

```bash
python tests/test_regression.py          # or: pytest tests
```

It solves reference cases (ITER, JET, MAST-U, TCV inputs, both profile
modes, delayed orbit loss off and on) and compares the results with
`tests/reference.json`. After an intended physics change, review the
differences, run `python tests/test_regression.py --update` and commit the
new reference together with the change.

### Changing the physics

1. Pull request to this repository: the change, its reference (paper, code
   or measurement) and the updated `tests/reference.json` and manual.
   Changes that move results by more than 10 % are added as options, off by
   default.
2. After review, a new version is tagged (`v0.10.0`, ...).
3. Each app adopts it in its own pull request: bump the pinned version and
   update the app's own regression reference.

## License

Apache License 2.0, see [LICENSE](LICENSE).
