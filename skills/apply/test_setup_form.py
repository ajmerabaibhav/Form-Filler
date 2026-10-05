"""Run: python3 test_setup_form.py — checks save/load round-trip and DOB parsing."""
import os, sys, tempfile

os.environ["APPLY_BASE"] = tempfile.mkdtemp()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup_form as sf

vals = {"First name": "Asha", "LinkedIn": "https://linkedin.com/in/asha",
        "Resume file (full path, for upload fields)": "/tmp/cv.pdf"}
sf.save(vals)
assert sf.load_existing() == vals, sf.load_existing()
assert sf.parse_dob("14 Aug 1998").isoformat() == "1998-08-14"
assert sf.parse_dob("1998-08-14").isoformat() == "1998-08-14"
assert sf.parse_dob("not a date") is None
print("ok")
