#!/usr/bin/env python3
"""Read explicit images without altering them; write encoded RGBA channel sheets.
Requires Pillow. Observations are not texture-role classification or Blender color tests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import warnings


def audit(paths, output, max_pixels=16777216):
    from PIL import Image, ImageDraw, ImageStat, UnidentifiedImageError
    output = Path(output)
    if output.exists():
        raise ValueError('Output directory exists; use a new evidence directory')
    if max_pixels <= 0 or max_pixels > 67108864:
        raise ValueError('max_pixels must be in 1..67108864')
    Image.MAX_IMAGE_PIXELS = max_pixels
    # Validate source readability before creating the output directory.
    sources = [Path(p).resolve(strict=True) for p in paths]
    if len(set(sources)) != len(sources):
        raise ValueError('Duplicate input paths')
    output.mkdir(parents=True)
    records = []
    for i, path in enumerate(sources):
        entry = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(path) as im:
                    if im.width * im.height > max_pixels:
                        raise ValueError('Pixel limit exceeded')
                    entry.update(format=im.format, mode=im.mode, size=list(im.size),
                                 frames=getattr(im, 'n_frames', 1),
                                 has_icc=bool(im.info.get('icc_profile')))
                    if getattr(im, 'n_frames', 1) != 1 or im.mode not in ('RGB','RGBA','L','LA','P'):
                        entry.update(status='unsupported', reason='Requires explicit high-bit-depth/multiframe inspection; no lossy role inference')
                        records.append(entry)
                        continue
                    # No ICC, gamma, orientation or premultiplication conversion is applied.
                    rgba = im.convert('RGBA')
                    tiles = [('RGB (encoded)',rgba.convert('RGB'))]
                    entry['channels'] = {}
                    for name, ch in zip('RGBA',rgba.split()):
                        hist = ch.histogram(); total = ch.width*ch.height
                        entry['channels'][name] = {'min':ch.getextrema()[0], 'max':ch.getextrema()[1],
                            'mean':ImageStat.Stat(ch).mean[0], 'zero_fraction':hist[0]/total,
                            'one_fraction':hist[255]/total,
                            'nonbinary_fraction':sum(hist[1:255])/total}
                        tiles.append((name+' (encoded)',ch.convert('RGB')))
                    sheet=Image.new('RGB',(5*260,290),'#303030'); draw=ImageDraw.Draw(sheet)
                    for j,(label,tile) in enumerate(tiles):
                        tile.thumbnail((252,252));sheet.paste(tile,(j*260+4,30));draw.text((j*260+4,8),label,fill='white')
                    filename=f'{i:03d}-{entry["sha256"][:12]}-channels.png'
                    sheet.save(output/filename)
                    entry.update(status='observed',sheet=filename,
                        alpha_note='RGBA conversion synthesizes opaque alpha when absent; channel statistics do not imply opacity use')
        except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning) as e:
            entry.update(status='blocked',reason=str(e))
        records.append(entry)
    report={'schema_version':1,'qualification':'encoded_image_observations_only',
            'limitations':['No role inference','No scene-linear or OCIO conversion','ICC presence recorded but not applied',
                          'No EXIF orientation transform','Float/HDR/high-bit-depth and multiframe require separate inspection'],
            'images':records}
    (output/'texture-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('images',nargs='+');p.add_argument('--output',required=True)
    p.add_argument('--max-pixels',type=int,default=16777216);a=p.parse_args()
    try:
        r=audit(a.images,a.output,a.max_pixels)
        print(json.dumps({'report':str(Path(a.output)/'texture-report.json'),
                          'observed':sum(x['status']=='observed' for x in r['images']),
                          'not_observed':sum(x['status']!='observed' for x in r['images'])}))
        return 0 if all(x['status']=='observed' for x in r['images']) else 3
    except (ImportError,OSError,ValueError) as e:
        p.exit(2,str(e)+'\n')

if __name__=='__main__':raise SystemExit(main())
