from karus.modules import GithubLookup
from karus.modules.github.commit import InformationListFactory


def test_github_lookup():
    github_lookup1 = GithubLookup(name="test")
    results1 = github_lookup1.run()

    github_lookup2 = GithubLookup(name="phishontop")
    results2 = github_lookup2.run()

    assert results1.get("github", None) == {"information": {}}
    assert results2["github"]["information"].get("discord_id", None) == ["944293157741404243"]


def test_github_information_list():
    information_list = InformationListFactory.create()

    assert "404" not in information_list.countries
    assert "404" not in information_list.coding_languages
    assert "404" not in information_list.email_domains
