# -*- coding: utf-8 -*-
"""
    sphinxcontrib.plot
    ~~~~~~~~~~~~~~~~~~~~~

    An extension providing a reStructuredText directive .. plot:: for including a plot in a Sphinx document.

    See the README file for details.

    :author: Yongping Guo <guoyoooping@163.com>
    :license: MIT
"""

import re, os, sys
import posixpath
from os import path
import shutil
import copy
from subprocess import Popen, PIPE
from PIL import Image
import shlex
import imghdr

try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO

try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri

OUTPUT_DEFAULT_FORMATS = dict(html='svg', latex='pdf', text=None)
OWN_OPTION_SPEC = dict( {
    #Explicitly give the output image for the command or inline script. If
    #it's given, will use it after execute. So make sure it's correct.
    'image': str,
    #Use it to replace the inline script. If given, the inline script is
    #ignored. You must make sure it's readable.
    'script': str,
    #Caption of the generated figure.
    'caption': str,
    #Control the output image size for gnuplot.
    'size': str,
    'plot_format': str,
    'annotate': str,
    'show_source': str,
    'hidden': str,
    'latex_show_max_png': int,
    #'background': str,
    })

def plot_image (app, plot):
    '''
    always plot it in this function, should check if the target exists before calling me.
    '''
    if app.builder.config.plot_log_level > 1:
        print("%s(), plot is:" %(sys._getframe().f_code.co_name))
        for k,v in plot.items():
            if k != "text":
                print("    %s: %s" %(k, v))
            else:
                print("    text: See below args")

    cmd = plot['cmd']
    args = shlex.split(cmd)
    text = plot['text']
    options = plot['total_options']
    rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    hashkey = str(cmd) + str(options) + str(plot['text'])
    hashkey = sha(hashkey.encode('utf-8')).hexdigest()
    infname = '%s-%s.%s' % (args[0], hashkey, plot['directive'])
    infullfn = path.join(app.builder.outdir, app.builder.imagedir, infname)
    ensuredir(path.join(app.builder.outdir, app.builder.imagedir))
    #Record the current dir and return here afterwards
    currpath = os.getcwd()

    plot_format = options.get("plot_format", None)
    outfname = '%s-%s.%s' %(args[0], hashkey, plot_format)
    out = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
        outfullfn = path.join(app.builder.outdir,
            app.builder.imagedir, outfname),
        outreference = None)

    #print("cmd: %s" %(cmd))
    if "ditaa" in cmd:
        if (not options.get("annotate", None)) and ("--svg " not in cmd):
            #to support Chinese, draw it always with --svg. 后面一定要有一个
            #空格以避免--svg-font-url被误判
            args.insert(1, "--svg")
        args.extend([infname, outfname])
        # Ditaa must work on the target directory.
        os.chdir(os.path.dirname(out["outfullfn"]))
    elif "seqdiag" in cmd or "blockdiag" in cmd \
            or "actdiag" in cmd or "nwdiag" in cmd:
        #seqdiag ... etc, only support svg, convert it to pdf automatically.
        if (plot_format in ["svg", "pdf"]) and ("-Tsvg" not in cmd):
            #ditaa support vector output by --svg parameter.
            args.insert(1, "-Tsvg")
            os.chdir(os.path.dirname(out["outfullfn"]))
        args.extend([infname, '-o', outfname])
    elif args[0] == "dot":
        # dot -Tpng in_file -o out_file
        args.extend([infullfn, '-o', out["outfullfn"]])
    #Will use :image: options to find the output image.
    #elif "python" in args[0]:
    #    pylib = "pyplot"
    #    lines = StringIO(text).readlines()
    #    for l in lines:
    #        if (not l.lstrip().startswith('#')) and \
    #                ("import matplotlib.pyplot" in l):
    #            # Find out pyplot module name, use pyplot if not found.
    #            result = re.search("(?<=import matplotlib.pyplot as )\w+",
    #                    l, flags=0)
    #            pylib = result and result.group() or "pyplot"
    #        elif ('.show()' in l or 'savefig(' in l):
    #            lines.remove(l)
    #    lines.append('%s.savefig("%s")\n' %(pylib, out["outfullfn"]))
    #    text = ''.join(lines)
    #    args.append(infullfn)
    elif args[0] == "gnuplot" and (not options.get("image", None)):
        #print("debug, args: %s" %(args))
        #print("debug, image: %s" %(options.get("image", None)))
        size = options.get("size", "900,600")
        if (plot_format in ["pdf", "eps"]):
            # pdf unit is inch while png is pixel, convert them.
            size = ",".join("%d" %(int(i.strip())/100) for i in size.split(","))
        lines = StringIO(text).readlines()
        # Remove the lines with set output/set terminal
        lines = [l for l in lines if (not re.search("^[^#]*set\s+output",
            l, flags=0)) and (not re.search("^[^#]*set\s+term", l, flags=0))]
        lines.insert(0, 'set output "%s"\n' %(out["outfullfn"]))
        terminal = (plot_format == "png") and "pngcairo" or plot_format
        lines.insert(0, 'set terminal %s size %s\n' %(terminal, size))
        text = ''.join(lines)
        args.append(infullfn)
    elif args[0] in ["imagemagick", "convert", "magick", "montage"]:
        #magick is the same as convert
        tmp = []
        #print("debug, args: %s" %(args))
        if text:
            args = ["sh", infullfn]
        else:
            #Only have command and not body: call args directly.
            args[-1] = out["outfullfn"]
            text = " ".join(args)
            #args = ["sh", infullfn]
    #else:
    #    print("args1: %s" %(args))
    #    args.append(infullfn)
    #    print("args2: %s" %(args))

    #Use :script: if it's given
    if options.get("script", None):
        if path.isfile(options["script"]):
            print("cp %s %s" %(options["script"], infullfn))
            os.system("cp %s %s" %(options["script"], infullfn))
        else:
            #:script: is given but not readable
            print("[31mWARNING: :script: %s is given but not readable!!![0m"
                    %(options["script"]))
            #out["outrelfn"] = None
            #out["outfullfn"] = None
            return out
    else:
        # write the text as infile.
        if app.builder.config.plot_log_level > 0:
            print("writing %s" %(infullfn))
        with open(infullfn, 'wb') as f:
            f.write(text.encode('utf-8'))

    if app.builder.config.plot_log_level > 1:
        print("%s(), args: %s" %(sys._getframe().f_code.co_name, args))
    # 2) generate the output file
    try:
        print(' '.join(args))
        p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout, stderr = (p.stdout.read(), p.stderr.read())
        if stdout:
            print("[1;30m%s[0m" %(stdout.decode(errors='ignore')))
        if stderr:
            print("[31m%s[0m" %(stderr.decode(errors='ignore')))
            #if not path.isfile(out["outfullfn"]):
            #    out["outrelfn"] = None
            #    out["outfullfn"] = None
            #    return out
    except OSError as err:
        os.chdir(currpath)
        print("[31mError in call: %s.[0m" %(args))
        raise PlotError('[1;31m%s[0m' %(err))

    if options.get("image", None):
        # 用户明确指出了输出文件，用用户指定的输出文件
        print("mv %s %s" %(options["image"], out["outfullfn"]))
        os.system("mv %s %s" %(options["image"], out["outfullfn"]))
    elif cmd in ["imagemagick", "convert", "magick", "montage"]:
        #Get the last word as the original output name
        #print("text: %s" %(text))
        for i in reversed(StringIO(text).readlines()):
            if i and (not (i.lstrip().startswith('#'))):
                conver_outfile = i.split()[-1]
                break
        if (app.builder.format == "latex") and \
                (conver_outfile.split(".")[-1] == "gif"):
            if options.get("latex_show_max_png", 8):
                i = Image.open(conver_outfile)
                #n = list(ImageSequence.Iterator(i)).size()
                max_num = (i.n_frames > 16) and 16 or i.n_frames
                #print("i: %d, max_num: %d"  %(i.n_frames, max_num))
                print("montage %s[0-%d] -coalesce -tile %dx %s" 
                        %(conver_outfile, max_num - 1,
                            options.get("latex_show_max_png", 8), out["outfullfn"]))
                os.system("montage %s[0-%d] -coalesce -tile %dx %s" 
                        %(conver_outfile, max_num - 1,
                            options.get("latex_show_max_png", 8), out["outfullfn"]))
                if max_num < i.n_frames:
                    #在图片最后写个"..."提示有截短
                    os.system("convert %s -gravity southeast -annotate +0+0 '...' %s"
                            %(out["outfullfn"], out["outfullfn"]))

                #print("options: %s" %(options))
                #如果.gif 指定了width, 需要为它加倍以免最终的图片太小看不清
                if options.get("width", None) and ("%" in options["width"]):
                    options.pop("width")
                elif options.get("width", None):
                    #print("options: %s" %(options))
                    options["width"] = int(options["width"]) * \
                            options.get("latex_show_max_png", 8)
                    #print("options: %s" %(options))

                os.system("rm %s" %(conver_outfile))
            else:
                print("convert %s[0] %s" 
                        %(conver_outfile, out["outfullfn"]))
                os.system("convert %s[0] %s" 
                        %(conver_outfile, out["outfullfn"]))
                os.system("rm %s" %(conver_outfile))
        else:
            print("mv %s %s" %(conver_outfile, out["outfullfn"]))
            os.system("mv %s %s" %(conver_outfile, out["outfullfn"]))
    elif (args[0] in ["ditaa", "dot", "seqdiag", "blockdiag", "actdiag", \
        "nwdiag"]) and (plot_format in ['pdf']):
        # In fact ditaa don't support pdf, we convert the .svg to .pdf inkscape
        if (args[0] == "dot"):
            print("mv %s %s-%s.svg" %(out["outfullfn"], args[0], hashkey))
            os.system("mv %s %s-%s.svg" %(out["outfullfn"], args[0], hashkey))
        else:
            print("mv %s %s-%s.svg" %(outfname, args[0], hashkey))
            os.system("mv %s %s-%s.svg" %(outfname, args[0], hashkey))

        inkscape = os.system("which inkscape 2> /dev/null")
        if inkscape != 0:
            print('[1;31minkscape does not exist, isntall it at first[0m')
        inkscape = os.popen("inkscape --version | awk  '{print $2}'") 
        #print(int(inkscape.read().split(".")[0]))
        if (int(inkscape.read().split(".")[0], 10) >= 1):
            print("inkscape %s-%s.svg --export-type pdf -o %s"
                    %(args[0], hashkey, out["outfullfn"]))
            os.system("inkscape %s-%s.svg --export-type pdf -o %s"
                    %(args[0], hashkey, out["outfullfn"]))
        else:
            print("inkscape -f %s-%s.svg -A %s"
                    %(args[0], hashkey, out["outfullfn"]))
            os.system("inkscape -f %s-%s.svg -A %s"
                    %(args[0], hashkey, out["outfullfn"]))
    else:
        print("mv %s %s" %(args[-1], out["outfullfn"]))
        os.system("mv %s %s" %(args[-1], out["outfullfn"]))

    os.chdir(currpath)

    if options.get("annotate", None):
        # We'd like to add annotate onto the output.
        c = "convert %s" %(out["outfullfn"])
        for i in StringIO(options["annotate"]).readlines():
            if (i.lstrip()[0] != "#"):
                c += " -annotate  %s" %(i.strip().rstrip("\\"))
        c += " %s" %(out["outfullfn"])
        print(c)
        os.system(c)

    if options.get("show_source", False):
        out["outreference"] = posixpath.join(rel_imgpath, infname)

    if app.builder.config.plot_log_level > 1:
        print("%s(), out is" %(sys._getframe().f_code.co_name))
        for k,v in out.items() :
            print("    %s: %s" %(k, v))

    return out

def cmd_2_image (app, plot):
    """
    1) 解析plot的内容, 最重要的是解析生成文件的后缀名。
    2) 判断是不是已经做过。如果已经做过，直接返回结果，避免重复调用。
    3) 将解析的结果根据options加以处理
    Render plot code into a PNG output file.
    """
    if app.builder.config.plot_log_level > 0:
        print("%s() format: %s, docname: %s, imagedir: %s"
                %(sys._getframe().f_code.co_name,
                    app.builder.format,
                    app.builder.env.docname,
                    app.builder.imagedir))
    #if app.builder.config.plot_log_level > 2:
    #    print("%s(), plot is: %s." %(sys._getframe().f_code.co_name, plot))

    args = shlex.split(plot['cmd'])
    text = plot['text']
    options = plot['total_options']

    # Guess the suffix
    plot_format = None
    if options.get("image", None) and ("." in options["image"]):
        # If explicitly given options["image"], use its suffix.
        plot_format = os.path.splitext(options["image"])[-1][1:]
    elif ("imagemagick" in args) or ("convert" in args) or \
            ("magick" in args) or ("montage" in args):
        if app.builder.format in ["html"]:
            # We get the suffix of the last word not in the comments
            for i in reversed(StringIO(text).readlines()):
                if i and (not (i.lstrip().startswith('#'))):
                    plot_format = i.split(".")[-1]
                    break
        else:
            # for latex, it's alwyas png.
            plot_format = "png"
    elif "dot" in args:
        #dot
        found = False
        # Guess the plot_format if -TXXX is given
        for param in args:
            if "-T" in param:
                plot_format = param[2:]
                found = True
                break
        if (not found):
            # Set the plot_format to -TXXX
            plot_format = "png"
            args.append("-Tpng")
            plot['cmd'] = ' '.join(args)
        if (plot_format == "svg"):
            plot_format = (app.builder.format in ["latex"]) \
                    and "pdf" or plot_format
    elif options.get("annotate", None):
        # If options include annotate, only support png
        plot_format = "png"
    elif options.get("plot_format", None):
        #User definition is higher priority.
        plot_format = options["plot_format"]
    else:
        #default
        print("args: %d" %(len(args)))
        if len(args) > 2:
            #if the last word has suffi, ，Use the last word's suffix:
            last_name = args[-1].split(".")
            print("last_name: %s/%d" %(last_name, len(last_name)))
            if (len(last_name) > 1):
                plot_format = last_name[1]
        print("plot_format: %s" %(plot_format))
        if not plot_format:
            #Use generic suffix
            format_map = OUTPUT_DEFAULT_FORMATS.copy()
            print("format_map: %s" %(format_map))
            format_map.update(app.builder.config.plot_output_format)
            plot_format = format_map.get(app.builder.format, "png")

    if app.builder.config.plot_log_level > 0:
        print("%s(), plot_format: %s, output image: %s"
                %(sys._getframe().f_code.co_name,
                    plot_format, options.get("image", None)))
    options["plot_format"] = plot_format
    hashkey = str(plot['cmd']) + str(options) + str(text)
    hashkey = sha(hashkey.encode('utf-8')).hexdigest()
    outfname = '%s-%s.%s' %(args[0], hashkey, plot_format)
    rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    out = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
        outfullfn = path.join(app.builder.outdir,
            app.builder.imagedir, outfname),
        outreference = None)
    if app.builder.config.plot_log_level > 0:
        print("%s(), out: %s" %(sys._getframe().f_code.co_name, out))

    #Really plot it
    if not path.isfile(out["outfullfn"]):
        out = plot_image(app, plot)
    else:
        print("file has already existed: %s" %(outfname))

    if app.builder.config.plot_log_level > 1:
        print("%s(), out is" %(sys._getframe().f_code.co_name))
        for k,v in out.items() :
            print("    %s: %s" %(k, v))
    return out

class PlotError(SphinxError):
    category = 'plot error'

class PlotDirective(directives.images.Figure):
    """
    扫描文档时如果找到..plot:: 命令后建议一个空的figure对象，并且将.. plot::
    的内容保存在figure对象上。
    """
    has_content = True
    required_arguments = 0
    option_spec = directives.images.Figure.option_spec.copy()
    option_spec.update(OWN_OPTION_SPEC)

    def plot_param_parser(self, content, options):
        '''
        Given content and return the parsed dictionary:
        {"cmd": xxx, "text": xxx, "option": xxx, "total_options": xxx}
        '''
        tmp = ""
        for line in content:
            #Find the fist verb not starting with '#'
            if (line and (not line.lstrip().startswith('#'))):
                tmp = line.split()[0]
                if not options.get("caption", None):
                    #If no :caption: is given, take the 1st line as caption.
                    tmp_line = line.rstrip()
                    if tmp_line[-1] == "\\":
                        options["caption"] = tmp_line[:-1] + "..."
                    else:
                        options["caption"] = tmp_line
                break
        if (tmp in ["imagemagick", "convert", "magick", "montage"]):
            #in case convert and montage: we put the cmd into the text itself
            cmd = tmp
            if len(content[0].split()) > 1:
                #所有的命令在命令行上
                text = '\n'.join(content)
            else:
                #命令行为convert, 所有的命令在内容里
                text = '\n'.join(content[1:])
        else:
            cmd = content[0]
            #There is a empty line between command and inlne script, remove it.
            text = '\n'.join(content[2:])

        total_options = options.copy()
        own_options = dict([(k,v) for k,v in total_options.items() 
                                  if k in OWN_OPTION_SPEC])

        dic = dict(cmd=cmd,text=text,options=own_options,
                directive="plot", total_options=total_options)
        return dic
  
    def run(self):
        '''
        将.. plot:: 的内容和参数保存到figure对象的.plot成员里以备后用。
        '''
        self.arguments = ['']
        params = self.plot_param_parser(self.content, self.options)
        #print("PlotDirective.run(), content: %s" %(self.content))
        #print("PlotDirective.run(), options: %s" %(self.options))
        #for k,v in params.items() :
        #    print("PlotDirective.run(), %s: %s" %(k, v))

        # Remove the own options from self-options which will be as figure
        # options.
        for x in params["options"].keys():
            self.options.pop(x)
        # don't parse the centent as legend, it's not legend.
        self.content = None

        #Create a empty image or figure object from self.
        if ("alt" in params["total_options"].keys()):
            #If there is alt parameters then it's inline image
            (node,) = directives.images.Image.run(self)
        else:
            #Figure
            (node,) = directives.images.Figure.run(self)
        if isinstance(node, nodes.system_message):
            return [node]

        #node.plot = dict(cmd=cmd,text=text,options=own_options,
        #        directive="plot", total_options=total_options)
        node.plot = dict(**params)
        #print("PlotDirective.run(), note: %s" %(node))
        return [node]

# http://epydoc.sourceforge.net/docutils/
def doctree_read_callback(app, doctree):
    uris = dict();

    #第一次遍历，生成inline image
    for img in doctree.traverse(nodes.image):
        #For candidate
        if not hasattr(img, 'plot'):
            if app.builder.config.plot_log_level > 1:
                print("%s(), img: %s" %(sys._getframe().f_code.co_name, img))
            continue

        print("----------------------------------------------------------------")
        if app.builder.config.plot_log_level > 0:
            print("%s(), img plot cmd: %s, alt: %s"
                    %(sys._getframe().f_code.co_name,
                        (hasattr(img, 'plot')) and img.plot['cmd'] or None,
                        img.get('alt', None)))
        text = img.plot['text']
        options = img.plot['options']
        cmd = img.plot['cmd']
        try:
            #relfn, outfn, relinfile = cmd_2_image(app, img.plot)
            out = cmd_2_image(app, img.plot)
            if options.get("hidden", False) or (not out["outfullfn"]):
                #Don't render the image if there is hidden
                nodes.image.pop(img)
                continue
            img['uri'] = out["outrelfn"]
            if img.get('alt', None):
                #For inline image:
                #    用于类似这样的调用:.. |test1| plot:: convert
                #    palms.jpg -grayscale rec601luma out.jpg
                uris[img['alt']] = img['uri']
                if app.builder.config.plot_log_level > 0:
                    print("uris: %s" %(uris))
            if os.path.splitext(out["outfullfn"])[-1] in [".png",".jpg",".gif"] \
                    and path.isfile(out["outfullfn"]):
                #对于png, jpg, gif 文件，手动获取它的大小
                print("get size of: %s" %(out["outfullfn"]))
                i = Image.open(out["outfullfn"])
                if img.get("scale", None):
                    img["width"] = "%d" %(i.width * img["scale"] / 100)
                    #print("width: %s" %(img["width"]))
                elif (not img.get("width", None)) and \
                        (not img.get("width", None)):
                    #Mainly for latex, give width if there is not.
                    img["width"] = "%d" %(i.width)
                if app.builder.config.plot_log_level > 1:
                    print("Guess the width: %s." %(img["width"]))
            #img['candidates']={'*': out["outrelfn"]}
            if out["outreference"]:
                reference_node = nodes.reference(refuri=out["outreference"])
                img.replace_self(reference_node)
                reference_node.append(img) 
            #if options.get("show_source", False):
            #    img.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text)))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            img.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue
        if app.builder.config.plot_log_level > 0:
            print("%s(), img: %s" %(sys._getframe().f_code.co_name, img))

    #第二次遍历，解析inline image
    for img in doctree.traverse(nodes.image):
        if (not hasattr(img, 'plot')) and img.get('alt', None) and \
                (img['alt'] in uris.keys()):
            #inline image
            img['uri'] = uris[img['alt']]
            #img['candidates'] = {'*': uris[img['alt']]}
            print("------------------------------------------------------------")
            print("inline uri = %s" %(img['uri']))
            if app.builder.config.plot_log_level > 0:
                print("%s(), img plot cmd: %s, alt: %s"
                        %(sys._getframe().f_code.co_name,
                            (hasattr(img, 'plot')) and img.plot['cmd'] or None,
                            img.get('alt', None)))

    for fig in doctree.traverse(nodes.figure):
        if not hasattr(fig, 'plot'):
            if app.builder.config.plot_log_level > 1:
                print("%s(), img: %s" %(sys._getframe().f_code.co_name, img))
            continue

        print("================================================================")
        if app.builder.config.plot_log_level > 0:
            print("%s(), figure plot: %s"
                    %(sys._getframe().f_code.co_name,
                        (hasattr(img, 'plot')) and img.plot['cmd'] or None))
        cmd = fig.plot['cmd']
        text = fig.plot['text']
        options = fig.plot['options']

        try:
            #调用cmd_2_image生成图像, 再把图像的地址链接到figure的uri里, 这样
            #就是显示在文档里了
            out = cmd_2_image(app, fig.plot)
            if app.builder.config.plot_log_level > 0:
                print("%s(), out is %s" %(sys._getframe().f_code.co_name, out))

            if options.get("hidden", False) or (not out["outfullfn"]):
                #Don't render the image if there is hidden
                nodes.figure.pop(fig)
                continue

            #Caption
            caption_node = nodes.caption("", options.get("caption", cmd))
            fig += caption_node
            fig['ids'] = ["plot"]

            #uri
            for img in fig.traverse(condition=nodes.image):
                img['uri'] = out["outrelfn"]
                if out["outreference"]:
                    reference_node = nodes.reference(refuri=out["outreference"])
                    reference_node += img
                    fig.replace(img, reference_node)
                if os.path.splitext(out["outfullfn"])[-1] in \
                        [".png", ".jpg", ".gif"] \
                        and path.isfile(out["outfullfn"]):
                    #对于png, jpg, gif 文件，手动获取它的大小
                    i = Image.open(out["outfullfn"])
                    if img.get("scale", None):
                        img["width"] = "%d" %(i.width * img["scale"] / 100)
                        #print("width: %s" %(img["width"]))
                    elif (not img.get("width", None)) and \
                            (not img.get("width", None)):
                        #Mainly for latex, give width if there is not.
                        img["width"] = "%d" %(i.width)
                    if app.builder.config.plot_log_level > 1:
                        print("Guess the width: %s." %(img["width"]))

            #if options.get("show_source", False):
            #    # rendere as a text
            #    fig["align"] = "left"
            #    fig.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text),
            #               align = "left"))
            #print("rending figure: %s" %(fig))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            fig.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue
        if app.builder.config.plot_log_level > 0:
            print("%s(), fig: %s" %(sys._getframe().f_code.co_name, fig))

def setup(app):
    #注册2个回调函数
    app.add_directive('plot', PlotDirective)
    app.connect('doctree-read', doctree_read_callback)

    app.add_config_value('plot', 'plot', 'html')
    app.add_config_value('plot_args', [], 'html')
    #plot_log_level, 0: don't print debug info; 1: only print in parameters
    #and out result. 2: debug info
    app.add_config_value('plot_log_level', 0, 'html')
    app.add_config_value('plot_output_format', OUTPUT_DEFAULT_FORMATS, 'html')

#References
###########

#. reStructuredText and Sphinx Reference, https://documatt.com/restructuredtext-reference/element/figure.html
