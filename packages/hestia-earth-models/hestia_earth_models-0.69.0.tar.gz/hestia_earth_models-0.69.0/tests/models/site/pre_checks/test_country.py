from unittest.mock import Mock, patch

from hestia_earth.models.site.pre_checks.country import run

class_path = 'hestia_earth.models.site.pre_checks.country'


@patch(f"{class_path}.download_hestia")
def test_run(mock_download_hestia: Mock):
    site = {'country': {'@type': 'Term', '@id': 'GADM-GBR'}}
    run(site)
    mock_download_hestia.assert_called_once_with('GADM-GBR')
