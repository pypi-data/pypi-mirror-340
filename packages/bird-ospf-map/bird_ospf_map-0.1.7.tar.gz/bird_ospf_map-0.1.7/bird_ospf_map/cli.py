import sys
import subprocess
import yaml
from .misc import parse_bird, filter_routers, filter_connections
from .misc import print_json, print_text_routers_diff_ready, print_text_connections_diff_ready
from .misc import print_markdown_mermaid, print_text_routers, print_text_connections
import click
from pathlib import Path
from .helpers import resolve_path


@click.command()
@click.option('--stdin', is_flag=True, default=True, help="Get the birdc output from stdin")
@click.option('--exec', is_flag=True, help="Execute birdc and get the output from it")
@click.option('--text', is_flag=True, default=True, help="Print in human readable format")
@click.option('--diff-ready', is_flag=True, help="Print in human readable format for urlwatch")
@click.option('--mermaid', is_flag=True, help="Print in Markdown Mermaid format")
@click.option('--json', is_flag=True, help="Print in json format")
@click.option('--tags', multiple=True, help="Print only routers marked with selected tags")
@click.option('-c', '--config', type=click.Path(path_type=Path), default='config.yaml',
              help='Path to config file (default: ./config.yaml)', callback=resolve_path)

def cli(stdin, exec, text, diff_ready, mermaid, json, tags, config):
    with open(config, 'r') as file:
        configFile = yaml.safe_load(file)

    if exec:
        output = subprocess.run(['/sbin/birdc', 'show ospf state all ngn'],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
    elif stdin:
        output = sys.stdin.read()

    if output:
        routers, connections, networks = parse_bird(configFile, output)

        filtered_routers = filter_routers(configFile['routers'], routers, tags)
        filtered_connections = filter_connections(configFile['routers'], connections, tags)
        sorted_connections = sorted(filtered_connections, key=lambda x: (x['priority'], x['source'], x['metric']))

        if mermaid:
            print_markdown_mermaid(configFile['routers'], filtered_routers, sorted_connections, networks)
        elif diff_ready:
            print_text_routers_diff_ready(configFile['routers'], filtered_routers, networks)
            print_text_connections_diff_ready(configFile['routers'], filtered_routers, sorted_connections)
        elif json:
            print_json(configFile['routers'], filtered_routers, sorted_connections, networks, tags)
        else:
            print_text_routers(configFile['routers'], filtered_routers, networks)
            print_text_connections(configFile['routers'], filtered_routers, sorted_connections)


if __name__ == "__main__":
    cli()
