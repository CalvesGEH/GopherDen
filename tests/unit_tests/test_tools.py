from repos.all_repositories import AllRepositories
from schema.tool import ToolCreate


class ToolCreationTests():
    def test_create_tool(self, database:AllRepositories) -> None:
        tool = ToolCreate(
            name="Crescent 4\" Adjustable Black Oxide Wrench",
            description="A small adjustable wrench for small jobs.",
            on_hand=False,
            store_link="https://www.amazon.com/Crescent-AT24VS-Finish-Adjustable-Wrench/dp/B0091A5G22/ref=sr_1_5?sr=8-5"
        )

        new_tool = database.tools.create(tool)
        assert new_tool is not None

        assert new_tool.name == tool.name
        assert new_tool.description == tool.description
        assert new_tool.on_hand == tool.on_hand
        assert new_tool.store_link == tool.store_link
        assert new_tool.slug == "crescent-4-adjustable-black-oxide-wrench"