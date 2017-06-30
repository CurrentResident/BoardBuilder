#! /usr/bin/python

import argparse
import json
import math
import os
import sys

from solid import *
from solid.utils import *

class BoardBuilder:
    def __init__(self, kle_json, horizontal_pad, vertical_pad, corner_radius, num_holes, hole_diameter, show_points, stabs):

        f = open(kle_json)
        self.layout = json.load(f)
        f.close()

        self.min_x = 10000
        self.max_x = 0
        self.min_y = 10000
        self.max_y = 0

        self.show_points = show_points
        self.stabs       = stabs

        self.corner_radius = corner_radius

        self.num_holes = num_holes
        self.hole_diameter = hole_diameter

        #Determine the left and right padding
        self.horizontal_pad = horizontal_pad
        try:
            left_padding, right_padding = horizontal_pad.split(',')
            self.left_pad = int(left_padding)
            self.right_pad = int(right_padding)
        except:
            self.left_pad = self.right_pad = int(horizontal_pad)

        # Determine the left and right padding
        self.vertical_pad = vertical_pad
        try:
            top_padding, bottom_padding = vertical_pad.split(',')
            self.top_pad = int(top_padding)
            self.bottom_pad = int(bottom_padding)
        except:
            self.top_pad = self.bottom_pad = int(vertical_pad)

        # Build the bottom plate after the top one because the plate dimensions are calculated
        # while building the top plate.
        #
        # TODO: Break out the top plate construction, and add parameters so that the order
        #       of construction doesn't have any hidden dependencies and we don't have to
        #       explicitly apply corners and such more than once.
        self.base_top_plate    = self.build_base_top_plate()
        self.base_bottom_plate = self.build_base_bottom_plate()

        if (corner_radius > 0):
            self.base_top_plate    = self.apply_corners(self.base_top_plate)
            self.base_bottom_plate = self.apply_corners(self.base_bottom_plate)

        if (self.num_holes > 3 and self.hole_diameter > 0):
            self.base_top_plate    = self.apply_screw_holes(self.base_top_plate)
            self.base_bottom_plate = self.apply_screw_holes(self.base_bottom_plate)

        # Create any mid layers by subtracting the interior section out of the bottom plate.
        self.mid_layers = self.build_mid_layers(self.base_bottom_plate)

    def update_mins_maxes(self, points):
        for point in points:
            if self.min_x > point[0]:
                self.min_x = point[0]
            if self.max_x < point[0]:
                self.max_x = point[0]
            if self.min_y > point[1]:
                self.min_y = point[1]
            if self.max_y < point[1]:
                self.max_y = point[1]

    def apply_corners(self, plate):

        def build_corner():
            return difference()(
                    square(self.corner_radius*2, center=True),
                    translate( [ self.corner_radius, self.corner_radius, 0 ] )(
                        circle(r = self.corner_radius, segments = 80)
                    )
                )

        return difference()(
            plate,
            union()(
                build_corner(),
                translate( [ self.exterior_width, 0, 0 ] )(
                    mirror( [ 1, 0, 0 ] )(
                        build_corner()
                    )
                ),
                translate( [ self.exterior_width, self.exterior_height, 0 ] )(
                    mirror( [ 1, 1, 0 ] )(
                        build_corner()
                    )
                ),
                translate( [ 0, self.exterior_height, 0 ] )(
                    mirror( [ 0, 1, 0 ] )(
                        build_corner()
                    )
                )
            )
        )

    def apply_screw_holes(self, plate):

        edge_distance = min(self.left_pad / 2, self.right_pad / 2, self.bottom_pad / 2, self.top_pad / 2)

        def build_screw_hole_row(y):

            num_holes_in_row = self.num_holes / 2
            holes = []

            x = edge_distance
            step_x  = (self.exterior_width - 2 * edge_distance) / (num_holes_in_row - 1)

            for h in range(num_holes_in_row):
                holes.append(
                    translate( [  x, y, 0 ] )(
                        circle(r = self.hole_diameter / 2, segments=20)
                    )
                )

                x = x + step_x

            return holes

        return difference()(
            plate,
            union()(
                build_screw_hole_row(y = edge_distance),
                build_screw_hole_row(y = self.exterior_height - edge_distance)
            )
        )

    def switch_hole(self, width_factor, height_factor):

        def stab_geometry():

            # Basic combined stab hole.  Designed from Cherry specs:
            #
            #   http://cherryamericas.com/wp-content/uploads/2014/12/mx_cat.pdf
            #
            #   Linked to from: http://cherryamericas.com/product/mx-series/
            #
            # One real nice thing about CSG is that you can just "follow the lines" on a spec drawing
            # with ordinary translations.
            #
            if self.stabs in ('both', 'cherry'):
                s = union()(
                    translate( [ 0, -6.77, 0 ] )(
                        union()(
                            translate( [ -3.325, 0, 0 ] )(
                                square(size=[6.65, 12.3 ] )
                            ),

                            # Costar cutout.  Ideally, X should be -1.6, but to line up with the Cherry cutout,
                            # it needs to be closer in by .05 mm.  Also, it needs to be "lower" than typical costar.
                            # I think we can live with that.
                            #
                            # Here's how we get to -1.6 from center of cutout:
                            #
                            #        |--------A--------|     A == 23.8 mm per Cherry spec
                            #         |-------B-------|      B == 20.6 mm per some internet people.
                            #       +-+   +-------+   +-+
                            #       | |   |       |   | |
                            #       | |   |       |   | |
                            #       | |   |       |   | |
                            #       +-+   +-------+   +-+

                            translate( [ -1.65, -1.2, 0 ] )(        # Bottom notch + Costar cutout.
                                square(size=[3.3, 14 ] )
                            ) if self.stabs == 'both' else translate( [-1.5, -1.2, 0] )(
                                square(size=[3.0, 2 ])
                            )
                        )
                    ),
                    translate( [ 0, -0.5, 0 ] )(
                        square(size=[4.2, 2.8 ] )
                    )
                )

            elif self.stabs == 'costar':

                s = translate( [ -1.6, -7.75, 0 ] )(
                    square(size=[3.3, 14])
                    )

            return s

        def build_stab(a, left=None, right=None):

            combined_stab = stab_geometry()

            if left == None and right == None:
                left  = a / 2
                right = a / 2

            # The stab is a union of the right cutout, the left cutout, and a connecting rectangle, for Cherry-
            # style stabs.
            stab = union()(
                translate( [ right, 0, 0 ] )(combined_stab),
                translate( [ -left, 0, 0 ] )(mirror( [ 1, 0, 0 ] )(combined_stab))
                )

            if self.stabs in ('both', 'cherry'):
                stab = union()(
                    stab,
                    translate( [ (right - left) / 2, 0, 0 ] )(
                        square(size=[right+left, 4.6], center=True)
                    )
                )

                # The 2u stab has an extra cutout.
                #   See http://cherryamericas.com/wp-content/uploads/2014/12/mx_cat.pdf

                if a < 24:
                    stab = union()(
                        stab,
                        translate( [ -11.9, -5.97, 0 ] )(
                            square(size=[23.8, 10.7 ] )
                        )
                    )

            return stab

        hole = square(size=[14, 14], center=True)

        if width_factor >= 2.0 or height_factor >= 2.0:

            # The spacebar stab spacing numbers came from:
            #   https://deskthority.net/wiki/Space_bar_dimensions
            #
            # TODO: Add some means of specifying and generating spacebar mount style variants.

            if width_factor >= 8.0 or height_factor >= 8.0:

                stab = build_stab(133.35)

            elif width_factor >= 7.0 or height_factor >= 7.0:

                stab = build_stab(114.0)

            elif width_factor >= 6.25 or height_factor >= 6.25:

                stab = build_stab(100.0)

            #elif width_factor >= 6.0 or height_factor >= 6.0:

                # TODO: Deal with this asymmetrical case.

            elif width_factor >= 3.0 or height_factor >= 3.0:

                stab = build_stab(38.1)

            else:

                stab = build_stab(23.8)

            # Important note: Because the plate gets flipped at the end, we have to build
            #   the geometry upside down!  i.e. notice the mirror call

            hole = union()(
                hole,
                mirror( [ 0, 1, 0 ] )(stab)
            )

            if height_factor > width_factor:

                hole = rotate( [ 0, 0, 90 ] )(hole)

        return hole

    def build_base_top_plate(self):
        key_hole_squares = []

        rx = 0
        ry = 0
        r = 0

        cursor_x = 0
        cursor_y = 0

        standard_key_spacing = 19.05    # From an older Cherry spec.
        key_space_points = []

        for row in self.layout:

            cursor_x = rx

            height_increment = standard_key_spacing
            next_key_width_factor  = 1.0
            next_key_height_factor = 1.0
            skip_next = False

            if type(row) == list:
                for e in row:

                    # All this handling is from keyboard-layout-editor.com's generated JSON.
                    #
                    if type(e) == dict:
                        if 'r' in e:    # Rotation angle
                            r = e['r']
                        if 'w' in e:                        # Forcing next key's unit width
                            next_key_width_factor = e['w']
                        if 'h' in e:                        # Forcing next key's unit height
                            next_key_height_factor = e['h']
                        if 'rx' in e:                               # Redefining the cursor's "reset" x coordinate.
                            rx = e['rx'] * standard_key_spacing
                            cursor_x = rx
                            cursor_y = ry
                        if 'ry' in e:                               # Redefining the cursor's "reset" y coordinate.
                            ry = e['ry'] * standard_key_spacing
                            cursor_x = rx
                            cursor_y = ry
                        if 'x' in e:                                            # Forcing the cursor's x positioning relative to "here."
                            cursor_x = cursor_x + (standard_key_spacing * e['x' ] )
                        if 'y' in e:                                            # Forcing the cursor's y positioning relative to "here."
                            cursor_y = cursor_y + (standard_key_spacing * e['y' ] )
                        if 'd' in e:                # Next "key" is really a decal.  Skip it.
                            skip_next = True

                    elif skip_next:
                        skip_next = False

                    else:

                        space_width =  standard_key_spacing * next_key_width_factor
                        space_height = standard_key_spacing * next_key_height_factor

                        space_relative_x_center = space_width  / 2
                        space_relative_y_center = space_height / 2

                        def trans2d(translation, point):
                            return [translation[0] + point[0],
                                    translation[1] + point[1]]

                        def rotate2d(degrees, point):
                            rads = degrees * 3.14159 / 180.0
                            return [point[0] * math.cos(rads) - point[1] * math.sin(rads),
                                    point[0] * math.sin(rads) + point[1] * math.cos(rads)]

                        def apply_square():
                            # Apply the transformation on an origin-centered rectangle representing the whole key space.
                            return [ apply_transform( [ -space_relative_x_center, -space_relative_y_center ] ),
                                     apply_transform( [  space_relative_x_center, -space_relative_y_center ] ),
                                     apply_transform( [  space_relative_x_center,  space_relative_y_center ] ),
                                     apply_transform( [ -space_relative_x_center,  space_relative_y_center ] )]

                        if r != 0.0:

                            def apply_transform(point):
                                return trans2d( [ rx, ry],
                                    rotate2d(r,
                                        trans2d( [ -rx, -ry],
                                            trans2d( [ cursor_x + space_relative_x_center, cursor_y + space_relative_y_center],
                                                point
                                            )
                                        )
                                    )
                                )

                            transformed_square = apply_square()

                            key_space_points.extend(transformed_square)

                            self.update_mins_maxes(transformed_square)

                            key_hole_squares.append(
                                translate( [ rx, ry, 0 ] )(
                                    rotate( [ 0, 0, r ] )(
                                        translate( [ -rx, -ry, 0 ] )(
                                            translate( [ cursor_x + space_relative_x_center, cursor_y + space_relative_y_center, 0 ] )(
                                                self.switch_hole(next_key_width_factor, next_key_height_factor)
                                            )
                                        )
                                    )
                                )
                            )

                        else:

                            # Support a simplied, non-rotated set of transformations just to cut down on the size of
                            # the generated scad file.

                            def apply_transform(point):
                                return trans2d( [ cursor_x + space_relative_x_center, cursor_y + space_relative_y_center], point)

                            transformed_square = apply_square()

                            key_space_points.extend(transformed_square)

                            self.update_mins_maxes(transformed_square)

                            key_hole_squares.append(
                                    translate( [ cursor_x + space_relative_x_center, cursor_y + space_relative_y_center, 0 ] )(
                                        self.switch_hole(next_key_width_factor, next_key_height_factor)
                                    )
                            )

                        cursor_x = cursor_x + space_width

                        next_key_width_factor  = 1.0
                        next_key_height_factor = 1.0

                # In KLE, the per-row Y increment seems to be a constant 1u, unlike the X increment, which is the key's entire width
                cursor_y = cursor_y + height_increment

        self.interior_width  = self.max_x - self.min_x
        self.interior_height = self.max_y - self.min_y

        self.exterior_width  = self.interior_width  + self.left_pad + self.right_pad
        self.exterior_height = self.interior_height + self.bottom_pad + self.top_pad

        plate = difference()(
                square(size=[self.exterior_width, self.exterior_height ] ),
                translate([self.left_pad, self.top_pad, 0])(
                    translate( [ -self.min_x, -self.min_y, 0 ] )(
                        key_hole_squares
                    )
                )
            )

        if self.show_points:
            point_collection = [ translate( [ p[0],p[1],1 ] )(circle(r=1, segments=20)) for p in key_space_points ]
            plate = union()(plate, color("red")(translate([self.left_pad + -self.min_x, self.top_pad + -self.min_y, 0])(point_collection)))

        return translate( [ 0, self.exterior_height, 0 ] )(
                mirror( [ 0, 1, 0 ] )(
                    plate
                )
            )

    def build_base_bottom_plate(self):

        return square(size=[self.exterior_width, self.exterior_height ] )

    def build_mid_layers(self, plate):
        #Get the shortest padding
        shortest_padding = min(self.left_pad, self.right_pad, self.top_pad, self.bottom_pad)
        return difference()(
            plate,
            translate([shortest_padding, shortest_padding, 0])(
                square(size=[self.exterior_width - shortest_padding*2, self.exterior_height - shortest_padding*2] )
                )
            )

    def render_top_plate(self, output_dir):
        scad_render_to_file(self.base_top_plate, os.path.join(output_dir, "top.scad"), include_orig_code=False)

    def render_bottom_plate(self, output_dir):
        scad_render_to_file(self.base_bottom_plate, os.path.join(output_dir, "bottom.scad"), include_orig_code=False)

    def render_mid_layers(self, output_dir):
        if self.mid_layers:
            scad_render_to_file(self.mid_layers, os.path.join(output_dir, "mid_closed.scad"), include_orig_code=False)

#------------------------------------------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-j',  '--json',            type=str,   default='',  required=True, help="JSON file to load.  Raw data download from keyboard-layout-editor.com.")
    parser.add_argument('-o',  '--output_dir',      type=str,   default='.', help="Directory into which the resulting .scad files will be generated.")
    parser.add_argument('-s',  '--stabs',           choices=['both', 'cherry', 'costar'], default='both', help="Specify the style of stabilizers to generate.")
    parser.add_argument('-hp', '--horizontal_pad',  type=str, default=0.0, help="Horizontal padding per side. Can also define left,right padding.")
    parser.add_argument('-vp', '--vertical_pad',    type=float, default=0.0, help="Vertical padding per side. Can also define top,bottom padding.")
    parser.add_argument('-c',  '--corner_radius',   type=float, default=0.0, help="Corner radius.")
    parser.add_argument('-n',  '--num_holes',       type=int,   default=0,   help="Number of screw holes.")
    parser.add_argument('-hd', '--hole_diameter',   type=float, default=0.0, help="Screw hole diameter.")
    parser.add_argument('-sp', '--show_points',     action="store_true",     help="Debug aid.  Add floating red points for key space rectangles.")
    
    args = parser.parse_args()

    board = BoardBuilder(args.json,
                         args.horizontal_pad,
                         args.vertical_pad,
                         args.corner_radius,
                         args.num_holes,
                         args.hole_diameter,
                         args.show_points,
                         args.stabs)

    board.render_top_plate(args.output_dir)
    board.render_bottom_plate(args.output_dir)
    board.render_mid_layers(args.output_dir)
