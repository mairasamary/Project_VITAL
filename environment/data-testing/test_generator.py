#!/usr/bin/env python3
import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEN = HERE/"generate_data.py"
VAL = HERE/"validate_data.py"

class GeneratorTests(unittest.TestCase):
    def generate(self, root, seed=42, count=20):
        subprocess.run([sys.executable,str(GEN),"--size","small","--seed",str(seed),
                        "--patients",str(count),"--output",str(root)], check=True,
                       stdout=subprocess.DEVNULL)

    def test_requested_count(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data"; self.generate(p,count=17)
            m=json.loads((p/"manifest.json").read_text())
            self.assertEqual(17,m["counts"]["patients"])

    def test_fixed_seed_is_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            self.generate(a,42,25); self.generate(b,42,25)
            for name in ["patients.csv","encounters.csv","vitals.csv"]:
                self.assertEqual((a/name).read_text(),(b/name).read_text())

    def test_different_seed_changes_data(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/"a",Path(d)/"b"
            self.generate(a,42,25); self.generate(b,99,25)
            self.assertNotEqual((a/"patients.csv").read_text(),(b/"patients.csv").read_text())

    def test_generated_data_validates(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data"; self.generate(p,42,30)
            r=subprocess.run([sys.executable,str(VAL),str(p)], capture_output=True, text=True)
            self.assertEqual(0,r.returncode,r.stdout+r.stderr)

if __name__=="__main__":
    unittest.main()
