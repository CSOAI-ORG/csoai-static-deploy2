#!/usr/bin/env python3
"""
SOV Submit Agent — Automated Kaggle submission using our tools
"""
import csv, json, time, subprocess, os
from pathlib import Path

KAGGLE = Path("/Users/nicholas/clawd/csoai-static-deploy2/kaggle")
API_TOKEN = os.environ.get("KAGGLE_API_TOKEN", "KGAT_d72d5146a3b5622d24bac06eaf4004f2")

class SOVSubmitAgent:
    """Automated submission agent"""
    
    def __init__(self):
        self.submission_file = KAGGLE / "submission_full_pipeline.csv"
    
    def check_submission(self):
        """Check if submission file exists and is valid"""
        if not self.submission_file.exists():
            print("ERROR: Submission file not found")
            return False
        
        # Validate format
        with open(self.submission_file) as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        
        if header != ["id", "winner_model_a", "winner_model_b", "winner_tie"]:
            print("ERROR: Invalid format")
            return False
        
        print(f"Submission valid: {len(rows)} rows")
        return True
    
    def submit_via_api(self):
        """Try submitting via Kaggle API"""
        print("Attempting API submission...")
        
        env = os.environ.copy()
        env["KAGGLE_API_TOKEN"] = API_TOKEN
        
        result = subprocess.run([
            "kaggle", "competitions", "submit",
            "llm-classification-finetuning",
            "-f", str(self.submission_file),
            "-m", "SOV Swarm: 4 models + 5-signal judgment"
        ], capture_output=True, text=True, env=env)
        
        if "successfully" in result.stdout.lower() or result.returncode == 0:
            print("API submission SUCCESS!")
            return True
        else:
            print(f"API failed: {result.stderr[:200]}")
            return False
    
    def submit_via_notebook(self):
        """Create a notebook that auto-submits"""
        print("Creating submission notebook...")
        
        notebook_code = '''
import csv, json, time, os
import kaggle

# Load competition data
input_dir = "/kaggle/input/llm-classification-finetuning"
test_data = []
with open(f"{input_dir}/test.csv") as f:
    for row in csv.DictReader(f):
        test_data.append(row)

# Create submission
with open("submission.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "winner_model_a", "winner_model_b", "winner_tie"])
    for row in test_data:
        r = judge(row.get("response_a", ""), row.get("response_b", ""))
        t = 0.05
        n = r["a"] + r["b"] + t
        w.writerow([row["id"], f"{r['a']/n:.10f}", f"{r['b']/n:.10f}", f"{t/n:.10f}"])

# Submit
kaggle.competition.submit("llm-classification-finetuning", "submission.csv", "SOV Swarm")
print("SUBMITTED!")
'''
        
        notebook_path = KAGGLE / "auto_submit.py"
        with open(notebook_path, "w") as f:
            f.write(notebook_code)
        
        print(f"Created: {notebook_path}")
        print("Upload to Kaggle and run to auto-submit")
        return True
    
    def run(self):
        """Main agent loop"""
        print("=" * 60)
        print("SOV SUBMIT AGENT")
        print("=" * 60)
        
        # Check submission
        if not self.check_submission():
            return False
        
        # Try API first
        if self.submit_via_api():
            return True
        
        # Fallback to notebook
        print("Falling back to notebook method...")
        self.submit_via_notebook()
        
        print("\n" + "=" * 60)
        print("SUBMISSION READY")
        print("=" * 60)
        print("Upload auto_submit.py to Kaggle and run it")
        return True

if __name__ == "__main__":
    agent = SOVSubmitAgent()
    agent.run()
