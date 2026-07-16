# Carney ARIA Workshop 2026 — Hierarchical Sequential Sampling Models with HSSM

Hands-on materials for the workshop: Jupyter notebooks built on
[HSSM](https://github.com/lnccbrown/HSSM), recomposed from the HSSM tutorial
collection. Notebooks 1–3 run on **hssm 0.4.0 from PyPI**; the RLSSM notebooks
(4–6) use current `main` for HSSM and
[`ssm-simulators`](https://github.com/lnccbrown/ssm-simulators) from PyPI
`>=0.13.2`, because the `RLSSMConfig` bridge APIs are not in an HSSM PyPI
release yet.

| # | Notebook | Open in Colab | What it covers |
|---|----------|---------------|----------------|
| 1 | [`01_hssm_intro.ipynb`](01_hssm_intro.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/01_hssm_intro.ipynb) | Your first HSSM model; simulating data with and without the do-operator; model cartoon plots; likelihood choice; priors through hierarchical regressions |
| 2 | [`02_scientific_workflow.ipynb`](02_scientific_workflow.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/02_scientific_workflow.ipynb) | A realistic end-to-end analysis: EDA → DDM → hierarchical DDM → angle model → iterative model criticism (pre-sampled traces included, so it runs fast) |
| 3 | [`03_advanced_topics.ipynb`](03_advanced_topics.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/03_advanced_topics.ipynb) | HSSM random variables in raw PyMC models (shipped and custom-built from ONNX likelihood networks); compiled log-likelihoods + the `zeus` sampler; per-parameter centered/non-centered parameterization |
| 4 | [`04_choice_only_rlssm.ipynb`](04_choice_only_rlssm.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/04_choice_only_rlssm.ipynb) | Choice-only reinforcement-learning models with `ssms.rl`: simulate a bandit, bridge into HSSM, fit hierarchical `rl_alpha` and `beta`, and run response-only PPC |
| 5 | [`05_rlssm_basic.ipynb`](05_rlssm_basic.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/05_rlssm_basic.ipynb) | RLSSM basics with choices and response times: Rescorla-Wagner learning, learned drift, `RLSSMConfig.from_ssms_model`, hierarchical fitting, recovery, and RLSSM-aware PPC |
| 6 | [`06_rlssm_advanced.ipynb`](06_rlssm_advanced.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/06_rlssm_advanced.ipynb) | Custom RLSSMs with `ssms.rl`: define a task environment, write a JAX-compatible learner, assemble `ModelConfig`, then reuse the HSSM bridge and inference workflow |

Modeling-challenge notebooks will be added separately.

## Run on Google Colab (no installation)

Click a badge above and run the notebook top to bottom — no edits needed.
The **setup cell** at the top detects Colab automatically, installs the needed
packages, and fetches whatever data the notebook uses (when run locally it does
nothing). Notes:

- On Colab, the install takes a minute or two.
- Notebook 2 additionally fetches ~310 MB of pre-sampled traces (one-time
  per Colab session).
- Notebooks 1–3 install `hssm==0.4.0` from PyPI; notebooks 4–6 install HSSM
  from GitHub `main` and `ssm-simulators>=0.13.2` from PyPI, so Colab can use
  the released ssms wheel instead of building ssms from source.
- Everything runs on a standard CPU runtime; no GPU needed.

## Run locally

Requirements: [uv](https://docs.astral.sh/uv/) and Python ≥ 3.12
(`uv python install 3.12` if needed). Graph rendering (`model.graph()`)
additionally wants the graphviz system binary (`brew install graphviz` /
`apt install graphviz`).

```bash
git clone https://github.com/lnccbrown/Carney_ARIA_Workshop_2026.git
cd Carney_ARIA_Workshop_2026

# 1. Create the environment (HSSM from main; ssm-simulators from PyPI >=0.13.2)
uv sync

# 2. Register the Jupyter kernel the notebooks reference
uv run ipython kernel install --user \
  --name hssm-workshop --display-name "HSSM Workshop"

# 3. Open the notebooks
uv run jupyter lab
```

In **VS Code**, either pick the `hssm-workshop` kernel (kernel picker →
*Select Another Kernel…* → *Jupyter Kernel…*; reload the window if it does not
appear) or select the `.venv` interpreter in this folder directly.

All data is bundled in [`data/`](data/) — after `uv sync`, the notebooks run
offline, with one exception: the small `angle.onnx`/`ddm.onnx` likelihood
networks used in several notebooks auto-download from HuggingFace
([`franklab/HSSM`](https://huggingface.co/franklab/HSSM)) on first use.

Expected runtimes (laptop CPU, all cells): notebook 1 ≈ 4 min, notebook 2
≈ 2 min (thanks to pre-sampled traces), notebook 3 ≈ 5 min. Notebooks 4-6
contain sampling-heavy RLSSM fits; use the default `FULL_RUN=0` settings for
workshop demonstrations and set `FULL_RUN=1` only when regenerating richer
outputs.

## Repository layout

- `0*.ipynb` — the workshop notebooks (outputs pre-baked where available, so they are
  readable without running anything)
- `data/` — workshop dataset (parquet/pkl), seven pre-sampled posterior
  traces (`data/idata/*/traces.nc`), ONNX likelihood networks, and the
  fixtures for the cartoon-plot section
- `images/` — figures referenced by the notebooks
- `pyproject.toml` / `uv.lock` — workshop environment; HSSM is sourced from
  GitHub `main`, while `ssm-simulators>=0.13.2` is sourced from PyPI

## Getting help

- HSSM documentation: <https://lnccbrown.github.io/HSSM/>
- HSSM issues: <https://github.com/lnccbrown/HSSM/issues>
