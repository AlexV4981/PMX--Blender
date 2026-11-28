"""Pure-data screening, not live Blender measurements or gate approval."""
import math

def screen(serial_fraction, threshold_percent):
    if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in (serial_fraction,threshold_percent)):
        raise ValueError("finite numeric inputs required")
    if not 0 <= serial_fraction < 1 or threshold_percent <= 0:
        raise ValueError("invalid fraction or threshold")
    upper = 100 * serial_fraction / (1-serial_fraction)
    return {"upper_bound_percent":upper,"screened_out":upper < threshold_percent,
            "notice":"Only valid for a defensible serial critical-path fraction; not an actual speed measurement."}

def coverage(first_moving, measured_frames, required_fields, fields):
    if type(first_moving) is not int or not isinstance(measured_frames,list) or not all(type(x) is int for x in measured_frames):
        raise ValueError("integer frames required")
    missing=[name for name in required_fields if fields.get(name) is not True]
    return {"status":"eligible" if measured_frames and any(x>=first_moving for x in measured_frames) and not missing else "blocked",
            "missing_or_unmeasured":missing,
            "notice":"Structural coverage only; inspect actual motion and measured fields."}

def reusable(previous, current, required):
    def valid(v):
        return isinstance(v,str) and len(v)==64 and all(c in "0123456789abcdef" for c in v)
    return bool(required) and all(valid(previous.get(k)) and previous.get(k)==current.get(k) for k in required)
