#!/bin/bash

FP='/Volumes/ESSENTIA/cosmos.csv'
MAXFLAG=0
MINFLUX=1.0
HEADER=119

# switch arrays of colors around if colors are different channels
# currently b=1, g=2, r=3
BLUE=(flux_c1_1 flux_c1_2 flux_c1_3 flux_c1_4)
GREEN=(flux_c2_1 flux_c2_2 flux_c2_3 flux_c2_4)
RED=(flux_c3_1 flux_c3_2 flux_c3_3 flux_c3_4)
OTHER=( flux_c4_1 flux_c4_2 flux_c4_3 flux_c4_4)

aq_pp -f,+$HEADER $FP -d i:id X X X X X X X X X X X X X i:flag f:flux_c1_1 f:err_c1_1 f:flux_c1_2 f:err_c1_2 f:flux_c1_3 f:err_c1_3 f:flux_c1_4 f:err_c1_4 i:fl_c1 f:flux_c2_1 f:err_c2_1 f:flux_c2_2 f:err_c2_2 f:flux_c2_3 f:err_c2_3 f:flux_c2_4 f:err_c2_4 i:fl_c2 f:flux_c3_1 f:err_c3_1 f:flux_c3_2 f:err_c3_2 f:flux_c3_3 f:err_c3_3 f:flux_c3_4 f:err_c3_4 i:fl_c3 f:flux_c4_1 f:err_c4_1 f:flux_c4_2 f:err_c4_2 f:flux_c4_3 f:err_c4_3 f:flux_c4_4 f:err_c4_4 i:fl_c4 \
-evlc flux_c1_1 "flux_c1_1 / 0.610"                                                    -evlc err_c1_1 "err_c1_1 / 0.610"                                                      -evlc flux_c1_2 "flux_c1_2 / 0.765"                                                   -evlc err_c1_2 "err_c1_2 / 0.765"                                                      -evlc flux_c1_3 "flux_c1_3 / 0.900"                                                   -evlc err_c1_3 "err_c1_3 / 0.900"                                                      -evlc flux_c1_4 "flux_c1_4 / 0.950"                                                   -evlc err_c1_4 "err_c1_4 / 0.950"                                                     -evlc flux_c2_1 "flux_c2_1 / 0.590"                                                   -evlc err_c2_1 "err_c2_1 / 0.590"                                                     -evlc flux_c2_2 "flux_c2_2 / 0.740"                                                   -evlc err_c2_2 "err_c2_2 / 0.740"                                                      -evlc flux_c2_3 "flux_c2_3 / 0.900"                                                   -evlc err_c2_3 "err_c2_3 / 0.900"                                                     -evlc flux_c2_4 "flux_c2_4 / 0.940"                                                   -evlc err_c2_4 "err_c2_4 / 0.940"                                                      -evlc flux_c3_1 "flux_c3_1 / 0.490"                                                   -evlc err_c3_1 "err_c3_1 / 0.490"                                                      -evlc flux_c3_2 "flux_c3_2 / 0.625"                                                   -evlc err_c3_2 "err_c3_2 / 0.625"                                                     -evlc flux_c3_3 "flux_c3_3 / 0.840"                                                   -evlc err_c3_3 "err_c3_3 / 0.840"                                                     -evlc flux_c3_4 "flux_c3_4 / 0.940"                                                   -evlc err_c3_4 "err_c3_4 / 0.940"                                                     -evlc flux_c4_1 "flux_c4_1 / 0.450"                                                   -evlc err_c4_1 "err_c4_1 / 0.450"                                                     -evlc flux_c4_2 "flux_c4_2 / 0.580"                                                   -evlc err_c4_2 "err_c4_2 / 0.580"                                                     -evlc flux_c4_3 "flux_c4_3 / 0.730"                                                   -evlc err_c4_3 "err_c4_3 / 0.730"                                                     -evlc flux_c4_4 "flux_c4_4 / 0.910"                                                   -evlc err_c4_4 "err_c4_4 / 0.910" \
-filt "flag <= $MAXFLAG && flux_c1_1 > $MINFLUX && flux_c1_2 > $MINFLUX && flux_c1_3 > $MINFLUX && flux_c1_4 > $MINFLUX && flux_c2_1 > $MINFLUX && flux_c2_2 > $MINFLUX && flux_c2_3 > $MINFLUX && flux_c2_4 > $MINFLUX && flux_c3_1 > $MINFLUX && flux_c3_2 > $MINFLUX&& flux_c3_3 > $MINFLUX && flux_c3_4 > $MINFLUX && flux_c4_1 > $MINFLUX && flux_c4_2 > $MINFLUX && flux_c4_3 > $MINFLUX && flux_c4_4 > $MINFLUX" \
-evlc 'f:r1' "${RED[0]}/${GREEN[0]}" \
-evlc 'f:b1' "${BLUE[0]}/${GREEN[0]}" \
-evlc 'f:r2' "${RED[1]}/${GREEN[1]}" \
-evlc 'f:b2' "${BLUE[1]}/${GREEN[1]}" \
-evlc 'f:r3' "${RED[2]}/${GREEN[2]}" \
-evlc 'f:b3' "${BLUE[2]}/${GREEN[2]}" \
-evlc 'f:r4' "${RED[3]}/${GREEN[3]}" \
-evlc 'f:b4' "${BLUE[3]}/${GREEN[3]}" \
-o color_aq.csv \
-c r1 b1 r2 b2 r3 b3 r4 b4



