class Node:
    def __init__(self, node_id, m, replication=2):
        self.id = node_id
        self.m = m
        self.max_id = 2 ** m
        self.fingers = []
        self.network = None
        self.data = {}
        self.replication = replication

    def set_network(self, network):
        self.network = network

    def build_fingers(self):
        """Xây dựng finger table"""
        self.fingers.clear()
        for i in range(self.m):
            start = (self.id + 2**i) % self.max_id
            succ = self.network.find_successor(start)
            self.fingers.append((start, succ.id))

    def find_successor(self, key):
        """Tìm successor gần nhất cho key"""
        sorted_nodes = sorted(self.network.nodes, key=lambda n: n.id)
        for node in sorted_nodes:
            if node.id >= key:
                return node
        return sorted_nodes[0]

    def store_key(self, key, value):
        """Lưu dữ liệu với replication"""
        main_node = self.find_successor(key)
        nodes = self.network.get_successor_list(main_node, self.replication)
        for n in nodes:
            n.data[key] = value
        return nodes

    def find_key(self, key):
        """Tra cứu key"""
        for n in self.network.nodes:
            if key in n.data:
                return n.data[key], n
        return None, None

    def migrate_keys(self):
        """Khi node join: lấy lại key thuộc về node mới"""
        succ = self.find_successor((self.id + 1) % self.max_id)
        keys_to_move = [k for k in succ.data if self.id >= k or (self.id < succ.id and k <= self.id)]
        for k in keys_to_move:
            self.data[k] = succ.data.pop(k)

    def route_lookup(self, start_node, key):
        """Mô phỏng đường đi lookup"""
        path = [start_node.id]
        current = start_node
        while True:
            succ = current.find_successor(key)
            if succ.id == current.id:
                return path, succ
            path.append(succ.id)
            if succ.id >= key or succ.id == self.network.nodes[0].id:
                return path, succ
            current = succ


class ChordNetwork:
    def __init__(self, m, replication=2):
        self.m = m
        self.nodes = []
        self.replication = replication

    def add_node(self, node_id):
        """Thêm node mới vào vòng"""
        node = Node(node_id, self.m, self.replication)
        self.nodes.append(node)
        for n in self.nodes:
            n.set_network(self)
        self.stabilize()
        node.migrate_keys()  # lấy lại dữ liệu thuộc về node mới
        return node

    def remove_node(self, node_id):
        """Xóa node và chuyển dữ liệu cho successor"""
        node = next((n for n in self.nodes if n.id == node_id), None)
        if not node:
            return
        succ = node.find_successor((node.id + 1) % node.max_id)
        for k, v in node.data.items():
            succ.data[k] = v
        self.nodes.remove(node)
        self.stabilize()

    def get_successor_list(self, node, count):
        """Trả về danh sách successor"""
        sorted_nodes = sorted(self.nodes, key=lambda n: n.id)
        idx = sorted_nodes.index(node)
        result = []
        for i in range(count):
            result.append(sorted_nodes[(idx + i) % len(sorted_nodes)])
        return result

    def find_successor(self, key):
        if not self.nodes:
            return None
        return self.nodes[0].find_successor(key)

    def stabilize(self):
        """Cập nhật finger table cho toàn mạng"""
        for n in self.nodes:
            n.build_fingers()

    def print_data_distribution(self):
        print("=== Phân phối dữ liệu ===")
        for node in sorted(self.nodes, key=lambda n: n.id):
            print(f"Node {node.id}: {node.data}")
        print()

    def print_statistics(self):
        """Thống kê hệ thống"""
        print("=== Statistics ===")
        print(f"Tổng số node: {len(self.nodes)}")
        total_keys = sum(len(n.data) for n in self.nodes)
        print(f"Tổng số key: {total_keys}")
        for n in sorted(self.nodes, key=lambda n: n.id):
            print(f"Node {n.id} giữ {len(n.data)} key")
        print()

    def visualize(self):
        """Bỏ phần vẽ, chỉ in danh sách node"""
        print("=== Nodes trong mạng Chord ===")
        for n in sorted(self.nodes, key=lambda n: n.id):
            print(f"- Node {n.id}")
        print()
