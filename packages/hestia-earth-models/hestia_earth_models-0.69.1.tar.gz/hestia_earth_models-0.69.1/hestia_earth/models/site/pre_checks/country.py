from hestia_earth.utils.api import download_hestia


def run(site: dict): return site | {'country': download_hestia(site.get('country', {}).get('@id'))}
