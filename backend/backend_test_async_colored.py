# backend_test_async_colored.py
import asyncio
import httpx
from colorama import Fore, Style, init

init(autoreset=True)

BASE_URL = "http://127.0.0.1:8000"
TEST_FARM_ID = 1  # You can change this later

TEST_USER = {
    "email": "admin@example.com",  # update with a real email from DB
    "password": "password123"
}

# --- Helper Functions ---
async def test_auth(client):
    print(f"{Fore.CYAN}Testing Auth...{Style.RESET_ALL}")
    try:
        response = await client.post(f"{BASE_URL}/auth/login", json=TEST_USER)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"{Fore.GREEN}✅ Auth login successful.{Style.RESET_ALL}")
            return token
        else:
            print(f"{Fore.RED}❌ Auth login failed:{Style.RESET_ALL}", response.text)
            return None
    except Exception as e:
        print(f"{Fore.RED}⚠️ Error during auth test:{Style.RESET_ALL}", e)
        return None


async def test_endpoint(client, token, path, label):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await client.get(f"{BASE_URL}/{path}/{TEST_FARM_ID}", headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ {label} OK{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ {label} failed:{Style.RESET_ALL}", response.text)
            return False
    except Exception as e:
        print(f"{Fore.RED}⚠️ Error testing {label}:{Style.RESET_ALL}", e)
        return False


async def main():
    async with httpx.AsyncClient(timeout=15.0) as client:
        token = await test_auth(client)
        if not token:
            print(f"{Fore.RED}Cannot proceed without a valid token.{Style.RESET_ALL}")
            return

        results = {
            "Dashboard": await test_endpoint(client, token, "summary", "Dashboard"),
            "Finance": await test_endpoint(client, token, "finance", "Finance"),
            "Crops": await test_endpoint(client, token, "crops", "Crops")
        }

        print("\n" + Fore.YELLOW + "-" * 40)
        print(" TEST SUMMARY ".center(40, "-"))
        print("-" * 40 + Style.RESET_ALL)
        for name, passed in results.items():
            color = Fore.GREEN if passed else Fore.RED
            status = "PASSED" if passed else "FAILED"
            print(f"{name:<15}: {color}{status}{Style.RESET_ALL}")
        print(Fore.YELLOW + "-" * 40 + Style.RESET_ALL)

if __name__ == "__main__":
    asyncio.run(main())
