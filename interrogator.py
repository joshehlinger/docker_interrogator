import requests
import json
import argparse


def convert_to_mb(size_bytes):
    mb = round(size_bytes / 1000000, 2)
    return mb


def docker_interrogate(config):
    session = requests.Session()
    session.headers.update({
        'Accept': 'application/vnd.docker.distribution.manifest.v2+json'
    })
    url = f'{config.registry}/v2/_catalog'
    csv_file = open('registry_results.csv', 'w')
    csv_file.write('Repo,Size(MB)\n')

    loop_control = True
    while loop_control:
        catalog = session.get(url)
        if 'next' in catalog.links:
            url = f'{config.registry}{catalog.links["next"]["url"]}'
        else:
            loop_control = False
        raw_repos = catalog.content
        repos = json.loads(raw_repos.decode("utf-8"))
        for repo_path in repos['repositories']:
            counter = 0
            raw_tags = session.get(f'{config.registry}/v2/{repo_path}/tags/list').content
            tags = json.loads(raw_tags.decode("utf-8"))['tags']
            if tags is not None:
                for tag in tags:
                    raw_manifest = session.get(f'{config.registry}/v2/{repo_path}/manifests/{tag}').content
                    manifest = json.loads(raw_manifest.decode("utf-8"))
                    for layer in manifest['layers']:
                        counter += layer['size']
            if counter != 0:
                row = f'{repo_path},{convert_to_mb(counter)}{chr(10)}'
                csv_file.write(row)

    csv_file.close()


def arg_parser() -> argparse.ArgumentParser:
    desc = 'Add your docker registry URL'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--registry',
                        dest='registry',
                        metavar='STRING',
                        help='url of docker registry')
    return parser


def main(args=None):
    parser = arg_parser()
    config = parser.parse_args(args=args)
    docker_interrogate(config)


if __name__ == '__main__':
    main()