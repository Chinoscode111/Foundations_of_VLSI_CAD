import re
class Node:
    def __init__(self, node_number, node_type,num_inputs=0, num_outputs=0,  level=0, inversion_parity=False, controlling_value=None):
        self.node_number = node_number       # Node number (e.g., U1, U2, etc.)
        self.node_type = node_type             # Node type (AND, OR, NOT, etc.)         
        self.inputs = []                          # Inputs - list of connected nodes or signals
        self.outputs = []
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs           # Outputs - list of connected nodes or signals
        self.level = level                       # Level number (can be used for logic level assignment later)
        self.inversion_parity = inversion_parity   # True for inverting gates, False for non-inverting
        self.controlling_value = controlling_value  # Controlling value (if applicable)
       
    def add_input(self, input_node):
        self.inputs.append(input_node)
        self.num_inputs = len(self.inputs)
   
    # Function to add outputs to the node
    def add_output(self, output_node):
        self.outputs.append(output_node)
        self.num_outputs = len(self.outputs)
 
    def gate_function(self,inputs):
        gate_type = self.node_type
        if not isinstance(inputs, list) or len(inputs) == 0:
            return None  # Handle cases where inputs are not provided properly
 
        if gate_type == 'AND':
            result = inputs[0]
            for i in inputs[1:]:
                result &= i
            return result
 
        elif gate_type == 'OR':
            result = inputs[0]
            for i in inputs[1:]:
                result |= i
            return result
 
        elif gate_type == 'NOT':
            return ~inputs[0] & 1  # NOT only works on a single input
 
        elif gate_type == 'XOR':
            result = inputs[0]
            for i in inputs[1:]:
                result ^= i
            return result
 
        elif gate_type == 'XNOR':
            result = inputs[0]
            for i in inputs[1:]:
                result ^= i
            return ~result & 1  # Inverse of XOR
 
        elif gate_type == 'NAND':
            result = inputs[0]
            for i in inputs[1:]:
                result &= i
            return ~result & 1
 
        elif gate_type == 'NOR':
            result = inputs[0]
            for i in inputs[1:]:
                result |= i
            return ~result & 1
 
        return None  # Handle unknown gate types
 
    def __repr__(self):
        return ( f"Node({self.node_number}, "
                f"Node({self.node_type}, "
                f"Inputs: {self.inputs}, Outputs: {self.outputs}, "
                f"Num Inputs: {self.num_inputs}, Num Outputs: {self.num_outputs}, "
                f"Level: {self.level}, Inversion: {self.inversion_parity}, "
                f"Control: {self.controlling_value}, "
                f"Num Inputs: {len(self.inputs)}, Num Outputs: {len(self.outputs)})")
 
class DFlipFlop(Node):
    def __init__(self, node_number, node_type, value=0, level=0):
        # Initialize the parent Node class
        super().__init__(node_number=node_number, node_type=node_type,level=level, num_inputs=1, num_outputs=1)
        self.d = value  # D input
        self.q = value  # Q output
 
    def clock_edge(self):
        """Capture the value of D on the rising edge of the clock."""
        self.q = self.d
 
    def set_d(self, value):
        """Set the D input value."""
        self.d = value
 
    def get_q(self):
        """Get the Q output value."""
        return self.q
 
    def __repr__(self):
        return ( f"Node({self.node_number}, "
                f"Node({self.node_type},"
                f"Inputs: {self.inputs}, Outputs: {self.outputs}, "
                f"Num Inputs: {self.num_inputs}, Num Outputs: {self.num_outputs}, "
                f"Level: {self.level}, Inversion: {self.inversion_parity}, "
                f"Control: {self.controlling_value}, "
                f"Num Inputs: {len(self.inputs)}, Num Outputs: {len(self.outputs)})")
   
 
 
 
# Define global lists to store input, output, wires, and assign statements
wires = []
main_ip = []
main_op = []
assign = []
assignments_dict = {}
 
# Sample Verilog data (replace this with your data)
filename = 'dff.txt'  # Replace with your filename
 
with open(filename, 'r') as file:
    verilog_data = file.read()  
 
def parse_line(line):
    """Parse a single line and extract relevant tokens."""
    tokens = line.split()
    return tokens
 
def process_wires(tokens, wires):
    """Extract wire information."""
    if len(tokens) > 1:
        wire_name = tokens[1].strip(';')
        wires.append(wire_name)
 
def process_inputs(tokens, main_ip):
    """Extract input information."""
    if len(tokens) > 1:
        input_name = tokens[1].strip(';')
        main_ip.append(input_name)
 
def process_outputs(tokens, main_op):
    """Extract output information."""
    if len(tokens) > 1:
        output_name = tokens[1].strip(';')
        main_op.append(output_name)
 
def process_assignment(tokens, assign, assignments_dict):
    """Extract assignment information."""
    lhs = tokens[1].strip(';')
    rhs = tokens[3].strip(';')
    assign.append(f"{lhs} = {rhs}")
    assignments_dict[lhs] = rhs
 
 
# Step 1: Function to fetch input, output, wires, and assignments from the data
def fetch(data):
 
    for line in data.splitlines():
        tokens = parse_line(line)
        if not tokens:  # Skip empty lines
            continue
        if 'wire' in tokens:
            process_wires(tokens, wires)
        elif 'input' in tokens:
            process_inputs(tokens, main_ip)
        elif 'output' in tokens:
            process_outputs(tokens, main_op)
        elif 'assign' in tokens:
            process_assignment(tokens, assign, assignments_dict)
 
    return wires, main_ip, main_op, assign, assignments_dict
 
# Fetch the input, output, wire, and assignments
fetch(verilog_data)

# Step 1: Parsing port names and creating nodes
pattern = r"\.(\w+)\("
matches = re.findall(pattern, verilog_data)
unique_ports = set()
for match in matches:
    if match != 'Y' and match != 'Q' and match != 'QN': 
        unique_ports.add(match)
 
# Step 2: Parsing gate connections and creating nodes
pattern = r'(\w+)\s+(\w+)\s*\((.*?)\);'
matches = re.findall(pattern, verilog_data, re.DOTALL)
matches.pop(0)

# Initialize node list
node_list = {}
 
for match in matches:
    gate_type, gate_name, connections = match
    if gate_type == 'DFF':
        node = DFlipFlop(node_number=gate_name,node_type=gate_type)    
    else:
        node = Node(node_number=gate_name , node_type=gate_type)

    if gate_type == 'NOT' or gate_type == 'NOR' or gate_type == 'NAND':
        node.inversion_parity = True
 
    if gate_type == 'AND' or gate_type == 'NAND':
        node.controlling_value = 0
    elif gate_type == 'OR' or gate_type == 'NOR':
        node.controlling_value = 1
 
    connection_pattern = r'\.(\w+)\s*\((\w+)\)'
    connection_matches = re.findall(connection_pattern, connections)
   
    # Add inputs and outputs based on port names
    for port, var in connection_matches:
        if port in unique_ports:  
            node.add_input(var)
        elif port == 'Y' or port == 'Q' or port == 'QN':  
            node.add_output(var)
   
    node_list[gate_name] = node


 
# Step 3: Updating connections with assignment values
for node in node_list.values():
    # Update input and output connections if any variable is found in assignments_dict
    node.inputs = [assignments_dict.get(inp, inp) for inp in node.inputs]
    node.outputs = [assignments_dict.get(out, out) for out in node.outputs]

 
# Step 4: Populate inputs and outputs with references to other nodes where applicable
for node_name, node in node_list.items():
    # Replace input/output names with actual node references if they match node names
    node.inputs = [node_list.get(inp, inp) for inp in node.inputs]
    node.outputs = [node_list.get(out, out) for out in node.outputs]

# Step 5: Assign levels to nodes 
def levelize(node_list):
    # Initialize levels dictionary
    temp_nodes = node_list.copy()
    current_input = {input_name: 0 for input_name in main_ip}
 
    # Function to recursively assign levels to nodes
    def assign_levels(node, current_level):
        node.level = current_level  # Set the node's level
        temp_nodes.pop(node.node_number)  # Remove the node from temp_nodes
 
    # Assign levels starting from nodes with no inputs
    while temp_nodes:
        for node in list(temp_nodes.values()):  # Create a list to avoid mutation issues during iteration
            # Check if all of the node's inputs are in main_ip
            if all(inp in main_ip for inp in node.inputs):
                assign_levels(node, 0)  # Assign level 0 if all inputs are in main_ip
                current_input[node.outputs[0]] = 1
            elif all(inp in current_input for inp in node.inputs):
                # Get the levels of the node inputs from current_input
                input_levels = [current_input.get(inp, -1) for inp in node.inputs]
               
                # Assign the maximum level found, default to 0 if no inputs found
                if input_levels:  # If there are inputs
                    max_level = max(input_levels)
                    current_input[node.outputs[0]] = max_level + 1  # Update the current_input for the output
                    assign_levels(node, max_level)  # Assign the next level
                else:
                    # If no inputs, you can decide what to do, here we skip assigning
                    print(f"Node {node.node_number} has no inputs to assign levels.")
                    continue
 
levelize(node_list=node_list)
 
node_list2 = list(node_list.values())
sorted_nodes = sorted(node_list2, key=lambda node: node.level)
for node in sorted_nodes:
    print(node)
 
def calculate_gate_output(sorted_list, main_ip, main_op , i):
    results = main_ip.copy()
    for node in sorted_list:
        if node.node_type == 'DFF':
            temp_gate_name = node.node_type
            input = [None] * node.num_inputs
            clk = int(main_ip['clk'][i])
            if(type(results.get(node.inputs[1])) == str):
                d = int(results.get(node.inputs[1][0], None)[i])
            else:
                d = int(results.get(node.inputs[1], None))
            if clk == 1:
                node.set_d(d)
                node.clock_edge()
                results[node.outputs[0]] = int(node.get_q())
            else:
                results[node.outputs[0]] = int(node.get_q())
        # Print individual gate information
            print(f"\nGate Name: {node.node_type}")
            print(f"Input clk ({node.inputs[0]}): {clk}")
            print(f"Input D ({node.inputs[1]}): {d}")
            print(f"Output Q ({node.outputs[0]}): {results[node.outputs[0]]}")
        else:
            temp_gate_name = node.node_type
            input = [None] * node.num_inputs
            for j in range(node.num_inputs):
                input[j] = results.get(node.inputs[j], None)
                if(type(input[j]) == str):
                    input[j] = int(input[j][i])
            output = node.gate_function(input)
            results[node.outputs[0]] = output
   
            # Print individual gate information
            print(f"\nGate Name: {temp_gate_name}")
            for j in range(node.num_inputs):
                print(f"Input {j} ({node.inputs[j]}): {input[j]}")    
            print(f"Output Y ({node.outputs[0]}): {output}")
 
    print("\nFinal Outputs:")
    for output in main_op:
        # Use the assignments_dict to map the main_op to the actual wire that contains the result
        wire = assignments_dict.get(output, None)
        if wire and wire in results:
            final_output = results[wire]
        else:
            final_output = 'N/A'
        print(f"Output {output}: {final_output}")
 
# Map user inputs to main inputs
def get_input_values(main_ip):
    input_values = {}
    for ip in main_ip:
        if ip == "clk":  # Assuming 'clock' is the name of the clock input
            clock_signal = input("Enter the clock signal as a binary string (e.g., '0101010101010101'), or type 'STOP' to finish: ")
            clock_sequence = []
 
            while clock_signal != 'STOP':
                # Validate the input to ensure it's a binary string
                if not all(bit in '01' for bit in clock_signal):
                    print("Invalid input. Please enter a binary string (only 0s and 1s).")
                else:
                    clock_sequence.append(clock_signal)
 
                clock_signal = input("Enter the next clock signal (or type 'STOP' to finish): ")
 
            input_values[ip] = ''.join(clock_sequence)  # Combine all clock signals into a single string
        elif ip == "D":  # Assuming 'D' is the name of the D input
            def getd():
                D_signal = input("Enter the D signal as a binary string (e.g., '0101010101010101'), or type 'STOP' to finish: ")
                D_sequence = []
    
                while D_signal != 'STOP':
                    # Validate the input to ensure it's a binary string
                    if not all(bit in '01' for bit in D_signal):
                        print("Invalid input. Please enter a binary string (only 0s and 1s).")
                    else:
                        D_sequence.append(D_signal)
    
                    D_signal = input("Enter the next D signal (or type 'STOP' to finish): ")
                return D_sequence
            D_sequence = getd()
            if(len(D_sequence[0]) != len(input_values['clk'])):
                print("Length of D signal should be equal to clock signal\n")
                print("Please enter the D signal again")
                D_sequence = getd()               

            input_values[ip] = ''.join(D_sequence)  # Combine all clock signals into a single string
        else:
            val = int(input(f"Enter the value for {ip} (0 or 1): "))
            input_values[ip] = val
           
    return input_values
 
# Main execution
main_ip_values = get_input_values(main_ip)
print(main_ip_values)
 
if 'clk' not in main_ip_values:
    calculate_gate_output(sorted_nodes, main_ip_values, main_op , 0)
else:
    for i in range(len(main_ip_values['clk'])):
        calculate_gate_output(sorted_nodes, main_ip_values, main_op , i)