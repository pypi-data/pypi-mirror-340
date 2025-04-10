import tempfile
from dataclasses import dataclass
from pathlib import Path

import finesse

# import xml.etree.ElementTree as ET
import lxml.etree

PREFIX = "finesse_hitbox_"


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float


hitbox_mapping: dict[str, Rect] = {}


def parse_layout(layout_dir: Path) -> tuple[finesse.Model, dict[str, Rect], str]:
    assert layout_dir.exists()
    kat_file = layout_dir / "layout.kat"
    assert kat_file.exists()
    svg_file = layout_dir / "layout.svg"
    assert svg_file.exists()

    model: finesse.Model = finesse.script.parse_file(kat_file)
    tree = lxml.etree.parse(svg_file, lxml.etree.XMLParser())
    root = tree.getroot()

    # I don't know if this viewbox thing is always added by inkscape or something more general
    svg_width = float(root.attrib["width"])
    svg_height = float(root.attrib["height"])
    viewbox = [float(val) for val in root.attrib["viewBox"].split()]
    viewbox_width = viewbox[2] - viewbox[0]
    viewbox_height = viewbox[3] - viewbox[1]
    x_scaling = svg_width / viewbox_width
    y_scaling = svg_height / viewbox_height

    # we just look for anything with the 'finesse_hitbox_<component_name> value
    # and look for x,y,width,height?
    for el in root.iter():
        hitbox = None
        for key, val in el.attrib.items():
            if val.startswith(PREFIX):
                hitbox = val
        if not hitbox:
            continue

        for attr in ("x", "y", "width", "height"):
            assert attr in el.attrib

        hitbox_mapping[hitbox.split(PREFIX)[-1]] = Rect(
            x=float(el.attrib["x"]) * x_scaling,
            y=float(el.attrib["y"]) * y_scaling,
            width=float(el.attrib["width"]) * x_scaling,
            height=float(el.attrib["height"]) * y_scaling,
        )
        parent = el.getparent()
        parent.remove(el)

    # Users should define components and named spaces/wires?
    # TODO will probably break at stuff like gauss and dofs
    elements_to_match = []
    for name, element in model.elements.items():
        # all models have an fsig element, but should not be present in the svg
        if name == "fsig":
            continue
        elif element in model.detectors:
            continue
        elements_to_match.append(name)
    elements_to_match = set(elements_to_match)
    diff = elements_to_match.symmetric_difference(set(hitbox_mapping.keys()))
    if len(diff):
        raise ValueError(f"Hitbox mapping and model elements dont match: {diff}")

    # TODO maybe check size?

    # I can not get the qt svg graphics item to read this from memory directly
    path = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
    with open(path, "w") as f:
        f.write(lxml.etree.tounicode(tree))
    return model, hitbox_mapping, path
