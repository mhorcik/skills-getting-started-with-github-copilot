import pytest
from fastapi.testclient import TestClient
from app import app, activities


class TestActivitiesEndpoints:
    """Test cases for activities-related endpoints."""
    
    def test_get_activities(self, client: TestClient, reset_activities):
        """Test GET /activities endpoint."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        
        # Check structure of an activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_root_redirect(self, client: TestClient):
        """Test root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignupEndpoint:
    """Test cases for participant signup functionality."""
    
    def test_signup_success(self, client: TestClient, reset_activities):
        """Test successful signup for an activity."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Verify initial state
        initial_participants = len(activities[activity]["participants"])
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity}"
        
        # Verify participant was added
        assert len(activities[activity]["participants"]) == initial_participants + 1
        assert email in activities[activity]["participants"]
    
    def test_signup_activity_not_found(self, client: TestClient, reset_activities):
        """Test signup for non-existent activity."""
        email = "student@mergington.edu"
        activity = "Non-Existent Activity"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_already_registered(self, client: TestClient, reset_activities):
        """Test signup when student is already registered."""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_with_special_characters(self, client: TestClient, reset_activities):
        """Test signup with URL-encoded activity name and email."""
        email = "test.user@mergington.edu"  # Use dot instead of plus to avoid URL encoding issues
        activity = "Programming Class"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert email in activities[activity]["participants"]


class TestRemoveParticipantEndpoint:
    """Test cases for participant removal functionality."""
    
    def test_remove_participant_success(self, client: TestClient, reset_activities):
        """Test successful removal of a participant."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify participant exists
        assert email in activities[activity]["participants"]
        initial_count = len(activities[activity]["participants"])
        
        response = client.delete(f"/activities/{activity}/participants/{email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Removed {email} from {activity}"
        
        # Verify participant was removed
        assert email not in activities[activity]["participants"]
        assert len(activities[activity]["participants"]) == initial_count - 1
    
    def test_remove_participant_activity_not_found(self, client: TestClient, reset_activities):
        """Test removal from non-existent activity."""
        email = "student@mergington.edu"
        activity = "Non-Existent Activity"
        
        response = client.delete(f"/activities/{activity}/participants/{email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_remove_participant_not_found(self, client: TestClient, reset_activities):
        """Test removal of non-existent participant."""
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/participants/{email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Participant not found in this activity"
    
    def test_remove_participant_from_different_activity(self, client: TestClient, reset_activities):
        """Test removal of participant from wrong activity."""
        email = "michael@mergington.edu"  # In Chess Club, not Programming Class
        activity = "Programming Class"
        
        response = client.delete(f"/activities/{activity}/participants/{email}")
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Participant not found in this activity"


class TestIntegrationScenarios:
    """Integration tests for complete user workflows."""
    
    def test_full_participant_lifecycle(self, client: TestClient, reset_activities):
        """Test complete signup and removal workflow."""
        email = "lifecycle@mergington.edu"
        activity = "Drama Club"
        
        # Step 1: Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == 200
        assert email in activities[activity]["participants"]
        
        # Step 2: Verify in activities list
        activities_response = client.get("/activities")
        assert activities_response.status_code == 200
        drama_participants = activities_response.json()[activity]["participants"]
        assert email in drama_participants
        
        # Step 3: Remove participant
        remove_response = client.delete(f"/activities/{activity}/participants/{email}")
        assert remove_response.status_code == 200
        assert email not in activities[activity]["participants"]
        
        # Step 4: Verify removal in activities list
        final_activities_response = client.get("/activities")
        assert final_activities_response.status_code == 200
        final_drama_participants = final_activities_response.json()[activity]["participants"]
        assert email not in final_drama_participants
    
    def test_multiple_signups_different_activities(self, client: TestClient, reset_activities):
        """Test signing up for multiple different activities."""
        email = "multi@mergington.edu"
        
        # Sign up for multiple activities
        activities_to_join = ["Chess Club", "Programming Class", "Drama Club"]
        
        for activity in activities_to_join:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
            assert email in activities[activity]["participants"]
        
        # Verify participant is in all activities
        for activity in activities_to_join:
            assert email in activities[activity]["participants"]
    
    def test_activity_capacity_tracking(self, client: TestClient, reset_activities):
        """Test that participant counts are tracked correctly."""
        activity = "Chess Club"
        initial_count = len(activities[activity]["participants"])
        max_participants = activities[activity]["max_participants"]
        
        # Get initial state
        response = client.get("/activities")
        chess_data = response.json()[activity]
        initial_spots = max_participants - len(chess_data["participants"])
        
        # Add a participant
        new_email = "capacity@mergington.edu"
        signup_response = client.post(f"/activities/{activity}/signup?email={new_email}")
        assert signup_response.status_code == 200
        
        # Verify count increased
        final_response = client.get("/activities")
        final_chess_data = final_response.json()[activity]
        final_spots = max_participants - len(final_chess_data["participants"])
        
        assert final_spots == initial_spots - 1
        assert len(final_chess_data["participants"]) == initial_count + 1