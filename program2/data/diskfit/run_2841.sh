#!/bin/bash
# Usage: ./run_diskfit.sh smoke|disk|boot
cd "$(dirname "$0")"
BB=DiskFit-1.2.3/DiskFit
mkdir -p logs
case "$1" in
  smoke)  # validate the binary on the shipped example (~min); compare to EXPECTED in TESTS/
    mkdir -p DiskFit-1.2.3/EXAMPLE/VELS/FITS/OUT
    ( cd DiskFit-1.2.3 && echo "'EXAMPLE/VELS/FITS/velsf_disk.inp'" | ./DiskFit ) 2>&1 | tee logs/smoke.log ;;
  disk)   # NGC2841 disk-only fit, no bootstrap (fast first look)
    ~/envs/astro/bin/python3 prep_2841.py
    echo "'ngc2841_disk.inp'" | caffeinate -i $BB 2>&1 | tee logs/n2841_disk.log ;;
  boot)   # NGC2841 with bootstrap errors (the real run; NBOOT in prep_2841.py)
    ~/envs/astro/bin/python3 prep_2841.py
    echo "'ngc2841_boot.inp'" | caffeinate -i $BB 2>&1 | tee logs/n2841_boot.log ;;
  *) echo "usage: $0 smoke|disk|boot";;
esac
