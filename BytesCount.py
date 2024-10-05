import os

# 1. Bytes Sent and Received
def get_network_io(pid):
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
                bytes_received = int(stats[0]) if len(stats) > 0 else 0
                bytes_sent = int(stats[8]) if len(stats) > 8 else 0

                data[interface] = {
                    "bytes_received": bytes_received,
                    "bytes_sent": bytes_sent
                }

        return data

    except Exception as e:
        print(f"Error reading network stats for PID {pid}: {e}")
        return None