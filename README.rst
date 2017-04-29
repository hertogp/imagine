.. code:: stdout

                                              \\\///
                                             / _  _ \
                                           (| (.)(.) |)
                    .--------------------.OOOo--()--oOOO.-------------------.
                    |                                                       |
                    |        ____                          _                |
                    |       /  _/____ ___   ____ _ ____ _ (_)____   ___     |
                    |       / / / __ `__ \ / __ `// __ `// // __ \ / _ \    |
                    |     _/ / / / / / / // /_/ // /_/ // // / / //  __/    |
                    |    /___//_/ /_/ /_/ \__,_/ \__, //_//_/ /_/ \___/     |
                    |                           /____/                      |
                    |                                                       |
                    '-------------------.oooO-------------------------------'
                                         (   )   Oooo.
                                          \ (    (   )
                                           \_)    ) /
                                                 (_/

A pandoc-filter to process codeblocks into images and/or ascii art
------------------------------------------------------------------

Imagine is a pandoc-filter that will turn codeblocks tagged with certain
classes into images or ascii art. The following classes are currently
supported:

::

    actdiag, asy, asymptote, blockdiag, boxes, circo, ctioga2, ditaa, dot, fdp,
    figlet, flydraw, gle, gnuplot, graph, graphviz, gri, imagine, mermaid, mscgen,
    neato, nwdiag, octave, packetdiag, pic, pic2plot, plantuml, plot, ploticus,
    protocol, pyxplot, rackdiag, seqdiag, sfdp, shebang, twopi

Examples
--------

*`Mscgen <http://www.mcternan.me.uk/mscgen/>`__*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ```{.mscgen imgout="fcb,img"}
    msc {
     hscale="1.3", arcgradient = "8";

     a [label="Client"],b [label="Server"];

     a=>b [label="data1"];
     a-xb [label="data2"];
     a=>b [label="data3"];
     a<=b [label="ack1, nack2"];
     a=>b [label="data2", arcskip="1"];
     |||;
     a<=b [label="ack3"];
     |||;
    }
    ```

|image0|

For more examples see the `sample.pdf <examples/sample.pdf>`__.

*`Octave <https://www.gnu.org/software/octave>`__*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ```{.octave imgout="fcb,img"}
    figure(1, 'visible', 'off');
    surf(peaks);
    title("peaks");
    print(1, argv(){1});
    ```

|image1|

`Shebang <http://www.google.com/search?q=linux+shebang>`__ using Python & Pygal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ```{.shebang imgout="fcb,img"}
    #!/usr/bin/env python3
    import sys
    import pygal
    from math import cos
    xy_chart = pygal.XY()
    xy_chart.title = 'XY Cosinus'
    xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
    xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
    xy_chart.render_to_png(sys.argv[-1])
    ```

|image2|

*`boxes <http://boxes.thomasjensen.com>`__*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    ```{.shebang imgout="fcb,stdout"}
    #!/bin/bash
    # I seem to have got myself boxed in!
    cat $0 | boxes -d peek -p h4
    ```

.. code:: stdout

    /*       _\|/_
             (o o)
     +----oOO-{_}-OOo------------------------------+
     |    #!/bin/bash                              |
     |    # I seem to have got myself boxed in!    |
     |    cat $0 | boxes -d peek -p h4             |
     +--------------------------------------------*/

All details
-----------

.. code:: stdout

    class <class 'imagine.Asy'>
    class <class 'imagine.BlockDiag'>
    class <class 'imagine.Boxes'>
    class <class 'imagine.Ctioga2'>
    class <class 'imagine.Ditaa'>
    class <class 'imagine.Figlet'>
    class <class 'imagine.Flydraw'>
    class <class 'imagine.Gle'>
    class <class 'imagine.GnuPlot'>
    class <class 'imagine.Graph'>
    class <class 'imagine.Graphviz'>
    class <class 'imagine.Gri'>
    class <class 'imagine.Imagine'>
    class <class 'imagine.Mermaid'>
    class <class 'imagine.MscGen'>
    class <class 'imagine.Octave'>
    class <class 'imagine.Pic2Plot'>
    class <class 'imagine.PlantUml'>
    class <class 'imagine.Plot'>
    class <class 'imagine.Ploticus'>
    class <class 'imagine.Protocol'>
    class <class 'imagine.PyxPlot'>
    class <class 'imagine.SheBang'>

        ```asy
        code
        ```
        =>  asy -o <fname>.<fmt> [<options>] <fname>.asy
        <=  Para(Image)
        

.. raw:: html

   <!-- vim:set ft=pandoc: -->

.. |image0| image:: pd-images/48e1334a80a0ac5f5854e139f328920f9e7d67c4.png
.. |image1| image:: pd-images/97a5ccef8c2f73c2897bc3f07ebe27fb971d957b.png
.. |image2| image:: pd-images/8296b8c4e66da192e78d37c805a731fa3374e1c8.png

