# chord_network.py

class Node:
    def __init__(self, node_id, m):
        self.id = node_id
        self.m = m
        self.finger_table = [None] * m
        self.successor = None
        self.keys = {}  # lưu key-value

    def __str__(self):
        return f"Node({self.id})"

class ChordNetwork:
    def __init__(self, m):
        self.m = m
        self.nodes = []

    def add_node(self, node_id):
        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)
        self.nodes.sort(key=lambda n: n.id)
        self.update_successors()
        self.update_finger_tables()
        self.migrate_keys()
        return new_node

    def remove_node(self, node_id):
        node = self.get_node(node_id)
        if node:
            # chuyển key sang successor
            for k, v in node.keys.items():
                node.successor.keys[k] = v
            self.nodes.remove(node)
            self.update_successors()
            self.update_finger_tables()

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def update_successors(self):
        n = len(self.nodes)
        for i, node in enumerate(self.nodes):
            node.successor = self.nodes[(i+1)%n]

    def update_finger_tables(self):
        N = 2 ** self.m
        for node in self.nodes:
            for i in range(self.m):
                start = (node.id + 2**i) % N
                node.finger_table[i] = self.find_successor(start)

    def find_successor(self, key):
        for node in self.nodes:
            if node.id >= key:
                return node
        return self.nodes[0]  # quay vòng

    def insert_key(self, key, value):
        node = self.find_successor(key)
        node.keys[key] = value
        return node

    def lookup_key(self, start_node_id, key):
        path = []
        node = self.get_node(start_node_id)
        while True:
            path.append(node.id)
            if key in node.keys:
                return node, path
            # đi tới finger gần nhất <= key
            next_node = None
            for i in reversed(range(self.m)):
                finger = node.finger_table[i]
                if finger.id <= key and finger.id != node.id:
                    next_node = finger
                    break
            if not next_node:
                next_node = node.successor
            if next_node == node:
                return None, path
            node = next_node

    def migrate_keys(self):
        # đơn giản: đảm bảo node nhận key thuộc về nó
        for node in self.nodes:
            succ = node.successor
            keys_to_move = {}
            for k, v in succ.keys.items():
                if node.id >= k or node.id < succ.id:
                    keys_to_move[k] = v
            for k in keys_to_move:
                node.keys[k] = keys_to_move[k]
                del succ.keys[k]

    def print_nodes(self):
        for node in self.nodes:
            print(f"Node {node.id} -> Successor {node.successor.id}, Keys: {list(node.keys.keys())}")

# ===== TEST CASE =====
if __name__ == "__main__":
    chord = ChordNetwork(m=4)
    # thêm node
    chord.add_node(1)
    chord.add_node(5)
    chord.add_node(9)
    chord.add_node(12)
    print("Mạng sau khi thêm node:")
    chord.print_nodes()

    # insert key
    keys = {2:'A', 7:'B', 10:'C', 14:'D'}
    for k, v in keys.items():
        node = chord.insert_key(k, v)
        print(f"Insert key {k} vào Node {node.id}")

    print("\nMạng sau khi insert key:")
    chord.print_nodes()

    # lookup key
    key_to_lookup = 10
    start_node = 1
    node, path = chord.lookup_key(start_node, key_to_lookup)
    print(f"\nLookup key {key_to_lookup} từ node {start_node}:")
    print(f"Đường đi: {path}, Tìm thấy tại node {node.id}")

    # node join
    chord.add_node(6)
    print("\nMạng sau khi node 6 join:")
    chord.print_nodes()

    # node leave
    chord.remove_node(5)
    print("\nMạng sau khi node 5 leave:")
    chord.print_nodes()
