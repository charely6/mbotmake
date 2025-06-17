from mbotmake2.grammars.toolpath import grammar
from mbotmake2.transformers.toolpath import ToolpathTransformer


def test_prusa_gcode_file() -> None:
    with open("testcases/prusaslicer_gcode/xyzCalibration_cube.gcode", "r") as file:
        ast = grammar.parse(file.read())
        transformer = ToolpathTransformer(0.0)
        assert transformer.visit(ast)
