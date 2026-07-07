#!/bin/bash
cd "$(dirname "$0")"
BB="../barolo_examples/BBarolo"
PY=~/envs/astro/bin/python3
for g in NGC_3198 NGC_2841 NGC_3521; do
  f="${g}_RO_CUBE_THINGS.FITS"
  # wait for file to exist and stop growing
  while [ ! -f "$f" ]; do sleep 30; done
  s1=0; s2=$(stat -f%z "$f")
  while [ "$s1" != "$s2" ]; do s1=$s2; sleep 45; s2=$(stat -f%z "$f"); done
  echo "$(date +%H:%M:%S) $g cube complete ($s2 bytes); making par + fitting"
  $PY make_par.py $g && $BB -p $(echo $g | tr A-Z a-z).par > ${g}_bbarolo.log 2>&1
  echo "$(date +%H:%M:%S) $g BBarolo done (exit $?)"
done
echo "ALL FITS DONE"
