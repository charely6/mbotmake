# mbotmake

A gcode to .makerbot conversion tool, compatible with Marlin gcode from Cura.
And likely others.

**This is currently defaults to a Replicator 5 with a Smart Extruder** 
I have added parameters to change which machine and extruder but I have only tested the 5th gen and a mini plus with the settings the rest of the settings have been "extracted" from makerbot print.

# Usage

It's a Python script that generates a .makerbot file from a .gcode file that is
passed as an argument on the command line.

There is now a github actin that generates a mbotmake.exe for windows users that don't want to have to get python working for this. I hope to eventual split the configuration for the different printers out to property files and come up with a way to change which is being used

I'm adding my orcaslicer configuration for printer and process that seems to be working "well" I'm still having some issues but I think those a physical not gcode/makerbot code.

Big notes for making your own config. Origin=middle, extruder absolute not relative.

There is global variable at the top of mbotmake called DEBUG this will add each processed line as a "comment" into the jsontool path file I don't know if printing with all that in there will cause issues but it might so I recommend leaving it at False unless you are having weird issues and want to compare gcode-> jsontoolpath directly.

# NEW FEATURE
## Parameter machine/extruder control  
There is now parameters to control which machine of the 5thgen/Plus family you are using and which extruder your using, These can be set in the post processing script in your slicer or when running in command line, You should be able to make a shortcut/batch script or something that would also use them for you.  
*Note these are only partially tested many of the settings have been taken from Makerbot Print, Use at your own risk and report and issues or feedback please.*

|               |               |
| ------------- | ------------- |
| Replicator 5th gen | -Rep5   |
| Replicator Mini (5th) | -Mini5 |
| Replicator Plus | -RepPlus |
| Repliactor Mini Plus | -MiniPlus |
| Smart Extruder | -SmartExt |
| Smart Extruder Plus | -SmartExtPlus |
| Smart Tough Extruder Plus | -ToughExt | 
| Experimental Smart Extruder Plus | -ExperimentalExt |


## PrusaSlicer 
Copied from [@sabesnait's](https://github.com/sabesnait) Fork of the original
Change these two settings in PrusaSlicer:
* Runs mbotmake automatically after exporting G-Code.<br><strong>[Print Settings] &rarr; [Output options] &rarr; [Post-processing scripts]:</strong><br>'[path to python] [.../]mbotmake -prusa -Rep5 -SmartExt'
* Generates the thumbnails for the Makerbot Replicator Gen5 display.<br><strong>[Printer Settings] &rarr; [General] &rarr; [G-code thumbnails]:</strong><br>
'55x40, 110x80, 320x200'

## OrcaSlicer
Change these two settings in OrcaSlicer:
* Runs mbotmake automatically after exporting G-Code.<br><strong>[Print Settings] &rarr; [Output options] &rarr; [Post-processing scripts]:</strong><br>'[path to python] [.../]mbotmake -orca -Rep5 -SmartExt'
* Generates the thumbnails for the Makerbot Replicator Gen5 display.<br><strong>[Printer Settings] &rarr; [General] &rarr; [G-code thumbnails]:</strong><br>
'55x40, 110x80, 320x200'

# TODO

More testing using different 5th gen and plus machines. 

~~Modify the script to handle all the different versions easily.~~ Now supported with Parameters

Figure out how to do other nozzle sizes specifically 0.2mm or 0.6mm 

Make printer configs for all the different printers and different slicers (cura, prusa slicer, orca slicer) 
