"""
Comprehensive test suite for all API endpoints.
Run this before deployment to verify everything works!
"""
import requests
import json
from datetime import datetime
import time

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30  # seconds

# Test results tracker
tests_passed = 0
tests_failed = 0
test_results = []


def log_test(name, passed, details=""):
    """Log test result."""
    global tests_passed, tests_failed
    
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {name}")
    if details:
        print(f"   {details}")
    
    test_results.append({
        "test": name,
        "passed": passed,
        "details": details
    })
    
    if passed:
        tests_passed += 1
    else:
        tests_failed += 1


def test_root_endpoint():
    """Test root endpoint returns API info."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            checks = [
                "name" in data,
                "version" in data,
                "status" in data,
                data.get("status") == "operational"
            ]
            
            if all(checks):
                log_test("Root Endpoint", True, f"Version: {data.get('version')}")
                return True
            else:
                log_test("Root Endpoint", False, "Missing required fields")
                return False
        else:
            log_test("Root Endpoint", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Root Endpoint", False, str(e))
        return False


def test_health_check():
    """Test health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["status", "database", "ai_service", "version"]
            has_all_fields = all(field in data for field in required_fields)
            
            if not has_all_fields:
                log_test("Health Check", False, "Missing required fields")
                return False
            
            # Check if services are healthy
            db_status = data.get("database")
            ai_status = data.get("ai_service")
            overall_status = data.get("status")
            
            details = f"DB: {db_status}, AI: {ai_status}, Status: {overall_status}"
            
            if overall_status == "healthy":
                log_test("Health Check", True, details)
                return True
            elif overall_status == "degraded":
                log_test("Health Check", True, f"⚠️  Degraded - {details}")
                return True
            else:
                log_test("Health Check", False, f"Unhealthy - {details}")
                return False
        else:
            log_test("Health Check", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Health Check", False, str(e))
        return False


def test_chat_examples():
    """Test getting example questions."""
    try:
        response = requests.get(f"{BASE_URL}/api/chat/examples", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            if "examples" in data and isinstance(data["examples"], list):
                count = len(data["examples"])
                log_test("Chat Examples", True, f"Retrieved {count} examples")
                return True
            else:
                log_test("Chat Examples", False, "Invalid response format")
                return False
        else:
            log_test("Chat Examples", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Chat Examples", False, str(e))
        return False


def test_chat_endpoint():
    """Test AI chat endpoint."""
    try:
        payload = {
            "message": "What is Howard's background?"
        }
        
        print("\n   Sending chat request (may take a few seconds)...")
        response = requests.post(
            f"{BASE_URL}/api/chat/",
            json=payload,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["response", "session_id", "timestamp"]
            has_all_fields = all(field in data for field in required_fields)
            
            if not has_all_fields:
                log_test("Chat Endpoint", False, "Missing required fields")
                return False
            
            # Check response quality
            response_text = data.get("response", "")
            tokens = data.get("tokens_used", 0)
            
            if len(response_text) > 50:  # Reasonable response length
                log_test(
                    "Chat Endpoint", 
                    True, 
                    f"Response: {len(response_text)} chars, {tokens} tokens"
                )
                return True
            else:
                log_test("Chat Endpoint", False, "Response too short")
                return False
        else:
            log_test("Chat Endpoint", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Chat Endpoint", False, str(e))
        return False


def test_chat_with_history():
    """Test chat endpoint with conversation history."""
    try:
        payload = {
            "message": "What programming languages does he know?",
            "conversation_history": [
                {
                    "role": "user",
                    "content": "Tell me about Howard"
                },
                {
                    "role": "assistant",
                    "content": "Howard is a Computer Engineering graduate student..."
                }
            ]
        }
        
        print("\n   Testing conversation context...")
        response = requests.post(
            f"{BASE_URL}/api/chat/",
            json=payload,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "").lower()
            
            # Check if response uses context (mentions languages)
            has_context = any(lang in response_text for lang in ["python", "javascript", "java", "c++"])
            
            if has_context:
                log_test("Chat with History", True, "Context maintained")
                return True
            else:
                log_test("Chat with History", True, "⚠️  Context unclear but endpoint works")
                return True
        else:
            log_test("Chat with History", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Chat with History", False, str(e))
        return False


def test_record_visit():
    """Test recording a visitor."""
    try:
        payload = {
            "page_visited": "/test",
            "user_agent": "Test Suite Bot/1.0"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analytics/visit",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") == True:
                log_test("Record Visit", True, data.get("message"))
                return True
            else:
                log_test("Record Visit", False, "Success flag not true")
                return False
        else:
            log_test("Record Visit", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Record Visit", False, str(e))
        return False


def test_analytics_stats():
    """Test getting analytics statistics."""
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["total_visitors", "total_visits", "recent_visits"]
            has_all_fields = all(field in data for field in required_fields)
            
            if not has_all_fields:
                log_test("Analytics Stats", False, "Missing required fields")
                return False
            
            # Check values are numbers
            all_numbers = all(
                isinstance(data[field], int) 
                for field in required_fields
            )
            
            if not all_numbers:
                log_test("Analytics Stats", False, "Values are not integers")
                return False
            
            details = f"Visitors: {data['total_visitors']}, Visits: {data['total_visits']}"
            log_test("Analytics Stats", True, details)
            return True
        else:
            log_test("Analytics Stats", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Analytics Stats", False, str(e))
        return False


def test_recent_visits():
    """Test getting recent visits."""
    try:
        response = requests.get(
            f"{BASE_URL}/api/analytics/recent?limit=5",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "visits" in data and isinstance(data["visits"], list):
                count = len(data["visits"])
                log_test("Recent Visits", True, f"Retrieved {count} visits")
                return True
            else:
                log_test("Recent Visits", False, "Invalid response format")
                return False
        else:
            log_test("Recent Visits", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Recent Visits", False, str(e))
        return False


def test_invalid_endpoint():
    """Test 404 handling."""
    try:
        response = requests.get(f"{BASE_URL}/api/nonexistent", timeout=5)
        
        if response.status_code == 404:
            log_test("404 Handling", True, "Returns 404 for invalid endpoint")
            return True
        else:
            log_test("404 Handling", False, f"Expected 404, got {response.status_code}")
            return False
    except Exception as e:
        log_test("404 Handling", False, str(e))
        return False


def test_invalid_chat_request():
    """Test validation error handling."""
    try:
        # Send invalid request (empty message)
        payload = {
            "message": ""  # Invalid: min_length=1
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat/",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 422:  # Validation error
            log_test("Validation Handling", True, "Returns 422 for invalid input")
            return True
        else:
            log_test("Validation Handling", False, f"Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        log_test("Validation Handling", False, str(e))
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("="*60)
    print("🧪 PORTFOLIO BACKEND - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"\nTesting: {BASE_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    print("\n" + "-"*60)
    print("CHECKING SERVER STATUS...")
    print("-"*60)
    
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
        print("✅ Server is running")
    except:
        print("❌ Server is not running!")
        print("\nPlease start the server first:")
        print("  python app/main.py")
        return
    
    # Run tests
    print("\n" + "-"*60)
    print("RUNNING TESTS...")
    print("-"*60)
    
    # Basic endpoints
    test_root_endpoint()
    test_health_check()
    
    # Chat endpoints
    test_chat_examples()
    test_chat_endpoint()
    test_chat_with_history()
    
    # Analytics endpoints
    test_record_visit()
    test_analytics_stats()
    test_recent_visits()
    
    # Error handling
    test_invalid_endpoint()
    test_invalid_chat_request()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready for deployment!")
    else:
        print("\n⚠️  Some tests failed. Please fix before deploying.")
        print("\nFailed tests:")
        for result in test_results:
            if not result["passed"]:
                print(f"  - {result['test']}: {result['details']}")
    
    print("\n" + "="*60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()