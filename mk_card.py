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
from typing import Optional, AnyStr, Pattern
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
    RE = re.compile(r'(?:^|\n)!!! card( *\[[a-z-]+=(.*)])*(?:\n|$)')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE.search(block) or \
               (block.startswith(' ' * self.tab_length) and sibling is not None and
                sibling.get('class', '').find(self.CLASSNAME) != -1)

    def run(self, parent: Element, blocks):
        sibling = self.lastChild(parent)
        block: str = blocks.pop(0)

        m = self.RE.search(block)

        title = self._get_title(block)
        width_class = self._get_width_class(block)
        icon = self._get_icon(block)
        subtitle = self._get_subtitle(block)
        color = self._get_color(block)

        if m:
            block = block[m.end():]  # removes the first line

        block, the_rest = self.detab(block)

        if m:
            row = etree.SubElement(parent, 'div')
            row.set('class', f'row {self.CLASSNAME}')

            col = etree.SubElement(row, 'div')
            col.set('class', width_class)

            card = etree.SubElement(col, 'div')
            card.set('class', f'card')

            card_header: Optional[Element] = None
            if title or icon:
                card_header = etree.SubElement(card, 'div')
                card_header.set('class', 'card-header')

            card_body = etree.SubElement(card, 'div')
            card_body.set('class', 'card-body')

            if card_header:
                if color:
                    card_header.attrib['class'] += f' card-header-{color}'

                if icon:
                    card_header.attrib['class'] += ' card-header-icon'

                    card_icon = etree.SubElement(card_header, 'div')
                    card_icon.set('class', 'card-icon')

                    card_icon_i = etree.SubElement(card_icon, 'i')
                    card_icon_i.set('class', 'material-icons')
                    card_icon_i.text = icon

                    if title:
                        card_title = etree.SubElement(card_body, 'h4')
                        card_title.set('class', 'card-title')
                        card_title.text = title

                    if subtitle:
                        print('Subtitle is not supported in conjunction with an icon.')

                else:
                    card_title = etree.SubElement(card_header, 'h4')
                    card_title.set('class', 'card-title')
                    card_title.text = title

                    if subtitle:
                        card_subtitle = etree.SubElement(card_header, 'p')
                        card_subtitle.set('class', 'category')
                        card_subtitle.text = subtitle
        else:
            card_body = sibling.find(".//div[@class = 'card-body']")

        self.parser.parseChunk(card_body, block)

        if the_rest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, the_rest)

    def _get_title(self, block: str) -> Optional[str]:
        return self._get_attribute(block, 'title')

    def _get_color(self, block: str) -> Optional[str]:
        return self._get_attribute(block, 'color')

    def _get_icon(self, block: str) -> Optional[str]:
        return self._get_attribute(block, 'icon')

    def _get_width_class(self, block: str):
        width_class = self._get_attribute(block, 'width-class')
        if width_class:
            return width_class
        return 'col-md-12'

    def _get_subtitle(self, block: str) -> Optional[str]:
        return self._get_attribute(block, 'subtitle')

    def _get_attribute(self, block: str, attribute: str) -> Optional[str]:
        pattern = self._get_attribute_pattern(attribute)
        value = pattern.search(block)

        if value:
            return value.group(1)

    @staticmethod
    def _get_attribute_pattern(attribute: str) -> Pattern[AnyStr]:
        return re.compile(rf'\[{attribute}=(.*?)]')


def makeExtension(**kwargs):  # pragma: no cover
    return AdmonitionExtension(**kwargs)
