import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from solutions.p4 import solve

folder = Path(__file__).parent / "p4_tests"

output_file = Path(__file__).parent / "results" / "p4_results.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for file in folder.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            input_data = f.readlines()

        line_idx = 0

        out.write("\n")
        out.write("⌈‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾⌉\n")
        out.write(f"Test: {file.name}\n")

        R, C = map(int, input_data[line_idx].split())
        line_idx += 1

        grid = []
        for i in range(R):
            row = input_data[line_idx].split()
            grid.append(row)
            line_idx += 1

        sr, sc, er, ec = map(int, input_data[line_idx].split())

        result = solve(grid, R, C, sr, sc, er, ec)

        out.write("Result:\n")
        out.write(str(result) + "\n")
        out.write("⌊__________________________________________⌋\n")

print(f"Results saved to {output_file}")