import json
from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface

class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata):
        print("Root path is:", self.root)

        metadata_file = Path(self.root) / "metadata.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found at: {metadata_file}")

        with metadata_file.open(encoding="utf-8") as f:
            meta = json.load(f)

        metadata["version"] = meta["version"]
        metadata["description"] = meta["description"]
        metadata["authors"] = meta["authors"]
