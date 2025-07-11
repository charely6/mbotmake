from parsimonious.grammar import Grammar

# ChamberTemperature = "M141"

NOT_STRICT = (
    "Line = (Move / ResetPosition / FanDuty / FanOff "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning / AbsolutePositioningForExtruders "
    "/ ArcMove / Unsupported / Comment) InlineComment? newline\n\n"
)

STRICT = (
    "Line = (Move / ResetPosition / FanDuty / FanOff "
    "/ ToolheadTemperature / BedTemperature / AbsolutePositioning / AbsolutePositioningForExtruders "
    "/ ArcMove / Comment) InlineComment? newline\n\n"
)

SYNTAX = r"""
BlankLine = ~r"[ \t\r]*\n"i
Comment = ";" (PrintingTime / IgnoredComment)

IgnoredComment = ~r"[^\n]*"i
InlineComment = ~r"[ \t]*;[^\n]*"i

ToolheadTemperature = "M104 S" Integer
BedTemperature = "M140 S" Integer
FanDuty = "M106 S" Decimal
FanOff = "M107"

AbsolutePositioning = "G90"
AbsolutePositioningForExtruders = "M82"
ResetPosition = "G92 E" ("0.0" / "0")

Move = "G1" (CoordSpiralVase / Coord3D / Coord2D / CoordE / CoordZ / Feedrate)
CoordZ = Z Decimal Feedrate?
Coord2D = X Decimal Y Decimal ExtruderPosition? Feedrate?
Coord3D = (X Decimal)? Y Decimal Z Decimal Feedrate?
CoordE = ExtruderPosition Feedrate
CoordSpiralVase = Z Decimal X Decimal Y Decimal ExtruderPosition

ArcMove = ~r"G[23] [^\n]*"
Unsupported = ~r"[MG][0-9]+[^\n;]*"i

ExtruderPosition = " E" Decimal
Feedrate = " F" Decimal

PrintingTime = ~r" estimated printing time [^=]*="i Hour? Minute? Second?
Hour = " " Integer "h"
Minute = " " Integer "m"
Second = " " Integer "s"
X = " X"
Y = " Y"
Z = " Z"

Integer = ~"[0-9]+"i
Decimal = ~r"-?(\d+\.\d+|\d+|\.\d+)"i
newline = "\n"
"""

grammar = Grammar("Document = (Line / BlankLine)+\n" + NOT_STRICT + SYNTAX)
