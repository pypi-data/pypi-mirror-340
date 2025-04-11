from unittest.mock import patch

from hestia_earth.models.utils.source import _list_sources, find_sources

class_path = 'hestia_earth.models.utils.source'
search_results = [{
    '@type': 'Source',
    '@id': 'source-1',
    'name': 'Source 1',
    'bibliography': {'title': 'Biblio 1'}
}]


def test_list_sources():
    sources = _list_sources()
    # test `BIBLIO_TITLE`
    assert 'Soil organic carbon sequestration rates in vineyard agroecosystems under different soil management practices: A meta-analysis' in sources  # noqa: E501
    # test `OTHER_BIBLIO_TITLES`
    assert '2006 IPCC Guidelines for National Greenhouse Gas Inventories' in sources
    assert 'COMMISSION DECISION of 10 June 2010 on guidelines for the calculation of land carbon stocks for the purpose of Annex V to Directive 2009/28/EC' in sources  # noqa: E501


@patch(f"{class_path}.search", return_value=search_results)
def test_find_sources(*args):
    sources = find_sources()
    assert sources == {
        'Biblio 1': {
            '@type': 'Source',
            '@id': 'source-1',
            'name': 'Source 1'
        }
    }
