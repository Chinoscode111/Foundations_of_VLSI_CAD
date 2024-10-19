# Digital Logic Simulator

This project simulates a digital logic circuit using Python. It parses a simple Verilog-like description of a circuit, constructs the logical nodes (gates and flip-flops), and evaluates the circuit based on user-provided input signals.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Format](#file-format)
- [How It Works](#how-it-works)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

## Overview

This simulator processes a textual representation of a digital circuit, allowing users to define inputs, outputs, wires, and assignments. The simulator supports basic logic gates (AND, OR, NOT, etc.) and D flip-flops, enabling the evaluation of the circuit based on input signals.

## Features

- Supports various logic gates: AND, OR, NOT, NAND, NOR, XOR, XNOR
- Implements D flip-flops for sequential logic
- Parses Verilog-like syntax for defining circuit components
- Allows user input for signals to simulate circuit behavior
- Displays gate operations and final output values

## Installation

To run this project, ensure you have Python 3.x installed. Clone the repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/Chinoscode111/Foundations_of_VLSI_CAD.git
cd Foundations_of_VLSI_CAD
cd logic_simulator
```

## Usage

1. Prepare a text file (e.g., `dff.txt`) containing the Verilog-like description of your digital circuit.

### How to create a txt file containing the Verilog-like description of your digital circuit

Write the verilog discription of your circuit in a verilog file.

#### **Command Workflow**
Here’s an explanation of your Yosys commands and what each does:

```bash
yosys
```
1. **Read your Verilog file:**
   ```verilog
   read_verilog testverilog.v
   hierarchy -top counter
   ```
   - This loads your design and sets the top module as `counter`.

2. **Pre-synthesis optimization:**
   ```verilog
   proc    # Converts processes into simpler logic.
   opt     # Runs an initial optimization pass.
   fsm     # Extracts finite state machines (FSMs).
   memory  # Handles memory mappings.
   opt     # Another optimization pass.
   ```

3. **Synthesize the design to use your standard cells:**
   ```verilog
   synth -top counter
   dfflibmap -liberty cmos_cells.lib
   abc -liberty cmos_cells.lib
   clean
   ```
   - The `dfflibmap` and `abc` steps map flip-flops and logic gates to the ones defined in `cmos_cells.lib`.
   - `abc` performs technology mapping to ensure only the gates defined in the Liberty file are used.

4. **Generate the Verilog netlist:**
   ```verilog
   write_verilog out2.txt
   ```

---

### Run Simulator
```bash
python simulator.py
```

3. Follow the prompts to enter input signals as binary strings (e.g., '01010101') for your inputs.

## File Format

The input file should have the following structure:

- Define wires, inputs, and outputs:
  ```
  wire W1, W2;
  input D;
  output Q;
  ```

- Define assignments and connections:
  ```
  assign W1 = D & clk;
  DFF U1 ( .D(W1), .Q(Q), .clk(clk) );
  ```

## How It Works

1. The script reads a Verilog-like description from a specified file.
2. It parses the file to extract information about wires, inputs, outputs, and assignments.
3. It creates nodes for each gate and flip-flop in the circuit.
4. User inputs are taken for the signals, and the simulator calculates the output based on the circuit's logic.
5. Results are printed, showing each gate's operation and final output values.

## Example

Here’s an example of a simple D flip-flop circuit:

### Input File (`dff.txt`)
```
wire W1;
input clk, D;
output Q;

assign W1 = D & clk;
DFF U1 ( .D(W1), .Q(Q), .clk(clk) );
```

### Running the Simulator
When prompted, enter the clock signal and D input values:

```
Enter the clock signal as a binary string: 010101
Enter the D signal as a binary string: 110011
```

The simulator will evaluate the circuit and print the outputs.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize the README further to suit your project’s needs!