"""Agent evaluation gate.

Scores routing accuracy and groundedness against a golden dataset and exits
non-zero below threshold, so the pipeline blocks promotion to production.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from app import agents  # noqa: E402

THRESHOLD = 0.9


def main():
    cases = json.loads((pathlib.Path(__file__).parent / "dataset.json").read_text())
    passed = 0
    for case in cases:
        result = agents.handle(case["message"], "cust1")
        routed = result["intent"] == case["intent"]
        grounded = case["must_include"].lower() in json.dumps(result).lower()
        ok = routed and grounded
        passed += ok
        status = "PASS" if ok else "FAIL"
        detail = "" if ok else f"  (got intent={result['intent']}, grounded={grounded})"
        print(f"{status}  {case['message'][:50]:<52}{detail}")

    score = passed / len(cases)
    print(f"\nscore {passed}/{len(cases)} = {score:.0%}  (threshold {THRESHOLD:.0%})")
    if score < THRESHOLD:
        print("AGENT EVALUATION GATE FAILED — blocking promotion")
        return 1
    print("agent evaluation gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
