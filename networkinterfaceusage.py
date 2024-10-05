import os

# 4. Network Interface Usage
def get_network_interface_usage(pid):
    net_dev_path = f'/proc/{pid}/net/dev'

    if not os.path.exists(net_dev_path):
        return None  # Process does not exist or does not have net/dev info

    try:
        with open(net_dev_path, 'r') as file:
            lines = file.readlines()

        # Skip the first two lines (header)
        data = {}
        for line in lines[2:]:
            # Split the line into interface name and stats
            parts = line.split(':')
            if len(parts) > 1:
                interface = parts[0].strip()
                stats = parts[1].strip().split()

                # Convert bytes sent and received to integers
                errorpackets = int(stats[2]) if len(stats) > 2 else 0
                dropped_received = int(stats[3]) if len(stats) > 3 else 0
                errors_transmitted = int(stats[10]) if len(stats) > 10 else 0
                dropped_transmitted = int(stats[11]) if len(stats) > 11 else 0

                data[interface] = {
                    "errors_received": errorpackets,
                    "dropped_received": dropped_received,
                    "errors_transmitted": errors_transmitted,
                    "dropped_transmitted": dropped_transmitted
                }

        return data

    except Exception as e:
        print(f"Error reading network stats for PID {pid}: {e}")
        return None