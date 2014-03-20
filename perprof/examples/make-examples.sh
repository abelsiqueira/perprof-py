#!/bin/bash

[ -x perprof ] && echo "perprof not installed or I could not find it" && exit 1

lang=en
case $1 in
  -l | --lang )
    case $2 in
      en | pt_BR )
        lang=$2
        ;;
      *)
        echo "Unrecognized language $2. Choose from {en, pt_BR}."
        exit 1
        ;;
    esac
    ;;
  *)
    ;;
esac

rm -rf plots
mkdir -p plots

args="-l $lang"

for backend in --tikz --mp
do
  perprof $backend $args --demo -o plots/abc
  perprof $backend $args --demo --semilog -o plots/abc-semilog
  perprof $backend $args --demo --semilog --black-and-white -o plots/abc-semilog-bw
  perprof $backend $args --demo --semilog --subset hs.subset -o plots/abc-semilog-hs
  perprof $backend $args --demo --tau 100 --semilog -o plots/abc-100
  perprof $backend $args --demo --maxtime 100 --semilog -o plots/abc-t100
  perprof $backend $args --demo --mintime 1 --semilog -o plots/abc-m1
  perprof $backend $args --demo --background 255,255,255 --semilog \
  -o plots/abc-whiteplot
  perprof $backend $args --demo --page-background 0,0,0 --semilog \
  -o plots/abc-blackpage
  perprof $backend $args --demo --page-background 0,0,0 --background \
  255,255,255 --semilog -o plots/abc-blackpage-whiteplot
done
