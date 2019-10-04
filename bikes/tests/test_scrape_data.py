from bikes.scrape_data import search_open_data_portal


def test_search_open_data_portal():
    url = "https://www.opengov-muenchen.de/group/5616e3e5-4f16-4d2b-acc2-81215c900cce?tags=Raddauerz%C3%A4hlstellen"
    visit_these_sites = search_open_data_portal(url)
    assert len(visit_these_sites) > 3
