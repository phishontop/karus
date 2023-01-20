from karus.modules import CompanyhouseSearch


def test_companyhouse_search():
    search1 = CompanyhouseSearch(fullname="william smith")
    results1 = search1.run()

    assert len(results1) > 0

    for result in results1:
        assert result.full_name.lower() == "william smith"
