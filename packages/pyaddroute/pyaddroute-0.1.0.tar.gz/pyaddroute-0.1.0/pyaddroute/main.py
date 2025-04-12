import FreeSimpleGUI as sg
import subprocess
import re
from loguru import logger

def get_network_interfaces():
    """Get list of network interfaces with their IPs, names, and IDs"""
    try:
        # Get interface names and indices
        output = subprocess.check_output(["netsh", "interface", "ip", "show", "interfaces"]).decode()
        interfaces_by_idx = {}
        for line in output.splitlines():
            if "connected" in line.lower() or "disconnected" in line.lower():
                parts = line.split()
                if len(parts) > 4:
                    idx = parts[0]
                    name = " ".join(parts[4:])
                    interfaces_by_idx[idx] = {'name': name, 'idx': idx}

        # Get IP addresses for each interface
        output = subprocess.check_output(["netsh", "interface", "ip", "show", "address"]).decode()
        current_interface = None
        interfaces_by_ip = {}
        interfaces_by_name = {}
        
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Configuration for interface"):
                current_interface = line.split('"')[1]
            elif line.startswith("IP Address:"):
                ip = line.split(":")[1].strip()
                for idx, info in interfaces_by_idx.items():
                    if info['name'] == current_interface:
                        interfaces_by_ip[ip] = info['name']
                        interfaces_by_name[info['name']] = {'ip': ip, 'idx': idx}
                        break
        
        return interfaces_by_ip, interfaces_by_name
    except Exception as e:
        sg.popup_error(f"Error getting interfaces with command 'netsh interface ip show interfaces': {str(e)}\nCommand: netsh interface ip show interfaces")
        return {}, {}

def get_current_routes():
    """Get current routing table from Windows using route print command"""
    try:
        output = subprocess.check_output(["route", "print"]).decode()
        routes = []
        start_parsing = False
        
        for line in output.splitlines():
            if "IPv4 Route Table" in line:
                start_parsing = True
                continue
            if "Active Routes" in line:
                continue
            if start_parsing and line.strip() and not line.startswith("="):
                parts = line.split()
                if len(parts) >= 5 and re.match(r"\d+\.\d+\.\d+\.\d+", parts[0]):
                    routes.append({
                        'network': parts[0],
                        'mask': parts[1],
                        'gateway': parts[2],
                        'interface_ip': parts[3],
                        'metric': parts[4]
                    })
        return routes
    except Exception as e:
        sg.popup_error(f"Error getting routes: {str(e)}\nCommand: route print")
        return []

def delete_route(network, mask, gateway):
    """Delete a route using Windows route command with network, mask, and gateway"""
    cmd = f"route delete {network} mask {mask}"
    logger.debug(f"Deleting route: {cmd}")
    try:
        result = subprocess.run(cmd.split(), check=True, capture_output=True, text=True)
        logger.debug(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with error: {e.stderr} {e.stdout}")
        sg.popup_error(f"Error deleting route: {e.stderr} {e.stdout}\nCommand: {cmd}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sg.popup_error(f"Unexpected error: {str(e)}\nCommand: {cmd}")
        return False

def get_interface_ip_from_name(interface_name, interfaces_by_name):
    """Get interface IP from interface name"""
    return interfaces_by_name.get(interface_name, {}).get('ip')

def get_interface_id_from_name(interface_name, interfaces_by_name):
    """Get interface ID from interface name"""
    return interfaces_by_name.get(interface_name, {}).get('idx')

def modify_route_popup(current_route, interfaces_by_name):
    """Popup window to modify a route"""
    text_width = 15
    input_width = 30
    layout = [
        [sg.Text("NIC Name", size=(text_width, 1)), sg.Combo(list(interfaces_by_name.keys()), default_value=current_route['nic_name'], key='-INTERFACE-', size=(input_width, 1))],
        [sg.Text("Network", size=(text_width, 1)), sg.Input(current_route['network'], key='-NETWORK-', size=(input_width, 1))],
        [sg.Text("Mask", size=(text_width, 1)), sg.Input(current_route['mask'], key='-MASK-', size=(input_width, 1))],
        [sg.Text("Gateway", size=(text_width, 1)), sg.Input(current_route['gateway'], key='-GATEWAY-', size=(input_width, 1))],
        [sg.Text("Metric", size=(text_width, 1)), sg.Input(current_route['metric'], key='-METRIC-', size=(input_width, 1))],
        [sg.Text("Interface IP", size=(text_width, 1)), sg.Input(current_route['interface_ip'], key='-INTERFACE_IP-', size=(input_width, 1), disabled=True)],
        [sg.Button("Save", button_color=('black', 'yellow')), sg.Button("Cancel")]
    ]
    
    window = sg.Window("Modify Route", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return None
        if event == "Save":
            interface_ip = None
            interface_id = None
            if values['-INTERFACE-']:
                interface_id = get_interface_id_from_name(values['-INTERFACE-'], interfaces_by_name)
                interface_ip = get_interface_ip_from_name(values['-INTERFACE-'], interfaces_by_name)
            interface_id = get_interface_id_from_name(values['-INTERFACE-'], interfaces_by_name)
            if not interface_ip or not interface_id:
                sg.popup_error("Invalid interface selected!")
                continue
            new_route = {
                'interface_ip': interface_ip,
                'interface_id': interface_id,
                'nic_name': values['-INTERFACE-'],
                'network': values['-NETWORK-'],
                'mask': values['-MASK-'],
                'gateway': values['-GATEWAY-'],
                'metric': values['-METRIC-']
            }
            window.close()
            logger.debug(f"new route is {new_route}")
            return new_route
        
def refresh_routes_table(window):
    """Refresh the routes table with updated data."""
    routes = get_current_routes()
    interfaces_by_ip, interfaces_by_name = get_network_interfaces()
    for route in routes:
        interface_ip = route['interface_ip']
        route['nic_name'] = interfaces_by_ip.get(interface_ip, f"Unknown ({interface_ip})")
        for name, info in interfaces_by_name.items():
            if info['ip'] == interface_ip:
                route['interface_id'] = info['idx']
                break
        if 'interface_id' not in route:
            route['interface_id'] = "Unknown"
    table_data = [
        [
            route['nic_name'],
            route['network'],
            route['mask'],
            route['gateway'],
            route['metric'],
            route['interface_ip'],
            'add',
            'modify',
            'delete'
        ]
        for route in routes
    ]
    try:
        window['-TABLE-'].update(values=table_data)
    except Exception as e:
        logger.error(f"Error updating table: {str(e)}")
        sg.popup_error(f"Error updating table: {str(e)}")

def main():
    # Get initial data
    routes = get_current_routes()
    interfaces_by_ip, interfaces_by_name = get_network_interfaces()
    
    # Map interface IPs to names and IDs in the routes
    for route in routes:
        interface_ip = route['interface_ip']
        route['nic_name'] = interfaces_by_ip.get(interface_ip, f"Unknown ({interface_ip})")
        for name, info in interfaces_by_name.items():
            if info['ip'] == interface_ip:
                route['interface_id'] = info['idx']
                break
        if 'interface_id' not in route:
            route['interface_id'] = "Unknown"
    
    # Define column headers
    headings = ['nic name', 'network', 'mask', 'gateway', 'metric', 'IF', 'add', 'modify', 'delete']
    
    # Create table data
    table_data = []
    for route in routes:
        table_data.append([
            route['nic_name'],
            route['network'],
            route['mask'],
            route['gateway'],
            route['metric'],
            route['interface_ip'],  # IF column shows interface_ip
            'add',
            'modify',
            'delete'
        ])
    
    # Define the layout with expandable table
    layout = [
        [sg.Table(
            values=table_data,
            headings=headings,
            auto_size_columns=True,
            justification='center',
            key='-TABLE-',
            enable_events=True,
            row_height=25,
            num_rows=min(len(table_data), 10),
            expand_x=True,
            expand_y=True,
            enable_click_events=True
        )],
        [sg.Button("Refresh"), sg.Button("Exit")]
    ]
    
    window = sg.Window("Network Interface Route Manager", layout, resizable=True, finalize=True, size=(1200, 500))
    window['-TABLE-'].expand(True, True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, "Exit"):
            break
            
        if event == "Refresh":

            try:
                refresh_routes_table(window)
            except Exception as e:
                logger.error(f"Error updating table: {str(e)}")
                sg.popup_error(f"Error updating table: {str(e)}")
            
        # Handle table click events
        if isinstance(event, tuple) and event[0] == '-TABLE-' and event[1] == '+CLICKED+':
            row, col = event[2]
            if row is None or col is None or row < 0:
                continue
                
            selected_route = routes[row]
            
            if col == 6 or col == 7:  # Modify column
                new_route = modify_route_popup(selected_route, interfaces_by_name)
                if new_route:
                    if new_route['network'] == selected_route['network']:   
                        logger.debug(f"new route and selected route are same, just update the gateway")
                        cmd = f"route change {new_route['network']} mask {new_route['mask']} {new_route['gateway']} {new_route['interface_ip']}"
                        logger.debug(f"new route and selected route are same, just update the gateway")
                        cmd = f"route change {new_route['network']} mask {new_route['mask']} {new_route['interface_ip']}"
                        logger.debug(f"Modifying route: {cmd}")
                    else:
                        logger.debug(f"new route and selected route are different, add the new route")
                        
                        # Add the new route
                        cmd = f"route add {new_route['network']} mask {new_route['mask']} {new_route['interface_ip']}"
                        logger.debug(f"Adding route: {cmd}")
                    try:
                        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                        sg.popup("Route modified successfully!", f"Output:\n{result.stdout}")
                        # Refresh the table
                        refresh_routes_table(window)
                    except subprocess.CalledProcessError as e:
                        logger.error(f"Command failed with error: {e.stderr} {e.stdout}")
                        sg.popup_error(f"Error deleting route: {e.stderr} {e.stdout}\nCommand: {cmd}")
                        return False
                    except Exception as e:
                        logger.error(f"Unexpected error: {str(e)}")
                        sg.popup_error(f"Unexpected error: {str(e)}\nCommand: {cmd}")
                        
            elif col == 8:  # Delete column
                confirm = sg.popup_yes_no(
                    f"Are you sure you want to delete this route?\n\n\n"
                    f"NIC name: {selected_route['nic_name']}\n"
                    f"Network: {selected_route['network']}\n"
                    f"Mask: {selected_route['mask']}\n"
                    f"Gateway: {selected_route['gateway']}\n"
                    f"Metric: {selected_route['metric']}\n"
                    f"Interface IP: {selected_route['interface_ip']}",
                    title="Confirm Delete",
                    button_color=('white', 'red')
                )
                if confirm == "Yes":
                    if delete_route(
                        selected_route['network'],
                        selected_route['mask'],
                        selected_route['gateway']
                    ):
                        sg.popup("Route deleted successfully!")
                        

                        # Replace the $SELECTION_PLACEHOLDER$ with a call to the new function
                        refresh_routes_table(window)
    
    window.close()

if __name__ == "__main__":
    main()