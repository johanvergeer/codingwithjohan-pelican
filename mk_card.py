"""
Admonition extension for Python-Markdown
========================================
Adds rST-style admonitions. Inspired by [rST][] feature with the same name.
[rST]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions  # noqa
See <https://Python-Markdown.github.io/extensions/admonition>
for documentation.
Original code Copyright [Tiago Serafim](https://www.tiagoserafim.com/).
All changes Copyright The Python Markdown Project
License: [BSD](https://opensource.org/licenses/bsd-license.php)
"""
from xml.etree.ElementTree import Element

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class AdmonitionExtension(Extension):
    """ Admonition extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.register(AdmonitionProcessor(md.parser), 'admonition', 105)


class AdmonitionProcessor(BlockProcessor):

    CLASSNAME = 'mk-card'
    RE = re.compile(r'(?:^|\n)!!! ?([\w\-]+(?: +[\w\-]+)*)(?: +\[title=(.*?)\])? *(?:\n|$)')
    RE_SPACES = re.compile('  +')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE.search(block) or \
            (block.startswith(' ' * self.tab_length) and sibling is not None and
             sibling.get('class', '').find(self.CLASSNAME) != -1)

    def run(self, parent: Element, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            block = block[m.end():]  # removes the first line

        block, the_rest = self.detab(block)

        if m:
            klass, title = self.get_class_and_title(m)

            row = etree.SubElement(parent, 'div')
            row.set('class', f'row {self.CLASSNAME}')

            col = etree.SubElement(row, 'div')
            col.set('class', 'col-md-12')

            card = etree.SubElement(col, 'div')
            card.set('class', f'card {klass}')
            if title:
                card_header = etree.SubElement(card, 'div')
                card_header.set('class', 'card-header')

                card_title = etree.SubElement(card_header, 'h4')
                card_title.set('class', 'card-title')
                card_title.text = title

            card_body = etree.SubElement(card, 'div')
            card_body.set('class', 'card-body')
        else:
            card_body = sibling.find(".//div[@class = 'card-body']")

        self.parser.parseChunk(card_body, block)

        if the_rest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, the_rest)

    def get_class_and_title(self, match):
        klass, title = match.group(1).lower(), match.group(2)
        klass = self.RE_SPACES.sub(' ', klass)
        if title is None:
            # no title was provided, use the capitalized classname as title
            # e.g.: `!!! note` will render
            # `<p class="admonition-title">Note</p>`
            title = klass.split(' ', 1)[0].capitalize()
        elif title == '':
            # an explicit blank title should not be rendered
            # e.g.: `!!! warning ""` will *not* render `p` with a title
            title = None
        return klass, title


def makeExtension(**kwargs):  # pragma: no cover
    return AdmonitionExtension(**kwargs)
