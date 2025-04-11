# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Inaimathi
#    Copyright 2025
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License 3
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""
Element constants for pyccup.

This module provides constants for HTML/XML tag names, allowing for a cleaner
syntax when constructing HTML/XML trees.

Usage example:

    import pyccup.elems as e
    from pyccup.core import html

    html_tree = [e.html,
                 [e.head,
                  [e.title, "My Page"]],
                 [e.body,
                  [e.div, {"class": "container"},
                   [e.h1, "Hello, World!"],
                   [e.p, "This is a paragraph."]]]]

    html_string = html(html_tree)
"""

# HTML5 tag names with chain assignments (lowercase and uppercase variants together)

# Basic structure
HTML = html = "html"
HEAD = head = "head"
BODY = body = "body"

# Metadata
BASE = base = "base"
LINK = link = "link"
META = meta = "meta"
STYLE = style = "style"
TITLE = title = "title"

# Content sectioning
ADDRESS = address = "address"
ARTICLE = article = "article"
ASIDE = aside = "aside"
FOOTER = footer = "footer"
HEADER = header = "header"
H1 = h1 = "h1"
H2 = h2 = "h2"
H3 = h3 = "h3"
H4 = h4 = "h4"
H5 = h5 = "h5"
H6 = h6 = "h6"
HGROUP = hgroup = "hgroup"
MAIN = main = "main"
NAV = nav = "nav"
SECTION = section = "section"

# Text content
BLOCKQUOTE = blockquote = "blockquote"
DD = dd = "dd"
DIV = div = "div"
DL = dl = "dl"
DT = dt = "dt"
FIGCAPTION = figcaption = "figcaption"
FIGURE = figure = "figure"
HR = hr = "hr"
LI = li = "li"
OL = ol = "ol"
P = p = "p"
PRE = pre = "pre"
UL = ul = "ul"

# Inline text semantics
A = a = "a"
ABBR = abbr = "abbr"
B = b = "b"
BDI = bdi = "bdi"
BDO = bdo = "bdo"
BR = br = "br"
CITE = cite = "cite"
CODE = code = "code"
DATA = data = "data"
DFN = dfn = "dfn"
EM = em = "em"
I = i = "i"
KBD = kbd = "kbd"
MARK = mark = "mark"
Q = q = "q"
RP = rp = "rp"
RT = rt = "rt"
RUBY = ruby = "ruby"
S = s = "s"
SAMP = samp = "samp"
SMALL = small = "small"
SPAN = span = "span"
STRONG = strong = "strong"
SUB = sub = "sub"
SUP = sup = "sup"
TIME = time = "time"
U = u = "u"
VAR = var = "var"
WBR = wbr = "wbr"

# Image and multimedia
AREA = area = "area"
AUDIO = audio = "audio"
IMG = img = "img"
MAP = map = "map"
TRACK = track = "track"
VIDEO = video = "video"

# Embedded content
EMBED = embed = "embed"
IFRAME = iframe = "iframe"
OBJECT = object = "object"
PARAM = param = "param"
PICTURE = picture = "picture"
SOURCE = source = "source"

# Scripting
CANVAS = canvas = "canvas"
NOSCRIPT = noscript = "noscript"
SCRIPT = script = "script"

# Demarcating edits
DEL = del_ = "del"  # Using del_ to avoid conflict with Python's del keyword
INS = ins = "ins"

# Table content
CAPTION = caption = "caption"
COL = col = "col"
COLGROUP = colgroup = "colgroup"
TABLE = table = "table"
TBODY = tbody = "tbody"
TD = td = "td"
TFOOT = tfoot = "tfoot"
TH = th = "th"
THEAD = thead = "thead"
TR = tr = "tr"

# Forms
BUTTON = button = "button"
DATALIST = datalist = "datalist"
FIELDSET = fieldset = "fieldset"
FORM = form = "form"
INPUT = input = "input"
LABEL = label = "label"
LEGEND = legend = "legend"
METER = meter = "meter"
OPTGROUP = optgroup = "optgroup"
OPTION = option = "option"
OUTPUT = output = "output"
PROGRESS = progress = "progress"
SELECT = select = "select"
TEXTAREA = textarea = "textarea"

# Interactive elements
DETAILS = details = "details"
DIALOG = dialog = "dialog"
MENU = menu = "menu"
SUMMARY = summary = "summary"

# Web Components
SLOT = slot = "slot"
TEMPLATE = template = "template"
