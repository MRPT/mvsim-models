#!/bin/bash
# Regenerates the normal maps of textures that have no official one.
# Columns: color texture, mean normal tilt [deg] (negative: invert height).
set -e
cd "$(dirname "$0")"

while read -r tex tilt; do
	case $tex in
	*_BaseColor.png) out=${tex%_BaseColor.png}_Normal.png ;;
	*) out=${tex%.*}_normal.png ;;
	esac
	echo "$tex -> $out"
	./generate-normal-map.py "$tex" "$out" "$tilt"
done <<'LIST'
wall-bricks-01.png -25
wall-bricks-02.png -25
wall-concrete-01.jpg 20
concrete-ground-1.jpg 12
TwoLaneRoadCracks01_1K_BaseColor.png 15
TwoLaneRoadCracks01_1K_Turn90_BaseColor.png 15
TwoLaneSolidLineRoadClean01_1K_BaseColor.png 10
BathroomTiles03_1K_BaseColor.png 6
Pebbles02_512_BaseColor.png 30
Dirt01_512_BaseColor.png 25
Dirt02_1K_BaseColor.png 25
ConcreteWall02_1K_BaseColor.png 20
Grass01_1K_BaseColor.png 25
WoodenPlanks01_1K_BaseColor.png 20
WhiteGravel02_512_BaseColor.png 30
PavingStone11_1K_BaseColor.png 25
LIST
