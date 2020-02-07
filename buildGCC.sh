#!/bin/bash

GCCVER=9.1.0
GCCPRE=9.1

rm -rfv build/
mkdir build
cd build

../gcc-$GCCVER/configure -v --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu --prefix=$HOME/Source/GCC/bin/gcc-$GCCPRE --enable-checking=release --enable-languages=c,c++,fortran --disable-multilib --program-suffix=-$GCCPRE
make -j12
make install-strip
