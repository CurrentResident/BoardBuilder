#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, re

from solid import *
from solid.utils import *
from euclid import *
# NOTE: The PyEuclid on PyPi doesn't include several elements added to 
# the module as of 13 Feb 2013.  Add them here until euclid supports them
# TODO: when euclid updates, remove this cruft. -ETJ 13 Feb 2013
def patch_euclid():
    def as_arr_local( self):
        return [ self.x, self.y, self.z]
    
    if 'as_arr' not in dir( Vector3):
        Vector3.as_arr = as_arr_local
patch_euclid()

def thread( outline_pts, inner_rad, pitch, length, segments_per_rot=32,
                        neck_in_degrees=0, neck_out_degrees=0):
    '''
    Sweeps outline_pts (an array of points describing a closed polygon in XY)
    through a spiral. 
    
    This is done by creating and returning one huge polyhedron, with potentially
    thousands of faces.  An alternate approach would make one single polyhedron,
    then repeat it over and over in the spiral shape, unioning them all together.  
    This would create a similar number of SCAD objects and operations, but still
    require a lot of transforms and unions to be done in the SCAD code rather than
    in the python, as here.  Also would take some doing to make the neck-in work
    as well.  Not sure how the two approaches compare in terms of render-time. 
    -ETJ 16 Mar 2011     
    
    outline_pts: a list of points (NOT an OpenSCAD polygon) that define the cross 
            section of the thread
            
    inner_rad: radius of cylinder the screw will wrap around
    pitch: height for one revolution
    length: distance from bottom-most point of screw to topmost
    segments_per_rot: segments per rotatio
    neck_in_degrees: degrees through which the outer edge of the screw thread will move from 
                    a thickness of zero (inner_rad) to its full thickness
    neck_out_degrees: degrees through which outer edge of the screw thread will move from 
                    full thickness back to zero
                    
    NOTE: if pitch is less than the height of each tooth (outline_pts), OpenSCAD will likely
    crash, since the resulting screw would self-intersect all over the place
    '''
    a = union()
    rotations = float(length)/pitch
    
    total_angle = 360.0*rotations
    up_step = float(length) / (rotations*segments_per_rot)
    total_steps = int(ceil( rotations * segments_per_rot))
    step_angle = total_angle/ total_steps
    
    all_points = []
    all_tris = []
    euc_up = Vector3( *UP_VEC)
    poly_sides = len( outline_pts)
    
    # Figure out how wide the tooth profile is
    min_bb, max_bb = bounding_box( outline_pts)
    outline_w = max_bb[0] - min_bb[0]
    outline_h = max_bb[1] - min_bb[1]
    
    min_rad = max( 0, inner_rad-outline_w-EPSILON)    
    
    # outline_pts, since they were created in 2D , are in the XY plane.
    # But spirals move a profile in XZ around the Z-axis.  So swap Y and Z
    # co-ords... and hope users know about this
    # Also add inner_rad to the profile
    euc_points = []
    for p in outline_pts:
        # If p is in [x, y] format, make it [x, y, 0]
        if len( p) == 2:
            p.append( 0)
        # [x, y, z] => [ x+inner_rad, z, y]
        s =  Point3( p[0], p[2], p[1]) # adding inner_rad, swapping Y & Z
        euc_points.append( s)
        
    for i in range( total_steps):
        angle = i*step_angle
        elevation = i*up_step
        if angle > total_angle:
            angle = total_angle
            elevation = length
        
        rad = inner_rad
        if angle < neck_in_degrees:
            rad = min_rad + angle/neck_in_degrees * outline_w
        elif angle > total_angle - neck_out_degrees:
            rad =min_rad +  (total_angle - angle)/neck_out_degrees * outline_w
        
        elev_vec = Vector3( rad, 0, elevation)
        
        for p in euc_points:
            pt = (p + elev_vec).rotate_around( axis=euc_up, theta=radians( angle))
            all_points.append( pt.as_arr())
        
        # Add the connectivity information
        if i < total_steps -1:
            ind = i*poly_sides
            for j in range( ind, ind + poly_sides - 1):
                all_tris.append( [ j, j+1,   j+poly_sides])
                all_tris.append( [ j+1, j+poly_sides+1, j+poly_sides])
            all_tris.append( [ ind, ind + poly_sides-1+poly_sides, ind + poly_sides-1])
            all_tris.append( [ ind, ind + poly_sides, ind +poly_sides-1+poly_sides])       
        
    # End triangle fans for beginning and end
    last_loop = len(all_points) - poly_sides
    for i in range( poly_sides -2):
        all_tris.append( [ 0,  i+2, i+1])
        all_tris.append( [ last_loop, last_loop + i+1, last_loop + i + 2])
        
        
    # Make the polyhedron
    a = polyhedron( points=all_points, triangles=all_tris)
    
    # Subtract the center, to remove the neck-in pieces
    # subtract above and below to make sure the entire screw fits within height 'length'
    cube_side = 2*(inner_rad + outline_w)
    subs = union()(
                down( outline_h/2)( cylinder( inner_rad, length + outline_h)),
                down( cube_side/2)(         cube( cube_side, center=True)),
                up( cube_side/2 + length)(  cube( cube_side, center=True))
            )
            
    return render()(a - subs)

def default_thread_section( tooth_height, tooth_depth, exterior=True):
    if not exterior:
        tooth_depth = -tooth_depth
    res = [ [ 0, -tooth_height/2],
             [ tooth_depth, 0],
             [ 0, tooth_height/2]
            ]
    return res


def assembly():
    # Scad code here
    a = union()
    
    rad = 5
    pts = [ [ 0, -1, 0],
            [ 1,  0, 0],
            [ 0,  1, 0],
            [ -1, 0, 0],
            [ -1, -1, 0]    ]
            
    a = thread( pts, inner_rad=10, pitch= 6, length=2, segments_per_rot=31, 
                            neck_in_degrees=30, neck_out_degrees=30)
    
    return a + cylinder( 10+EPSILON, 2)

if __name__ == '__main__':
    a = assembly()    
    scad_render_to_file( a)