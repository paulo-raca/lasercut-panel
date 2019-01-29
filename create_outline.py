#!/usr/bin/env python3

import argparse
import re
import inspect

def parseDimensions(value):
    float_regex = r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)'  # https://stackoverflow.com/a/12643073/995480
    dimension_regex = f'^(?P<W>{float_regex})x(?P<H>{float_regex})$'
    match = re.match(dimension_regex, value)
    if not match:
        raise ValueError(f'Expected "{{Width}}x{{Height}}", got "{value}"')
    return float(match.group('W')), float(match.group('H'))

parser = argparse.ArgumentParser(
                    description='Generate SVG file with profile for a retangular frame with tabs on the top edge')
parser.add_argument('dimensions', metavar='WxH', type=parseDimensions,
                    help='Dimension of the main area, as "{Width}x{Height}"')
parser.add_argument('--units', metavar='UNIT', default='cm', choices=['cm', 'mm', 'in'],
                    help='Units used on dimensions')
parser.add_argument('--tabs', metavar='NUM_TABS', type=int, default=1,
                    help='Number of tabs added above top edge')
parser.add_argument('--hole-size', metavar='DIAMETER', type=float,
                    help='Size of the tab hole')
parser.add_argument('--hole-padding', metavar='PADDING_SIZE', type=float,
                    help='Size of the padding around the tab hole')
parser.add_argument('--from-border', action='store_true',
                    help='Align tabs with corners')


args = parser.parse_args()
W = args.dimensions[0]
H = args.dimensions[1]
units = args.units
num_tabs = args.tabs
from_border = args.from_border
hole_diameter = args.hole_size if args.hole_size is not None else W/100
hole_radius = hole_diameter / 2
hole_padding  = args.hole_padding if args.hole_padding is not None else W/100
tab_height = hole_diameter + hole_padding
tab_width = hole_diameter + 2 * hole_padding

svg_outer_path = [
    f'M {W} {tab_height}',
    f'L {W} {H + tab_height}',
    f'L {0} {H + tab_height}',
    f'L {0} {tab_height}',
]
svg_holes = []

extra_space = W - num_tabs * tab_width
if num_tabs < 1:
    raise ValueError(f'--num_tabs must be at least 1')
if from_border and num_tabs < 2:
    raise ValueError(f'When using --from_border, --num_tabs must be at least 2')
if extra_space < 0:
    raise ValueError(f'{num_tabs} tabs would take {num_tabs * tab_width}{units}, but the frame width is only {W}{units}')

for tab_i in range(num_tabs):
    if from_border and num_tabs > 1:
        rel_pos = tab_i / (num_tabs - 1)
    else:
        rel_pos = (tab_i + 0.5) / (num_tabs)
    hook_center = (tab_i + 0.5) * tab_width + rel_pos * extra_space
    hook_left = hook_center - tab_width/2.0
    hook_right = hook_center + tab_width/2.0

    hole_top = hole_padding
    hole_middle = hole_padding + hole_radius
    hole_bottom = hole_padding + hole_diameter

    corner_y_radius = hole_radius
    corner_x_radius = min(corner_y_radius, extra_space / (2 * (num_tabs - 1 if from_border else num_tabs)))
    corner_x_radius_left = 0 if from_border and tab_i == 0 else corner_x_radius
    corner_x_radius_right = 0 if from_border and tab_i == num_tabs - 1 else corner_x_radius

    svg_outer_path += [
        f'L {hook_left - corner_x_radius_left} {tab_height}',
        f'A {corner_x_radius_left} {corner_y_radius} 0 0 0 {hook_left} {hole_middle}' if corner_x_radius_left > 0 else f'L {hook_left} {hole_middle}',
        f'A {tab_width/2} {tab_width/2} 0 0 1 {hook_right} {hole_middle}',
        f'A {corner_x_radius_right} {corner_y_radius} 0 0 0 {hook_right+corner_x_radius_right} {tab_height}' if corner_x_radius_right > 0 else f'L {hook_right+corner_x_radius_right} {tab_height}',
    ]
    svg_holes += [
        f'M {hook_center} {hole_top}',
        f'A {hole_radius} {hole_radius} 0 1 0 {hook_center} {hole_bottom}',
        f'A {hole_radius} {hole_radius} 0 1 0 {hook_center} {hole_top}',
        f'Z',
    ]

svg_outer_path += [
    f'L {W} {tab_height}',
    f'Z',
]

newline = '\n'
SVG_TEMPLATE = \
f"""<?xml version="1.0"?>
<svg width="{W}{units}" height="{H + tab_height}{units}"
     viewBox="0 0 {W} {H + tab_height}"
     xmlns="http://www.w3.org/2000/svg">

  <path id="frame" d="{newline.join(svg_outer_path + svg_holes)}" fill="grey" />
</svg>
"""

print(SVG_TEMPLATE)
