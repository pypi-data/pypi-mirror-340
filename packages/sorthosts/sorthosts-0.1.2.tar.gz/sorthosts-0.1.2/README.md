# sorthosts

Sort ssh known_hosts file.

- group by algorithm and hash
- sort by IP addresses and domains


## Install

`pip install sorthosts`


## Usage

- `INPUT` input file (default: ~/.ssh/known_hosts)
- `OUTPUT` output file, print to screen if not defined

`python3 -m sorthosts [-i INPUT] [-o OUTPUT]`

