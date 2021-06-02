from random import *
import numpy as np
from qiskit import IBMQ, execute
from qiskit import QuantumCircuit
from qiskit.circuit import quantumcircuit
from qiskit.circuit.library import GroverOperator
from qiskit import algorithms
from qiskit.algorithms.amplitude_amplifiers.grover import GroverResult
import cinet_graphgen # Dr. Oster's script for creating a preference graph


#IBMQ.load_account()
#qc = QuantumCircuit(5) # Create circuit with 5 qubits

# Graph as an adj. List
A = cinet_graphgen.convert_to_preference_graph("cinet.txt")
print(A[0])
V  = []
P = "(a|b|c|d|,)^*"
j = 1 # multiple
bitCtr = 0x0

i = 0
for e in A[0]:
    # set "bits" accordingly
    if 'a' in e or 'a,' in e:
        bitCtr = bitCtr | 1
    if 'b' in e or ',b,' in e:
        bitCtr = bitCtr | 2
    if 'c' in e or ',c,' in e:
        bitCtr = bitCtr | 4
    if 'd' in e or ',d' in e:
        bitCtr = bitCtr | 8
    V.append(bitCtr)    
    bitCtr = 0x0
    i += 1

# Quantum Triangle Algorithm No. 3 from J.  Cirasella's Thesis
print(V)
# fill in quantum circuit here.
#u = randint(0, len(V)) # random vertex u
# Query all elements, make a list T
T = V

v = randint(0, len(T)) # random vertex in T

# Create quantum circuit using V

# Run Grover (built-in)
#g = GroverOperator()
# AA (built-in)
# Run AA over the results from Grover
#gResults = algorithms.AmplificationProblem(g)

# Run again
#results = algorithms.AmplificationProblem(gResults)

#qc.measure_all()
#qc.draw()

# Use IBM's qasm_simulator
#provider =  IBMQ.get_provider()
#simulator = provider.get_backend('ibmq_qasm_simulator')
#machine = provider.get_backend('ibmq_16_melbourne')

# Execute the circuit on the qasm simulator
#job = execute(qc, simulator, shots=1000)

# Grab results from the job
#result = job.result()

# Return counts
#counts = result.get_counts(qc)

# END
