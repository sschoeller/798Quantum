# Scott Schoeller (sschoellerSTEM)
from random import *
import numpy as np
from qiskit import IBMQ, execute
from qiskit import QuantumCircuit
from qiskit.circuit import quantumcircuit
from qiskit.circuit.classicalregister import ClassicalRegister
from qiskit.circuit.library import GroverOperator
from qiskit import algorithms
from qiskit.algorithms.amplitude_amplifiers.grover import GroverResult
import cinet_graphgen # Dr. Oster's script for creating a preference graph


IBMQ.load_account()
qc = QuantumCircuit(15) # Create circuit with 15 qubits

# Graph as an adj. List
A = cinet_graphgen.convert_to_preference_graph("./current.cinet")
print(A[0])
V  = []
bitCtr = 0x0

i = 0
for e in A[0]:
    if e == 0:
        continue
    # set "bits" accordingly
    if 'v0' in e or 'v0,' in e:
        bitCtr = bitCtr | 1
    if 'v1' in e or ',v1,' in e:
        bitCtr = bitCtr | 2
    if 'v2' in e or ',v2,' in e:
        bitCtr = bitCtr | 4
    if 'v3' in e or ',v3' in e:
        bitCtr = bitCtr | 8
    V.append(bitCtr)    
    bitCtr = 0x0
    i += 1

# Quantum Triangle Algorithm No. 3 from J.  Cirasella's Thesis
print(V)
# fill in quantum circuit here.
Q = [ ]
for l in range(0,15):
    Q.append(0)

for i in range(0,4):
    num = V[i]
    if num % 2 == 1: # odd number
        # set "1" qubit
        Q[0] = 1
    if num == 2:
        # set "2" qubit
        Q[1] = 1
    if num == 4:
        Q[2] = 1
    if num == 8:
        Q[3] = 1

for i in range(4,8):
    num = V[i]
    if num % 2 == 1: # odd number
        # set "" qubit
        Q[4] = 1
    if num == 2:
        # set "" qubit
        Q[5] = 1
    if num == 4:
        Q[6] = 1
    if num == 8:
        Q[7] = 1

for i in range(8,12):
    num = V[i]
    if num % 2 == 1: # odd number
        # set "" qubit
        Q[8] = 1
    if num == 2:
        # set "" qubit
        Q[9] = 1
    if num == 4:
        Q[10] = 1
    if num == 8:
        Q[11] = 1

for i in range(12,len(V)):
    num = V[i]
    if num % 2 == 1: # odd number
        # set "" qubit
        Q[12] = 1
    if num == 2:
        # set "" qubit
        Q[13] = 1
    if num == 4:
        Q[14] = 1
    if num == 8:
        Q[15] = 1

#u = randint(0, len(V)) # random vertex u
# Query all elements, make a list T
#T = V

#v = randint(0, len(T)) # random vertex in T

# Create quantum circuit using T

cr = ClassicalRegister(15)
k = 0
for bit in range(1, len(Q)):
    if Q[k] == 1:
        qc.x(bit, Q[k])
    k += 1

# Run Grover (built-in)
g = GroverOperator(qc)

# AA (built-in)
# Run AA over the results from Grover
amp1 = algorithms.AmplificationProblem(oracle=qc, grover_operator=g)

# Run again
amp2 = algorithms.AmplificationProblem(amp1)

qc.measure_all(amp2)
qc.draw()

# Use IBM's qasm_simulator
provider =  IBMQ.get_provider()
simulator = provider.get_backend('ibmq_qasm_simulator')
machine = provider.get_backend('ibmq_16_melbourne')

# Execute the circuit
job = execute(qc, machine, shots=1000)

# Grab results from the job
result = job.result()

# Return counts
counts = result.get_counts(qc)

# END
