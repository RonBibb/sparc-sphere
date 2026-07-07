set terminal postscript eps enhanced color font 'Helvetica,14'
set output 'out_NGC_2841/NGC2841H_rc_inc_pa.eps'
unset key
set size 0.60, 1
set style line 1 lc rgb '#A9A9A9' lt 4 pt 7 lw 1
set style line 2 lc rgb '#B22222' lt 9 pt 9 lw 1
set macros
XTICS   = 'set xtics 150.000000; set mxtics 2; set format x "%g" '
NOXTICS = 'unset xlabel; set xtics  150.000000; set mxtics 2; set format x '' '
LABELF  = 'set xlabel font "Helvetica,13"; set ylabel font "Helvetica,13" '
TICSF   = 'set xtics font "Helvetica,12"; set ytics font "Helvetica,12" '
TMARGIN = 'set tmargin at screen 0.95; set bmargin at screen 0.47; set lmargin at screen 0.10; set rmargin at screen 0.50'
MMARGIN = 'set tmargin at screen 0.47; set bmargin at screen 0.27; set lmargin at screen 0.10; set rmargin at screen 0.50'
BMARGIN = 'set tmargin at screen 0.27; set bmargin at screen 0.10; set lmargin at screen 0.10; set rmargin at screen 0.50'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [-5:1796.95]
set ylabel 'V_c  [km/s]'
set ytics 50
set mytics 5
plot 'out_NGC_2841/rings_final1.txt' u 2:3 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:3 w lp ls 2
set title ''
@MMARGIN
@NOXTICS
set yrange [66.33:81.07]
set ylabel 'i [deg]'
set ytics 5
set mytics 5
plot 'out_NGC_2841/rings_final1.txt' u 2:5 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:5 w lp ls 2
@BMARGIN
@XTICS
set xlabel 'Radius [arcsec]'
set yrange [131.415:396]
set ylabel 'P.A. [deg]'
set ytics 5
set mytics 5
plot 'out_NGC_2841/rings_final1.txt' u 2:6 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:6 w lp ls 2
unset multiplot
set output 'out_NGC_2841/NGC2841H_disp_vsys_z0.eps'
unset key
set xlabel 'Radius [arcsec]'
set xtics 200
set mxtics 2
set macros
TMARGIN = 'set tmargin at screen 0.94; set bmargin at screen 0.66; set lmargin at screen 0.10; set rmargin at screen 0.50'
MMARGIN = 'set tmargin at screen 0.66; set bmargin at screen 0.38; set lmargin at screen 0.10; set rmargin at screen 0.50'
BMARGIN = 'set tmargin at screen 0.38; set bmargin at screen 0.10; set lmargin at screen 0.10; set rmargin at screen 0.50'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [0:11]
set ylabel '{/Symbol s} [km/s]'
set ytics 5
set mytics 5
plot 'out_NGC_2841/rings_final1.txt' u 2:4 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:4 w lp ls 2
@MMARGIN
@NOXTICS
set yrange [560.33:707.07]
set ylabel 'V_{sys} [km/s]'
plot 'out_NGC_2841/rings_final1.txt' u 2:12 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:12 w lp ls 2
@BMARGIN
@XTICS
set xlabel 'Radius [arcsec]'
set yrange [9:11]
set ylabel 'Scale height [arcsec]'
plot 'out_NGC_2841/rings_final1.txt'u 2:8 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:8 w lp ls 2
unset multiplot
set output 'out_NGC_2841/NGC2841H_xc_yc_cd.eps'
set multiplot layout 3,1 rowsfirst
@LABELF
@TICSF
@TMARGIN
@NOXTICS
set yrange [456.48:557.92]
set ylabel 'X_c [pix]'
plot 'out_NGC_2841/rings_final1.txt' u 2:10 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:10 w lp ls 2
@MMARGIN
@NOXTICS
set yrange [461.07:563.53]
set ylabel 'Y_c [pix]'
plot 'out_NGC_2841/rings_final1.txt' u 2:11 w lp ls 1, 'out_NGC_2841/rings_final2.txt' u 2:11 w lp ls 2
unset multiplot; reset
