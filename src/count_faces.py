import json
import warnings
from pathlib import Path
from typing import Iterable

from facenet_pytorch import MTCNN
from PIL import Image
from tqdm import tqdm


def extract_metadata(file: Path) -> dict:
    """Extracts page metadata from file path."""
    journal, year, month, day, _, page = file.stem.split("-")
    return {
        "journal": journal,
        "page": page,
        "year": int(year),
        "month": int(month),
        "day": int(day),
        "decade": (int(year) // 10) * 10,
        "file": str(file),
    }


def stream_records(files: list[Path], mtcnn) -> Iterable[dict]:
    """Streams records for each image with metadata and bounding boxes.
    If an exception occurs, an error record is saved."""
    for file in tqdm(files, desc="Processing all images."):
        metadata = extract_metadata(file)
        try:
            with Image.open(file) as img:
                boxes, _ = mtcnn.detect(img)
                boxes = [] if boxes is None else boxes.tolist()
                yield {
                    "type": "success",
                    "boxes": boxes,
                    "n_faces": len(boxes),
                    **metadata,
                }
        except Exception as e:
            warnings.warn(f"Failed processing {file}, reason: {e}")
            yield {
                "type": "error",
                "reason": str(e),
                **metadata,
            }


def main():
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    print("Finding images.")
    in_dir = Path("dat/images/")
    files = list(in_dir.glob("**/*.jpg"))

    print("Loading model")
    mtcnn = MTCNN(keep_all=True)

    out_path = results_dir.joinpath("faces.jsonl")
    # Streaming results to output file
    with out_path.open("w") as out_file:
        for record in stream_records(files, mtcnn=mtcnn):
            out_file.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
