#!/bin/bash
base="https://www2.mpia-hd.mpg.de/THINGS/Data_files"
for g in NGC_2403 NGC_2841 NGC_3198 NGC_3521 NGC_2903 NGC_5055 NGC_6946 NGC_7331; do
  for mom in MOM0 MOM1 MOM2; do
    f="${g}_RO_${mom}_THINGS.FITS"
    [ -f "$f" ] || curl -s --max-time 300 -o "$f" "$base/$f" && echo "got $f $(du -h $f | cut -f1)"
  done
done
echo "FETCH DONE"
