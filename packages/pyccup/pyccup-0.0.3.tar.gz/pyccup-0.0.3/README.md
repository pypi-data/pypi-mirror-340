# pyccup

[![Upload Python Package](https://github.com/inaimathi/pyccup/actions/workflows/python-publish.yml/badge.svg)](https://github.com/inaimathi/pyccup/actions/workflows/python-publish.yml)

Python version of clojure hiccup https://github.com/weavejester/hiccup
Original concept by James Reeves

Pyccup is derived from [nbessi](https://github.com/nbessi)'s [Pyhiccup](https://github.com/nbessi/pyhiccup) library, and makes only incremental in python compatibility.

Pyccup is a library for representing HTML in Python. It uses list or tuple
to represent elements, and dict to represent an element's attributes. Supports Python versions 3.4 and later.

## Install

```
pip install pyccup
```

## Syntax

Here is a basic example of pyccup syntax.

```python
>>> from pyccup.core import html
>>> data = [
>>>    ['div',
>>>     {'class': 'a-class', 'data-y': '23'},
>>>     ['span', 'my-text',
>>>      ['ul', [['li', x] for x in ['café', 'milk', 'sugar']]]]]
>>> ]
>>> html(data)
u'<!DOCTYPE html><html lang="en" xml:lang="en" dir="rtl"><div data-y="23" class="a-class"><span>my-text<ul><li>café<li>milk<li>sugar</ul></span></div></html>'
```

The `html` function supports different default type `html5, html4, xhtml-strict, xhtml-transitional`

```python
>>> from pyccup.core import html
>>> data = []
>>> html(data, etype='xhtml-strict')
>>> u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html lang="en" xml:lang="en" dir="rtl" xmlns="http://www.w3.org/1999/xhtml"/>'
```

You can pass arbitrary keyword arguments to the `html` they will be transformed into `html` tag attributes

```python
>>> from pyccup.core import html
>>> data = []
>>> html(data, etype='xhtml-strict', an-attr='foo')
u'... <html an-attr="foo" lang="en" xml:lang="en" dir="rtl" xmlns="http://www.w3.org/1999/xhtml"/>'
```

Pyccup also provides a function to represent XML. Arbitrary keyword arguments are also supported.

```python
>>> from pyccup.core import xml
>>> data = ['form-desc',
>>>         ['field', {'name': 'a_name'}],
>>>         ['field', {'name': 'a_other_name'}]]
>>> conv = xml(data, 'foo-ns', bar='an_attr')
u'<?xml version="1.0" encoding="UTF-8"?><foo-ns bar="an_attr"><form-desc><field name="a_name"/><field name="a_other_name"/></form-desc></foo-ns>'
```

Some time you want to be able to create XML/HTML chunk out of a namespace. The `core.convert` is made for this.

```python
>>> from pyccup.core import convert
>>> from pyccup.element import link_to
>>> convert(link_to('http://github.com/inaimathi/pyccup', 'pyccup'))
u'<a href="http://github.com/inaimathi/pyccup">pyccup</a>'
```

Helpers are available on the elements namespace. The will help you to add hyperlink, images etc.

```python
>>> from pyccup.element import link_to
>>> link_to(u'https://github.com/inaimathi/pyccup', u'pyccup' )
[u'a', {u'href': u'https://github.com/inaimathi/pyccup'}, u'pyccup']
```

## Using pyccup.elems

The `elems` module provides constants for HTML/XML tag names, allowing for a more elegant and IDE-friendly syntax when constructing HTML/XML trees.

### Basic Usage

```python
import pyccup.elems as e
from pyccup.core import html

# Create an HTML tree
html_tree = [
    e.html, 
    [e.head, 
     [e.title, "My Website"]],
    [e.body, 
     [e.div, {"class": "container"},
      [e.h1, "Welcome!"],
      [e.p, "This is a paragraph with ", [e.strong, "bold text"], "."]]]
]

# Convert to HTML string
html_string = html(html_tree)
print(html_string)
```

### Case Flexibility

The module supports both lowercase and uppercase tag names:

```python
# These are equivalent
[e.div, [e.p, "Content"]]
[e.DIV, [e.P, "Content"]]
```

### Available Tags

The module includes constants for all HTML5 tags, including:

- Document structure: `html`, `head`, `body`
- Headings: `h1` through `h6`
- Text containers: `p`, `div`, `span`, etc.
- Lists: `ul`, `ol`, `li`
- Forms: `form`, `input`, `button`, etc.
- Tables: `table`, `tr`, `td`, etc.
- And many more...

### Special Cases

The `del` tag is available as `del_` (with an underscore) to avoid conflict with Python's `del` keyword.

### Integration with pyccup

This module is designed to work seamlessly with the rest of the pyccup library:

```python
from pyccup.core import html, convert
import pyccup.elems as e

# For full HTML documents
document = html([
    e.div, {"id": "content"},
    [e.h1, "Title"],
    [e.p, "Paragraph"]
])

# For HTML fragments
fragment = convert([
    e.div, {"id": "content"},
    [e.h1, "Title"],
    [e.p, "Paragraph"]
])
```
