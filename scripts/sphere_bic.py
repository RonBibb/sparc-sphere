#!/usr/bin/env python3
"""
sphere_bic.py

Nested "onion" halo model: fit N finite uniform-density spheres (N = 1..NMAX)
to each SPARC halo rotation curve and use BIC to select how many spheres the
data actually justify. Each sphere costs 2 parameters (a density and a radius),
so BIC charges a complexity penalty of k*ln(n) with k = 2N. A more complex model
is adopted only if it lowers BIC by at least DBIC_THRESH (program convention = 6,
"strong preference").

This is the sphere-family analogue of the program's shell BIC selection: it tells
you how many density components the data support, NOT that the halo is literally
N uniform balls. A smooth declining density is approximated by a staircase, and a
finer staircase always fits better -- BIC just caps how fine the noise permits.

Conventions (locked to the program):
    G = 4.30091e-6 kpc (km/s)^2 / Msun
    Upsilon_disk = 0.5, Upsilon_bul = 0.7   (3.6 micron)
    1 km/s velocity-error floor
    Fit and likelihood are in VELOCITY space (matches the 1 km/s floor convention).

Run from repo root:
    python scripts/sphere_bic.py
DATA_DIR defaults to ../Rotmod_LTG (one level up). Override with $DATA_DIR or argv[1].
Output: data/sphere_bic.csv  (+ summary printed to stdout).

Notes / caveats baked into the design:
  * A galaxy is only OFFERED an N-sphere model if it has > 2N+1 data points
    (need more points than parameters). So 5-sphere fits are only attempted on
    galaxies with >= 12 points; the high-N statistics are on well-sampled galaxies.
  * Early stop: once adding a sphere fails to lower BIC, higher N is not attempted
    (more spheres essentially never help once one stops helping). This is a greedy
    prune for speed; it can in rare multimodal cases miss a better high-N fit.
  * Multi-sphere fits are multimodal; we use 2 radius seedings per N and keep the
    best chi^2. Spheres are exchangeable, so the fitted ordering is not meaningful.
"""
import os
import sys
import glob
import csv
import numpy as np
from scipy.optimize import curve_fit

# ----------------------------- locked constants -----------------------------
G           = 4.30091e-6        # kpc (km/s)^2 / Msun
YD, YB      = 0.5, 0.7          # Upsilon disk / bulge at 3.6 um
ERR_FLOOR   = 1.0               # km/s
DBIC_THRESH = 6.0               # strong-preference threshold (program convention)
NMAX        = 5                 # maximum number of spheres to try

DATA_DIR = (sys.argv[1] if len(sys.argv) > 1
            else os.environ.get("DATA_DIR", "../Rotmod_LTG"))
OUT_CSV  = "data/sphere_bic.csv"


# ----------------------------- model -----------------------------
def Munif(r, lrho, R):
    """Enclosed mass of a finite uniform sphere: rho=10**lrho for r<R, constant beyond."""
    rr = np.minimum(r, R)
    return (4.0 / 3.0) * np.pi * (10.0 ** lrho) * rr**3


def make_model(nsph, vbar2):
    """Velocity-space model V(r; params) for nsph finite uniform spheres + baryons."""
    def model(r, *p):
        v2 = np.zeros_like(r)
        for i in range(nsph):
            v2 += G * Munif(r, p[2 * i], p[2 * i + 1]) / r
        return np.sqrt(np.clip(vbar2 + v2, 0, None))
    return model


def load_rotmod(path):
    rows = []
    for ln in open(path):
        if ln.startswith("#") or not ln.strip():
            continue
        try:
            rows.append([float(ln.split()[i]) for i in range(6)])
        except (ValueError, IndexError):
            pass
    return np.array(rows).T if len(rows) >= 6 else None


def fit_nsph(rad, vobs, errv, vbar2, nsph, rmax):
    """Fit nsph spheres in velocity space; return (chi2, bic, rms) for best seed."""
    f = make_model(nsph, vbar2)
    lo = [3.0, 0.05] * nsph
    hi = [11.0, 2.5 * rmax] * nsph
    best = None
    for fr in (np.linspace(0.15, 1.2, nsph), np.geomspace(0.1, 1.5, nsph)):
        p0 = []
        for j, ff in enumerate(fr):
            p0 += [8.5 - 0.5 * j, max(0.1, ff * rmax)]
        try:
            popt, _ = curve_fit(f, rad, vobs, p0=p0, sigma=errv,
                                bounds=(lo, hi), maxfev=20000)
            chi2 = np.sum(((vobs - f(rad, *popt)) / errv) ** 2)
            if best is None or chi2 < best[0]:
                best = (chi2, popt)
        except Exception:
            continue
    if best is None:
        return None
    chi2, popt = best
    n = len(rad)
    bic = chi2 + 2 * nsph * np.log(n)
    rms = np.sqrt(np.mean((vobs - f(rad, *popt)) ** 2))
    return chi2, bic, rms


def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*_rotmod.dat")))
    if not files:
        sys.exit(f"No *_rotmod.dat files found in {DATA_DIR!r}")

    rows = []
    counts = {k: 0 for k in range(1, NMAX + 1)}
    ntot = len(files)
    for idx, path in enumerate(files, 1):
        gname = os.path.basename(path).replace("_rotmod.dat", "")
        print(f"[{idx:3d}/{ntot}] {gname:14s} ...", end="", flush=True, file=sys.stderr)
        d = load_rotmod(path)
        if d is None:
            print(" skip (no data)", file=sys.stderr)
            continue
        rad, vobs, errv, vgas, vdisk, vbul = d
        errv = np.maximum(errv, ERR_FLOOR)
        vbar2 = np.sign(vgas) * vgas**2 + YD * vdisk**2 + YB * vbul**2
        rmax = rad.max()
        npts = len(rad)

        res = {}
        for n in range(1, NMAX + 1):
            if npts < 2 * n + 2:          # need more points than params (+2 dof)
                break
            r = fit_nsph(rad, vobs, errv, vbar2, n, rmax)
            if r is None:
                break
            res[n] = r
            # early stop: if this sphere did not lower BIC vs the previous, more won't help
            if n >= 2 and res[n][1] >= res[n - 1][1]:
                break
        if 1 not in res:
            continue

        # stepwise selection: step up only if BIC drops by >= threshold
        chosen = 1
        for n in range(2, NMAX + 1):
            if n in res and (res[chosen][1] - res[n][1]) >= DBIC_THRESH:
                chosen = n
        counts[chosen] += 1
        print(f" offered<={max(res)}  chose {chosen}  RMS={res[chosen][2]:.1f}",
              file=sys.stderr)

        om = rad >= 0.75 * rmax
        row = dict(name=os.path.basename(path).replace("_rotmod.dat", ""),
                   n_pts=npts,
                   vflat=round(float(vobs[om].mean()), 1),
                   max_offered=max(res),
                   chosen=chosen,
                   rms_chosen=round(res[chosen][2], 2))
        for n in range(1, NMAX + 1):
            row[f"bic{n}"] = round(res[n][1], 1) if n in res else None
        rows.append(row)

    os.makedirs(os.path.dirname(OUT_CSV) or ".", exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    N = len(rows)
    print(f"Fitted {N} galaxies from {DATA_DIR}  (NMAX={NMAX}, DBIC threshold={DBIC_THRESH})")
    print("\nBIC-preferred number of spheres:")
    for k in range(1, NMAX + 1):
        print(f"  {k} sphere(s): {counts[k]:3d}  ({100 * counts[k] / N:.0f}%)")
    print(f"\nMedian RMS at BIC-chosen complexity: "
          f"{np.median([r['rms_chosen'] for r in rows]):.2f} km/s")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
