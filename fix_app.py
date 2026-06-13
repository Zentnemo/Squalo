"""Trim app.py to keep only the first (complete) create_app function."""
import os

path = os.path.join(os.path.dirname(__file__), 'app.py')
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the first "if __name__" line
cut = None
for i, line in enumerate(lines):
    if line.strip().startswith('if __name__ =='):
        cut = i
        break

if cut is None:
    print("ERROR: Could not find __main__ block")
else:
    # Keep lines 0..cut+3 (the if block + app = create_app() + app.run + blank)
    clean = lines[:cut + 4]
    # Remove any trailing blank lines then add one
    while clean and clean[-1].strip() == '':
        clean.pop()
    clean.append('\n')
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(clean)
    print(f"Trimmed from {len(lines)} to {len(clean)} lines (cut at line {cut+1})")
