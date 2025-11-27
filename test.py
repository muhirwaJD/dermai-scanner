"""Test to inspect contents of .keras model file"""

import zipfile

with zipfile.ZipFile('Skin_Cancer_Model_v1.keras', 'r') as z:
    print("Files in .keras archive:")
    z.printdir()

    # Check keras version metadata
    if 'metadata.json' in z.namelist():
        import json
        metadata = json.loads(z.read('metadata.json'))
        print(f"\nKeras version: {metadata.get('keras_version', 'unknown')}")
