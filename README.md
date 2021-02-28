# kuraOCP
This is an implementation of a Hamilton-Jacobi-Bellman equation which gives optimal controls for a family of problems with arbitrary cost on the state and quadratic cost on the control.

Details of theory are in the 'KuramotoOCP.pdf' file.

I have included a binary which is dynamically linked against the relevant libraries (finterp, gfortran, gomp) if they are contained within /usr/lib on your machine. This dynamic linking will likely break, however, so I'd advise compiling yourself.

To compile this code, you'll need a Fortran compiler and numpy, which is packaged with f2py, which generates Python-callable C-wrappers for Fortran code.

gfortran will certainly suffice.

You'll also need to compile 'finterp' written by Jacob Williams (to whom the author of this project kuraOCP is not connected in any way, shape, or form, and who does not endorse nor repudiate this work in any way to the author's knowledge. Please see licenses for details.) and link this dynamically against your code. You may find the source code for 'finterp' on github.

f2py doesn't seem to like static linking, so please make sure you dynamically link.

I have included a shell script which can be run to compile the code with the same options I used to compile my code.

Obviously, Windows/ Max users will need to substantially modify this to fit their needs.

Then, pick what parameters you like and run the "solve_HJB.py" script. Not all parameters yield stable solutions, so you might need to change spatial increments and time incremements if you pick certain parameters. Also, not all spatial incremements or time incremements yield stable solutions.

Save the data to a place you like, and then copy this location into the "solve_SDE.py" script so you can take numerical gradients of the value function and obtain approximations to optimal trajectories. You'll need to comment/uncomment things depending on what you decide to run.

Finally, if you want to plot the HJB data, run the plot_data.py script.
