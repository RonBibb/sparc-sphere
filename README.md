# sparc-sphere

Reproducibility package for **"Residual Radial Structure in SPARC Dark Matter
Halos Reproduces on Independently Derived Rotation Curves"** (R. Bibb, submitted
to *ApJL*).

The Letter reports that a minimum-order **radial-domain decomposition** of SPARC
rotation curves requires a second cored radial mass component in ~35% of galaxies,
and that this multi-domain selection **reproduces when the rotation curves are
independently re-derived from the original radio data cubes** — establishing the
structure as a property of the galaxies rather than of a particular published
velocity extraction. The claim is confined to the enclosed-mass profile M(<r); no
three-dimensional geometry or physical origin is claimed.

This repository contains the analysis pipeline, derived data products, figures, and
the manuscript source needed to reproduce the results.

## Contents
- `letter/`   — the manuscript source (LaTeX, AASTeX 7).
- `scripts/`  — the decomposition, model-selection, and validation pipeline.
- `data/`     — derived per-galaxy tables and analysis products (CSV).
- `figures/`  — the published figures.

Input rotation curves are the public SPARC database (Lelli, McGaugh & Schombert
2016). Third-party survey cubes (THINGS, VLA-ANGST, HALOGAS) are **not**
redistributed here; fetch scripts and parameter files reproduce the independent
re-derivations from the public sources.

## Reproducing the results
Requires Python 3 with numpy, scipy, pandas, astropy, and matplotlib. The
independent tilted-ring re-derivations additionally use 3D-Barolo (Di Teodoro &
Fraternali 2015).

```
pip install -r requirements.txt
```

Set the SPARC rotation-curve directory via the `DATA` path in
`scripts/tiered_spheres.py` (or symlink the SPARC `Rotmod_LTG` files into `data/`).

### Claim → script → output
| Result | Script | Output |
|---|---|---|
| Minimum-order selection, full sample (78/38/5; 36% multi-domain) | `tiered_spheres_full.py` | `data/tiered_spheres_full.csv` |
| Capped selection (79/41/0; 35%; 3-domain solutions collapse) | `tiered_spheres_capped.py` | `data/tiered_spheres_capped.csv` |
| Backbone independence (NFW / Burkert / Einasto) | `tiered_multi.py` | `data/tiered_multimodel.csv` |
| Composite vs single-profile win/loss (2-BIC tie band) | `sphere_vs_models.py` | (stdout grid) |
| 1-vs-2 decision margins (single profile never wins decisively) | `two_vs_one_losses.py`, `capped_winloss.py` | `data/two_vs_one_margins.csv`, `data/capped_winloss.csv` |
| Non-parametric ρ(r) inversion (basis-free) | `freeform_density.py` | `figures/freeform_density.png` |
| Cross-method radial concordance (ρ=0.73; partial ρ=0.62) | `spatial_coincidence_both.py` | `data/spatial_coincidence_capped.csv` |
| Forced-two-domain null control | `forced_component_null.py` | `data/forced_two_sphere.csv` |
| Compromise-scale bias (single-fit scale between the two domains) | `bulge_and_ain_tests.py` | `data/ain_vs_burkert.csv` |
| Independent-cube reproduction (NGC 2403, NGC 3198, etc.) | `program2_barolo_n2403.py`, `program2_barolo_refit.py`, `program2_iorio_refit.py`, `sellwood_reproduce.py` | per-galaxy refits |
| Figure 1 (worked decomposition, NGC 2403) | `fig1_composite_single.py` | `figures/fig1_composite.png` |
| Figure 2 (radial concordance) | `fig2_concordance.py` | `figures/fig2_concordance.png` |
| Figure 3 (forced-fit null) | `fig3_forced_null.py` | `figures/fig3_forced_null.png` |

`scripts/tiered_spheres.py` is the core fitter (N cored components with density
decreasing and scale increasing outward, BIC-selected order); most other scripts
import it.

## Data products (`data/`)
Per-galaxy selection tables (`tiered_spheres_{full,capped}.csv`,
`tiered_multimodel.csv`), decision margins (`two_vs_one_margins.csv`,
`capped_winloss.csv`), cross-method concordance (`spatial_coincidence_capped.csv`),
the forced-fit control (`forced_two_sphere.csv`), and the single-profile control
sample (`single_burkert_control.csv`).

## Citation
If you use this code or these data products, please cite the paper (reference to be
added on acceptance) and this archived release:

> Bibb, R. 2026, sparc-sphere: reproducibility package (vX.Y.Z), Zenodo,
> doi:10.5281/zenodo.XXXXXXXX

## License
See `LICENSE`.
