# halo-spheres

Concentric radial-domain decomposition of SPARC dark-matter halos, and its
validation against an independent Gaussian-shell method. Method-paper material.

Assembled 2026-06-05 from work originally scattered across `sparc-shells-relaxed/`.

## Working thesis (method paper)
A constrained concentric-domain ("sphere") decomposition detects residual radial
structure in SPARC halos beyond a single smooth equilibrium profile. The detection
is validated by:
1. **Robustness** to component constraints (capped a in [r_min,r_max] ~ uncapped: 35% vs 36% multi-domain).
2. **Basis-independence** - a non-parametric rho(r) inversion recovers the same structure with no imposed functional form.
3. **Cross-method galaxy concordance** - flags the same galaxies as an independent Gaussian shell model; survives mass control (CMH odds ratio 37.5, raw 38).
4. **Cross-method radial concordance** - sphere crossover radius correlates with independent shell radius (capped rho=0.73, p<1e-4; beats permutation null p=0.004; survives controlling for R_eff, partial rho=0.62, p=4e-4).

Interpretation kept deliberately agnostic: the second component is NOT claimed as a
literal sphere or a merger remnant, but as a method-independent marker of a second
radial support domain. No ontology, no merger claims.

## Headline numbers
- Minimum-order selection (BIC), N=121 galaxies:
  - uncapped: 78 / 38 / 5  (1 / 2 / 3 spheres)  -> 36% multi-domain
  - capped:   79 / 41 / 0(+1 N=4)               -> 35% multi-domain
  - 3-domain solutions COLLAPSE under capping (5 -> 0): three domains are extrapolation artifacts; two are robust.
- Win/loss of composite vs single standard profile (BIC, capped 2-sphere galaxies):
  beats single NFW ~29/41, single Burkert 41/41, single Einasto ~34/41.
- Per-backbone minimum-order (own single-profile null): NFW 37%, Burkert 36%, Einasto 54%
  (Einasto inflated by fixed alpha=0.16; note as caveat).

## NEGATIVES (report as such - they discipline the interpretation)
- Outer/inner scale ratio does NOT map to a dimensionless galaxy scale (R_HI/R_d, R_last/R_d ~ 0);
  ratio tracks absolute galaxy SIZE only -> mass sequence, not a privileged scale.
- Inner and outer spheres do NOT share one Donato surface-density manifold (differ p<0.001).
- Gas fraction at fixed mass: null (no non-mass structural predictor here).
- All galaxy-class predictors (T, SBeff, R_HI, L36) are absorbed by mass in logistic regression;
  ONLY shell-bearing survives mass control (LR chi2=49.7, p<1e-4).

## KNOWN ISSUE TO FIX BEFORE WRITE-UP
- `sphere_vs_models.py` vs-Burkert column: when composite = 1 sphere it IS a single Burkert,
  so those should score as TIES, not wins/losses. Float noise currently resolves them
  (caused the spurious capped 100/120 vs uncapped 73/120). Score N=1 vs Burkert as tie.

## scripts/  (run with ~/envs/astro/bin/python3; many import tiered_spheres.py)
PATH DEPENDENCY: scripts read rotmod files from
  ../Rotmod_LTG  and catalog/shell CSVs from ../sparc-shells-relaxed/...
via the DATA constant in tiered_spheres.py. If this folder is moved, update DATA
and the relative paths, or symlink Rotmod_LTG and the needed CSVs in here.

- tiered_spheres.py        Core fitter: N Burkert spheres, rho0 decreasing + a increasing, soft mass-closure, BIC-select N. Imported by most others.
- tiered_spheres_full.py   Uncapped full-sample run -> tiered_spheres_full.csv (78/38/5).
- tiered_spheres_capped.py Two-sided cap a in [r_min,r_max] -> tiered_spheres_capped.csv (79/41/0+1).
- tiered_multi.py          Generalized to 3 backbones (Burkert/NFW/Einasto) -> tiered_multimodel.csv. Validates Burkert=78/38/5.
- sphere_vs_models.py      FROZEN composite vs single NFW/Burkert/Einasto win/loss grid by sphere count. (has the tie bug above)
- compare_to_burkert.py    Original 5-galaxy 3-way comparison (spheres vs Burkert vs shells).
- panels_tiers.py          10-panel rotation-curve decompositions (5 two-sphere, 5 three-sphere).
- ngc2403_mass.py          NGC2403 enclosed mass M(<r) + dM/dr decomposition.
- two_vs_one_losses.py     BIC margins 1 vs 2 spheres (the "single Burkert never wins decisively" result).
- capped_winloss.py        Capped win/loss with margins (42 win / 79 lose; median win +43).
- freeform_density.py      Non-parametric rho(r), no Burkert/ordering: core-vs-cusp inner slope test.
- spatial_coincidence.py   Crossover-vs-shell radius + permutation null (uncapped).
- spatial_coincidence_both.py  Same test for BOTH capped & uncapped side by side.
- tiered_capped_test.py, tiered_composite_plot.py, sphere_bic.py  earlier exploratory/plot helpers.

## data/
- tiered_spheres_full.csv      Uncapped per-galaxy: N_best, chi2red, bic, dBIC, tier scales. (PRIMARY uncapped)
- tiered_spheres_capped.csv    Capped per-galaxy: N_capped, chi2red, tier_a. (PRIMARY - use this)
- tiered_spheres_validation.csv  Initial 5-galaxy validation (full + inner-2/3).
- tiered_multimodel.csv        Per-galaxy N_best for each of NFW/Burkert/Einasto backbones.
- two_sphere_params.csv        Uncapped two-sphere parameters (p0_in,a_in,p0_out,a_out) + ratios/surface densities.
- two_sphere_organization.csv  Organization metrics (radial ratio, sigma-equiv, Donato).
- two_vs_one_margins.csv       Per-galaxy BIC_1, BIC_2, margin, chi2 gain + catalog covariates.
- capped_winloss.csv           Per-galaxy capped win/loss vs single Burkert + Vflat.
- compare_to_burkert.csv       5-galaxy 3-way numbers.
- single_burkert_control.csv   59 no-structure control galaxies (single sphere AND no shell).
- spatial_coincidence.csv      Uncapped crossover vs shell radius.
- spatial_coincidence_capped.csv  Capped crossover vs shell radius + R_eff (the strong version, partial rho=0.62).
- two_shell_organization.csv   (SHELL-model, not sphere) 2-shell radial ratio/sigma/R_HI - included for cross-reference.

## figures/
- tiered_full_summary.png      N-distribution bar + chi2red improvement scatter.
- panels_tiers_2and3.png       10-panel decompositions.
- two_sphere_organization.png  (a, rho0) Donato plot + radial-ratio histogram.
- compare_to_burkert.png       5-galaxy chi2red bars (spheres vs Burkert vs shells).
- ngc2403_mass.png             NGC2403 enclosed mass + dM/dr.
- freeform_density.png         6 free-form rho(r), core-vs-cusp slopes.
- tiered_composite_curves.png  composite sphere rotation curves.
- ngc2841_sphere_outer_test.png  NGC2841 outer-rise / extended-sphere test.
- shell_mass_confound.png      (SHELL) mass/Vflat distributions, control vs structured.
- two_shell_structure.png      (SHELL) radial ratio, sigma/r, fractional radii, R_HI correlation.

## NEXT STEP (not yet done)
Claim-by-claim evidence map (claim -> file -> statistic -> figure) as the write-up
skeleton; fix the vs-Burkert tie artifact first.

## Addendum 2026-06-10 — halo-spheres is now the WORKING folder (shells-relaxed retiring)
Input data copied in for self-containment: data/raw/sparc_sample123.csv (catalog),
data/raw/shell_model_sweep_{summary,shells}.csv (shell-method results used by the
cross-method tests). Rotmod files remain at ../Rotmod_LTG (absolute path in
tiered_spheres.py DATA constant).

New results since assembly:
- **Bulge null:** bulge presence (Vbul>0; 30/121) does NOT predict multi-domain
  beyond mass (LR chi2=0.01, p=0.93). Kills the bulge/disk M/L objection.
  -> scripts/bulge_and_ain_tests.py
- **Compromise-scale result:** in ALL 41 capped two-domain galaxies the single-
  Burkert scale lies BETWEEN a_in and a_out (41/41), median a_B/a_in=2.19.
  Single smooth fits bias inferred core scales ~2x. -> data/ain_vs_burkert.csv
- **Forced-2-sphere negative control (STRONG):** fitting N=2 on the 79 single-
  sphere galaxies: only 8/79 fit better (penalty-blocked); 71/79 second sphere
  useless. Forced fits collapse to degenerate twins (median a_out/a_in=1.16 vs
  9.09 for winners; drop 3.97 vs 1.77 dex). Coupling a_in<->a_out at fixed size:
  winners partial rho=0.56 (p=1e-4), forced rho=0.13 (p=0.25). Real two-domain
  systems are structurally distinct components, not basis flexibility.
  -> data/forced_two_sphere.csv, scripts/forced_two_sphere.py
- Letter draft at v0.3 (chat outputs); v0.4 pending to fold in the negative control.
