from pathlib import Path


def resolve_path(ctx, param, value):
    """Convert path string to absolute Path object"""
    return Path(value).resolve()


def ip2name(routers, ip):
    for router in routers:
        if router['ip'] == ip:
            return router['name']
    return ip


def ip2reverse(ip):
    """Perform reverse DNS lookup for the given IP address."""
    try:
        import socket
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return ip


def stripIp(ip):
    """Remove the subnet mask from the IP address in case /32 or /31"""
    if '/' in ip:
        return ip.split('/')[0]


def is_p2p(ip):
    """Check if the IP address is a point-to-point address."""
    return ip.endswith('/32') or ip.endswith('/31') or ip.endswith('/30')


def get_priority(routers, ip):
    for router in routers:
        if router['ip'] == ip:
            return router['priority']
    return 10


def precompute_connections_dict(connections):
    connections_dict = {}
    for c in connections:
        key = (c['source'], c['destination'])
        if key not in connections_dict:  # Only store if it doesn't exist yet
            connections_dict[key] = c['metric']
    return connections_dict


def precompute_routers_tags_dict(routers):
    tagged_routers = {}
    for router in routers:
        for tag in router['tags']:
            tagged_routers.setdefault(router['ip'], []).append(tag)
    return tagged_routers


def precompute_routers_position_dict(routers):
    routers_position = {}
    for router in routers:
        position = router.get('position')
        if position:
            routers_position[router['ip']] = position
    return routers_position


def is_unique_connection(connection, x_metric, y_metric, used):
    return (x_metric and y_metric
            and (connection['source'], connection['destination']) not in used
            and (connection['destination'], connection['source']) not in used)
