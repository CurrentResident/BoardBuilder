BoardBuilder
=====================

Copyright (c) 2016-2019, Jim Thoenen
All rights reserved.  See license below.

This is a python script that processes keyboard-layout-editor.com JSON files and
generates OpenSCAD .scad files that can be further modified and exported to .dxf
or other formats as desired within OpenSCAD.

Usage
=====

BoardBuilder may be invoked directly on the command line, or it may be included as
a module from another Python script.  Please invoke with `--help` to see the
accepted arguments.

Hints and Notes
===============

This script generates fairly simple plate drawings which are intended to be
a reasonable starting point for a keyboard.  Once generated, consider
`include`ing them into hand-crafted .scad files where you can further modify
the final drawing for additional features (e.g. screw holes for feet, cutouts
for LCDs, etc).  This provides a clean separation of hand-crafted and generated
content, and works nicely with OpenSCAD's automatic reloading of externally-
modified files.  Also, remember you can often cut down costs by combining
multiple parts of identical material and thickness onto a single drawing.

BoardBuilder also produces a `holes.scad` file that contains only the
"negative space" switch and stabilizer cutouts.  This allows you to
independently design your own plates and then CSG-difference out the holes.

While the script allows combined Cherry + Costar stabilizer cutouts, their
use is discouraged, particularly if the resulting board will actually use
Cherry stabilizers.  This is because the Costar-compatibility cutouts
literally undermine the Cherry stabilizer's "top" clips, hurting their ability
to securely grab onto the plate.

The script adjusts the vertical displacement of the Costar stab cutouts WRT
the switch cutouts from -0.75mm to -0.55mm, which eliminates sticking on most
plates.  Be warned, however, that plates thicker than 1.5mm can distort
Costar stabs such that a displacement of -0.45mm might be needed.  This can
be commanded by specifying `--stab_vertical_adjustment -0.1`.  The downside to
doing so is that the Costar wire can *just barely* make contact with switch
itself in the fully-depressed position.  I don't know if that's enough to
matter, though, or if `-0.05` would address the issue.  Please do let me know
if you try it out.  :)

License
=====================

BoardBuilder
Copyright (c) 2016-2019, Jim Thoenen
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
* Neither the name of Jim Thoenen nor the names of any contributors may
    be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL JIM THOENEN BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
