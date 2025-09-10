# chord_network_full.py

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.successor = None
        self.keys = {}  # Lưu key-value

    def __str__(self):
        return f"Node({self.id})"

class ChordNetwork:
    def __init__(self):
        self.nodes = []

    # ===== Thêm node =====
    def add_node(self, node_id):
        new_node = Node(node_id)
        self.nodes.append(new_node)
        self.nodes.sort(key=lambda n: n.id)
        self.update_successors()
        self.redistribute_keys()
        return new_node

    # ===== Xóa node =====
    def remove_node(self, node_id):
        node = self.get_node(node_id)
        if node:
            # Chuyển key của node này sang successor
            for k, v in node.keys.items():
                node.successor.keys[k] = v
            # Xóa node
            self.nodes.remove(node)
            self.update_successors()
            self.redistribute_keys()

    # ===== Helper =====
    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    # Cập nhật successor
    def update_successors(self):
        n = len(self.nodes)
        for i, node in enumerate(self.nodes):
            node.successor = self.nodes[(i + 1) % n]

    # Chèn key
    def insert_key(self, key, value):
        for node in self.nodes:
            if node.id >= key:
                node.keys[key] = value
                return node
        self.nodes[0].keys[key] = value
        return self.nodes[0]

    # Phân phối lại key sau thêm/xóa node
    def redistribute_keys(self):
        all_keys = {}
        for node in self.nodes:
            all_keys.update(node.keys)
            node.keys.clear()
        for k, v in all_keys.items():
            self.insert_key(k, v)

    # Hiển thị trạng thái mạng
    def print_nodes(self):
        for node in self.nodes:
            print(f"Node {node.id} -> Successor {node.successor.id}, Keys: {list(node.keys.keys())}")


# ===== TEST CASE =====
if __name__ == "__main__":
    chord = ChordNetwork()

    # 1. Thêm node [1,5,9,12]
    for n_id in [1,5,9,12]:
        chord.add_node(n_id)
    print("Mạng sau khi thêm node:")
    chord.print_nodes()

    # 2. Chèn key {2:'A',7:'B',10:'C',14:'D'}
    keys = {2:'A', 7:'B', 10:'C', 14:'D'}
    for k, v in keys.items():
        node = chord.insert_key(k, v)
        print(f"Insert key {k} vào Node {node.id}")

    print("\nMạng sau khi insert key:")
    chord.print_nodes()

    chord.remove_node(9)
    print("\nMạng sau khi xóa node 9:")
    chord.print_nodes()

    chord.add_node(6)
    print("\nMạng sau khi thêm node 6:")
    chord.print_nodes()
