"""
Compare Test Results
====================

Compares the results from single port and dual port tests.

Usage:
    python compare_results.py
"""

import json
from pathlib import Path


def load_results(output_dir: Path):
    """Load both test results"""
    single_port_path = output_dir / "single_port_test_result.json"
    dual_port_path = output_dir / "dual_port_test_result.json"

    results = {}

    if single_port_path.exists():
        with open(single_port_path, "r", encoding="utf-8") as f:
            results["single_port"] = json.load(f)
    else:
        results["single_port"] = None

    if dual_port_path.exists():
        with open(dual_port_path, "r", encoding="utf-8") as f:
            results["dual_port"] = json.load(f)
    else:
        results["dual_port"] = None

    return results


def print_comparison(results: dict):
    """Print comparison summary"""

    print("\n" + "=" * 70)
    print("GPT-SoVITS MODEL SWITCHING BOTTLENECK COMPARISON")
    print("=" * 70)

    single = results.get("single_port")
    dual = results.get("dual_port")

    if not single or not dual:
        print("\nERROR: Both test results must be available!")
        print(f"  Single port: {'OK' if single else 'MISSING'}")
        print(f"  Dual port: {'OK' if dual else 'MISSING'}")
        return

    # Extract key metrics
    sp_summary = single["summary"]
    dp_summary = dual["summary"]

    print("\n[TEST CONFIGURATION]")
    print(f"  Dialogue turns: {sp_summary['num_turns']}")

    print("\n[SINGLE PORT (9880) - Model Switching]")
    print(f"  Total time:            {sp_summary['total_time']:.2f}s")
    print(f"  Avg model load time:   {sp_summary['avg_model_load_time']:.2f}s/turn")
    print(f"  Avg generation time:  {sp_summary['avg_generation_time']:.2f}s/turn")
    print(f"  Avg total per turn:   {sp_summary['avg_total_time']:.2f}s/turn")
    print(f"  Total model load:     {sp_summary['total_model_load_time']:.2f}s")
    print(f"  Total generation:    {sp_summary['total_generation_time']:.2f}s")

    print("\n[DUAL PORTS (31801/31802) - No Switching]")
    print(f"  Total time:            {dp_summary['total_time']:.2f}s")
    print(
        f"  One-time model load:  {dp_summary['one_time_model_load_time']:.2f}s (setup)"
    )
    print(f"  Avg generation time:  {dp_summary['avg_generation_time']:.2f}s/turn")
    print(f"  Avg total per turn:   {dp_summary['avg_total_time']:.2f}s/turn")
    print(f"  Total generation:     {dp_summary['total_generation_time']:.2f}s")

    # Calculate savings
    time_saved = sp_summary["total_time"] - dp_summary["total_time"]
    time_saved_percent = (time_saved / sp_summary["total_time"]) * 100

    print("\n[COMPARISON]")
    print(
        f"  Time saved with dual ports:  {time_saved:.2f}s ({time_saved_percent:.1f}%)"
    )

    if time_saved > 0:
        print(f"  Conclusion: DUAL PORT is FASTER by {time_saved:.2f}s")
    else:
        print(f"  Conclusion: SINGLE PORT is FASTER by {-time_saved:.2f}s")

    # Model load overhead
    sp_model_load = sp_summary["total_model_load_time"]
    dp_model_load = dp_summary["one_time_model_load_time"]

    print(f"\n[MODEL LOAD OVERHEAD]")
    print(f"  Single port (switching every turn): {sp_model_load:.2f}s")
    print(f"  Dual port (one-time setup):          {dp_model_load:.2f}s")
    print(f"  Overhead difference:                {sp_model_load - dp_model_load:.2f}s")

    print("\n" + "=" * 70)
    print("DETAILED TURN-BY-TURN COMPARISON")
    print("=" * 70)

    print("\n[Single Port Turns]")
    print(f"{'Turn':<6} {'Char':<6} {'Model Load':<12} {'Generate':<12} {'Total':<12}")
    print("-" * 50)
    for turn in single["turns"]:
        print(
            f"{turn['turn_index'] + 1:<6} {turn['character']:<6} {turn['model_load_time']:<12.2f} {turn['generation_time']:<12.2f} {turn['total_time']:<12.2f}"
        )

    print("\n[Dual Port Turns]")
    print(f"{'Turn':<6} {'Char':<6} {'Generate':<12}")
    print("-" * 30)
    for turn in dual["turns"]:
        print(
            f"{turn['turn_index'] + 1:<6} {turn['character']:<6} {turn['generation_time']:<12.2f}"
        )

    print("\n" + "=" * 70)


def main():
    output_dir = Path(__file__).parent / "output"

    print("Loading test results...")
    results = load_results(output_dir)
    print_comparison(results)


if __name__ == "__main__":
    main()
