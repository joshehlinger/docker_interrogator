# Docker Interrogator

Script to talk the docker registry and gather metrics on the various
sizes of repos. It will create a CSV file named `registry_results.csv`
that will be populated with each repo in the docker registry and their
respective size in MB.


A 3/10 on the Jank Scale.

## Development

Developed on Python 3.7

Create a virtual environment and

`pip install -r requirements.txt`

## Usage
`python interrogator.py --registry=https://my.docker.registry`