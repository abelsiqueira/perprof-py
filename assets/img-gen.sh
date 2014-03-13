#!/bin/bash

cmd="perprof --demo $1"

rm -f *.png
rm -f *.pdf *.tex

for backend in --mp --tikz
do
  $cmd $backend -o abc
  $cmd $backend --semilog -o abc-semilog
  $cmd $backend --semilog --black-and-white -o abc-semilog-bw
  $cmd $backend --semilog --subset hs.subset -o abc-semilog-hs
  $cmd $backend --tau 100 -o abc-100 --semilog
  $cmd $backend --maxtime 100 -o abc-t100 --semilog
  $cmd $backend --mintime 1 -o abc-m1 --semilog
  $cmd $backend --background 255,255,255 --semilog -o abc-whiteplot
  $cmd $backend --page-background 0,0,0 --semilog -o abc-blackpage
  $cmd $backend --page-background 0,0,0 --background 255,255,255 --semilog -o abc-blackpage-whiteplot
done

for i in *.png
do
  mv $i ${i//./-mp.}
done

for i in *.pdf
do
  convert -density 400 $i -scale 800x600 ${i//.pdf/-tikz}.png
done
