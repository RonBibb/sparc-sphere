# Method-Independent Detection of Residual Radial Structure in SPARC Dark Matter Halos Beyond Single Smooth Equilibrium Profiles

**Ron Bibb** (ORCID 0009-0004-1153-2464)
Independent Researcher, Lilburn, GA, USA
[TODO: contact email]

*Draft v0.5 — 2026-06-12 (review pass 3: dead PASP gate removed; companion citation moved to Zenodo deposit; new §3.7 reproduction on independently derived curves; new §3.8 shell absorption by the domain model; Discussion geometric-degeneracy paragraph added). Target: ApJL. Core numbers frozen from the `halo-spheres/` analysis of 2026-06-05; §3.7–3.8 from the `program2/` analysis of 2026-06-12; see README.md and program2/SCOPING.md in that folder.*

*Known fix before submission: `sphere_vs_models.py` vs-Burkert tie artifact (N=1 composite == single Burkert must score as a tie). Only 2-sphere-row numbers are quoted here, which are unaffected.*

---

## Abstract

Single smooth equilibrium halo profiles leave statistically significant, radially organized residuals in roughly one third of SPARC rotation curves. We introduce a minimum-order radial-domain decomposition: the dark-matter contribution is approximated by a minimum-order sum of tiered cored support components (Burkert form), with the order selected by the Bayesian Information Criterion. Across 121 galaxies, 35% robustly require a second radial domain — a fraction unchanged when component scales are confined to the measured radii, a constraint that simultaneously collapses all three-domain solutions, and reproduced with an NFW backbone (37%). The central result is convergence: galaxies requiring a second domain coincide with galaxies independently flagged by a localized Gaussian-shell decomposition (odds ratio 38; mass-adjusted 37.5), and the domain crossover radius tracks the independently fitted shell radius (ρ = 0.73, permutation p = 0.004, surviving half-light-radius control). Forced two-domain fits to single-domain galaxies collapse to degenerate configurations, providing an internal null. Where the structure is strong enough to test, the multi-domain selection reproduces on rotation curves re-derived from the original radio cubes by independent software — decisively (ΔBIC = 121 for NGC 2403) and at the same crossover radius — establishing that it is a property of the galaxy, not of the fitting basis. In all 41 two-domain systems the single-profile scale radius lies between the two domain scales (median factor 2.2): single smooth fits are systematically biased summaries, not merely incomplete ones. We interpret the second component as a method- and data-independent marker of a second radial support domain, make no claim about its three-dimensional geometry — which rotation curves cannot constrain — and remain agnostic as to its physical origin.

**Keywords:** Dark matter — Galaxy rotation curves — Galaxy dark matter halos — Astrostatistics

---

## 1. Introduction

Rotation curves of late-type galaxies are conventionally decomposed into baryonic contributions plus a single smooth equilibrium dark matter halo, described by cuspy profiles motivated by ΛCDM simulations (NFW; Navarro et al. 1996), observationally motivated cored profiles (Burkert 1995), or intermediate forms (Einasto 1965). The adequacy of a *single* smooth profile is usually assessed only through global fit quality. Localized departures — coherent residual features at particular radii — have been discussed largely in connection with baryonic features ("Renzo's rule"; Sancisi 2004), but a systematic, model-agnostic census of whether single smooth halos suffice is lacking.

In a companion analysis (Bibb 2026, Zenodo, doi:10.5281/zenodo.20263016) we modeled localized residual structure in SPARC (Lelli et al. 2016) rotation curves with Gaussian mass shells superposed on a Burkert backbone, finding BIC-selected shells in roughly half the sample. That decomposition is used here only as a structurally independent comparison basis, not as a source of physical claims. The present Letter asks a deliberately minimal, complementary question: *what is the minimum number of smooth, concentric, cored radial domains required by each rotation curve?* Because any sufficiently flexible component will absorb residuals — so that inferred "structure" may reflect the chosen basis rather than the galaxy — the credibility of either decomposition rests on validation. We therefore test the answer against the structurally unrelated shell decomposition, against mass-driven confounds, against an internal forced-fit null, and — most stringently — against rotation curves of the same galaxies derived independently from the original radio data cubes.

Four properties make the result reportable. First, it is robust: the multi-domain fraction is unchanged when components are forbidden from extrapolating beyond the measured radii, while unstable three-domain solutions are eliminated by the same constraint. Second, it is backbone-independent: NFW and Burkert nulls give the same fraction. Third, it is method-independent: two unrelated decompositions flag the same galaxies and localize structure to consistent radii, and this concordance is not explained by galaxy mass. Fourth, and most stringently, it is *data*-independent where it can be tested: for galaxies whose rotation curves can be re-derived from the original radio cubes by independent software, the multi-domain selection reproduces — decisively, and at the same radius. A fit improvement on one curve, however constrained the basis, cannot predict the outcome of an independent derivation from a different instrument; that this prediction succeeds is the strongest available evidence that the structure is a property of the galaxy rather than of the parameterization. We emphasize equally what the analysis does *not* find, and we make no claim about the physical origin or three-dimensional geometry of the detected structure.

## 2. Data and Methods

### 2.1 Sample and baryonic model

We use the SPARC database (Lelli et al. 2016): [TODO: confirm final sample definition] 123 galaxies with ≥ 6 rotation-curve points after quality cuts, of which 121 yield converged fits. Baryonic contributions adopt fixed mass-to-light ratios Υ_disk = 0.5 and Υ_bul = 0.7 at 3.6 μm with the gas contribution at unity, combined with signed squares so that V²_bar = V_gas|V_gas| + 0.5 V_disk|V_disk| + 0.7 V_bul|V_bul|. Velocity uncertainties are floored at 1 km/s. [TODO: state exclusion rule for points with V²_obs ≤ V²_bar, matching the companion paper.]

### 2.2 Minimum-order concentric-domain decomposition

The inferred dark-matter contribution is approximated by a minimum-order sum of cored radial support components of Burkert form,

> V²_DM(r) = Σᵢ V²_B(r; ρ₀ᵢ, aᵢ),   i = 1…N

subject to ordering constraints that enforce a tiered structure and break exchange degeneracies: ρ₀ᵢ strictly decreasing and aᵢ strictly increasing outward. A soft prior ties the total enclosed dark mass at the outermost measured point to the dynamically inferred value. Fits use bounded nonlinear least squares with 20–24 random restarts; model order is selected by BIC = χ² + 2N ln n_pts, evaluated for N = 1–4. At N = 1 the model reduces exactly to a single Burkert halo, providing the null hypothesis within the same machinery.

Two variants are run. In the **unconstrained** variant, scale radii are free. In the **capped** variant, every component is required to satisfy aᵢ ∈ [r_min, r_max], the measured radial range, so that no component's characteristic scale lies where there are no data. The cap is not a technical variant but a **stability discriminator**: structure that survives it is resolved by the data, while structure that collapses is identified as extrapolation artifact. It thereby provides an internal falsification mechanism for each candidate domain.

### 2.3 Comparison methods

**Gaussian-shell decomposition.** The companion method models localized residuals as Gaussian mass shells of center r_s, width σ, and mass M_s on a single Burkert backbone, with shell count BIC-selected and a width constraint σ/r ≤ 0.4 that defines locality. The preferred fractional width is cap-invariant: the median σ/r ≈ 0.22 is unchanged as the allowed ceiling is raised from 0.4 to 1.0, with only 4% of shells near the ceiling at a cap of 1.0. The shell and domain decompositions share data but use structurally unrelated basis functions — a localized annular perturbation versus a global cored profile — and are fit independently.

**Backbone generalization.** The minimum-order analysis of §2.2 is repeated with NFW and Einasto (fixed α = 0.16, preserving two parameters per component for a fair BIC) in place of Burkert.

## 3. Results

### 3.1 A robust two-domain population

The table below summarizes the BIC-selected model order. Unconstrained: 78/38/5 galaxies select N = 1/2/3 (64/31/4%). Capped: 79/41/0 (one galaxy selects N = 4). The multi-domain fraction is essentially unchanged, 36% versus 35%, and 95% (41/43) of multi-domain galaxies retain N ≥ 2 under the cap. By contrast, **all five** three-domain solutions collapse: in every case the third component was an inner spike below the first measured point or an outer ramp beyond the last, i.e. extrapolation rather than measurement. The data support at most two resolved radial domains.

| Variant | N=1 | N=2 | N=3 | N≥2 fraction |
|---|---|---|---|---|
| Unconstrained | 78 | 38 | 5 | 36% |
| Capped (a ∈ [r_min, r_max]) | 79 | 41 | 0 ᵃ | 35% |
| NFW backbone (unconstrained) | 76 | 36 | 9 | 37% |
| Einasto backbone ᵇ | 56 | 47 | 18 | 54% |

ᵃ One galaxy selects N = 4.
ᵇ Fixed α = 0.16; the rigid shape inflates the multi-domain fraction and should be read as a caveat on fixed-shape nulls, not as additional structure.

The decision margins are strongly asymmetric. Where two domains win, they win decisively: median ΔBIC = +43.3 over the single profile, with 23/42 cases exceeding +30 and a maximum of +1115. Where the single profile wins, it never wins decisively: the median losing margin is +4.8, 81% of losses are within ΔBIC < 6, and **no** galaxy prefers a single Burkert by ΔBIC > 10. The single-domain population is therefore adequate rather than demanded, and the quoted 35% should be read as threshold-dependent in the usual information-criterion sense.

A direct consequence concerns what a single profile reports when two domains are present. In all 41 capped two-domain systems, the single-Burkert scale radius lies between the inner and outer domain scales, with a median a_Burkert/a_in = 2.19, indicating that a single smooth backbone compresses the two-domain structure into a biased intermediate scale rather than recovering the inner domain plus a residual correction. Smooth fits can therefore not only conceal radial structure but systematically bias inferred core scales, by a factor of ~2 in this sample.

### 3.2 Backbone independence and comparison to single profiles

With an NFW backbone the multi-domain fraction is 37%, statistically indistinguishable from the Burkert 36%: the residual structure is not an artifact of fitting a cored profile to cuspy halos or vice versa. The fixed-shape Einasto null returns 54%, which we attribute to its inflexible inner slope at fixed α (table note b).

For the 41 capped two-domain galaxies, the composite outperforms every single-profile alternative on BIC, including the parameter penalty: 41/41 against a single Burkert, 29/41 against a single NFW, and 34/41 against a single Einasto. The residual structure is not absorbable by exchanging one smooth profile family for another.

### 3.3 Galaxy-level concordance with the shell method, controlling for mass

The central result is cross-method agreement. Of the 42 capped multi-domain galaxies, 39 are independently shell-bearing; of the 79 single-domain galaxies, 59 are shell-free (Fisher exact p < 10⁻⁴; odds ratio 38; overall agreement 81%).

Because both structure indicators correlate with galaxy mass, we test whether the concordance is a mass artifact. In logistic regression for multi-domain selection with log M⋆ as the base predictor, shell-bearing status adds likelihood-ratio χ² = 49.7 (p < 10⁻⁴) — an order of magnitude beyond any other covariate — while T-type, effective surface brightness, R_HI, gas fraction, and bulge presence (LR χ² = 0.01, p = 0.93) are entirely absorbed by mass, and V_flat contributes only weakly (p = 0.013). The bulge null additionally disarms the concern that the second component merely compensates for bulge–disk mass-to-light errors: if it did, bulge presence would predict multi-domain selection at fixed mass, and it does not. Stratifying into log M⋆ tertiles, the shell–domain association holds within every bin (Fisher p = 0.011, <10⁻⁴, <10⁻⁴), and the Cochran–Mantel–Haenszel mass-adjusted odds ratio is 37.5 — indistinguishable from the raw 38. At fixed mass, shell-bearing galaxies are ~37 times more likely to require a second radial domain.

### 3.4 Radial-level concordance

Co-occurrence in the same galaxies could still mean the two methods describe different features. We therefore compare *where* they place structure. For each capped two-domain galaxy we compute the crossover radius r× at which the outer component's velocity contribution overtakes the inner, and compare it to the independently fitted shell radius (nearest shell; n = 28 galaxies host both).

The two radii are strongly correlated: Spearman ρ = 0.73 (p < 10⁻⁴), with a median fractional offset |r× − r_s|/r_max = 0.188 against 0.387 for permuted shell assignments (permutation p = 0.0038). Both quantities partly track the optical half-light radius (ρ = 0.57 for r× vs. R_eff), so we control for it: residualizing both radii on R_eff, the shell–crossover correlation persists at partial ρ = 0.62 (p = 4 × 10⁻⁴). The two methods localize structure to common radii for reasons beyond a shared preference for the mid-disk. Notably, the capped fits show **stronger** radial concordance than the unconstrained fits (ρ = 0.73 vs. 0.68; permutation p = 0.004 vs. 0.047), as expected if the cap removes extrapolated components that scatter the crossover radius.

### 3.5 An internal null: forced two-domain fits

As an internal control, we force N = 2 fits on the 79 galaxies whose BIC-selected solution is single-domain. In 71/79 the added component yields negligible likelihood improvement (Δχ² < 2); only 8/79 improve genuinely but fail the BIC penalty. The forced components collapse toward degenerate configurations: median a_out/a_in = 1.16, versus 9.09 in selected two-domain systems (p < 10⁻⁴), with the added component's density suppressed by ~4 dex. Moreover, the inner–outer scale coupling present in selected systems survives control for galaxy size (partial ρ = 0.56, p = 10⁻⁴), whereas in forced fits it vanishes (partial ρ = 0.13, p = 0.25). The decomposition therefore possesses an identifiable null morphology, distinct from the selected multi-domain population.

### 3.6 What does not predict the second domain

Three deliberately reported negative results bound the interpretation.

**No privileged scale ratio.** The capped outer/inner scale ratio has median a_out/a_in ≈ 9, but it does not correlate with the dimensionless structural ratios R_HI/R_d or r_max/R_d (|ρ| ≤ 0.13, p > 0.4); it correlates only with absolute size and mass. The absolute scales track the measured extent (a_out vs. r_max: ρ = 0.80). The decomposition scales with the galaxy; it does not identify a special radius ratio.

**No common surface-density manifold.** Pooled components follow a ρ₀–a anticorrelation of slope −1.29, superficially resembling the constant surface-density relation (Donato et al. 2009), but inner and outer components occupy significantly different surface-density levels (log ρ₀a = 8.59 vs. 7.98; p < 0.001). The two tiers are not a single scaling law sampled twice.

**No gas-fraction signal at fixed mass.** Within mass tertiles, multi-domain and single-domain galaxies have indistinguishable gas fractions (p = 0.13–0.96).

### 3.7 Reproduction on independently derived rotation curves

The preceding tests establish that the second domain is independent of the fitting basis. They do not, by themselves, exclude the possibility that the structure originates in the specific rotation curves published by SPARC — for example in a localized systematic of one velocity-field extraction. We therefore test the strongest form of independence available: whether the multi-domain selection reproduces when the rotation curve is re-derived from the original radio data cubes by independent software, holding the baryonic model fixed so that only the measured velocities change.

For the dwarf control galaxies DDO 154 and DDO 168, asymmetric-drift-corrected circular-velocity curves derived by an independent group from the same survey cubes (3D forward-modeling; Iorio et al. 2017) reproduce the single-domain selection (N = 1) in both cases. On the multi-domain side, we re-derived curves for NGC 2403 and NGC 3198 directly from public THINGS-class cubes using independent tilted-ring forward-modeling software, with geometry fixed to literature tilted-ring solutions. Both reproduce the multi-domain selection decisively: NGC 2403 selects N = 2 at ΔBIC = 121 with the domain crossover at 1.9 kpc (SPARC-based value ~2.3 kpc), and NGC 3198 selects N = 2 at ΔBIC = 55. For NGC 2403 the independent curve also derives from different observations than those underlying the SPARC curve, strengthening the test.

A subset of multi-domain galaxies could not be adjudicated by this route, for stated reasons rather than negative results: the discriminating structure falls at radii where moment-map velocities are beam-suppressed (NGC 3521, where the second-domain evidence lies inside ~3.4 kpc), or the host requires warp-aware deprojection that blind fixed-geometry fits cannot supply (NGC 2841), or the independent extraction recovers too few rings to test (NGC 1003). In each such case a power control — fitting the SPARC velocities on the identical radial support and uncertainties — confirms that the failure is one of test power, not a true non-reproduction; where the independent derivation has the sampling and resolution to test the structure, it agrees. We report these as instrument-limited and defer them to derivations with per-ring uncertainty propagation. The pattern across the adjudicable cases is uniform: three reproductions across three classes of independence (same cubes/different software, different observations, different telescope), with no case in which an adequately powered independent derivation contradicted the SPARC-based selection.

### 3.8 Relation to the shell decomposition: absorption by the domain model

The galaxy- and radius-level concordance of §3.3–3.4 shows that the shell and domain methods flag the same galaxies at the same radii. A sharper question is whether the localized shells carry information *beyond* the broad two-domain structure, or whether they are largely a localized re-parameterization of it. We test this directly by freezing the BIC-selected sphere-domain model of each galaxy and asking whether Gaussian shells, fit to the residual of that frozen model using the identical shell machinery and BIC penalty of the companion analysis, survive.

They mostly do not. Among the capped two-domain galaxies, 21 of 28 shells that are selected against a single-Burkert backbone are absorbed once the second domain is modeled — they no longer improve the fit beyond the BIC penalty. Population-wide, shell detections fall from 33 to 11 once the domain model is in place. Only three galaxies retain a shell at ΔBIC > 10 against the frozen two-domain backbone; in these, the surviving shell sits well away from the domain crossover, consistent with a genuinely localized feature distinct from the broad structure. The implication is twofold: most localized "shells" in the companion analysis are the broad two-domain structure expressed in a localized basis — which is why a localized basis drew the objection that it merely improves the fit — and the domain decomposition is the more economical description, with a small residual minority of genuinely localized features isolated for separate study.

## 4. Discussion

The evidential chain is: (1) a single smooth equilibrium profile — whether NFW or Burkert — leaves BIC-significant residual structure in ~35% of SPARC galaxies; (2) the structure is limited to two resolvable radial domains, with three-domain solutions exposed as extrapolation by the data-range constraint; (3) an unrelated localized-shell decomposition flags the same galaxies, and the association is untouched by mass control; (4) the two methods place structure at consistent radii, beyond both a permutation null and a generic mid-disk scale; (5) no other measured galaxy property predicts the second domain; (6) where the structure is strong enough to test, it reproduces on rotation curves re-derived from the original radio cubes by independent software, at the same radius; and (7) when the broad two-domain model is fit first, it absorbs the large majority of the localized shells, identifying them as the same structure in a localized basis rather than independent features.

We emphasize what is and is not being claimed. The present analysis does not imply that galaxies physically contain discrete Burkert subhalos, and it does not claim decomposition **uniqueness**. It claims decomposition **convergence**: structurally independent decomposition bases repeatedly recover the same subset of galaxies as inconsistent with a single smooth equilibrium support profile. We accordingly interpret the second component as a **marker of a second radial support domain**, not as a literal nested halo: the negative results of §3.6 argue specifically against reading the components as physical objects with preferred scale ratios or a shared structural relation. A preliminary non-parametric density inversion on a demonstration subset is consistent with this picture — the freely fit ρ(r) shows low-order curvature rather than fragmenting into features at arbitrary radii — though we defer its quantitative development.

A second boundary on interpretation is geometric and absolute. A rotation curve constrains only the enclosed-mass profile M(<r) through V²(r) = GM(<r)/r; it carries no information about how the mass producing a given M(<r) is arranged in angle or in the third dimension. A second radial domain, a spherical shell, a planar ring, a stream, a warp-induced redistribution, and a localized deposit are indistinguishable in V(r) if they enclose the same mass within each radius. We therefore make no claim about the three-dimensional geometry of the detected structure: the components of our decomposition are radial mass-profile features, and the labels "domain" and "shell" denote parameterizations, not shapes. Discriminating a centrally concentrated from a localized geometry requires observables that carry angular information — azimuthal structure in the velocity field or in resolved tracers — and is deferred to analyses of that kind. The present claim is confined to what rotation curves can support: a reproducible, basis-independent feature in the enclosed-mass profile.

The forced-fit control of §3.5 makes the basis-flexibility question empirical. Forced two-domain fits to single-domain galaxies collapse toward degenerate same-scale, vanishing-density configurations with negligible likelihood gain; BIC-selected two-domain systems instead exhibit separated inner and outer scales with residual scale coupling at fixed galaxy size. The detected structure is therefore not a generic consequence of basis-function flexibility: the basis has a recognizable signature for "nothing here," and the selected population does not show it.

Nor should single-domain galaxies be read as negative detections. The margin asymmetry of §3.1 — decisive multi-domain wins against uniformly marginal single-profile wins — indicates heterogeneous structural complexity across the population: some systems clearly demand additional radial structure, while many are merely **adequately** described by a single profile rather than positively inconsistent with further structure. Whether the detected structure's origin is baryonic (e.g. features propagated from the gas disk; Sancisi 2004), kinematic, or a genuine property of the dark matter distribution is not determined here, and we decline to speculate. The single external fact available is that, at fixed mass, the second domain co-occurs with localized shell structure at odds ratio ~37.

We address directly the objection that a constrained multi-component fit might simply be an elaborate means of minimizing χ², reproducible by any sufficiently flexible function such as a high-order polynomial. Three results bear on it. The forced-fit null (§3.5) shows the basis declines to add structure where none is selected — a polynomial does not refuse. The shell-absorption test (§3.8) shows the domain model is the more economical description, absorbing the majority of localized features rather than multiplying them. And the data-independence test (§3.7) shows the selection reproduces on rotation curves derived independently from the original cubes: a flexible fit to one published curve predicts nothing about an independent derivation from a different instrument, yet the prediction holds. A χ²-minimizing re-parameterization has none of these properties.

Two limitations bound the claims. The concordant sample is modest (~40 galaxies at the galaxy level; 28 at the radial level). The basis-independence and data-independence tests are partial: the former shares the data across methods, and the latter is currently established for the subset of galaxies whose curves can be re-derived from public cubes at sufficient quality, with several multi-domain systems instrument-limited and deferred (§3.7). Confirmation against independent tracers of the same galaxies [TODO: cross-reference the multi-tracer companion analysis] is the natural next test, and is also the route to the geometric discrimination that rotation curves cannot provide.

## 5. Conclusions

A minimum-order concentric-domain decomposition of 121 SPARC rotation curves shows that ~35% of galaxies require a second radial domain beyond any single smooth equilibrium profile (NFW, Burkert, or Einasto), a result robust to confining all components within the measured radii — a constraint that simultaneously eliminates all three-domain solutions as artifacts. The detection is method-independent: an unrelated Gaussian-shell decomposition identifies the same galaxies (mass-adjusted odds ratio 37.5) and consistent radii (partial ρ = 0.62 controlling for the half-light radius), and when the domain model is fit first it absorbs the majority of those shells, identifying them as the same structure in a localized basis. Where it can be tested, the selection is also data-independent: it reproduces on rotation curves re-derived from the original radio cubes by independent software, decisively and at the same radius. The component parameters do not organize on a privileged scale ratio or a common surface-density relation, and no galaxy property beyond mass and shell structure — including bulge presence — predicts the second domain. Where two domains are present, the single-profile scale radius is a biased compromise between the two domain scales (41/41 betweenness; median factor 2.2), so smooth fits both conceal the structure and distort the inferred core scale. The residual radial structure concealed by single smooth halo fits is therefore real, bounded, reproducible on independent data, and — as to its three-dimensional geometry and physical origin — deliberately left open, to be addressed with observables that carry the angular information rotation curves lack.

---

**Acknowledgments:** [TODO: acknowledgments; SPARC database citation statement.]

**Software:** numpy, scipy, pandas, astropy, matplotlib

**Data availability:** [TODO: Zenodo DOI for the halo-spheres analysis package (scripts, per-galaxy tables, figures), including the companion shell analysis (doi:10.5281/zenodo.20263016) and the independent-derivation reproductions of §3.7.]

## References

- Burkert, A. 1995, ApJL, 447, L25
- Donato, F., Gentile, G., Salucci, P., et al. 2009, MNRAS, 397, 1169
- Einasto, J. 1965, Trudy Astrofiz. Inst. Alma-Ata, 5, 87
- Iorio, G., Fraternali, F., Nipoti, C., et al. 2017, MNRAS, 466, 4159
- Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, AJ, 152, 157
- Navarro, J. F., Frenk, C. S., & White, S. D. M. 1996, ApJ, 462, 563
- Sancisi, R. 2004, in IAU Symp. 220, Dark Matter in Galaxies, ed. S. Ryder et al. (San Francisco: ASP), 233
- [TODO: 3D-Barolo reference — Di Teodoro & Fraternali 2015, MNRAS, 451, 3021]
- [TODO: THINGS reference — Walter et al. 2008, AJ, 136, 2563]

---

## Figure plan (not yet built — three figures, ApJL-typical)

**Fig 1:** Two-panel. (a) N-distribution bar chart, unconstrained vs capped side by side (data: `tiered_spheres_full.csv`, `tiered_spheres_capped.csv`). (b) Win/loss margin asymmetry: histogram of ΔBIC for 2-domain wins vs single-profile wins (data: `capped_winloss.csv`). Existing prototype for (a): `tiered_full_summary.png`.

**Fig 2 (THE KILLER FIGURE):** two panels that are the paper. (a) Shell-bearing × multi-domain fourfold contingency, per-mass-tertile Fisher p annotated (cross-method agreement). (b) Forced vs selected fits in the (a_out/a_in, density-drop) plane: forced fits pile at ratio ~1 / drop ~4 dex, winners separate at ratio ~9 / drop ~1.8 (not basis flexibility). Data: `forced_two_sphere.csv`. Together: "same galaxies" + "not flexibility" in one figure.

**Fig 3:** One worked example galaxy (suggest NGC 6015 or NGC 2403): rotation curve with single-Burkert fit, two-domain composite, and the independent shell location marked — the whole letter in one panel. Existing prototype: panels from `panels_tiers_2and3.png`.

**Fig 4 (NEW — data independence):** NGC 2403 rotation curve as published by SPARC and as independently re-derived from the radio cube, overplotted, each with its two-domain composite fit and crossover radius marked — showing the same two-domain structure at the same radius from independent data. Optionally a second panel: ΔBIC(N=2 vs N=1) for SPARC-based vs independently-derived curves across the adjudicable galaxies. Data: `program2/SCOPING.md`, `out_NGC_*/rings_final2.txt`, `program2_barolo_refit.py` outputs.

## Evidence map (claim → source)

| Claim | Source |
|---|---|
| 35% / robustness | `tiered_spheres_full.csv`, `tiered_spheres_capped.csv` |
| Margins +43.3 / +4.8 | `capped_winloss.csv`, `two_vs_one_margins.csv` |
| NFW 37% / Einasto 54% | `tiered_multimodel.csv` |
| 41/41, 29/41, 34/41 | `sphere_vs_models.py` output (2-sphere rows only; tie artifact does not affect these rows) |
| OR 38 / CMH 37.5 | mass-control analysis (Test A/C session output) |
| LR χ² = 49.7 | logistic regression session output |
| ρ = 0.73 / p = 0.0038 | `spatial_coincidence_capped.csv` |
| Partial ρ = 0.62 | R_eff-control session output |
| σ/r cap-invariance | shell sweep, caps 0.4–1.0 table |
| Negatives | `two_sphere_params.csv`, organization analyses |
| 41/41 betweenness, median 2.19 | `ain_vs_burkert.csv` (`bulge_and_ain_tests.py`) |
| Bulge null (LR χ²=0.01) | `bulge_and_ain_tests.py` output |
| Forced null (1.16 vs 9.09; partial ρ 0.56 vs 0.13) | `forced_two_sphere.csv` |
| §3.7 data-independence: NGC2403 ΔBIC121 r×1.9; NGC3198 ΔBIC55; DDO154/168 N=1 | `program2/SCOPING.md`, `program2_barolo_refit.py` / `program2_iorio_refit.py` outputs |
| §3.7 instrument-limited (2841 warp, 3521 inner, 1003 extraction) + power controls | `program2/SCOPING.md` |
| §3.8 shell absorption (21/28 absorbed; 33→11; 3 survive ΔBIC>10) | `shells_after_spheres.py`, `data/shells_after_spheres.csv` |
