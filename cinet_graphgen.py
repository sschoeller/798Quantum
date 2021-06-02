'''
Python code to translate CI-net specs into induced preference graphs,
as lists of lists of variables.

Translated from Java by Zach Oster
for Scott Schoeller's COMPSCI 798 (quantum computing) final project

Workflow:
1) Ingest the CI-net spec, with format:

VARIABLES
v1,v2,v3,v4
PREFERENCES
{d};{}:{b};{c}
{b};{a}:{c};{d}
{};{a}:{b,d};{c}
{a};{c}:{b};{d}
{a};{c}:{d};{b}

2) Ground the CI-net to create a UI-net (all preferences are unconditional)

3) Translate the CI-net into a preference graph. The algorithm that Scott is
using is Grover's algorithm, which takes lists-of-lists as input. If each
distinct set of variables is represented as its own string, then the PG can be
represented as a list of 2-lists of strings.

4) Scott writes code to feed the resulting preference graph into Grover's
algorithm to decide whether the CI-net is consistent
'''

import sys
import os
import itertools

# 1. Ingest the CI-net spec:
#   a. Open file
#   b. Create the list of variables
#   c. Create the list of statements
#
# Returns a CINet, which is a list that contains at [0] a list of the variables
# in the CINet and at [1] a list of 4-lists of strings representing statements.
def getCINet(cinet_file_path):
    cinet = [[], []]
    with open(cinet_file_path) as f:
        f.readline() # ignore "VARIABLES" label
        cinet[0] = f.readline().rstrip('\n').split(',') # read in variables
        #print('variables are:', str(cinet[0]))
        f.readline() # ignore "PREFERENCES" label
        cinet[1] = []
        ci_stmt_line = f.readline()
        while ci_stmt_line != '':
            # split into conditions and preferences
            ci_stmt_halves = ci_stmt_line.rstrip('\n').split(':')
            ci_stmt_cond = ci_stmt_halves[0].split(';')
            ci_stmt_pref = ci_stmt_halves[1].split(';')

            # reassemble into a CI-statement
            ci_stmt = [ci_stmt_cond[0].lstrip('{').rstrip('}'),
                       ci_stmt_cond[1].lstrip('{').rstrip('}'),
                       ci_stmt_pref[0].lstrip('{').rstrip('}'),
                       ci_stmt_pref[1].lstrip('{').rstrip('}')]

            # add CI-statement to the list
            cinet[1].append(ci_stmt)
            #print('read CI-statement:', str(ci_stmt))

            # read next line of input file
            ci_stmt_line = f.readline()

    return cinet
            

# 2. Ground the CI-net to create a UI-net (all preferences are unconditional).
# Output: a simplified CI-net, as a 2-list where [0] is the list of variables
# and [1] is a list of 2-lists denoting grounded unconditional preferences.
def ground(cinet):
    variables = cinet[0]
    statements = cinet[1]
    grounded_cinet = [variables, []]

    for stmt in statements:
        # find the set of variables not appearing in this statement
        # (NOTE: we're just using substring checks to find variables appearing
        #  in each CI-statement, so this won't work correctly if any variable's
        #  name is a substring of any other variable's name)
        unusedVars = []
        for var in variables:
            varFound = False
            for part in stmt:
                if var in part:
                    varFound = True
                    break
            if not varFound:
                unusedVars.append(var)

        ##print('---> processing', str(stmt))
        ##print('      using unusedVars =', str(unusedVars))
                
        # generate new CI-net statement for each subset of the unused variables
        unusedVarsPowerset = powerset(unusedVars)
        betterSet = []
        worseSet = []
        for unusedVarSet in unusedVarsPowerset:
            betterSet = ','.join([stmt[0], stmt[2], ','.join(unusedVarSet)]).rstrip(',').lstrip(',')
            worseSet = ','.join([stmt[0], stmt[3], ','.join(unusedVarSet)]).rstrip(',').lstrip(',')
            grounded_cinet[1].append([betterSet, worseSet])        
        
    return grounded_cinet

# 3. Translate the CI-net into a preference graph, represented as a list of
#    2-lists of strings, where each string contains all variables for that node
#    of the preference graph
def make_prefgraph(grounded_cinet):
    variables = grounded_cinet[0]
    statements = grounded_cinet[1]

    # 1. Create empty lists of nodes and edges
    nodes = []
    edges = []
    
    # 2. Construct nodes: powerset of CI-net variables
    varPowerset = powerset(variables)
    for varSet in varPowerset:
            nodes.append(','.join(varSet).rstrip(',').lstrip(','))

    #print('preference graph nodes:', str(nodes))

    # 3. Create monotonicity edges (in an ugly, inefficient way)
    for start_node in nodes:
        shouldCreateEdge = True
        node_vars = start_node
        for other_node in nodes:
            if start_node == other_node:
                shouldCreateEdge = False  # avoid self-loop edges
            else:
                # Check other_node to see if it contains every variable in
                # start_node. If so, create edge from start_node to other_node.
                for node_var in node_vars:
                    if not (node_var in other_node):
                        shouldCreateEdge = False
                        break

            if shouldCreateEdge:
                edges.append([start_node, other_node])

            # Reset edge creation flag
            shouldCreateEdge = True

    #print("--- Monotonicity edges only ---")
    #print(edges)
    #print("--- End monotonicity edges ---")
    #print()

    # 4. For each grounded CI-net statement, add an edge from the
    # less-preferred variable set to the more-preferred variable set
    # (this reverses the order of the preference statements, which have the
    # more-preferred variable set first)
    for stmt in statements:
        if not ([stmt[1], stmt[0]] in edges):
            edges.append([stmt[1], stmt[0]])

    return [nodes, edges]

# powerset function created using the recipe at:
# https://docs.python.org/3/library/itertools.html?highlight=powerset
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r)
                                         for r in range(len(s)+1))

# Main preference-graph-converter function
def convert_to_preference_graph(cinet_file_path):
    cinet = getCINet(cinet_file_path)
    #print("--- Original CI-net ---")
    #print(cinet)

    grounded_cinet = ground(cinet)
    #print()
    #print("--- Grounded CI-net ---")
    #print(grounded_cinet)                                

    prefgraph = make_prefgraph(grounded_cinet)
    return prefgraph

# main program
#prefgraph = convert_to_preference_graph('./current.cinet')
#
### comment out these lines if you don't want the debugging output
#print("--- Preference graph nodes ---")
#print(prefgraph[0])
#print("--- Preference graph edges ---")
#print(prefgraph[1])
# end of main program
