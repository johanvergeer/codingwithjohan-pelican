"""
Card extension for Python-Markdown
========================================
Adds material style cards. Base on [Material Kit][] By Creative Tim.
[Material Kit]: https://www.creative-tim.com/product/material-kit
Original code Copyright [Creative Tim](https://www.creative-tim.com/).
All changes Copyright RedGyro
License: [MIT](https://opensource.org/licenses/MIT)
"""
import re
from dataclasses import dataclass
from typing import AnyStr, Optional, Pattern
from xml.etree.ElementTree import Element

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class CardExtension(Extension):
    """ Card extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Card to Markdown instance. """
        md.registerExtension(self)

        md.parser.blockprocessors.register(CardProcessor(md.parser), "card", 105)


@dataclass(frozen=True)
class CardType:
    icon: Optional[str]
    color: Optional[str]


class CardProcessor(BlockProcessor):
    CLASSNAME = "mk-card"
    RE = re.compile(r"(?:^|\n)!!! " r"([a-z]+)" r"( *\[[a-z-]+=(.*)])*" r"(?:\n|$)")

    card_types = {
        "card": CardType(icon=None, color=None),
        "info": (CardType(icon="info", color="info")),
        "warning": CardType(icon="warning", color="warning"),
        "tip": CardType(icon="emoji_objects", color="success"),
        "important": CardType(icon="notification_important", color="danger"),
    }

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE.search(block) or (
            block.startswith(" " * self.tab_length)
            and sibling is not None
            and sibling.get("class", "").find(self.CLASSNAME) != -1
        )

    def run(self, parent: Element, blocks):
        sibling = self.lastChild(parent)
        block: str = blocks.pop(0)

        m = self.RE.search(block)

        title = self._get_title(block)
        width_class = self._get_width_class(block)
        icon = self._get_icon(block)
        subtitle = self._get_subtitle(block)
        color = self._get_color(block)
        card_type: Optional[CardType] = None

        if m:
            card_type = self._get_card_type(block)
            block = block[m.end() :]  # removes the first line

        block, the_rest = self.detab(block)

        if m:
            row = etree.SubElement(parent, "div")
            row.set("class", f"row {self.CLASSNAME}")

            col = etree.SubElement(row, "div")
            col.set("class", width_class)

            card = etree.SubElement(col, "div")
            card.set("class", f"card")

            card_header: Optional[Element] = None
            if title or icon or card_type.icon:
                card_header = etree.SubElement(card, "div")
                card_header.set("class", "card-header")

            card_body = etree.SubElement(card, "div")
            card_body.set("class", "card-body")

            if card_header is not None:
                if color:
                    card_header.attrib["class"] += f" card-header-{color}"
                elif card_type.color:
                    card_header.attrib["class"] += f" card-header-{card_type.color}"

                if icon or card_type.icon:
                    icon = icon if icon is not None else card_type.icon
                    card_header.attrib["class"] += " card-header-icon"

                    card_icon = etree.SubElement(card_header, "div")
                    card_icon.set("class", "card-icon")

                    card_icon_i = etree.SubElement(card_icon, "i")
                    card_icon_i.set("class", "material-icons")
                    card_icon_i.text = icon

                    if title:
                        card_title = etree.SubElement(card_body, "h4")
                        card_title.set("class", "card-title")
                        card_title.text = title

                    if subtitle:
                        print("Subtitle is not supported in conjunction with an icon.")

                else:
                    card_title = etree.SubElement(card_header, "h4")
                    card_title.set("class", "card-title")
                    card_title.text = title

                    if subtitle:
                        card_subtitle = etree.SubElement(card_header, "p")
                        card_subtitle.set("class", "category")
                        card_subtitle.text = subtitle
        else:
            card_body = sibling.find(".//div[@class = 'card-body']")

        self.parser.parseChunk(card_body, block)

        if the_rest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, the_rest)

    def _get_card_type(self, block: str) -> CardType:
        card_type = self.RE.match(block).group(1)
        if card_type is not None:
            return self.card_types.get(card_type)
        valid_card_types = ", ".join(self.card_types.keys())
        raise ValueError(
            f"{card_type} is not a valid card type. use one of {valid_card_types}"
        )

    def _get_title(self, block: str) -> Optional[str]:
        return self._get_attribute(block, "title")

    def _get_color(self, block: str) -> Optional[str]:
        return self._get_attribute(block, "color")

    def _get_icon(self, block: str) -> Optional[str]:
        return self._get_attribute(block, "icon")

    def _get_width_class(self, block: str):
        width_class = self._get_attribute(block, "width-class")
        if width_class:
            return width_class
        return "col-md-12"

    def _get_subtitle(self, block: str) -> Optional[str]:
        return self._get_attribute(block, "subtitle")

    def _get_attribute(self, block: str, attribute: str) -> Optional[str]:
        pattern = self._get_attribute_pattern(attribute)
        value = pattern.search(block)

        if value:
            return value.group(1)

    @staticmethod
    def _get_attribute_pattern(attribute: str) -> Pattern[AnyStr]:
        return re.compile(rf"\[{attribute}=(.*?)]")


def makeExtension(**kwargs):  # pragma: no cover
    return CardExtension(**kwargs)
