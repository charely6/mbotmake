# mbotmake

A gcode to .makerbot conversion tool, compatible with Marlin gcode from Cura.
And likely others.

**This is a fork that works for the Makerbot Replicator Mini+**, and it is unclear if
it still works for the 5th Generation. See the original repository if you have
a 5th gen.

# Usage

It's a Python script that generates a .makerbot file from a .gcode file that is
passed as an argument on the command line.

There is now a github actin that generates a mbotmake.exe for windows users that don't want to have to get python working for this. I hope to eventual split the configuration for the different printers out to property files and come up with a way to change which is being used

You are almost guaranteed to have to understand the makerbot file format
anyway, so just read the code.

I'm adding my orcaslicer configuration for printer and process that seems to be working "well" I'm still having some issues but I think those a physical not gcode/makerbot code.

Big notes for making your own config. Origin=middle, extruder absolute not relative.

I also added a global variable at the top of mbotmake called DEBUG this will add each processed line as a "comment" into the jsontool path file I don't know if printing with all that in there will cause issues but it might so I recommend leaving it at False unless you are having weird issues and want to compare gcode-> jsontoolpath directly.

# TODO

More testing using different 5th gen and plus machines. 

Modify the script to handle all the different versions easily. 

Figure out how to do other nozzle sizes specifically 0.2mm or 0.6mm 

Make printer configs for all the different printers and different slicers (cura, prusa slicer, orca slicer) 