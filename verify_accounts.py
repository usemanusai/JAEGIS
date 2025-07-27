#!/usr/bin/env python3
"""
GitHub Account Verification Script
Verifies that all configured GitHub accounts have proper access and permissions
"""

import os
import sys
import asyncio
import aiohttp
import json
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


async def verify_account(session, account_name, token, username, target_repo="usemanusai/JAEGIS"):
    """Verify a single GitHub account."""
    
    print(f"\n{Fore.CYAN}🔍 Verifying {account_name} ({username})...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'JAEGIS-Account-Verifier/1.0'
    }
    
    results = {
        "account_name": account_name,
        "username": username,
        "token_valid": False,
        "user_info": None,
        "rate_limit": None,
        "repo_access": False,
        "repo_permissions": None,
        "errors": []
    }
    
    try:
        # Test 1: Verify token and get user info
        print(f"  {Fore.YELLOW}📋 Testing authentication...")
        async with session.get('https://api.github.com/user', headers=headers) as response:
            if response.status == 200:
                user_data = await response.json()
                results["token_valid"] = True
                results["user_info"] = {
                    "login": user_data.get("login"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "public_repos": user_data.get("public_repos"),
                    "private_repos": user_data.get("total_private_repos")
                }
                print(f"    {Fore.GREEN}✅ Authentication successful")
                print(f"    {Fore.WHITE}   User: {user_data.get('login')} ({user_data.get('name', 'No name')})")
                print(f"    {Fore.WHITE}   Public repos: {user_data.get('public_repos', 0)}")
                print(f"    {Fore.WHITE}   Private repos: {user_data.get('total_private_repos', 0)}")
            else:
                error_text = await response.text()
                results["errors"].append(f"Authentication failed: HTTP {response.status} - {error_text}")
                print(f"    {Fore.RED}❌ Authentication failed: HTTP {response.status}")
                return results
        
        # Test 2: Check rate limits
        print(f"  {Fore.YELLOW}⏱️  Checking rate limits...")
        async with session.get('https://api.github.com/rate_limit', headers=headers) as response:
            if response.status == 200:
                rate_data = await response.json()
                core_limit = rate_data.get("resources", {}).get("core", {})
                results["rate_limit"] = {
                    "limit": core_limit.get("limit"),
                    "remaining": core_limit.get("remaining"),
                    "reset": datetime.fromtimestamp(core_limit.get("reset", 0)).isoformat() if core_limit.get("reset") else None
                }
                print(f"    {Fore.GREEN}✅ Rate limit info retrieved")
                print(f"    {Fore.WHITE}   Limit: {core_limit.get('limit', 0)}/hour")
                print(f"    {Fore.WHITE}   Remaining: {core_limit.get('remaining', 0)}")
                
                if core_limit.get("remaining", 0) < 100:
                    print(f"    {Fore.YELLOW}⚠️  Warning: Low rate limit remaining")
            else:
                results["errors"].append(f"Rate limit check failed: HTTP {response.status}")
                print(f"    {Fore.YELLOW}⚠️  Could not check rate limits: HTTP {response.status}")
        
        # Test 3: Check repository access
        print(f"  {Fore.YELLOW}🏛️  Testing repository access...")
        repo_url = f'https://api.github.com/repos/{target_repo}'
        async with session.get(repo_url, headers=headers) as response:
            if response.status == 200:
                repo_data = await response.json()
                results["repo_access"] = True
                results["repo_permissions"] = repo_data.get("permissions", {})
                
                permissions = repo_data.get("permissions", {})
                print(f"    {Fore.GREEN}✅ Repository access confirmed")
                print(f"    {Fore.WHITE}   Repository: {repo_data.get('full_name')}")
                print(f"    {Fore.WHITE}   Private: {repo_data.get('private', False)}")
                print(f"    {Fore.WHITE}   Permissions:")
                print(f"    {Fore.WHITE}     - Read: {permissions.get('pull', False)}")
                print(f"    {Fore.WHITE}     - Write: {permissions.get('push', False)}")
                print(f"    {Fore.WHITE}     - Admin: {permissions.get('admin', False)}")
                
                if not permissions.get('push', False):
                    results["errors"].append("No write (push) permission to repository")
                    print(f"    {Fore.RED}❌ No write permission! Add account as collaborator.")
                
            elif response.status == 404:
                results["errors"].append("Repository not found or no access")
                print(f"    {Fore.RED}❌ Repository not found or no access")
            else:
                error_text = await response.text()
                results["errors"].append(f"Repository access failed: HTTP {response.status} - {error_text}")
                print(f"    {Fore.RED}❌ Repository access failed: HTTP {response.status}")
        
        # Test 4: Test file upload capability (dry run)
        print(f"  {Fore.YELLOW}📤 Testing upload capability...")
        test_content = "# Test file for JAEGIS multi-account upload verification"
        import base64
        encoded_content = base64.b64encode(test_content.encode()).decode()
        
        test_file_path = f"test_upload_verification_{account_name}_{int(datetime.now().timestamp())}.md"
        upload_url = f'https://api.github.com/repos/{target_repo}/contents/{test_file_path}'
        
        upload_data = {
            'message': f'test: Upload verification for {account_name}',
            'content': encoded_content,
            'branch': 'main'
        }
        
        # Note: We're not actually uploading, just checking if we could
        print(f"    {Fore.CYAN}ℹ️  Upload test skipped (dry run mode)")
        print(f"    {Fore.WHITE}   Would upload to: {test_file_path}")
        
    except Exception as e:
        results["errors"].append(f"Verification exception: {str(e)}")
        print(f"    {Fore.RED}❌ Verification failed with exception: {e}")
    
    return results


async def main():
    """Main verification function."""
    
    print(f"{Fore.MAGENTA}🔐 GITHUB ACCOUNT VERIFICATION")
    print(f"{Fore.MAGENTA}{'='*50}")
    
    # Collect account information
    accounts = []
    
    # Account 1 (Primary)
    token1 = os.getenv('GITHUB_TOKEN_1') or os.getenv('GITHUB_TOKEN')
    if token1:
        accounts.append({
            "name": "Primary Account",
            "token": token1,
            "username": os.getenv('GITHUB_USERNAME_1', 'usemanusai')
        })
    
    # Account 2
    token2 = os.getenv('GITHUB_TOKEN_2')
    if token2:
        accounts.append({
            "name": "Secondary Account",
            "token": token2,
            "username": os.getenv('GITHUB_USERNAME_2', 'account2')
        })
    
    # Account 3
    token3 = os.getenv('GITHUB_TOKEN_3')
    if token3:
        accounts.append({
            "name": "Tertiary Account",
            "token": token3,
            "username": os.getenv('GITHUB_USERNAME_3', 'account3')
        })
    
    # Account 4
    token4 = os.getenv('GITHUB_TOKEN_4')
    if token4:
        accounts.append({
            "name": "Quaternary Account",
            "token": token4,
            "username": os.getenv('GITHUB_USERNAME_4', 'account4')
        })
    
    if not accounts:
        print(f"{Fore.RED}❌ No GitHub tokens found!")
        print(f"{Fore.YELLOW}💡 Set environment variables:")
        print(f"   GITHUB_TOKEN_1=your_first_token")
        print(f"   GITHUB_TOKEN_2=your_second_token")
        print(f"   GITHUB_TOKEN_3=your_third_token")
        print(f"   GITHUB_TOKEN_4=your_fourth_token")
        sys.exit(1)
    
    print(f"{Fore.GREEN}📋 Found {len(accounts)} configured accounts")
    
    target_repo = f"{os.getenv('GITHUB_OWNER', 'usemanusai')}/{os.getenv('GITHUB_REPO', 'JAEGIS')}"
    print(f"{Fore.CYAN}🎯 Target repository: {target_repo}")
    
    # Verify all accounts
    results = []
    
    async with aiohttp.ClientSession() as session:
        for account in accounts:
            result = await verify_account(
                session, 
                account["name"], 
                account["token"], 
                account["username"],
                target_repo
            )
            results.append(result)
    
    # Summary report
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}📊 VERIFICATION SUMMARY")
    print(f"{Fore.CYAN}{'='*60}")
    
    valid_accounts = 0
    ready_accounts = 0
    
    for result in results:
        account_name = result["account_name"]
        
        if result["token_valid"] and result["repo_access"]:
            if not result["errors"]:
                status = f"{Fore.GREEN}✅ READY"
                ready_accounts += 1
            else:
                status = f"{Fore.YELLOW}⚠️  ISSUES"
            valid_accounts += 1
        else:
            status = f"{Fore.RED}❌ FAILED"
        
        print(f"\n{Fore.WHITE}{account_name}: {status}")
        
        if result["user_info"]:
            print(f"  Username: {result['user_info']['login']}")
        
        if result["rate_limit"]:
            remaining = result["rate_limit"]["remaining"]
            limit = result["rate_limit"]["limit"]
            print(f"  Rate Limit: {remaining}/{limit}")
        
        if result["repo_permissions"]:
            can_write = result["repo_permissions"].get("push", False)
            print(f"  Write Access: {'Yes' if can_write else 'No'}")
        
        if result["errors"]:
            print(f"  {Fore.RED}Issues:")
            for error in result["errors"]:
                print(f"    • {error}")
    
    # Final assessment
    print(f"\n{Fore.CYAN}🎯 FINAL ASSESSMENT:")
    print(f"  Total Accounts: {len(accounts)}")
    print(f"  Valid Accounts: {valid_accounts}")
    print(f"  Ready Accounts: {ready_accounts}")
    
    if ready_accounts >= 2:
        print(f"\n{Fore.GREEN}🚀 READY FOR MULTI-ACCOUNT UPLOAD!")
        print(f"  You have {ready_accounts} working accounts")
        print(f"  Expected rate limit: {ready_accounts * 5000} requests/hour")
        print(f"  Run: python multi_account_bulk_upload.py")
    elif ready_accounts == 1:
        print(f"\n{Fore.YELLOW}⚠️  SINGLE ACCOUNT ONLY")
        print(f"  Only 1 account is ready - you'll still hit rate limits")
        print(f"  Add more accounts as collaborators for better performance")
    else:
        print(f"\n{Fore.RED}❌ NOT READY")
        print(f"  No accounts are properly configured")
        print(f"  Fix the issues above before proceeding")
    
    # Save detailed results
    results_file = f"account_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n{Fore.CYAN}📄 Detailed results saved: {results_file}")


if __name__ == "__main__":
    asyncio.run(main())
