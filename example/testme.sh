#!/usr/bin/env bash
cd $(dirname "$0")
python -m tscprojpy.cli xyscale --scale 300 --input 2507vlteas2.cmproj/project.tscproj --output 2507vlteas4.cmproj/project.tscproj
open 2507vlteas2.cmproj
open 2507vlteas3.cmproj
open 2507vlteas4.cmproj
