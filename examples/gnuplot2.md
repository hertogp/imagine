                                    \\\///
                                   / _  _ \
                                 (| (.)(.) |)
               .---------------.OOOo--()--oOOO.--------------.
               |                                             |
               |                             _       _       |
               |      __ _ _ __  _   _ _ __ | | ___ | |_     |
               |     / _` | '_ \| | | | '_ \| |/ _ \| __|    |
               |    | (_| | | | | |_| | |_) | | (_) | |_     |
               |     \__, |_| |_|\__,_| .__/|_|\___/ \__|    |
               |     |___/            |_|                    |
               |                                             |
               '--------------.oooO--------------------------'
                               (   )   Oooo.
                                \ (    (   )
                                 \_)    ) /
                                       (_/

[*Gnuplot*](http://gnuplot.sourceforge.net)
===========================================

Note:

-   Imagine catches gnuplot's output on stdout and saves it to an output
    file. So don't `set output <name>` or Imagine will get confused and
    die miserably.

Line
----

    ```{.gnuplot im_out="fcb,img" height="50%" caption="Created by GnuPlot"}
    set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
    set key inside left top vertical Right noreverse enhanced autotitles box linetype -1 linewidth 1.000
    set samples 200, 200
    plot [-30:20] besj0(x)*0.12e1 with impulses, (x**besj0(x))-2.5 with points
    ```

![Created by GnuPlot](pd-images/c2150e3dac9dced8b67b4159c7cac0a7e28ea8b6.png){height="50%"}

Real sine
---------

    ```{.gnuplot im_out="fcb,img" height="50%" caption="Created by GnuPlot"}
    set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350
    set key inside left top vertical Right noreverse enhanced autotitles box linetype -1 linewidth 1.000
    set samples 400, 400
    plot [-10:10] real(sin(x)**besj0(x))
    ```

![Created by GnuPlot](pd-images/2ef2efb34d3080c1f08841727d323a6f93bc8ffc.png){height="50%"}

Surface
-------

    ```{.gnuplot im_out="fcb,img" caption="Another GnuPlot example"}
    set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
    set border 4095 front linetype -1 linewidth 1.000
    set view 130, 10, 1, 1
    set samples 50, 50
    set isosamples 50, 50
    unset surface
    set title "set pm3d scansbackward: correctly looking surface" 
    set pm3d implicit at s
    set pm3d scansbackward
    splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)
    ```

![Another GnuPlot example](pd-images/8c38a6039114e9b4cfbc8c1f8327ba2c170a4d20.png)

Surface revisted, but now with svg-output.

    ```{.gnuplot im_out="fcb,img" im_fmt="svg" caption="Surface via svg"}
    set terminal svg
    set border 4095 front linetype -1 linewidth 1.000
    set view 130, 10, 1, 1
    set samples 50, 50
    set isosamples 50, 50
    unset surface
    set title "set pm3d scansbackward: correctly looking surface" 
    set pm3d implicit at s
    set pm3d scansbackward
    splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)
    ```

![Surface via svg](pd-images/44d694d20745e0371bc7e64960c5af7516f27f5b.png){im_fmt="svg"}

Interlocking Tori
-----------------

    ```{.gnuplot im_fmt="png" im_out="fcb,img" caption="Gnuplot's interlocking Tori example"}
    set terminal png
    set dummy u,v
    set key bmargin center horizontal Right noreverse enhanced autotitles nobox
    set parametric
    set view 50, 30, 1, 1
    set isosamples 50, 20
    set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
    set ticslevel 0
    set title "Interlocking Tori" 
    set urange [ -3.14159 : 3.14159 ] noreverse nowriteback
    set vrange [ -3.14159 : 3.14159 ] noreverse nowriteback
    splot cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) with lines, 1+cos(u)+.5*cos(u)*cos(v),.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines
    ```

![Gnuplot\'s interlocking Tori example](pd-images/64b55c51dc289ed072df49bead687161a473fdcf.png){im_fmt="png"}

    ```{.gnuplot im_fmt="svg" im_out="fcb,img" caption="Gnuplot's interlocking Tori example"}
    set terminal svg
    set dummy u,v
    set key bmargin center horizontal Right noreverse enhanced autotitles nobox
    set parametric
    set view 50, 30, 1, 1
    set isosamples 50, 20
    set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
    set ticslevel 0
    set title "Interlocking Tori" 
    set urange [ -3.14159 : 3.14159 ] noreverse nowriteback
    set vrange [ -3.14159 : 3.14159 ] noreverse nowriteback
    splot cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) with lines, 1+cos(u)+.5*cos(u)*cos(v),.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines
    ```

![Gnuplot\'s interlocking Tori example](pd-images/b359f6ff5adc2ca27b01e03dcaefe9cd694462e1.png){im_fmt="svg"}

Documentation
=============

Imagine
-------

    gnuplot

        sudo apt-get install gnuplot
        http://www.gnuplot.info
        notes:
        - graphic data is printed to stdout
        - so 'stdout' in im_out option is silently ignored
        
        gnuplot [options] <fname>.gnuplot > <fname>.png

gnuplot -h
----------

    Usage: gnuplot [OPTION] ... [FILE]
    for X11 options see 'help X11->command-line-options'
      -V, --version
      -h, --help
      -p  --persist
      -d  --default-settings
      -c  scriptfile ARG1 ARG2 ... 
      -e  "command1; command2; ..."
    gnuplot 5.2 patchlevel 2

man page
--------

    GNUPLOT(1)               General Commands Manual               GNUPLOT(1)

    NAME
           gnuplot - an interactive plotting program

    SYNOPSIS
           gnuplot [X11 options] [options] [file ...]

    DESCRIPTION
           Gnuplot is a command-driven interactive plotting program.

           If  file  names  are  given on the command line, gnuplot loads and
           executes each file in the order specified,  and  exits  after  the
           last  file  is  processed.  If no files are given, gnuplot prompts
           for interactive commands.

           Here are some of its features:

           Plots any number of functions, built up of  C  operators,  C  math
           library  functions, and some things C doesn't have like **, sgn(),
           etc.

           User-defined constants and functions.

           All computations performed in the complex domain.  Just  the  real
           part  is  plotted  by default, but functions like imag() and abs()
           and arg() are available to override this.

           Many presentation  styles  for  plotting  user  data  from  files,
           including  surface-fitting, error bars, boxplots, histograms, heat
           maps, and simple manipulation of image data.  There is an  on-line
           demo collection at
           http://gnuplot.info/demo

           Nonlinear least-squares fitting.

           2D  and  3D  plots  with  mouse-controlled  zooming, rotation, and
           hypertext.

           Shell escapes and command line substitution.

           Load and save capability.

           Support for a huge variety of output devices and file formats.

    OPTIONS
           -p, --persist lets plot windows survive after main gnuplot program
           exits.

           -c  scriptname  ARG1  ARG2 ..., load script using gnuplot's "call"
           mechanism and pass it the remainder of the command line  as  argu-
           ments

           -d,  --default settings.  Do not read from gnuplotrc or ~/.gnuplot
           on entry.

           -e "command list" executes the requested commands  before  loading
           the next input file.

           -h, --help print summary of usage

           -V show current version

    X11 OPTIONS
           For  terminal  type  x11,  gnuplot  accepts the standard X Toolkit
           options and resources such as geometry, font, and background.  See
           the  X(1) man page for a description of common options.  For addi-
           tional X options specific to gnuplot, type help x11 on the gnuplot
           command  line.  These  options  have  no  effect on other terminal
           types.

    ENVIRONMENT
           A number of shell environment variables are understood by gnuplot.
           None of these are required.

           GNUTERM
                  The  name of the terminal type to be used by default.  This
                  can be overridden by the  gnuplotrc  or  .gnuplot  start-up
                  files and, of course, by later explicit "set terminal" com-
                  mands.

           GNUHELP
                  The pathname of the HELP file (gnuplot.gih).

           HOME   The name of a directory to search for a .gnuplot file.

           PAGER  An output filter for help messages.

           SHELL  The program used for the "shell" command.

           FIT_SCRIPT
                  Specifies a gnuplot command to be executed when  a  fit  is
                  interrupted---see "help fit".

           FIT_LOG
                  The name of the logfile maintained by fit.

           GNUPLOT_LIB
                  Additional  search  directories for data and command files.
                  The variable may contain a single directory name, or a list
                  of  directories  separated  by  ':'.  The  contents of GNU-
                  PLOT_LIB are appended to the "loadpath" variable,  but  not
                  saved with the "save" and "save set" commands.

           GDFONTPATH
                  Several  gnuplot terminal drivers access TrueType fonts via
                  the gd library.  This variable gives the font  search  path
                  for these drivers.

           GNUPLOT_DEFAULT_GDFONT
                  The default font for the terminal drivers that access True-
                  Type fonts via the gd library.

           GNUPLOT_FONTPATH
                  The font search path used by the postscript  terminal.  The
                  format is the same as for GNUPLOT_LIB. The contents of GNU-
                  PLOT_FONTPATH are appended to the "fontpath" variable,  but
                  not saved with the "save" and "save set" commands.

           GNUPLOT_PS_DIR
                  Used  by  the postscript driver to locate external prologue
                  files. Depending on the  build  process,  gnuplot  contains
                  either  a  builtin  copy of those files or simply a default
                  hardcoded path. Use this variable to  test  the  postscript
                  terminal  with  custom prologue files. See "help postscript
                  prologue".

    FILES
           gnuplotrc
                  When gnuplot is run, it first looks for a system-wide  ini-
                  tialization file named gnuplotrc.  The standard location of
                  this file expected by the program is reported by the  "show
                  loadpath" command.

           .gnuplot
                  After  loading the system-wide initialization file, if any,
                  Gnuplot looks for a private initialization file in the HOME
                  directory.   It may contain any legal gnuplot commands, but
                  typically they are limited to setting the preferred  termi-
                  nal  and  line types and defining frequently-used functions
                  or variables.

           fit.log
                  The default name of the logfile output by  the  "fit"  com-
                  mand.

    AUTHORS
           Original authors: Thomas Williams and Colin Kelley.  Starting with
           gnuplot version 3.8, the project  source  is  cooperatively  main-
           tained on SourceForge by a large number of contributors.

    BUGS
           Please report bugs using the project bug tracker on SourceForge.

    SEE ALSO
           See the printed manual or the on-line help for details on specific
           commands.  Project web site at http://gnuplot.info

    4th Berkeley Distribution      11 June 2014                    GNUPLOT(1)
