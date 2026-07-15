# Carney ARIA Workshop 2026 — Hierarchical Sequential Sampling Models with HSSM

Hands-on materials for the workshop: three Jupyter notebooks built on
[HSSM](https://github.com/lnccbrown/HSSM) (v0.4.1), recomposed from the HSSM
tutorial collection.

| # | Notebook | Open in Colab | What it covers |
|---|----------|---------------|----------------|
| 1 | [`01_hssm_intro.ipynb`](01_hssm_intro.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/01_hssm_intro.ipynb) | Your first HSSM model; simulating data with and without the do-operator; model cartoon plots; likelihood choice; priors through hierarchical regressions |
| 2 | [`02_scientific_workflow.ipynb`](02_scientific_workflow.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/02_scientific_workflow.ipynb) | A realistic end-to-end analysis: EDA → DDM → hierarchical DDM → angle model → iterative model criticism (pre-sampled traces included, so it runs fast) |
| 3 | [`03_advanced_topics.ipynb`](03_advanced_topics.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lnccbrown/Carney_ARIA_Workshop_2026/blob/main/03_advanced_topics.ipynb) | HSSM random variables in raw PyMC models (shipped and custom-built from ONNX likelihood networks); compiled log-likelihoods + the `zeus` sampler; per-parameter centered/non-centered parameterization |

## Run on Google Colab (no installation)

Click a badge above and run the notebook top to bottom — no edits needed.
The **setup cell** at the top detects Colab automatically, installs HSSM
v0.4.1, and fetches whatever data the notebook uses (when run locally it
does nothing). Notes:

- On Colab, the install builds HSSM from GitHub and takes ~2–3 minutes.
- Notebook 2 additionally fetches ~310 MB of pre-sampled traces (one-time
  per Colab session).
- Everything runs on a standard CPU runtime; no GPU needed.

## Run locally

Requirements: [uv](https://docs.astral.sh/uv/) and Python ≥ 3.12
(`uv python install 3.12` if needed). Graph rendering (`model.graph()`)
additionally wants the graphviz system binary (`brew install graphviz` /
`apt install graphviz`).

```bash
git clone https://github.com/lnccbrown/Carney_ARIA_Workshop_2026.git
cd Carney_ARIA_Workshop_2026

# 1. Create the environment (installs hssm v0.4.1 and all dependencies)
uv sync

# 2. Register the Jupyter kernel the notebooks reference
uv run ipython kernel install --user \
  --name hssm-workshop --display-name "HSSM Workshop (hssm v0.4.1)"

# 3. Open the notebooks
uv run jupyter lab
```

In **VS Code**, either pick the `hssm-workshop` kernel (kernel picker →
*Select Another Kernel…* → *Jupyter Kernel…*; reload the window if it does not
appear) or select the `.venv` interpreter in this folder directly.

All data is bundled in [`data/`](data/) — after `uv sync`, the notebooks run
offline, with one exception: the small `angle.onnx`/`ddm.onnx` likelihood
networks used in notebooks 1 and 3 auto-download from HuggingFace
([`franklab/HSSM`](https://huggingface.co/franklab/HSSM)) on first use.

Expected runtimes (laptop CPU, all cells): notebook 1 ≈ 4 min, notebook 2
≈ 2 min (thanks to pre-sampled traces), notebook 3 ≈ 5 min.

## Repository layout

- `0*.ipynb` — the three workshop notebooks (outputs pre-baked, so they are
  readable without running anything)
- `data/` — workshop dataset (parquet/pkl), seven pre-sampled posterior
  traces (`data/idata/*/traces.nc`), ONNX likelihood networks, and the
  fixtures for the cartoon-plot section
- `images/` — figures referenced by the notebooks
- `pyproject.toml` / `uv.lock` — pinned environment (hssm v0.4.1 via git tag;
  will switch to the PyPI release once available)

## Getting help

- HSSM documentation: <https://lnccbrown.github.io/HSSM/>
- HSSM issues: <https://github.com/lnccbrown/HSSM/issues>
