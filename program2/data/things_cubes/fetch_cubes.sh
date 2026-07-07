#!/bin/bash
base="https://www2.mpia-hd.mpg.de/THINGS/Data_files"
for g in NGC_3198 NGC_2841 NGC_3521; do
  f="${g}_RO_CUBE_THINGS.FITS"
  [ -f "$f" ] && [ -s "$f" ] || curl -s --max-time 3600 -o "$f" "$base/$f"
  echo "$(date +%H:%M:%S) done $f $(du -h $f 2>/dev/null | cut -f1)"
done
echo "ALL CUBES DONE"
