from karus.modules import RobloxLookup


def test_roblox_lookup():
    roblox_lookup1 = RobloxLookup.from_username(name="roblox")
    results1 = roblox_lookup1.run()

    roblox_lookup2 = RobloxLookup.from_username(name="clearlyany")
    results2 = roblox_lookup2.run()

    assert results1["roblox"].get("roblox_id", None) == 1
    assert results1["roblox"].get("games_played", None) == []

    assert results2["roblox"].get("roblox_id", None) == 2520457787
    assert "RoseWoodHotelsHolder" in results2["roblox"].get("previous_names", None)
