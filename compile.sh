MODCODE='linear_interpolation_module.f90' # module file name
LIBOUT='libfinterp.a'                     # name of library
DOCDIR='./doc/'                           # build directory for documentation
SRCDIR='./src/'                           # library source directory
TESTSRCDIR='./src/tests/'                 # unit test source directory
BINDIR='./bin/'                           # build directory for unit tests
LIBDIR='./lib/'                           # build directory for library
FORDMD='finterp.md'   


f2py --fcompiler=gfortran -c -L/usr/lib -L/usr/lib -lfinterp -lgfortran -lgomp solve_HJB.f90 -m HJB --opt='-funroll-all-loops -fopenmp -O3 -mavx2 -fPIC'

