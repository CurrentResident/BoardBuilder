BoardBuilder
=====================

Copyright (c) 2016-2017, Jim Thoenen
All rights reserved.  See license below.

This is a python script that turns keyboard layout JSON files from
www.keyboard-layout-editor.com and generates OpenSCAD .scad files that can be
further modified and exported to .dxf or other formats as desired within
OpenSCAD.

Workflow-wise, I find what works best hand-coding my own top-level .scad files,
defining one module for each desired plate, and including the generated plate
scad file by name within the module.  It separates the hand-mods from the auto
generated plates cleanly, and works nicely with OpenSCAD's automatic reloading
of externally-modified open scad files.

License
=====================

BoardBuilder
Copyright (c) 2016-2017, Jim Thoenen
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
