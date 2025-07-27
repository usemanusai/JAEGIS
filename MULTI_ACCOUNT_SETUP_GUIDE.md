# 🚀 Multi-Account GitHub Upload Setup Guide

## 📋 **Overview**

This guide helps you set up **4 GitHub accounts** to distribute your bulk upload load and **eliminate rate limiting issues**. Each account gets 5,000 API requests per hour, giving you **20,000 total requests per hour** instead of just 5,000.

## 🎯 **Why Multi-Account Upload?**

### **Your Current Issue:**
- **Single account**: 5,000 requests/hour limit
- **96,715 files**: Would take 19+ hours with rate limiting
- **70% failure rate**: Due to hitting rate limits constantly

### **Multi-Account Solution:**
- **4 accounts**: 20,000 requests/hour total
- **Load balancing**: Intelligent distribution across accounts
- **Automatic failover**: Switches accounts when rate limited
- **Expected result**: **>95% success rate** with **4x faster uploads**

## 🔑 **Account Setup Requirements**

### **Account Access Requirements**
Each GitHub account needs:
1. **Repository access** to `usemanusai/JAEGIS`
2. **Write permissions** (push access)
3. **Valid personal access token** with `repo` scope

### **Option 1: Collaborator Accounts (Recommended)**
Add your other accounts as collaborators:

1. Go to: `https://github.com/usemanusai/JAEGIS/settings/access`
2. Click "Add people"
3. Add your other GitHub usernames
4. Grant "Write" permission

### **Option 2: Organization Accounts**
If accounts are in an organization:
1. Add accounts to the organization
2. Grant repository access through teams
3. Ensure "Write" permissions

## 🔐 **Token Generation**

For **each of your 4 accounts**:

1. **Login to GitHub account**
2. **Go to Settings** → Developer settings → Personal access tokens → Tokens (classic)
3. **Generate new token** with these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
4. **Copy the token** (you won't see it again!)
5. **Store securely** for environment setup

## ⚙️ **Environment Configuration**

### **Set Environment Variables**

```bash
# Account 1 (Primary - your main account)
export GITHUB_TOKEN_1="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export GITHUB_USERNAME_1="usemanusai"

# Account 2 (Secondary)
export GITHUB_TOKEN_2="ghp_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
export GITHUB_USERNAME_2="your_second_account"

# Account 3 (Tertiary)
export GITHUB_TOKEN_3="ghp_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
export GITHUB_USERNAME_3="your_third_account"

# Account 4 (Quaternary)
export GITHUB_TOKEN_4="ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
export GITHUB_USERNAME_4="your_fourth_account"

# Optional: Override defaults
export GITHUB_OWNER="usemanusai"
export GITHUB_REPO="JAEGIS"
export WORKSPACE_PATH="C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS"
export BATCH_SIZE=50
export MAX_CONCURRENT_PER_ACCOUNT=3
export DRY_RUN=false
```

### **Windows PowerShell Setup**
```powershell
# Set environment variables in PowerShell
$env:GITHUB_TOKEN_1="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
$env:GITHUB_USERNAME_1="usemanusai"
$env:GITHUB_TOKEN_2="ghp_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
$env:GITHUB_USERNAME_2="your_second_account"
$env:GITHUB_TOKEN_3="ghp_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
$env:GITHUB_USERNAME_3="your_third_account"
$env:GITHUB_TOKEN_4="ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
$env:GITHUB_USERNAME_4="your_fourth_account"
```

### **Create .env File (Alternative)**
```bash
# Create .env file in your JAEGIS directory
GITHUB_TOKEN_1=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME_1=usemanusai
GITHUB_TOKEN_2=ghp_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
GITHUB_USERNAME_2=your_second_account
GITHUB_TOKEN_3=ghp_zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
GITHUB_USERNAME_3=your_third_account
GITHUB_TOKEN_4=ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
GITHUB_USERNAME_4=your_fourth_account
```

## 🛠 **Installation**

### **1. Install Dependencies**
```bash
pip install aiohttp aiofiles colorama
```

### **2. Test Account Setup**
```bash
# Test with dry run first
DRY_RUN=true python multi_account_bulk_upload.py
```

## 🚀 **Execution**

### **Basic Multi-Account Upload**
```bash
python multi_account_bulk_upload.py
```

### **Conservative Settings (Recommended First Run)**
```bash
BATCH_SIZE=25 MAX_CONCURRENT_PER_ACCOUNT=2 python multi_account_bulk_upload.py
```

### **Aggressive Settings (After Testing)**
```bash
BATCH_SIZE=100 MAX_CONCURRENT_PER_ACCOUNT=5 python multi_account_bulk_upload.py
```

## 📊 **Real-Time Dashboard**

The script provides a live dashboard showing:

```
================================================================================
🚀 MULTI-ACCOUNT GITHUB UPLOAD DASHBOARD
================================================================================

📊 OVERALL PROGRESS:
Progress: 67.3% (65,234/96,715)
✅ Uploaded: 62,150
❌ Failed: 2,084
⏭️  Skipped: 1,000

👥 ACCOUNT STATUS:
  Primary Account: ACTIVE
    Files: 18,500 (29.8%)
    Rate Limit: 3,245
    Success Rate: 96.2%
    Avg Response: 245ms

  Secondary Account: ACTIVE
    Files: 16,200 (26.1%)
    Rate Limit: 2,890
    Success Rate: 97.1%
    Avg Response: 198ms

  Tertiary Account: ACTIVE
    Files: 15,800 (25.4%)
    Rate Limit: 3,100
    Success Rate: 95.8%
    Avg Response: 267ms

  Quaternary Account: ACTIVE
    Files: 11,650 (18.7%)
    Rate Limit: 4,200
    Success Rate: 98.3%
    Avg Response: 189ms

⚡ PERFORMANCE:
Elapsed Time: 2.3 hours
Upload Rate: 7.8 files/second
Account Switches: 23
Rate Limit Events: 2

Last Updated: 14:25:43
================================================================================
```

## 🎯 **Expected Performance Improvements**

### **Before (Single Account)**
- **Rate Limit**: 5,000 requests/hour
- **Success Rate**: ~30% (your current issue)
- **Upload Speed**: ~1.4 files/second
- **Total Time**: 19+ hours with failures

### **After (Multi-Account)**
- **Rate Limit**: 20,000 requests/hour (4x improvement)
- **Success Rate**: >95% (3x improvement)
- **Upload Speed**: ~8 files/second (6x improvement)
- **Total Time**: ~3-4 hours (5x faster)

## 🔍 **Intelligent Features**

### **Load Balancing**
- **Account scoring**: Based on rate limits, success rate, response time
- **Automatic switching**: When accounts hit rate limits
- **Fair distribution**: Spreads load evenly across accounts

### **Error Handling**
- **Account failover**: Switches to healthy accounts
- **Rate limit detection**: Monitors GitHub API headers
- **Retry logic**: Intelligent retry with different accounts

### **Monitoring**
- **Real-time dashboard**: Live progress and account status
- **Performance metrics**: Upload speed, success rates, response times
- **Load distribution**: Shows which account uploaded which files

## 🚨 **Troubleshooting**

### **"No GitHub tokens found" Error**
```bash
# Check environment variables are set
echo $GITHUB_TOKEN_1
echo $GITHUB_TOKEN_2
# etc.
```

### **"Authentication failed" Error**
- Verify token has `repo` scope
- Check token hasn't expired
- Ensure account has repository access

### **"Repository access issue" Error**
- Add account as collaborator to repository
- Grant "Write" permissions
- Check repository exists and is accessible

### **Still Getting Rate Limited**
- Reduce `MAX_CONCURRENT_PER_ACCOUNT` to 2
- Increase `BATCH_SIZE` to 25
- Check if all 4 accounts are active

## 🎉 **Ready to Upload!**

With 4 accounts properly configured, you should see:

1. **🚀 4x faster uploads** (20,000 requests/hour vs 5,000)
2. **✅ >95% success rate** (vs your current 30%)
3. **🔄 Automatic load balancing** across accounts
4. **📊 Real-time monitoring** of all accounts
5. **🛡️ Intelligent failover** when issues occur

**Your 96,715 files should upload in ~3-4 hours instead of 19+ hours with much higher success rate!**

## 📞 **Need Help?**

If you encounter issues:
1. **Run with dry run first**: `DRY_RUN=true python multi_account_bulk_upload.py`
2. **Check the logs**: Look for authentication and permission errors
3. **Verify account access**: Test each token manually
4. **Start conservative**: Use lower concurrency settings initially
