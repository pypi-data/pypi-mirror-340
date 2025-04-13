import re
import json
from .helpers import ip2name, ip2reverse, stripIp, is_p2p, get_priority, precompute_connections_dict, is_unique_connection
from .helpers import precompute_routers_tags_dict, precompute_routers_position_dict


def parse_bird(config, output):
    routers = []
    connections = []
    networks = []
    current_router = None
    for line in output.splitlines():
        line = line.rstrip()
        if re.match(r'^\trouter (\S+)$', line):
            parts = line.split()
            routers.append(parts[1])
            current_router = parts[1]
        if re.match(r'^\t\t(external|stubnet) (\S+) metric (\d+)$', line):
            parts = line.split()
            networks.append({
                'router': current_router,
                'network': parts[1],
                'metric': parts[3]
            })
        if re.match(r'^\t\trouter (\S+) metric (\d+)$', line):
            parts = line.split()
            connections.append({
                'source': current_router,
                'destination': parts[1],
                'metric': parts[3],
                'priority': get_priority(config['routers'], current_router)
            })
    return routers, connections, networks


def filter_routers(config_routers, routers, tags):
    """
    Filter routers based on selected tags

    Parameters:
    * config_routers: list of routers from config
    * routers: list of routers
    * tags: bool

    Returns:
    * filtered_routers: list of routers
    """
    tagged_routers = precompute_routers_tags_dict(config_routers)
    filtered_routers = []
    for r in routers:
        if (set(tags) & set(tagged_routers.get(r, []))) or not tags:
            filtered_routers.append(r)
    return filtered_routers


def filter_connections(config_routers, connections, tags):
    """
    Filter connections based involved routers matching selected tags

    Parameters:
    * config_routers: list of routers from config
    * connections: list of connections
    * tags: bool

    Returns:
    * filtered_connections: list of connections
    """
    tagged_routers = precompute_routers_tags_dict(config_routers)
    filtered_connections = []
    for c in connections:
        # Both source and destination routers are tagged
        if (set(tags) & set(tagged_routers.get(c['source'], []))) and (set(tags) & set(tagged_routers.get(c['destination'], []))):
            filtered_connections.append(c)
        # Only source router is tagged
        elif (set(tags) & set(tagged_routers.get(c['source'], []))) and (not set(tagged_routers.get(c['destination'], []))):
            filtered_connections.append(c)
        # Only destination router is tagged
        elif (not set(tagged_routers.get(c['source'], []))) and (set(tags) & set(tagged_routers.get(c['destination'], []))):
            filtered_connections.append(c)
        # Not source nor destination routers are tagged
        elif not tags:
            filtered_connections.append(c)
    return filtered_connections


def print_markdown_mermaid(routers, unique_routers, sorted_connections, networks):
    print("```mermaid")
    print("flowchart TB")

    for router in unique_routers:
        print(f"    {ip2name(routers, router)}[\"{ip2name(routers, router)}")
        for network in networks:
            if network['router'] == router:
                print(f"    {network['network']}")
        print("    \"]")

    connections_dict = precompute_connections_dict(sorted_connections)

    # Use a set to track used connections
    used = set()

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        if is_unique_connection(c, x_metric, y_metric, used):
            x_name = ip2name(routers, c['source'])
            y_name = ip2name(routers, c['destination'])

            print(f"    {x_name} o-- {x_metric}-{y_metric} --o {y_name}")

            used.add((c['source'], c['destination']))

    print("```")


def print_text_routers(routers, unique_routers, networks):
    print(f"We currently have {len(unique_routers)} routers.\n")
    for router in unique_routers:
        print(f"Router {ip2name(routers, router)} ({router} - {ip2reverse(router)}):")
        for network in networks:
            if network['router'] == router:
                if '/' in network['network'] and is_p2p(network['network']):
                    ip = stripIp(network['network'])
                    reverse = ip2reverse(ip)
                    print(f"- {network['network']} ({reverse})")
                else:
                    print(f"- {network['network']}")
        print("")


def print_text_routers_diff_ready(routers, unique_routers, networks):
    print(f"We currently have {len(unique_routers)} routers.\n")
    for router in unique_routers:
        print(f"Router {ip2name(routers, router)} ({router}) - {ip2reverse(router)}):")
        for network in networks:
            if network['router'] == router:
                if '/' in network['network'] and is_p2p(network['network']):
                    ip = stripIp(network['network'])
                    reverse = ip2reverse(ip)
                    print(f"Router {ip2name(routers, router)} publishes {network['network']} ({reverse}).")
                else:
                    print(f"Router {ip2name(routers, router)} publishes {network['network']}.")
        print("")


def print_text_connections(routers, unique_routers, sorted_connections):
    print(f"We currently have {len(sorted_connections)//2} connections.\n")

    connections_dict = precompute_connections_dict(sorted_connections)

    # Use a set to track used connections
    used = set()

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        if is_unique_connection(c, x_metric, y_metric, used):
            x_name = ip2name(routers, c['source'])
            y_name = ip2name(routers, c['destination'])

            print(f"Connection {x_name} <--> {y_name} ({x_metric}/{y_metric})")

            used.add((c['source'], c['destination']))


def print_text_connections_diff_ready(routers, unique_routers, sorted_connections):
    print(f"We currently have {len(sorted_connections)//2} connections.\n")

    connections_dict = precompute_connections_dict(sorted_connections)

    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))

        x_name = ip2name(routers, c['source'])
        y_name = ip2name(routers, c['destination'])

        print(f"Connection {x_name} <--> {y_name} ({x_metric}/{y_metric})")


def print_json(routers, unique_routers, sorted_connections, networks, tags):
    routers_tags_dict = precompute_routers_tags_dict(routers)
    routers_position_dict = precompute_routers_position_dict(routers)

    output = {"nodes": [], "links": []}
    for router in unique_routers:
        router_reverse = ip2reverse(router)
        corresponding_networks = []
        for network in networks:
            if network['router'] == router:
                if '/' in network['network'] and is_p2p(network['network']):
                    ip = stripIp(network['network'])
                    net_reverse = ip2reverse(ip)
                    corresponding_networks.append({
                        "network": network['network'],
                        "reverse": net_reverse
                    })
                else:
                    corresponding_networks.append({
                        "network": network['network'],
                    })

        node = {
            "id": ip2name(routers, router),
            "name": ip2name(routers, router),
            "ip": router,
            "reverse": router_reverse,
            "tags": routers_tags_dict.get(router, []),
            "networks": corresponding_networks,
            "position": routers_position_dict.get(router, [])
        }
        output['nodes'].append(node)

    connections_dict = precompute_connections_dict(sorted_connections)
    used = set()
    for c in sorted_connections:
        x_metric = connections_dict.get((c['destination'], c['source']))
        y_metric = connections_dict.get((c['source'], c['destination']))
        if is_unique_connection(c, x_metric, y_metric, used):
            output['links'].append({
                "source": ip2name(routers, c['source']),
                "target": ip2name(routers, c['destination']),
                "source_metric": x_metric,
                "target_metric": y_metric
            })
            used.add((c['source'], c['destination']))
    print(json.dumps(output))
