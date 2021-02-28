
f2py --fcompiler=gfortran -c -L/usr/lib -L/usr/lib -lfinterp -lgfortran -lgomp solve_HJB.f90 -m HJB --opt='-funroll-all-loops -fopenmp -O3 -mavx2 -fPIC'

