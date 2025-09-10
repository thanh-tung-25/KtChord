from ktchord import ChordNetwork

if __name__ == "__main__":
    net = ChordNetwork(m=5, replication=2)
    for nid in [3, 10, 20, 27]:
        net.add_node(nid)

    # Insert dữ liệu
    print("=== Insert dữ liệu với replication ===")
    for k, v in {5: "A", 12: "B", 25: "C", 30: "D"}.items():
        nodes = net.nodes[0].store_key(k, v)
        print(f"Key {k}:{v} lưu tại {[n.id for n in nodes]}")

    net.print_data_distribution()
    net.print_statistics()

    # Lookup với routing mô phỏng
    print("=== Lookup đường đi ===")
    path, node = net.nodes[0].route_lookup(net.nodes[0], 25)
    print(f"Tìm key 25 qua đường đi {path}, đến Node {node.id}")

    # Node join
    print("\n=== Node mới join ===")
    net.add_node(15)
    net.print_data_distribution()
    net.print_statistics()

    # Node leave
    print("\n=== Node leave ===")
    net.remove_node(10)
    net.print_data_distribution()
    net.print_statistics()

    # Visualization (chỉ in ra)
    net.visualize()
