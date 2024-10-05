import os

# 3. Active UDP Connections
def get_active_udp_connections(pid):
    net_udp_path = f'/proc/{pid}/net/udp'

    if not os.path.exists(net_udp_path):
        return None  # Process does not exist or does not have net/tcp info

    try:
        with open(net_udp_path, 'r') as file:
            lines = file.readlines()

        connections = []

        # Skip the first line (header)
        for line in lines[1:]:
            parts = line.split()

            if len(parts) >= 10:
                local_address = parts[1]
                remote_address = parts[2]
                state = parts[3]
                pid_inode = parts[9]

                # Format addresses for readability
                local_ip, local_port = format_address(local_address)
                remote_ip, remote_port = format_address(remote_address)

                # Translate the TCP state from hex to readable form
                state_name = tcp_state(state)

                connections.append({
                    "local_ip": local_ip,
                    "local_port": local_port,
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "state": state_name,
                    "pid_inode": pid_inode
                })

        return connections

    except Exception as e:
        print(f"Error reading TCP connections for PID {pid}: {e}")
        return None


def format_address(address):
    """Convert raw hex IP:port to readable format."""
    ip_port = address.split(':')
    if len(ip_port) != 2:
        return None, None

    # Convert the hex IP to dotted-decimal notation
    ip = format_ip(ip_port[0])
    # Convert the hex port to decimal
    port = int(ip_port[1], 16)

    return ip, port


def format_ip(hex_ip):
    """Convert a hex IP to dotted-decimal format."""
    hex_ip = hex_ip.zfill(8)
    ip_parts = [str(int(hex_ip[i:i+2], 16)) for i in range(0, 8, 2)]
    return '.'.join(ip_parts[::-1])


def tcp_state(state_hex):
    """Convert hex TCP state to human-readable form."""
    states = {
        '01': 'ESTABLISHED',
        '02': 'SYN_SENT',
        '03': 'SYN_RECV',
        '04': 'FIN_WAIT1',
        '05': 'FIN_WAIT2',
        '06': 'TIME_WAIT',
        '07': 'CLOSE',
        '08': 'CLOSE_WAIT',
        '09': 'LAST_ACK',
        '0A': 'LISTEN',
        '0B': 'CLOSING'
    }
    return states.get(state_hex, 'UNKNOWN')