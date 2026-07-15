"""Compose the three workshop notebooks from existing HSSM tutorials.

PROVENANCE RECORD: this script documents which cells of which upstream
HSSM tutorials the notebooks were originally recomposed from. It was
authored in the HSSMSpine repo and needs an HSSM checkout to re-run;
the notebooks in this repo have since been hand-edited and are the
source of truth — do NOT re-run this script over them.

Every code/markdown cell is taken verbatim from the source tutorials in
`repos/HSSM/docs/tutorials/` (cell ranges below), except for:
- path rewrites (assets bundled under this folder's `images/` and `data/`),
- the pinned Colab install lines (hssm v0.4.1 git tag instead of bare pip),
- short bridge markdown cells (the BRIDGE_* literals in this file are the
  only newly written prose).

Re-run from the spine root:
    uv run --project tutorials/hssm_workshop python tutorials/hssm_workshop/_build/compose.py
"""

import re
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent.parent
SRC = HERE.parent.parent / "repos" / "HSSM" / "docs" / "tutorials"

KERNELSPEC = {
    "name": "hssm-workshop",
    "display_name": "HSSM Workshop (hssm v0.4.1)",
    "language": "python",
}

PIN = "git+https://github.com/lnccbrown/HSSM@v0.4.1"

# ---------------------------------------------------------------- rewrites
# Applied to every cell taken from the named source notebook.
REWRITES = {
    "main_tutorial.ipynb": [
        (r"#\s*!pip install git\+https://github\.com/lnccbrown/HSSM\b",
         f"# !pip install {PIN}"),
    ],
    "plotting.ipynb": [
        # Fixtures are bundled locally for the workshop.
        (r'Path\("\.\./\.\./tests/fixtures"\)', 'Path("data")'),
    ],
    "scientific_workflow_hssm.ipynb": [
        (r"#\s*!pip install hssm\b", f"# !pip install {PIN}"),
        # Local asset layout: scientific_workflow_hssm/{data,idata} -> data/
        (r"scientific_workflow_hssm/idata/", "data/idata/"),
        (r"scientific_workflow_hssm/data/?", "data/"),
        (r"\./scientific_workflow_hssm/images/", "images/"),
        (r"\./images/", "images/"),
        # Upstream Colab wget cells download to paths the loader never
        # reads; point them at the layout the code actually uses.
        (r"!wget -P\s+data/carney_workshop_2025_data/", "!wget -P data/"),
        (r"!wget -P\s+idata/", "!wget -P data/idata/"),
    ],
    "pymc.ipynb": [
        (r"#\s*!pip install hssm\b", f"# !pip install {PIN}"),
    ],
    "pymc_to_hssm.ipynb": [
        (r"#\s*!pip install hssm\b", f"# !pip install {PIN}"),
        (r'Path\(\s*"pymc_to_hssm",\s*"mathpsych_workshop_2025_data",',
         'Path("data",'),
        (r"pymc_to_hssm/mathpsych_workshop_2025_data/?", "data/"),
        (r"pymc_to_hssm/images/", "images/"),
    ],
    "do_operator.ipynb": [
        # Demote the source H1 so the workshop notebook keeps one title.
        (r"^# Using the `do-operator` to simulate data",
         "## Simulating data with the `do-operator`"),
    ],
    "compile_logp.ipynb": [],
    "parameterization_per_parameter.ipynb": [],
}

_cache: dict[str, nbformat.NotebookNode] = {}


def cells(src: str, lo: int, hi: int) -> list:
    """Cells lo..hi (inclusive) from a source notebook, rewritten."""
    if src not in _cache:
        _cache[src] = nbformat.read(SRC / src, as_version=4)
    out = []
    for cell in _cache[src].cells[lo : hi + 1]:
        c = nbformat.from_dict(cell)
        for pat, repl in REWRITES[src]:
            c.source = re.sub(pat, repl, c.source, flags=re.MULTILINE)
        if c.cell_type == "code":
            c.outputs = []
            c.execution_count = None
        c.metadata.pop("id", None)
        out.append(c)
    return out


def md(text: str) -> list:
    return [nbformat.v4.new_markdown_cell(text.strip())]


def write(name: str, parts: list[list]) -> None:
    nb = nbformat.v4.new_notebook()
    nb.cells = [c for part in parts for c in part]
    nb.metadata["kernelspec"] = dict(KERNELSPEC)
    nb.metadata["language_info"] = {"name": "python"}
    nbformat.validator.normalize(nb)
    nbformat.validate(nb)
    nbformat.write(nb, HERE / name)
    print(f"wrote {name}: {len(nb.cells)} cells")


# ------------------------------------------------------------ bridge prose
BRIDGE_INTRO_HEADER = """
> **HSSM workshop — notebook 1 of 3.** This notebook recomposes sections of
> the [Main tutorial](https://lnccbrown.github.io/HSSM/tutorials/main_tutorial/),
> the [do-operator tutorial](https://lnccbrown.github.io/HSSM/tutorials/do_operator/),
> and the [Plotting tutorial](https://lnccbrown.github.io/HSSM/tutorials/plotting/).
> Environment setup and the `hssm-workshop` Jupyter kernel are described in the
> [workshop README](README.md).
"""

BRIDGE_DO_OPERATOR = """
So far we simulated data by passing parameter values to `hssm.simulate_data()`
directly. HSSM also supports a complementary route: intervening on an already
specified model with the *do-operator*. The next section is taken from the
do-operator tutorial.
"""

BRIDGE_CARTOON = """
## Visualizing models: cartoon plots

Before moving on to likelihood choices, one more way of looking at a fitted
model. *Model cartoon plots* overlay the model's structural story (drift,
boundaries, non-decision time) on the predicted and observed response-time
distributions. The following section is taken from the Plotting tutorial; it
uses a small pre-fitted hierarchical DDM on the Cavanagh EEG dataset (data and
a pre-sampled trace are bundled with this workshop under `data/`), so no
sampling is needed here.
"""

BRIDGE_INTRO_CONTINUE = """
With simulation and visualization in hand, we return to the Main tutorial:
choosing likelihoods beyond the classic DDM, and customizing priors and model
structure up to hierarchical regressions.
"""

BRIDGE_INTRO_CLOSING = """
## Where to go next

This notebook ends where the workshop's second notebook picks up. For the
material we skipped, see the full tutorials:

- [Main tutorial](https://lnccbrown.github.io/HSSM/tutorials/main_tutorial/) —
  model comparison (§4) and advanced extensions (§5)
- [Plotting](https://lnccbrown.github.io/HSSM/tutorials/plotting/) — the full
  plotting tour, including cartoon plots for N-choice race models
- Notebook 2: a realistic scientific workflow with HSSM
- Notebook 3: custom PyMC models, compiled likelihoods + zeus, and
  per-parameter (non-)centering
"""

BRIDGE_WORKFLOW_HEADER = """
> **HSSM workshop — notebook 2 of 3.** This is the
> [Scientific Workflow tutorial](https://lnccbrown.github.io/HSSM/tutorials/scientific_workflow_hssm/)
> with data, pre-sampled traces, and images bundled locally under `data/` and
> `images/` (Colab users: see the download cells below). Each modeling step
> loads a pre-computed trace when available and falls back to live sampling
> otherwise.
"""

BRIDGE_ADVANCED_HEADER = """
# Advanced topics: HSSM meets raw PyMC

> **HSSM workshop — notebook 3 of 3.** Three advanced topics, each recomposed
> from an existing tutorial:
>
> 1. **Custom PyMC models with HSSM random variables** — from the
>    [PyMC tutorial](https://lnccbrown.github.io/HSSM/tutorials/pymc/) and the
>    [MathPsych 2025 workshop](https://lnccbrown.github.io/HSSM/tutorials/pymc_to_hssm/):
>    first with distributions HSSM already ships, then constructing a new
>    random variable from an ONNX likelihood network.
> 2. **Compiling the likelihood and sampling with `zeus`** — from the
>    [compiled log-likelihood tutorial](https://lnccbrown.github.io/HSSM/tutorials/compile_logp/).
> 3. **Per-parameter centered/non-centered parameterization** — from the
>    [parameterization tutorial](https://lnccbrown.github.io/HSSM/tutorials/parameterization_per_parameter/)
>    (requires hssm >= 0.4.1).
"""

BRIDGE_ADVANCED_COLAB = f"""
## Colab instructions

Running locally with the workshop environment? Skip ahead. On Google Colab,
uncomment and run:

```
# !pip install {PIN} zeus-mcmc
# ONNX networks used in part 1 (bundled locally under data/ otherwise):
# !wget -P data/ https://raw.githubusercontent.com/lnccbrown/HSSM/main/docs/tutorials/pymc_to_hssm/mathpsych_workshop_2025_data/race_3_no_bias_lan.onnx
```
"""

BRIDGE_CUSTOM_RV = """
The distributions above already existed inside HSSM. The next section — from
the MathPsych 2025 workshop tutorial — builds a **new** random variable from
scratch: a 3-accumulator race model, whose likelihood comes as an ONNX
network, wired into a raw `pm.Model` via `make_likelihood_callable` and
`make_distribution`.
"""

BRIDGE_ZEUS = """
## Compiling the likelihood and sampling with `zeus`

HSSM models expose their log-likelihood as a compiled function, which makes it
easy to hand the model to samplers outside the PyMC ecosystem. This section is
the compiled log-likelihood tutorial, run on a simple DDM; the same recipe
works for the Race-3 model above (see the MathPsych tutorial for that
variant).
"""

BRIDGE_NONCENTERED = """
## Per-parameter centered vs. non-centered parameterization

Sampling geometry matters as much as model specification. Since hssm 0.4.1 you
can choose the parameterization *per parameter*. This section is the
parameterization tutorial in full.
"""

BRIDGE_ADVANCED_CLOSING = """
## Where to go next

- [MathPsych 2025 workshop tutorial](https://lnccbrown.github.io/HSSM/tutorials/pymc_to_hssm/)
  — the medium- and high-level interfaces for the Race-3 model, and zeus on
  its compiled likelihood
- [Likelihood functions in HSSM](https://lnccbrown.github.io/HSSM/tutorials/likelihoods/)
- [Variational inference](https://lnccbrown.github.io/HSSM/tutorials/variational_inference/)
"""

# ------------------------------------------------------------ compositions
write(
    "01_hssm_intro.ipynb",
    [
        cells("main_tutorial.ipynb", 0, 4),      # title, framing, workflow map
        md(BRIDGE_INTRO_HEADER),
        cells("main_tutorial.ipynb", 5, 8),      # Colab (pinned) + setup
        cells("main_tutorial.ipynb", 9, 65),     # §1 first model
        md(BRIDGE_DO_OPERATOR),
        cells("do_operator.ipynb", 0, 16),       # do-operator, whole
        md(BRIDGE_CARTOON),
        cells("plotting.ipynb", 2, 2),           # imports
        cells("plotting.ipynb", 4, 8),           # fixtures -> model -> trace
        cells("plotting.ipynb", 39, 47),         # cartoon plots (2-choice)
        md(BRIDGE_INTRO_CONTINUE),
        cells("main_tutorial.ipynb", 66, 79),    # §2 likelihood choice
        cells("main_tutorial.ipynb", 80, 153),   # §3 priors -> hierarchical
        md(BRIDGE_INTRO_CLOSING),
    ],
)

write(
    "02_scientific_workflow.ipynb",
    [
        cells("scientific_workflow_hssm.ipynb", 0, 0),  # title
        md(BRIDGE_WORKFLOW_HEADER),
        cells("scientific_workflow_hssm.ipynb", 1, 136),  # everything else
    ],
)

write(
    "03_advanced_topics.ipynb",
    [
        md(BRIDGE_ADVANCED_HEADER),
        md(BRIDGE_ADVANCED_COLAB),
        cells("pymc.ipynb", 0, 0),               # part 1a title
        cells("pymc.ipynb", 3, 14),              # named RVs + factories
        md(BRIDGE_CUSTOM_RV),
        cells("pymc_to_hssm.ipynb", 6, 7),       # load modules
        cells("pymc_to_hssm.ipynb", 20, 41),     # Example 1: custom RV
        cells("pymc_to_hssm.ipynb", 42, 52),     # Example 2: regression model
        md(BRIDGE_ZEUS),
        cells("compile_logp.ipynb", 1, 19),      # compile_logp + zeus
        md(BRIDGE_NONCENTERED),
        cells("parameterization_per_parameter.ipynb", 1, 13),
        md(BRIDGE_ADVANCED_CLOSING),
    ],
)
