from datetime import datetime, timedelta

from backend.repos.all_repositories import AllRepositories
from backend.schema.chore import ChoreCreate
from backend.schema.tool import ToolCreate, ChoreToolCreate


class ChoreCreationTests():
    def test_create_chore(self, database:AllRepositories) -> None:
        chore = ChoreCreate(
            name="Clean the Tub Drain",
            description="Clean out the upstairs tub drain.",
            total_time="30 minutes",
            frequency=timedelta(weeks=4),
            next_due=datetime.now() + timedelta(days=30),
            instructions=[
                {
                    "title": "Remove the Drain Bolt",
                    "text": "Take the 15mm socket wrench and remove the drain bolt in the middle of the drain.",
                    "position": 1
                },
                {
                    "title": "Remove the Drain and Gasket",
                    "text": "Lift up the drain, using a screwdriver to pry it up if necessary. Remove the old gasket.",
                    "position": 2
                },
                {
                    "title": "Clean the Drain",
                    "text": "Clean the drainwith soap and paper towels.",
                    "position": 3
                },
                {
                    "title": "Replace the Gasket and Drain",
                    "text": "Place the new gasket on the drain and replace the drain in the tub.",
                    "position": 4
                },
                {
                    "title": "Tighten the Drain Bolt",
                    "text": "Use the 15mm socket wrench to tighten the drain bolt in the middle of the drain. Make sure it is extra tight to prevent leaks.",
                    "position": 5
                }
            ]
        )

        new_chore = database.chores.create(chore)
        assert new_chore is not None

        assert new_chore.name == chore.name
        assert new_chore.description == chore.description
        assert new_chore.total_time == chore.total_time
        assert new_chore.frequency == chore.frequency
        assert new_chore.next_due == chore.next_due
        assert new_chore.slug == "clean-the-tub-drain"
        for instruction in chore.instructions:
            for new_instruction in new_chore.instructions:
                if instruction["position"] == new_instruction.position:
                    assert instruction["title"] == new_instruction.title
                    assert instruction["text"] == new_instruction.text
                    break

    def test_add_tool(self, database:AllRepositories, unique_chore:ChoreCreate, unique_tool:ToolCreate) -> None:
        chore = database.chores.create(unique_chore)
        assert chore.tools == []

        tool = ChoreToolCreate(quantity=1, **unique_tool.model_dump())
        print(chore)
        print(tool)
        updated_chore = database.chores.add_tool(chore.id, tool)

        assert updated_chore is not None

        assert tool in updated_chore.tools

        # Ensure tool exists in database
        db_tool = database.tools.from_slug(tool.slug)
        assert db_tool
