from pathlib import Path

from parsimonious.exceptions import ParseError

from mbotmake2.grammars.thumbnails import grammar
from mbotmake2.transformers.thumbnails import PNGImage, ThumbnailDecoder


def extractThumbnails(filename: Path, output_dir: Path) -> list[Path]:
    with open(filename, "r") as file:
        # Read the file in chunks to extract only relevant parts containing THUMBNAIL_BLOCK_START or THUMBNAIL_BLOCK_END
        # Load first 5MB of the file
        file.seek(0)
        content = file.read(5_000_000)

        # It seems that these are pretty standard for thumbnail blocks
        # Orcaslicer uses '; THUMBNAIL_BLOCK_START' and '; THUMBNAIL_BLOCK_END' additionally to wrap the thumbnail block.
        THUMBNAIL_BLOCK_START = "; thumbnail begin"
        THUMBNAIL_BLOCK_END   = "; thumbnail end"

        currentlyCollectingThumbnail = False
        countCollectedThumbnail = 0
        relevant_parts = []
        for line in content.splitlines():
            if THUMBNAIL_BLOCK_START in line:
                currentlyCollectingThumbnail = True
                #print(f"Found '{THUMBNAIL_BLOCK_START}'. Starting to collect thumbnail data.")

            if currentlyCollectingThumbnail:
                if line.strip() and line.strip() != ";":
                    relevant_parts.append(line)

            if THUMBNAIL_BLOCK_END in line:
                currentlyCollectingThumbnail = False
                countCollectedThumbnail += 1
                #print(f"Found '{THUMBNAIL_BLOCK_END}'. Stopped collecting thumbnail data.")

        # Combine the relevant parts for parsing
        relevant_content = "\n".join(relevant_parts) + "\n"

        #print(f"Extracted {len(relevant_parts)} lines of thumbnail data.")
        #print("Relevant content for parsing:")
        #print(relevant_content)

        try:
            print("Attempting to parse the extracted thumbnail blocks...")
            ast = grammar.match(relevant_content)
            #print("Parsing successful. AST generated.")
        except ParseError as e:
            print("No thumbnails were not found or parsing failed. Skipping thumbnail generation...")
            print(f"ParseError: {e}")
            return []

    decoder = ThumbnailDecoder()
    #print("Decoding the AST into a list of PNGImage objects...")
    thumbnails: list[PNGImage] = decoder.visit(ast)

    # Checking if all thumbnails made it through decoding to PNG
    if countCollectedThumbnail == len(thumbnails):
        print(f"Successfully collected and parsed all {len(thumbnails)} thumbnails.")
    else:
        print(f"Warning: {countCollectedThumbnail} collected thumbnails do not match the {len(thumbnails)} parsed thumbnails.")

    thumbnail_paths: list[Path] = []
    for tn in thumbnails:
        h = tn.header
        filename = output_dir / f"thumbnail_{h.width}x{h.height}.png"
        with open(filename, "wb") as image_file:
            image_file.write(tn.payload)

        print(f"Saved thumbnail with dimensions {h.width}x{h.height} to {filename}.")
        thumbnail_paths.append(filename)

    print(f"Thumbnail extraction completed. {len(thumbnail_paths)} thumbnails saved.")
    return thumbnail_paths
