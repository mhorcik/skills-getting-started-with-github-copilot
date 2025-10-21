# FastAPI Tests

This directory contains comprehensive test coverage for the High School Management System API.

## Test Structure

```
tests/
├── __init__.py          # Makes tests a Python package
├── conftest.py          # Shared test fixtures and configuration
├── test_api.py          # Main API endpoint tests
└── README.md            # This file
```

## Test Categories

### 1. **Activities Endpoints Tests** (`TestActivitiesEndpoints`)
- ✅ **GET /activities** - Retrieve all activities
- ✅ **GET /** - Root redirect functionality

### 2. **Signup Endpoint Tests** (`TestSignupEndpoint`) 
- ✅ **Successful signup** - Add new participant to activity
- ✅ **Activity not found** - Handle invalid activity names
- ✅ **Already registered** - Prevent duplicate signups
- ✅ **Special characters** - Handle emails with special characters

### 3. **Remove Participant Tests** (`TestRemoveParticipantEndpoint`)
- ✅ **Successful removal** - Remove existing participant
- ✅ **Activity not found** - Handle invalid activity names  
- ✅ **Participant not found** - Handle non-existent participants
- ✅ **Wrong activity** - Prevent removing from wrong activity

### 4. **Integration Scenarios** (`TestIntegrationScenarios`)
- ✅ **Full lifecycle** - Complete signup → verify → remove → verify workflow
- ✅ **Multiple activities** - Sign up for multiple different activities
- ✅ **Capacity tracking** - Verify participant counts are accurate

## Running Tests

### Option 1: Using the Test Runner (Recommended)
```bash
# Basic tests
python run_tests.py

# With coverage report
python run_tests.py coverage

# Install dependencies
python run_tests.py install

# Run everything
python run_tests.py all
```

### Option 2: Direct pytest Commands
```bash
# Basic test run
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=term-missing -v

# Run specific test class
python -m pytest tests/test_api.py::TestSignupEndpoint -v

# Run specific test method
python -m pytest tests/test_api.py::TestSignupEndpoint::test_signup_success -v
```

## Test Coverage

Current coverage: **100%** of the FastAPI application code

The tests cover:
- ✅ All API endpoints (`/activities`, `/activities/{name}/signup`, `/activities/{name}/participants/{email}`)
- ✅ All error conditions (404s, 400s)
- ✅ All success paths
- ✅ Data validation and state changes
- ✅ Integration workflows

## Test Fixtures

### `client` Fixture
- Provides a FastAPI TestClient for making HTTP requests
- Automatically handles app lifecycle

### `reset_activities` Fixture  
- Resets the activities database before each test
- Ensures test isolation and repeatability
- Restores original test data after each test

## Dependencies

The following packages are required for testing:

```
pytest>=8.0.0           # Testing framework
pytest-asyncio>=1.2.0   # Async test support  
pytest-cov>=4.0.0       # Coverage reporting
httpx>=0.28.0            # HTTP client for FastAPI testing
```

## Best Practices

1. **Test Isolation** - Each test is independent and can run in any order
2. **Descriptive Names** - Test names clearly describe what is being tested
3. **Comprehensive Coverage** - Tests cover both success and failure scenarios
4. **Real HTTP Requests** - Tests use actual HTTP requests via TestClient
5. **Data Validation** - Tests verify both response data and backend state changes

## Adding New Tests

When adding new functionality to the API:

1. Add test methods to the appropriate test class
2. Use the `reset_activities` fixture to ensure clean state
3. Test both success and error conditions
4. Verify data changes in the backend state
5. Update this README if adding new test categories

Example new test:
```python
def test_new_feature(self, client: TestClient, reset_activities):
    """Test description of what this tests."""
    # Arrange
    test_data = "setup data"
    
    # Act  
    response = client.post("/new-endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    assert "expected" in response.json()
```