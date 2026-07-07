# PAPER 2 (companion, "Bibb 2026b") — OUTSTANDING ITEMS LEDGER
Created 2026-07-06. Current draft: halo_spheres_paper.tex (renamed from the
v0_8_XX cascade 2026-07-06 — now on git 'companion' branch; history lives in
commits, NOT filenames; edit in place + git diff, no new version-files).

*** REPO MODEL [RB 07-06]: letter + companion share one repo. companion branch
carries this paper; letter revisions on main (or letter branch). Submitted-letter
state must stay tagged as the anchor for future letter fixes (branch-from-tag,
not cherry-pick). revision_working/ copy of the letter is now REDUNDANT under
the branch model — delete it; the branch is the working copy. ***

*** TRIGGER [RB 07-06]: READY-ON-DESK-PASS. Companion must be submission-ready
when AAS78771 passes ApJL desk review (days-scale, not report-scale). Desk-pass
dissolves the hold-for-report conflict: nothing report-dependent blocks freeze
(sec:absorption already lives here; inbound-cuts question defers to revision).
STATUS [RB 07-06 pm]: HOLDING ~days. Word tweaks only until AAS78771 desk
view / review feedback gives direction. No analysis, no structural passes,
no freezes during hold. On desk-pass signal: run checklist below top-down.
AAS78771 TRACKING [07-06 eve screenshot]: stage = "Seeking Scientific Editor",
editor Not Assigned — pre-desk, quality check cleared, assignment queue
(typ. days). WATCH: editor name appears = assigned; stage "Under Review" =
DESK PASS (fires checklist); editor decision w/o review = desk action.
NOTE: submission-form metadata title has "Reproduces onIndependently" (space
lost at ingestion); manuscript + cover letter CORRECT on disk — cosmetic,
fix via msubmit correspondence one-liner or at revision. RB call.
FALLBACK TREE [RB objective 07-06: publication > prestige; letter = segue +
standalone]: AAS corridor system cross-refers proactively (RB precedent: prior
ApJ submission auto-routed to AJ editor) -> most probable "rejection" =
transfer offer to ApJ (or AJ), reviews travel with it -> ACCEPT (zero cost)
but PRICE AS LOTTERY TICKET, not warm arrival — RB experience: corridor
routing can be mechanical and AJ desk decisions are quick/arbitrary-feeling.
RULE: ONE transfer hop max, then exit to OJAp — don't burn calendar on
coin-flip desks. Quick desk-rejects = LOW-INFORMATION (fit/mood, nobody read
the science); only reviewed rejections update beliefs about the manuscript.
Exit-AAS branch: reviewed-reject at
transfer venue too, or significance-flavored dead-end -> OPEN JOURNAL OF
ASTROPHYSICS (no impact gate, zero cost, independent-friendly). Substance-
reject on the reproduction claim itself -> fold into companion §3.7 (already
hardened, tail-scoped) and ship one paper.
PREREQ ACTION [do now, regardless of ApJL outcome]: arXiv endorsement for
astro-ph.GA — OJAp is arXiv-overlay, unaffiliated authors need endorsement.
Natural endorsers: Sellwood / Spekkens (already engaged; credited §2.2).
Unlocks arXiv presence for the ENTIRE series (gamma, geometric, acquisition
emails). Days to arrange, zero cost to hold in reserve.
RB TIMELINE [07-06]: companion done 1-2 wk, letter ideally published first;
gamma paper ~1 mo concurrent (mostly data labor); geometric paper sketch
starting ~weekend — present as pure geometric structure, NO child-universe
language, at most a single embedding-interpretations fence sentence.
READINESS CHECKLIST:
  [ ] 1. DATA-AVAILABILITY BLOCK — the one hard tex blocker (commented TODO
        after acknowledgments). Needs: release package incl. NEW artifacts the
        text now cites (m121_fixed/freey10/freey20.csv, free_upsilon_bic_engine.py,
        forced_component_null.csv, einasto_free_alpha.csv) → GitHub tag →
        Zenodo DOI → fill block. If companion shares the letter repo, this is
        tag-and-mint. RB action: tag + mint; Claude action: draft block +
        package inventory. STILL THE ONE HARD BLOCKER as of 07-06.
  [x] 2. Validation-architecture item — SATISFIED IN TABLE FORM (v0_8_12,
        Table tab:alternatives at Discussion head): alternative x test x
        outcome x ref, 11 rows incl. prior/threshold rows, shared-baseline
        tablenote, tail-scoped cubes row, NOT-EXCLUDED final row. RB-proposed,
        honesty-corrected. Schematic figure now optional.
  [ ] 3. Discussion de-dup pass (v0.9 item, report-independent).
  [ ] 4. VENUE — RB decision.
  [ ] 5. Freeze v0.9 → optional round-6 sim on frozen draft → done.
  [ ] 6. WHEN LETTER CLEARS DESK (done — fired 07-06, "Seeking Reviewer"):
        send personal thank-you to J.~Sellwood — for the THINGS fit-output
        tar ball (16 galaxies incl. 2841/3521, 2026-06-12) AND the diagnostic
        guidance on why those two are the hard warp cases. Two purposes: it's
        earned, and he is THE natural arXiv-endorsement ask (see PREREQ ACTION
        above). Warm, specific, short. Offer to share the companion when ready.
NOT blockers (revision-response tier): bar covariate, soft-prior-in-k line,
rho(r) inversion (response seed banked §3), alpha>0.5 rerun. ***

WORD-TWEAK LOG (hold-scope, v0_8_12, per external stat-language review grade A):
"not absorbable"->reviewer rewrite; "strongest form of independence"->"a
demanding validation"; "clearly demand"->"require"; "adequate rather than
demanded"->"required"; conclusions "convergent"->"consistent" (title/abstract
keep Convergent — review says reduce frequency, not eliminate); abstract 2nd
"diagnostic"->"empirical signature" (defined-term uses kept).

================================================================
## SIM-6 QUESTIONS (2026-07-06) — RB addressing over weekend of 07-11
================================================================
Status: RB agrees w/ triage; on target. Verdicts + banked seeds below.

Q5 [PRE-EMPT — best EV; one Discussion paragraph] "Could two mathematically
  different decompositions recover the same crossover radius despite differing
  component parameters?" ANSWER = YES AND THAT'S THE CLAIM: r_x is the basis-
  stable observable; component parameters are basis-dependent (gauge). Evidence
  already in-paper: shell vs domain parameters differ, radii agree (rho=0.73);
  betweenness shows single fits bias the RADIUS specifically. Converts the
  non-uniqueness disclaimer from apology to positive statement. Dovetails w/
  banked inversion seed (model-free curvature AT r_x = test of the invariant).

Q2 [PRE-EMPT — two sentences in Limitations] Inclination systematics:
  coherent inclination error rescales V amplitudes (1/sin i) -> masses/
  densities shift, radial LOCATION of shape features does not; r_x is a shape
  feature. Radius-dependent inclination (warps) = the real threat, already
  handled honestly in sec:dataindep (warp-aware, underpowered). Backup if
  pushed: i+/-5deg refit check, ~20min, not needed for text.

Q4 [AUDIT ONLY — likely zero edits] "Shell absorption = variance already
  absorbed, not identical physical structure?" — attacks a claim v0_8_12 no
  longer makes; shared-baseline tablenote + retitle conceded this. AUDIT:
  read sec:absorption for pre-retitle remnants; consider softening conclusions
  "the same structure in a localized basis" -> "the same residual captured in
  a localized basis".

Q1 [DO NOT PRE-EMPT — bank response] Radial M/L gradients reproducing r_x:
  honest answer already in print 3x (global closed by free-Y; gradient channel
  explicitly not excluded). RESPONSE SEED: the real answer is unWISE W1 radial
  profiles (62 SPARC gal, in holdings, sparc-shells-relaxed/data/external/wise/)
  = MEASURED per-galaxy gradient constraints, stronger on demand than a
  synthetic estimate pre-emptively. CAUTION: do NOT reach for the R_eff-control
  argument here — shared baseline means concordance surviving R_eff control
  does not discriminate a gradient-driven feature.

Q3 [DO NOT PRE-EMPT — already fenced] Bars: table not-excluded row +
  Limitations already state it; covariate needs HyperLEDA/S4G join; on ledger
  as revision-response tier. Referee gets pointed at text that answers
  "we know, and here's the plan."

WEEKEND EXECUTION: Q5 paragraph + Q2 sentences + Q4 audit = <1hr text, no
analysis, inside hold scope -> cut as v0_8_13. Q1/Q3 stay banked.

Sources: two simulated referee reports (2026-07-06 session): SIM-A (encouraging,
major-revision) and SIM-B (critical, major-revision). SIM-B numbers are UNVERIFIED
against v0.8.6 — simulated referees confabulate statistics. VERIFY BEFORE ACTING.

STATUS TAGS: [OPEN] [BLOCKED-ON-x] [DECIDED] [DONE] [KILLED]

================================================================
## 0. VERIFICATION PASS (do FIRST — gates everything below)
================================================================
[OPEN] Confirm SIM-B's cited numbers actually appear in v0_8_6.tex:
  - rho(crossover, R_eff) = 0.57 raw
  - median losing single-domain margin = +4.8; 81% of losses ΔBIC < 6
  - 23/42 exceed ΔBIC > 30 (decisive population ~19%)
  - Einasto multi-domain alpha rails at upper bound of [0.1, 0.3]
  - population bookkeeping collision: 43 (uncapped N≥2, Table 1) vs 42 (capped
    N≥2, §3.3) vs 41 (N=2 exact, abstract/§3.1) vs 79 single-domain (§3.5)
  - soft prior on outer enclosed DM mass, charged k=2N in BIC
  - inner-point exclusion rule: V²obs ≤ V²bar cut + first-reliable-radius cut
Each confirmed number promotes its item below; each confabulated one demotes it
(test may still be right; smoking gun isn't lit).

================================================================
## 1. ANALYSIS DEBT (disk-runnable; ordered by lethality)
================================================================
[DONE 07-06] **FREE-UPSILON SELECTION RERUN** (SIM-B Major 1 — the kill shot; same flank
  flagged independently in 07-06 session as fixed Y* 0.5/0.7 vulnerability).
  Test: Υ_disk, Υ_bul free w/ lognormal prior σ≈0.1 dex (Li et al. convention),
  rerun minimum-order selection, all 165.
  GATE: NGC 2403 first (canonical ΔBIC=1115). PRE-REGISTER before full run:
  expected = decisive tail (ΔBIC>30) survives; marginal population (ΔBIC<6) erodes;
  fiducial 35% → toward ~20%.
  Outcome fork: survives → strongest robustness figure in the paper.
  Collapses → paper becomes disk-halo degeneracy result; TITLE must change.
  Second barrel: unWISE W1 photometric Υ pinning (62 SPARC gal, already in
  sparc-shells-relaxed/data/external/wise/).
  DOWNSTREAM: rerun BEFORE the f_in×feed-class fingerprint test (queue item 2,
  gamma campaign) — N=2 membership list inherits from this run.

[DONE-TEXT-FIX 07-06 v0_8_10] Einasto multi-domain alpha range: PIPELINE AUDIT
  found text-vs-code mismatch — paper said [0.1,0.3] railing at 0.3; actual run
  (einasto_free_alpha.py + .csv, the 32%) used [0.05,0.50], railing at 0.50 in
  89/120. v0_8_10 corrects Methods + tablenote b + de-fossilizes "unphysically
  flexible" single-Einasto wording. SIM-B Major 5 now HALF-CLOSED by correction
  (the wide box was already run); residual = alpha>0.5, defended as exiting
  observed halo-shape regime + port differential shows widening RAISES fraction.
  [OPEN-OPTIONAL, downgraded] paper-pipeline rerun at alpha_max>0.5 only if a
  real referee pushes past 0.5.
  Prior entry (differential port run) below for provenance:
[DONE-DIFFERENTIAL 07-06] Einasto multi-domain refit, alpha ∈ [0.1, 1.0] (SIM-B
  Major 5). CAVEAT: einasto_alpha_engine.py is NOT a faithful paper-pipeline port
  (abs fraction 16.5% at [0.1,0.3] vs paper 32%) — differential answer only.
  RESULT: widening [0.1,0.3]->[0.1,1.0] RAISES fraction 16.5%->22.6% (erosion
  worry INVERTED); railing reproduces (96% N=2 @0.3; 70% still rail @1.0; single-
  comp rails too, 76%@0.3). BUT membership churns: 18/27 retained, 19 new.
  Text posture: fraction non-decreasing under widening; membership bound-
  sensitive; Einasto = secondary leg. [OPEN-OPTIONAL] absolute rerun through
  paper pipeline if a referee demands the paper's own 32% under wide alpha.

[OPEN] Soft-prior ΔBIC contribution — one line quantifying (SIM-B minor; also
  closes the correlated-error/ΔBIC-inflation concern from 07-06 session, SIM-A era).
  Cheap companion: refit a validation galaxy w/ inflated errors, watch ΔBIC scaling.

[DONE 07-06] Inner-point exclusion robustness: PAPERCUTS flag. Fixed-Y 30.3->32.3%
  w/ cut; free-Y 29.1->28.5%. Incidence stable to cut convention. Closed.

[OPEN] Bar-presence covariate in §3.3 logistic regression (SIM-B minor). Cheap.
  Addresses mid-disk streaming confound the scale-ratio covariates miss.

[MOSTLY-DONE 07-06] Reconcile 30% engine vs ~35% companion: V²bar cut explains
  ~half (30.3->32.3%); remainder = cap variant (a∈[rmin,rmax] vs fixed bounds)
  + start-grid differences. [OPEN-SMALL] pin the last ~3pts w/ cap-variant flag
  if referee computes it; answer is already "cut/cap conventions, not a bug."

================================================================
## 2. FRAMING / TEXT DEBT (wording, not analysis)
================================================================
[OPEN] **DECISIVE-POPULATION RESTRUCTURE** (SIM-B Majors 3+4, merged): lead
  abstract w/ decisive ~1-in-5 (ΔBIC≫10) embedded in threshold-sensitive fraction
  reaching ~35% at fiducial cut. Threshold ladder = explicit organizing device
  (also dissolves the 30/35 discrepancy if framed this way).

[OPEN] §3.7 scope honesty: "reproduction demonstrated for the decisive tail;
  marginal population untested against independent cubes." Stop leaning on §3.7
  as "strongest/most direct" for the population-level 35%.

[OPEN] NGC 2841/3521 warp pair: report as UNDERPOWERED (n=2 splitting 1–1),
  not reproduction-plus-honest-failure. Take SIM-B verbatim. Forking-paths
  vulnerability otherwise.

[OPEN] Radius-concordance boundary statement: rho=0.73 establishes both bases
  localize the SAME feature; silent on dark vs baryonic origin. Say so explicitly
  (SIM-B Major 2, the part that survives regardless of freeform decision).

[OPEN] "Second resolved radial mass domain" = property of inferred enclosed-mass
  profile, not evidence of physically distinct components — state EARLIER
  (SIM-A clarification 1; both sims agree detection-vs-interpretation must stay loud).

[OPEN] Explicit statement: 35% fraction expected to evolve w/ larger samples
  (SIM-A clarification 3; slightly stronger than current wording).

[OPEN] rms-rejection positioning: 67% of N=2 rms-rejected vs 24% baseline
  (engine result). Disclose fit-quality distribution of N=2 class so hostile
  referee can't frame the second domain as garbage-collection for non-circular
  motions. Check what v0_8_6 currently says. (07-06 session, pre-SIM-B.)

[OPEN] Prep one-paragraph answer: what distinguishes NGC 3521 non-reproduction;
  does that failure mode generalize to the untested marginal 30%? (SIM-A era.)

================================================================
## 3. STANDING DECISIONS (context; do not silently reverse)
================================================================
[DECIDED 07-06, TRIAGE R4] INVERSION DEFERRED TO REVISION (supersedes the
  pending fork above for the one-week window): retitle removes the title-level
  dependence on method-independence, making deferral defensible; response-
  letter framing is banked (below). If a referee demands it, the run costs
  days and the framing is pre-written:
  RESPONSE-LETTER SEED: "The reviewer is correct that the shell and domain
  bases perturb a common single-profile baseline; the revised text states
  this (§intro, §conclusions) and the title no longer claims independence.
  To adjudicate 'discrete second domain' vs 'single bent profile' we now
  include a non-parametric enclosed-mass/density inversion for the decisive
  systems [Figure X]: separated curvature features at the crossover radius
  support the domain reading; a single monotonic bend would have supported
  profile inadequacy alone." Fork disclosed: EITHER outcome is publishable;
  the noun changes, not the detection.

[DECIDED 07-05, UNDER PRESSURE] freeform_density stays one-sentence = deliberate
  referee bait; non-parametric expansion = reserved revision card.
  SIM-B ESCALATION: welds the shared-antecedent tautology critique to the TITLE
  claim ("method-independent") — a referee who ties it to the title can reject
  over it, not just request revision. Options on the table 07-06:
  (a) hold bait, soften title ("method-independent" = extraction- +
      basis-family-independent, concede shared baseline in one sentence);
  (b) play the card now — promote inversion into a numbered section during v0.9.
  RB DECISION PENDING. Reversal of a logged decision — flag, don't smooth.

[DECIDED 07-05] v0.9 = STRUCTURAL PASS ONLY (convergence-first abstract,
  validation-architecture schematic, Discussion de-dup).
  07-06 AMENDMENT: v0.9 scope grows — Letter referee (real) may push shell-
  absorption material INTO this paper (SIM-A clarification 2 license) and Letter
  cuts land here. HOLD v0.9 until real AAS78771 report arrives — restructure once,
  not twice. Free-Υ + Einasto runs (§1) are NOT gated on this; run now.

[STANDING] Tier fence: no child/universe/topology language in this paper. Ever.

================================================================
## 4. WHAT NOT TO OVER-CORRECT (both sims agree these are strengths)
================================================================
- Forced-fit null + inner/outer forcing asymmetry (§3.5) — keep central.
- Cap-as-stability-discriminator (kills all N=3) — keep.
- Betweenness 41/41, median factor 2.2 — crisp falsifiable lead candidate
  (SIM-B suggests arguably better lead than 35%).
- Explicit non-reproduction reporting (3521, 1003) — keep the practice.
- Detection-vs-interpretation discipline in abstract/Discussion — keep.

================================================================
## LOG
2026-07-06  Created. SIM-A + SIM-B ingested. Verification pass not yet run.
2026-07-06  §0 DONE: SIM-B confabulated NOTHING — all cited numbers confirmed
  verbatim in v0_8_6 (0.57@L413, +4.8/81%@L264, 23/42@L262, alpha-rail@L341-344,
  43/42/41/79@L294/379/99/336/438, k=2N+soft prior@L195-198, cuts@L175-183,
  fixed-Y@L177-180). All §1 items promoted.
2026-07-06  Free-Y engine built (scripts/free_upsilon_bic_engine.py; flags FREEY/
  PAPERCUTS/GAL). GATE PASSED: NGC2403 fixed-Y dBIC=1115.1 bit-exact parity.
  Free-Y: dBIC 1115->264, still N=2. MECHANISM CONFIRMED ON CANONICAL GALAXY:
  N=1 inflates Yd to 0.79 to absorb inner domain; N=2 pulls Yd to 0.28.
  SIM-B Concern-1 degeneracy is real; question is the marginal population.
2026-07-06  PRE-REGISTERED (before full-165 free-Y run):
  P1. Decisive tail (fixed-Y dBIC>30, 23 systems): >=75% remain N=2 under free-Y.
  P2. Marginal (fixed-Y 0<dBIC<6): >=50% flip to N=1.
  P3. Overall N=2 fraction: 30% (engine fixed-Y baseline) -> 18-26% under free-Y.
  P4. PAPERCUTS on fixed-Y engine moves 30% TOWARD companion's 35% (delta is
      cut-convention, not a bug).
  Falsification stakes: P1 fail -> paper is disk-halo-degeneracy result, title
  changes. P3 landing ~30% unchanged -> strongest robustness figure available.
2026-07-06  FULL-165 RESULTS (all outputs copied to future-work/_repro/):
  SCORING: P1 PASS (21/23 = 91% of decisive tail stays N=2). P2 FAIL (only
  4/11 marginals flip, vs >=50% predicted — marginals MORE robust than expected).
  P3 FAIL FAVORABLY (29.1% vs predicted 18-26% — fraction UNCHANGED from 30%).
  P4 PASS-PARTIAL (cuts: 30.3->32.3%; ~half the 30-vs-35 delta).
  => SIM-B CONCERN 1 RESOLVED TO THE STRONG FORK. Free-Y is the robustness
  figure. Winners' Yd median 0.48 [0.32,0.53] — second domain does NOT live by
  dragging M/L. Honest attenuation to report: stayers' median dBIC 37->12 (~3x).
  CHURN (9 out, 7 in): NGC3521 flips OUT — coheres w/ its §3.7 non-reproduction
  (one consistent object: Y-degenerate AND non-reproducing — use in text).
  NGC7331 flips IN — MEASURED-MASS galaxy => measured∩two-sphere possibly
  NON-EMPTY under free-Y selection => crossover-vs-influence dart may unblock
  (gamma-campaign downstream; different selection convention, scrutinize first).
  NGC0289 flips OUT — gamma battery member (0289-outer); check gamma entry impact.
  Einasto: differential widening RAISES fraction (16.5->22.6%), railing persists
  at any bound, membership churns 33% — secondary-leg posture; details in §1.
  STILL OPEN in §1: soft-prior dBIC line; bar covariate (needs bar labels);
  optional paper-pipeline Einasto absolute; unWISE photometric-Y second barrel.
2026-07-06  v0_8_7 CUT (compiles clean, 0 errors, refs resolve): new \S sec:freeml
  (free-Y robustness, convention-matched numbers: 32.3->28.5%, decisive 21/24,
  Yd 0.48 [0.34,0.56], attenuation 36.5->12.1, NGC3521-exit coherence); Methods
  pointer; Limitations updated (fixed-Y confound now explicitly bounded; bars/
  Y-gradients explicitly deferred); Li+2020 bibitem. Einasto numbers deliberately
  NOT folded in (port not pipeline-faithful). Full changelog in tex header.
  DOWNGRADE: NGC7331 flip-in does NOT survive the papercuts convention — the
  measured∩two-sphere/crossover-dart unblock flag from the no-cuts run weakens;
  treat as convention-sensitive, not a finding. NGC0289 exits under BOTH
  conventions — the gamma-battery check stands.
2026-07-06  SECOND-ROUND SIM ingested. Its arithmetic concerns (32.3-vs-35, 23-vs-
  24, churn) were REAL but MISDIAGNOSED: root cause = v0_8_7 freeml numbers were
  computed on the engine's 158-curve superset, not the fiducial 121 (my error,
  not a convergence subset). FIX = matched-sample rerun (GALLIST+SIGMA flags
  added to engine): fixed 43/121=35.5% REPRODUCES Table 1; free-Y(0.1) 38/121=
  31.4%; decisive retention anchored to the PAPER's 23: 20/23. PRIOR-WIDTH
  (sim's new attack surface): sigma=0.2 -> decisive retention IDENTICAL 20/23,
  fraction 28.1% — prior sensitivity confined to marginals. NGC3521 exits at
  both widths. v0_8_8 CUT (compiles clean): freeml rewritten fiducial-chained;
  abstract free-Y clause; dataindep rhetoric demoted to tail-scoped; global-vs-
  gradient M/L scope sentence. Data: _repro/m121_*.csv.
  §2 items CLOSED by v0_8_8: §3.7-scope-honesty, decisive-vs-35 partially
  (abstract now carries both, full restructure still held for real report).
  STILL OPEN: rho(r) inversion promotion (sim escalated AGAIN, round 2 — RB
  decision pending, §3); Einasto paper-pipeline rerun; bar covariate;
  soft-prior dBIC line; radial-Y-gradient channel (now explicitly fenced in
  text, analysis deferred).
2026-07-06  TRIAGE R4 ingested + EXECUTED (v0_8_9, compiles clean):
  #1 DONE — RETITLE "Convergent Radial-Domain Structure in SPARC Dark Matter
  Halos Beyond Single Smooth Equilibrium Profiles" (kept "Dark Matter" vs
  triage's "SPARC Halos" — RB may trim); abstract re-led with betweenness,
  convergence demoted, "establishing"->"consistent with"; independence
  language swept (title, shorttitle, intro x2, evidence list w/ shared-
  baseline concession, methods "dissimilar", conclusions).
  #3 CLOSED BY INSPECTION — triage's premise false in code: the -0.95/-3.44
  offsets come from tiered_spheres_capped.fit_N, which has NO mass-closure
  prior (prior lives only in tiered_spheres.py). Confirmed by rerunning
  forced_component_null.py (reproduces -0.95/-3.44 exactly). Outer two-sample
  MW p=2.1e-4 / KS 2.0e-4 (already in text at v0_8_8, verified). One clause
  ADDED: offsets computed prior-free. Zero refits. NOTE: paper already
  discloses inner non-diagnosticity (p=0.10) — 4th report's fear was pre-
  fenced since v0.7-era edit.
  BONUS from engine work: selection side of #3 independently bounded — the
  free-Y engine has no soft prior and reproduces 35.5% + decisive 23.
  #2 DEFERRED per triage — logged as standing decision w/ response-letter
  seed (§3). Inversion remains the v1.0-revision card, now by explicit
  decision rather than drift.
2026-07-06  PIPELINE AUDIT (RB request): originals vs engine ports compared.
  Burkert cores IDENTICAL (mass integral, chi2, BIC k=2N, floor, Y, signed
  squares, trf) — explains bit-exact 1115.1 gate. Divergences: sample iteration
  (catalog vs glob), cut location (load vs flag), bounds regime (uncapped/
  capped/engine-fixed = 3 regimes), soft prior (uncapped+einasto only, never
  in k), starts (random-24 seed7 vs grid-12/36), NMAX (4 vs 2). Engine einasto
  16.5%-vs-32% delta = config not formula (alpha box, prior, param, starts).
  FINDING: Einasto text-vs-code mismatch (above) → v0_8_10 cut (compiles clean,
  0 errors): range corrected, railing restated 0.50 (89/120), single-Einasto
  null wording de-fossilized. Current draft: v0_8_10.
2026-07-06  REPORT 5 (submit call): both sentence-items VERIFIED then executed
  in v0_8_11 (compiles clean): (1) prior-free cross-reference in Methods —
  capped 35% vs standard 35.5%, capped carries no prior, Table pointer; (2)
  note-b denominator clause — missing galaxy IDENTIFIED as UGC06923 (list-diff
  vs single_burkert_all), stated as free-alpha convergence failure.
  Report 5's ledger accepted: no submission blockers remain. Its self-
  correction (P2-unconstrained rerun downgraded must-do -> sentence) matches
  our code-inspection finding from R4.
  SUBMIT CALL vs STANDING DECISIONS — flagged, RB to resolve:
  (a) v0.9 structural-pass hold-for-real-Letter-report [DECIDED 07-05/06] —
      report 5 says ship without it. Betweenness-led abstract (v0_8_9) already
      delivered the convergence-first-abstract intent; remaining v0.9 items =
      schematic + Discussion de-dup + SIM-A's shell-absorption-inbound question,
      which genuinely depends on the Letter referee. Options: ship as-is now;
      or hold days for AAS78771 signal per the one-week plan.
  (b) VENUE undecided on disk (companion cited as Bibb 2026b; letter cites it
      as in-preparation). Submission requires venue choice + Zenodo/GitHub
      release tag + data-availability DOI block check.
  Current draft: v0_8_11.
2026-07-06 (eve)  ACKNOWLEDGMENTS strengthened in halo_spheres_paper.tex:
  Sellwood & Spekkens named for the warp-aware NGC2841/3521 curves (tar ball
  2026-06-12, THINGS cubes) that enabled sec:dataindep, + kinematic-modeling
  guidance; Hazel personal thanks added. Letter's submitted acknowledgments
  left as-is (mid-review); same strengthening staged in revision_working/ for
  letter revision (now redundant under branch model — delete, use branch).
  ORCID CHECK: 0009-0004-1153-2464 is CORRECT (verified orcid.org 2026-07-06
  via RB screenshot). Earlier Claude concern about -2454 was STALE MEMORY,
  wrong — do NOT "correct" the ORCID; it is right in both letter + companion.
  AAS78771 STATE 07-06: editor ASSIGNED = Dr. Frederic Rasio; stage advanced
  "Seeking Scientific Editor" -> editor assigned -> "Seeking Reviewer" =
  DESK PASS CLEARED. Checklist above is now LIVE (was ready-hold). Companion
  should reach submission-ready before the letter's referee report (~2-3 wk).
  TERMINOLOGY STRAGGLERS (found 07-06, not yet fixed): Fig1 caption + sec:absorption
  still say "two-sphere"/"sphere-domain" (pre-retitle survivors); everywhere else
  swept to "two-domain". One-word fixes, do on next pass — a referee flags this.
  Current draft: halo_spheres_paper.tex (companion branch).
