# backend_test.py
import requests

BASE_URL = "http://127.0.0.1:8000"
TEST_FARM_ID = 1  # Change this to match a real farm in your database

def test_auth():
    print("Testing Auth...")
    # Use email instead of username
    data = {"email": "admin@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Auth login successful.")
        return token
    else:
        print("❌ Auth login failed:", response.text)
        return None

def test_dashboard(token):
    print("Testing Dashboard Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/summary/{TEST_FARM_ID}", headers=headers)
    if response.status_code == 200:
        print("✅ Dashboard data fetched successfully.")
        print("Sample keys:", list(response.json().keys()))
    else:
        print("❌ Dashboard fetch failed:", response.text)

def test_finance(token):
    print("Testing Finance Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/finance/{TEST_FARM_ID}", headers=headers)
    if response.status_code == 200:
        print("✅ Finance data fetched successfully.")
    else:
        print("❌ Finance fetch failed:", response.text)

def test_crops(token):
    print("Testing Crop / Agronomy Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/crops/{TEST_FARM_ID}", headers=headers)
    if response.status_code == 200:
        print("✅ Crop data fetched successfully.")
    else:
        print("❌ Crop fetch failed:", response.text)

def main():
    token = test_auth()
    if not token:
        print("Cannot proceed without a valid auth token.")
        return

    test_dashboard(token)
    test_finance(token)
    test_crops(token)
    print("\nAll basic backend tests complete.")

if __name__ == "__main__":
    main()
