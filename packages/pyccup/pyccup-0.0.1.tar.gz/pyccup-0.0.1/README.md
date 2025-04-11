# pyccup 0.1

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
