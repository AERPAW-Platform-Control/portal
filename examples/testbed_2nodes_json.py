import json

node1 = {}
node1['name'] = "node1"
node1['hardware_type'] = "FixedNode"
node1['component_id'] = "CC1"

node2 = {}
node2['name'] = "node2"
node2['hardware_type'] = "FixedNode"
node2['component_id'] = "CC2"

nodes = []
nodes.append(node1)
nodes.append(node2)

print(json.dumps(nodes))