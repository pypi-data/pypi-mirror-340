sphinxcontrib-plot
*********************

A sphinx extension to plot all kinds of graph such as ditaa, gnuplot, pyplot,
dot, magick, blockdiag, seqdiag, actdiag, nwdiag.

.. image:: http://gnuplot.sourceforge.net/demo_5.2/transparent.2.png

The extension defines a new ".. plot::" directive.

The directive execute the given command/script and insert the generated figure
into the document (like the .. image:: directive). It is indeed composed by
two steps:

    1) Execute the command or script in ".. plot::" directive to generate the
       image.

    2) Include the generated image as the built-in ".. image::" directive.
       Sometimes you may desginate the image name by ":image:" options.

For example you execute "some_command parameters_or_script" to generate the
"command_output.png", Writing the directive as following would include the
image into you document::

    .. plot command_to_generate_image parameters_or_script
       :image: command_output.png

A real examples is magick as following and more examples are shown later.::

    .. plot:: magick rose: -fill none -stroke white -draw 'line 5,40 65,5'  rose_raw.png
       :image: rose_raw.png 

This is the output: |imagemagick_example1|

.. .. contents::
..     :depth: 2

1. Installing and setup
=======================

1) Install::

    pip install sphinxcontrib-plot

2) Set "sphinx_plot_directive" to the list of extensions in the conf.py::

    extensions = ['sphinxcontrib.plot']

3) You may need to install extra plot command that sphinx-plot-directive depending on what plot command you call:

    apt install imagemagick inkscape

2. Usage
============

Inlcuding a ".. plot::" code block in your sphinx document would generate the figure into the built document directly. For HTML output it's .png(or other format figure), For LaTeX output, it will include a .pdf(or other format), etc..

The plot content may be defined in one of Three ways:

1) A simple plot command to generate a figure.::

    .. plot:: magick rose: -fill none -stroke white -draw 'line 5,40 65,5'  rose_raw.png

The output is:

|imagemagick_example1|.

2) A plot command(gnuplot, ditaa, matplotlib or graphviz) with inline script::

    .. plot:: gnuplot
        :caption: figure 3. illustration for gnuplot
        :image: test.png

        set output "test.png"
        set terminal pngcairo size 900,600
        set style fill transparent solid 0.5 noborder
        set style function filledcurves y1=0
        Gauss(x,mu,sigma) = 1./(sigma*sqrt(2*pi)) * exp( -(x-mu)**2 / (2*sigma**2) )
        d1(x) = Gauss(x, 0.5, 0.5)
        d2(x) = Gauss(x,  2.,  1.)
        d3(x) = Gauss(x, -1.,  2.)
        set xrange [-5:5]
        set yrange [0:1]
        set key title "Gaussian Distribution"
        set key top left Left reverse samplen 1
        set title "Transparent filled curves"
        plot d1(x) fs solid 1.0 lc rgb "forest-green" title "μ =  0.5 σ = 0.5", \
             d2(x) lc rgb "gold" title "μ =  2.0 σ = 1.0", \
             d3(x) lc rgb "dark-violet" title "μ = -1.0 σ = 2.0"

The output is:

|gnuplot_example|.

3) inline image used for showing small images as part of the line of a text - for example, an icons. ::

    This is a |rose|.

    .. |rose| plot:: magick rose: -fill none -stroke white -draw 'line 5,40 65,5'  rose_raw.png

The output is:

This is a |imagemagick_example1|.

3 Options
===========

sphinx-plot-directive provide some options for easy use.

3.1 command options
-------------------

First of all, you can add any parameter after the command. sphinx-plot-directive
doesn't know and interfere with it and only get the graph after it's executed.
for example::

    .. plot:: ditaa --no-antialias -s 2
       :caption: figure 1. illustration for ditaa with option.

        +--------+   +-------+    +-------+
        |        | --+ ditaa +--> |       |
        |  Text  |   +-------+    |diagram|
        |Document|   |!magic!|    |       |
        |     {d}|   |       |    |       |
        +---+----+   +-------+    +-------+
            :                         ^
            |       Lots of work      |
            +-------------------------+

3.2 sphinx-plot-directive options
---------------------------------

sphinx-plot-directive specific options:

    #. :caption: Caption of the generated figure.
    #. :image: Explicitly give the output image for the command or inline script.
    #. :script: Use it to replace the inline script. If given, the inline script is ignored. You must make sure it's readable.
    #. :plot_format: the output image format, for example svg, png, etc, overwrite global plot_format.
    #. :annotate: add annotate or watermark.
    #. :show_source: for text generated iamge, if the source code is shown. 
    #. :hidden: Only generate the image bug doesn't render it in the document.
    #. :latex_show_max_png: When the target is .gif, We can magick it to multiple .png, then this defines how many frames would be shown in latex output. it's integer.

Common image options:

Since plot generate figure/image, it's in fact a image. So all the options of figure and image could be used. For example:

    #. :name: the reference name for the figure/image. For html, it would rename the output file to the @name. Since latex doesn't do well in supporting :name: for example doesn't support Chinese/SPACE, doesn't generate linke to :name, we don't do that in latex.

For example::

    .. plot:: gnuplot
        :caption: figure 1. illustration for gnuplot with watermark.
        :size: 900,600
        :width: 600

        plot [-5:5] (sin(1/x) - cos(x))*erfc(x)

3.3 global options
---------------------------------

You can define the prefered format for different output. For example the the following options define we try best to generate the .svg for htm and .pdf for latex. It's best effort so if it couldn't be done, the output format might be .png or anything else.::

    plot_format = dict(html='svg', latex='pdf')

4. More Examples: gnuplot/ditaa/matplotlib/graphviz/imagemagick/seqdiag
=========================================================================

In rst we we use `image`_ and `figure`_ directive to render image/figure. In fact we can plot anything in rst as it was on shell. You need only include the command or script in the directive body, then the figure would be automatically included in your sphinx document. For examples:

4.1 gnuplot example
-------------------

The first example is gnuplot.::

    .. plot:: gnuplot
        :caption: figure 3. illustration for gnuplot
        :image: test.png

        set output "test.png"
        set terminal pngcairo size 900,600
        set style fill transparent solid 0.5 noborder
        set style function filledcurves y1=0
        Gauss(x,mu,sigma) = 1./(sigma*sqrt(2*pi)) * exp( -(x-mu)**2 / (2*sigma**2) )
        d1(x) = Gauss(x, 0.5, 0.5)
        d2(x) = Gauss(x,  2.,  1.)
        d3(x) = Gauss(x, -1.,  2.)
        set xrange [-5:5]
        set yrange [0:1]
        set key title "Gaussian Distribution"
        set key top left Left reverse samplen 1
        set title "Transparent filled curves"
        plot d1(x) fs solid 1.0 lc rgb "forest-green" title "μ =  0.5 σ = 0.5", \
             d2(x) lc rgb "gold" title "μ =  2.0 σ = 1.0", \
             d3(x) lc rgb "dark-violet" title "μ = -1.0 σ = 2.0"

After magick using gnuplot, the above file becomes: |gnuplot_example|

4.2 ditaa example
-------------------

Another example is ditaa. ditaa_ is a small command-line utility that can
magick diagrams drawn using ascii art into proper bitmap graphics. Ditaa is in
java and we We could use following directive to render the image with extra
parameters::

    .. plot:: ditaa
       :caption: figure 1. illustration for ditaa

        +--------+   +-------+    +-------+
        |        | --+ ditaa +--> |       |
        |  Text  |   +-------+    |diagram|
        |Document|   |!magic!|    |       |
        |     {d}|   |       |    |       |
        +---+----+   +-------+    +-------+
            :                         ^
            |       Lots of work      |
            +-------------------------+

To support vector image you can add --svg parameter, it could be converted to
.pdf in latex automatically::

    .. plot:: ditaa --svg
       :caption: figure 2. illustration for ditaa with option

          +--------+   +-------+    +-------+
          |        | --+ ditaa +--> |       |
          |  Text  |   +-------+    |diagram|
          |Document|   |!magic!|    |       |
          |     {d}|   |       |    |       |
          +---+----+   +-------+    +-------+
              :                         ^
              |       Lots of work      |
              +-------------------------+

After magick using ditaa, the above file becomes: |ditaa_example|

4.3 python(matplotlib) example
---------------------------------

Another example is mulplotlib.plot. ::

    .. plot:: python
        :caption: figure 4. illustration for python

        import numpy as np
        import matplotlib.pyplot as plt

        x = np.linspace(0, 1, 500)
        y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

        fig, ax = plt.subplots()

        ax.fill(x, y, zorder=10)
        ax.grid(True, zorder=5)
        plt.show()

After conversion using python, we could get the following image: |matplotlib_example|

4.4 graphviz(dot) example
--------------------------

Another example is graphivx(dot), since we want to generate png image, we add
the option in the command, it's dot's own option::

    .. plot:: dot -Tpng
        :caption: illustration for dot

        digraph G {

                subgraph cluster_0 {
                        style=filled;
                        color=lightgrey;
                        node [style=filled,color=white];
                        a0 -> a1 -> a2 -> a3;
                        label = "process #1";
                }

                subgraph cluster_1 {
                        node [style=filled];
                        b0 -> b1 -> b2 -> b3;
                        label = "process #2";
                        color=blue
                }
                start -> a0;
                start -> b0;
                a1 -> b3;
                b2 -> a3;
                a3 -> a0;
                a3 -> end;
                b3 -> end;

                start [shape=Mdiamond];
                end [shape=Msquare];
        }

After magick using dot, the above file becomes: |graphviz_example|

4.5 imagemagick example
-------------------------

Another example is magick. You can write the command in the commnad line::

    .. plot:: magick rose: -fill none -stroke white -draw 'line 5,40 65,5'  rose_raw.png
    :caption: illustration for magick

This is the output: |imagemagick_example1|

or you can write a magick script as the following::

    .. plot:: magick
        :caption: illustration for magick

        magick -size 140x130 xc:white -stroke black
        -fill red   -draw "path 'M 60,70 L   60,20   A 50,50 0 0,1 68.7,20.8 Z'"
        -fill green -draw "path 'M 60,70 L 68.7,20.8 A 50,50 0 0,1 77.1,23.0 Z'"
        -fill blue  -draw "path 'M 68,65 L 85.1,18.0 A 50,50 0 0,1  118,65   Z'"
        -fill gold  -draw "path 'M 60,70 L  110,70   A 50,50 0 1,1   60,20   Z'"
        -fill black -stroke none  -pointsize 10
        -draw "text 57,19 '10' text 70,20 '10' text 90,19 '70' text 113,78 '270'"

This is the output: |imagemagick_example2|

4.6 blockdiag, seqdiag, actdiag, nwdiag.
------------------------------------------

demo for blockdiag::

    .. plot:: blockdiag
        :caption: demo for blockdiag
        :name: demo for blockdiag

        blockdiag {
          // Set stacked to nodes.
          stacked [stacked];
          diamond [shape = "diamond", stacked];
          database [shape = "flowchart.database", stacked];

          stacked -> diamond -> database;
        }

This will generate the follong image on your .htm/.pdf document generated from
sphinx: |blockdiag_example|

demo for seqdiag::

    .. plot:: blockdiag
        :caption: demo for seqdiag
        :name: demo for seqdiag

    seqdiag {
      // Set edge metrix.
      edge_length = 300;  // default value is 192
      span_height = 80;  // default value is 40

      // Set fontsize.
      default_fontsize = 16;  // default value is 11

      // Do not show activity line
      activation = none;

      // Numbering edges automaticaly
      autonumber = True;

      // Change note color
      default_note_color = lightblue;

      browser  -> webserver [label = "GET \n/index.html"];
      browser <-- webserver [note = "Apache works!"];
    }

This will generate the follong image on your .htm/.pdf document generated from
sphinx: |seqdiag_example|

demo for actdiag::

    .. plot:: actdiag
        :caption: demo for actdiag
        :name: demo for actdiag

    actdiag {
      write -> convert -> image

      lane user {
         label = "User"
         write [label = "Writing reST"];
         image [label = "Get diagram IMAGE"];
      }
      lane actdiag {
         convert [label = "convert reST to Image"];
      }
    }

This will generate the follong image on your .htm/.pdf document generated from
sphinx: |actdiag_example| 

demo for nwdiag::

    .. plot:: nwdiag
        :caption: demo for actdiag
        :name: demo for actdiag

    nwdiag {
      network dmz {
          address = "210.x.x.x/24"

          web01 [address = "210.x.x.1"];
          web02 [address = "210.x.x.2"];
      }
      network internal {
          address = "172.x.x.x/24";

          web01 [address = "172.x.x.1"];
          web02 [address = "172.x.x.2"];
          db01;
          db02;
      }
    }

This will generate the follong image on your .htm/.pdf document generated from
sphinx: |nwdiag_example| 

5. License
==========

MIT

.. _ditaa: http://ditaa.sourceforge.net/
.. _image: http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
.. _figure: http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure


.. |imagemagick_example1| image:: https://legacy.imagemagick.org/Usage/draw/rose_raw.png
.. |imagemagick_example2| image:: https://legacy.imagemagick.org/Usage/draw/piechart.jpg
.. |gnuplot_example| image:: http://gnuplot.sourceforge.net/demo_5.2/transparent.2.png
.. |ditaa_example| image:: http://ditaa.sourceforge.net/images/first.png
.. |matplotlib_example| image:: https://matplotlib.org/2.0.2/_images/fill_demo1.png
.. |graphviz_example| image:: http://www.graphviz.org/Gallery/directed/cluster.png
.. |blockdiag_example| image:: http://blockdiag.com/en/_images/blockdiag-56cb174d92d602f8cc9013006e661c4806e1d5ab.png
.. |seqdiag_example| image:: http://blockdiag.com/en/_images/seqdiag-9d43a794bd1f63fc9418595e4451c5fb9c52ad39.png
.. |actdiag_example| image:: http://blockdiag.com/en/_images/actdiag-27aec367951ef70f7b5badceebbcc0c2bc687752.png
.. |nwdiag_example| image:: http://blockdiag.com/en/_images/nwdiag-be3d31eeeacd641176a6f63703748e33d278419a.png

6. Changelog
============

| 1.0 Initial upload.
| 1.0.8 Bug fix: When there is no :size: in gnuplot plot, it might crash.
| 1.0.10 Bug fix: fix the issue that magick doesn't work.
| 1.0.13 Support magick script
| 1.0.17 bug fix: magick can has no body.
| 1.0.18 New feature: 1) Support montage command; 2) Support including .gif image into html and pdf. If it's html, play the .gif, or else if it's pdf, magick the .gif to a list of frame.
| 1.0.19 Support lines starting with # in the magick/montage body.
| 1.1.0 Bug fix: It doesn't work for ditaa with magick parameters.
| 1.1.1 Support the following plot command: blockdiag, seqdiag, actdiag, nwdiag.
| 1.1.2 magick command must be in command line or in content with one worad “magick” in command line.
| 1.1.3 Bug fix: make html might cause the following error: AttributeError: 'str' object has no attribute 'extend'
| 1.1.4 Support inline image.
| 1.1.5 When the output is .gif, print the frames in 8 frames in every row by default.
| 1.1.6 When .gif is given width, then increase it in latexpdf output.
| 1.1.7 Support new commands: dwebp and others.

Refenreces
==========

#. gnuplot, http://www.gnuplot.info/
#. ditaa, https://github.com/tmthrgd/ditaa-ditaa
#. Matplotlib, https://matplotlib.org/
#. graphviz, https://graphviz.org/
#. imagemagick, https://imagemagick.org
#. blockdiag, http://blockdiag.com/en/blockdiag/index.html
#. seqdiag , http://blockdiag.com/en/seqdiag/index.html
#. actdiag , http://blockdiag.com/en/nwdiag/actdiag.html
#. nwdiag , http://blockdiag.com/en/nwdiag/index.html

