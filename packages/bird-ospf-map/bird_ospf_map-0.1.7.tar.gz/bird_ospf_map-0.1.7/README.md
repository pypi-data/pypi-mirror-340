# bird-ospf-map

OSPF connection parser and maybe later even map generator


## Development

```bash
poetry env activate
poetry install
ssh router sudo birdc show ospf state all ngn | poetry run bird_ospf_map -c ~/.bird-ospf-map.yaml
poetry run flake8
poetry run pytest
```


## Prerequisities
 * Bird2 with OSPF running


## Packaging

The package is in [PyPi](https://pypi.org/project/bird-ospf-map/) and in [OBS](https://build.opensuse.org/package/show/home:pdostal/python-bird-ospf-map) under `home:pdostal/python-bird-ospf-map`.

```bash
poetry version patch
git commit -am "axy"
git tag v$(poetry version -s) 
poetry build
poetry publish
py2pack fetch bird_ospf_map
osc add bird_ospf_map*
vim python-bird-ospf-map.spec # bump the version
osc vc # write changelog (use commit messages)
osc commit
```


## Resources
 * We generate the graph using [the `Mermaid` library](https://mermaid.js.org/syntax/flowchart.html).
 * The `json` output can be used by [D3.js](https://github.com/d3/d3)
