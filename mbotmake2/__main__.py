import argparse
import json
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import asdict
from itertools import islice
from pathlib import Path

from mbotmake2.extract_thumbnails import extractThumbnails
from mbotmake2.grammars.toolpath import grammar as toolpath_grammar
from mbotmake2.metafile import generateMetajson
from mbotmake2.progress import newProgressBar
from mbotmake2.transformers.toolpath import ToolpathTransformer
from mbotmake2.types import Command, ExtruderType, MachineType
from mbotmake2.validate import collectPrinterSettings


def countNewlines(file: Path) -> int:
    result = subprocess.check_output(["wc", "-l", file.as_posix()])
    return int(result.split()[0])


def decodeGCodefile(filename: Path) -> ToolpathTransformer:
    chunks = 4096

    progress_bar = newProgressBar(countNewlines(filename) // chunks * chunks + chunks)
    count = 0

    progress_bar.start()
    with open(filename, "r") as file:
        transformer = ToolpathTransformer()
        while True:
            next_n_lines = list(islice(file, chunks))
            if not next_n_lines:
                break

            ast = toolpath_grammar.parse("\n".join(next_n_lines))
            transformer.visit(ast)

            count += chunks
            progress_bar.update(count)

    progress_bar.finish()
    return transformer


def packageMBotFile(filename: Path, temp_dir: Path, thumbnail_paths: list[Path]) -> None:
    with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as mbotfile:
        for tn in thumbnail_paths:
            mbotfile.write(tn, arcname=tn.name)

        mbotfile.write(temp_dir / "meta.json", arcname="meta.json")
        mbotfile.write(temp_dir / "print.jsontoolpath", arcname="print.jsontoolpath")


def parseArgs(argv: list[str]) -> tuple[Path, MachineType, ExtruderType]:
    """Parse the command-line arguments.

    Following the convention of the GPX project at
    https://github.com/markwal/GPX, we pass through the machine type with
    the argument "-m", and the extruder type with "-e".
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-m",
        "--machine",
        type=MachineType,
        choices=list(MachineType),
        default=MachineType.REPLICATORPLUS.value,
        help="3D printer machine type",
    )
    parser.add_argument(
        "-e",
        "--extruder",
        type=ExtruderType,
        choices=list(ExtruderType),
        default=ExtruderType.SMARTEXTRUDERPLUS.value,
        help="Extruder type",
    )
    parser.add_argument("input", type=Path, help="Path to the input Gcode file")

    args = parser.parse_args(argv[1:])

    return args.input, args.machine, args.extruder


if __name__ == "__main__":
    input_file, machine_type, extruder_type = parseArgs(sys.argv)

    with tempfile.TemporaryDirectory() as tmpdir_name:
        temp_dir = Path(tmpdir_name)

        thumbnail_paths = extractThumbnails(input_file, temp_dir)

        transformer = decodeGCodefile(input_file)

        # Checking toolpath
        assert transformer.is_extrusion_absolute, "Fatal: Relative extrusion position detected."
        assert transformer.is_xyz_absolute, "Fatal: Relative xyz position detected."

        printer_settings = collectPrinterSettings(
            transformer.commands,
            transformer.z_transitions,
            transformer.printing_time_s,
        )

        # Write to meta json file
        print("Generating meta.json...")
        generateMetajson(temp_dir / "meta.json", printer_settings, machine_type, extruder_type)

        # Write to toolpath json file
        print("Generating print.jsontoolpath...")
        with open(temp_dir / "print.jsontoolpath", "w") as toolpathfile:
            toolpathfile.write("[\n")

            for cmd in transformer.commands:
                json.dump({"command": asdict(cmd)}, toolpathfile, sort_keys=True)
                toolpathfile.write(",\n")

            json.dump(
                {
                    "command": asdict(
                        Command(
                            "comment",
                            {"comment": "End of print"},
                        )
                    )
                },
                toolpathfile,
            )
            toolpathfile.write("\n]\n")

        output_file = input_file.with_suffix(".makerbot")
        print(f"Generating {output_file.name}...")
        packageMBotFile(output_file, temp_dir, thumbnail_paths)
