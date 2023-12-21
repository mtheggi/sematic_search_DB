import struct
import random

class Serial(object):
    def __init__(self, node):
        if node is None:
            return
        self.data = node.data
        self.left_id = node.left_id
        self.right_id = node.right_id
        self.node_id = node.node_id
        self.sel_axis = node.sel_axis

    def pack(self,dimensions):
        data_format = '!' + 'f' * dimensions + 'IIdI'
        return struct.pack(data_format, *self.data, self.node_id, self.left_id, self.right_id, self.sel_axis)

    def open_file(self, filename):
        return open(filename, 'rb+')

    def save_node(self, dimensions,filename):
        with self.open_file(filename) as file:
            file.seek(0, 2)  # Move to the end of the file
            offset = file.tell()
            file.write(self.pack(dimensions))
        return offset
    def save_nodes_batch(self, dimensions, filename, nodes):
        with self.open_file(filename) as file:
            file.seek(0, 2)  # Move to the end of the file
            offset = file.tell()

            # Pack all nodes into a single byte string
            data_format = '!' + 'f' * dimensions + 'IIdI'
            packed_data = b''.join([struct.pack(data_format, *node.data, node.node_id, node.left_id, node.right_id, node.sel_axis) for node in nodes])

            # Write the packed data to the file
            file.write(packed_data)

        return offset

class deserialize(object):
    def open_file(self, filename):
        return open(filename, 'rb+')
     
    def unpack(self, dimensions, data):
        data_format = '!' + 'f' * dimensions + 'IIdI'
        values = struct.unpack(data_format, data)
        self.data = list(values[:-4])
        self.node_id, self.left_id, self.right_id, self.sel_axis = values[-4:]

    def load_node(self, filename, offset, dimensions):
        data_format = '!' + 'f' * dimensions + 'IIdI'
        with self.open_file(filename) as file:
            file.seek(offset)
            data = file.read(struct.calcsize(data_format))
            self.unpack(dimensions,data)

# class Node:
#     def __init__(self, data, left_id, right_id, node_id, sel_axis):
#         self.data = data
#         self.left_id = left_id
#         self.right_id = right_id
#         self.node_id = node_id
#         self.sel_axis = sel_axis

# # Test the Serial and deserialize classes
# node = Node([1.0, 2.0, 3.0], 10, 20, 30, 0)
# dimensions = len(node.data)

# # Serialize the node and save to a file
# serializer = Serial(node)
# filename = "serialized_data.bin"
# offset = serializer.save_node(dimensions,filename)
# print(f"Node serialized and saved at offset: {offset}")

# # Deserialize the node from the file
# deserializer = deserialize()
# deserializer.load_node(filename, offset, dimensions)
# print("Node deserialized:")
# print(f"Data: {deserializer.data}")
# print(f"Left ID: {deserializer.left_id}")
# print(f"Right ID: {deserializer.right_id}")
# print(f"Node ID: {deserializer.node_id}")
# print(f"Selected Axis: {deserializer.sel_axis}")

# def print_serialized_file_content(filename, dimensions):
#     data_format = '!' + 'f' * dimensions + 'IIdI'
#     struct_size = struct.calcsize(data_format)

#     with open(filename, 'rb') as file:
#         while True:
#             data = file.read(struct_size)
#             if not data:
#                 break
#             values = struct.unpack(data_format, data)
#             print(f"Data: {list(values[:-4])}")
#             print(f"Left ID: {values[-4]}")
#             print(f"Right ID: {values[-3]}")
#             print(f"Node ID: {values[-2]}")
#             print(f"Selected Axis: {values[-1]}")
#             print()

# # Example usage
# filename = "serialized_data.bin"
# print_serialized_file_content(filename, dimensions)
            
class Node:
    def __init__(self, dimensions):
        self.data = [random.uniform(0, 1) for _ in range(dimensions)]
        self.left_id = random.randint(1, 100)
        self.right_id = random.randint(1, 100)
        self.node_id = random.randint(1, 100)
        self.sel_axis = random.randint(0, dimensions - 1)

# def generate_and_save_nodes(num_nodes, dimensions, filename):
#     for _ in range(num_nodes):
#         node = Node(dimensions)
#         serializer = Serial(node)
#         serializer.save_node(dimensions,filename)

def generate_and_save_nodes_batch(num_nodes, dimensions, filename, batch_size=1000):
    serializer = Serial(None)
    nodes = []

    for _ in range(num_nodes):
        node = Node(dimensions)
        nodes.append(node)

        if len(nodes) == batch_size:
            # Save nodes in batches
            offset = serializer.save_nodes_batch(dimensions, filename, nodes)
            print(f"Batch of {batch_size} nodes saved at offset: {offset}")
            nodes = []

    # Save any remaining nodes
    if nodes:
        offset = serializer.save_nodes_batch(dimensions, filename, nodes)
        print(f"Remaining nodes saved at offset: {offset}")

num_nodes = 1000000
dimensions = 70
filename = "serialized_data.bin"
generate_and_save_nodes_batch(num_nodes, dimensions, filename)
