# SAT_Solver
A SAT solver written in python to solve CNF's.

This project also contains a executable file for windows machines.

# Usage
The program takes two parameters:

- Heuristic: -Sn where n=1 (random DPLL), n=2 (Jeroslow Wang one-sided), n=3 (Minimum Remaining Values)
- Path: Path to the input file which is the concatenation of rules+given variables

The program outputs a .out file with the truth values for the variables
# To run

To run this program please follow one of these two methods:

### For Windows or Linux systems with Python:
execute the following command:

```bash
python SAT.py -Sn Path/To/Input
```

### Only for Windows machines
This will execute the .exe file

```bash
SAT -Sn Path/To/Input
```
