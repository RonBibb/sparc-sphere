#!/bin/bash
# Usage: ./run_diskfit.sh smoke|disk|boot
cd "$(dirname "$0")"
BB=DiskFit-1.2.3/DiskFit
mkdir -p logs
case "$1" in
  smoke)  # validate the binary on the shipped example (~min); compare to EXPECTED in TESTS/
    mkdir -p DiskFit-1.2.3/EXAMPLE/VELS/FITS/OUT
    ( cd DiskFit-1.2.3 && echo "'EXAMPLE/VELS/FITS/velsf_disk.inp'" | ./DiskFit ) 2>&1 | tee logs/smoke.log ;;
  disk)   # NGC3521 disk-only fit, no bootstrap (fast first look)
    ~/envs/astro/bin/python3 prep_3521.py
    echo "'ngc3521_disk.inp'" | caffeinate -i $BB 2>&1 | tee logs/n3521_disk.log ;;
  boot)   # NGC3521 with bootstrap errors (the real run; NBOOT in prep_3521.py)
    ~/envs/astro/bin/python3 prep_3521.py
    echo "'ngc3521_boot.inp'" | caffeinate -i $BB 2>&1 | tee logs/n3521_boot.log ;;
  *) echo "usage: $0 smoke|disk|boot";;
esac
