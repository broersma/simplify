# -*- coding: utf8 -*-
import sys
import re
import networkx as nx


def parse_input(input, name_pattern, money_pattern):
	for match in re.findall(name_pattern + r'.*?' + name_pattern + r'.*?' + money_pattern, input):
		yield tuple(match[:2]) + (int(''.join(match[2:])),)

def format_money(cents):
	sign = "-" if cents < 0 else ""
	cents = abs(cents)
	return "{}{},{:02}".format(sign, int(cents / 100), cents % 100)

def optimal_flow_graph(G):
	flow_dict = nx.network_simplex(G)[1]
	H = nx.DiGraph()
	for a in flow_dict:
		for b in flow_dict[a]:
			if flow_dict[a][b] > 0:
				H.add_edge(a, b, amount=flow_dict[a][b])
	return H

def balance(G, node, amount='amount'):
	return G.in_degree(node, amount) - G.out_degree(node, amount)
	
def simplify(input, print_format, name_pattern, money_pattern):
	# Create a graph G representing the debt/credit from input.
	G=nx.DiGraph()
	for creditor, borrower, amount in parse_input(input, name_pattern, money_pattern):
		G.add_edge(creditor, borrower, amount=amount)
	
	# Return if no correct input could be found.
	if not G:
		return

	# Remodel the graph as a flow network by setting the demand attribute for each node.
	for name in G.nodes():
		G.node[name]['demand'] = balance(G, name)

	# Ensure no-one pays more than their total debt by limiting the capacity.
	if True:
		for creditor, borrower in G.edges():
			G[creditor][borrower]['capacity'] = G.in_degree(borrower,'amount')

	# Get the optimal flow graph H.
	H = optimal_flow_graph(G)

	# Print the new list of transactions.
	for creditor, borrower, data in H.edges(data=True):
		if data:
			yield print_format.format(creditor, borrower, format_money(data['amount']))

	# Check for any subtle changes in total debt/credit.
	# TODO not sure if this is necessary anymore, maybe make it (part of) a doctest
	for name in G.nodes():
		if name in H.nodes():
			difference = balance(H, name) - balance(G, name)
			assert difference == 0, name + " has a difference: " + format_money(difference)
			
if __name__ == "__main__":
	name_pattern = r'((?:[A-Z][a-z-]+)+)'
	money_pattern = r'(\d+)[,\.](\d\d)'
	
	# Get input and parse printing format by looking at the first line of the input.
	input_lines = sys.stdin.readlines()
	print_format = re.sub(name_pattern + r'|' + money_pattern, '{}', input_lines[0]).decode('utf8').strip()
	input = "".join(input_lines)

	if input:
		for output in simplify(input, print_format, name_pattern, money_pattern):
			print output