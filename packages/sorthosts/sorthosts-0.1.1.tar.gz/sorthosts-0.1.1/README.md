# sorthosts

Sort ssh known_hosts file.

- group by algorithm and hash
- sort by IP addresses and domains


## install

`pip install sorthosts`


## Usage

- `-i` input file (default: ~/.ssh/known_hosts)
- `-o` output file, print to screen if not defined

`python3 -m sorthosts [-i INPUT] [-o OUTPUT]`

