from src.models import * 


def test_team_model():
    # Set up
    test_team = Team("Test Name")

    # First assert
    assert test_team.team_info == 'Test Name'

    # Modify data
    test_team.team_info = "New Test Name"

    # Second Assert
    assert test_team.team_info == 'New Test Name'
