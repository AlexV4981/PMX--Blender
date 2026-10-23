#!/usr/bin/env python3
"""Find the shared pipeline by frontmatter name, independent of installed folder IDs."""
from pathlib import Path
import re
import sys

def locate(root=None):
    root=Path(root).resolve() if root else Path(__file__).resolve().parents[2]
    found=[]
    for folder in root.iterdir():
        skill=folder/'SKILL.md'
        if not skill.is_file(): continue
        match=re.search(r'^name:\s*(.+)$',skill.read_text(encoding='utf-8'),re.M)
        if match and match.group(1).strip().strip(chr(34)+chr(39)) == 'anime-blender-pipeline':
            found.append(folder.resolve())
    if len(found)!=1:
        raise RuntimeError('Expected one installed anime-blender-pipeline sibling; install/locate the full pack before executing.')
    return found[0]

if __name__=='__main__':
    try: print(locate(sys.argv[1] if len(sys.argv)>1 else None))
    except (OSError,RuntimeError) as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(2)
