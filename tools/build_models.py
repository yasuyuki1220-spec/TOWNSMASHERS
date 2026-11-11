# Builds models.js from the Blender model scripts:  python3 tools/build_models.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bl_lib, models_chars, models_items
only = sys.argv[1:]
for f in models_chars.ALL + models_items.ALL:
    if not only or f.__name__ in only: f()
bl_lib.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models.js'))
