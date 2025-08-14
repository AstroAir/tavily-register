"""
Test fixtures and sample data for Tavily Register tests.

This module provides reusable test data, mock objects, and fixtures
for testing the automation system.
"""
import json
from datetime import datetime
from typing import Dict, List, Any


# Sample email data
SAMPLE_EMAILS = [
    {
        "sender": "noreply@tavily.com",
        "subject": "Verify your email address",
        "body": "Please click the following link to verify your email: https://app.tavily.com/verify?token=abc123",
        "timestamp": "2025-01-01 12:00:00",
        "is_unread": True
    },
    {
        "sender": "support@tavily.com", 
        "subject": "Welcome to Tavily",
        "body": "Welcome to Tavily! Your account has been created successfully.",
        "timestamp": "2025-01-01 12:05:00",
        "is_unread": False
    },
    {
        "sender": "notifications@2925.com",
        "subject": "New message in your inbox",
        "body": "You have received a new message from Tavily.",
        "timestamp": "2025-01-01 12:10:00",
        "is_unread": True
    }
]

# Sample cookie data
SAMPLE_COOKIES = [
    {
        "name": "session_id",
        "value": "abc123def456",
        "domain": "2925.com",
        "path": "/",
        "expires": 1735689600,  # 2025-01-01
        "httpOnly": True,
        "secure": True
    },
    {
        "name": "aut",
        "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdEAyOTI1LmNvbSIsIm5pY2tuYW1lIjoidGVzdCIsImV4cCI6MTczNTY4OTYwMH0.signature",
        "domain": "2925.com",
        "path": "/",
        "expires": 1735689600,
        "httpOnly": False,
        "secure": True
    },
    {
        "name": "preferences",
        "value": "lang=en&theme=light",
        "domain": "2925.com",
        "path": "/",
        "expires": 1735689600,
        "httpOnly": False,
        "secure": False
    }
]

# Sample API responses
SAMPLE_API_RESPONSES = {
    "tavily_signup_success": {
        "status": "success",
        "message": "Account created successfully",
        "user_id": "user_123456",
        "email": "test@2925.com"
    },
    "tavily_login_success": {
        "status": "success",
        "message": "Login successful",
        "api_key": "tvly-dev-abc123def456ghi789",
        "user_id": "user_123456"
    },
    "email_verification_success": {
        "status": "verified",
        "message": "Email verified successfully",
        "redirect_url": "https://app.tavily.com/dashboard"
    }
}

# Sample HTML content
SAMPLE_HTML_CONTENT = {
    "tavily_signup_page": """
    <html>
    <body>
        <form class="_form-signup-id">
            <input id="email" name="email" type="text" autocomplete="email" placeholder="Email address">
            <input id="password" name="password" type="password" placeholder="Password">
            <button type="submit">Sign up</button>
        </form>
        <p>Already have an account? <a href="/login">Sign in</a></p>
    </body>
    </html>
    """,
    
    "tavily_dashboard": """
    <html>
    <body>
        <div class="dashboard">
            <h1>Welcome to Tavily</h1>
            <div class="api-key-section">
                <label>Your API Key:</label>
                <code id="api-key">tvly-dev-abc123def456ghi789</code>
                <button onclick="copyApiKey()">Copy</button>
            </div>
        </div>
    </body>
    </html>
    """,
    
    "email_inbox": """
    <html>
    <body>
        <div class="email-list">
            <div class="email-row unread">
                <svg class="svg-common icon-svg-small">
                    <use xlink:href="#unread_mail"></use>
                </svg>
                <span class="sender">noreply@tavily.com</span>
                <span class="subject">Verify your email address</span>
                <span class="time">12:00</span>
            </div>
            <div class="email-row read">
                <svg class="svg-common icon-svg-small">
                    <use xlink:href="#read_mail"></use>
                </svg>
                <span class="sender">support@tavily.com</span>
                <span class="subject">Welcome to Tavily</span>
                <span class="time">11:30</span>
            </div>
        </div>
    </body>
    </html>
    """
}

# Sample configuration data
SAMPLE_CONFIGS = {
    "test_config": {
        "EMAIL_PREFIX": "test_user",
        "EMAIL_DOMAIN": "2925.com",
        "BROWSER_TYPE": "firefox",
        "HEADLESS": True,
        "WAIT_TIME_SHORT": 1,
        "WAIT_TIME_MEDIUM": 3,
        "WAIT_TIME_LONG": 5,
        "API_KEYS_FILE": "test_api_keys.md",
        "COOKIES_FILE": "test_cookies.json"
    },
    "production_config": {
        "EMAIL_PREFIX": "prod_user",
        "EMAIL_DOMAIN": "2925.com",
        "BROWSER_TYPE": "chromium",
        "HEADLESS": False,
        "WAIT_TIME_SHORT": 2,
        "WAIT_TIME_MEDIUM": 5,
        "WAIT_TIME_LONG": 10,
        "API_KEYS_FILE": "api_keys.md",
        "COOKIES_FILE": "email_cookies.json"
    }
}

# Sample automation results
SAMPLE_AUTOMATION_RESULTS = [
    {
        "email": "test1@2925.com",
        "password": "TavilyAuto123!",
        "api_key": "tvly-dev-abc123def456",
        "timestamp": "2025-01-01 12:00:00",
        "success": True,
        "duration": 45.2
    },
    {
        "email": "test2@2925.com",
        "password": "TavilyAuto123!",
        "api_key": "tvly-dev-ghi789jkl012",
        "timestamp": "2025-01-01 12:05:00",
        "success": True,
        "duration": 38.7
    },
    {
        "email": "test3@2925.com",
        "password": "TavilyAuto123!",
        "api_key": None,
        "timestamp": "2025-01-01 12:10:00",
        "success": False,
        "duration": 60.0,
        "error": "Email verification timeout"
    }
]


def get_sample_email_by_type(email_type: str) -> Dict[str, Any]:
    """Get sample email data by type."""
    email_map = {
        "verification": SAMPLE_EMAILS[0],
        "welcome": SAMPLE_EMAILS[1],
        "notification": SAMPLE_EMAILS[2]
    }
    return email_map.get(email_type, SAMPLE_EMAILS[0])


def get_sample_cookies_for_domain(domain: str) -> List[Dict[str, Any]]:
    """Get sample cookies filtered by domain."""
    return [cookie for cookie in SAMPLE_COOKIES if cookie["domain"] == domain]


def get_sample_html(page_type: str) -> str:
    """Get sample HTML content by page type."""
    return SAMPLE_HTML_CONTENT.get(page_type, "")


def create_mock_api_response(response_type: str, **kwargs: Any) -> Dict[str, Any]:
    """Create mock API response with optional overrides."""
    base_response = SAMPLE_API_RESPONSES.get(response_type, {})
    base_response.update(kwargs)
    return base_response


def generate_test_email_data(count: int = 5) -> List[Dict[str, Any]]:
    """Generate multiple test email entries."""
    emails = []
    for i in range(count):
        email = {
            "email": f"test{i+1}@2925.com",
            "password": "TavilyAuto123!",
            "api_key": f"tvly-dev-test{i+1:03d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "success": True
        }
        emails.append(email)
    return emails


def save_sample_data_to_file(filename: str, data_type: str) -> None:
    """Save sample data to JSON file for testing."""
    data_map = {
        "emails": SAMPLE_EMAILS,
        "cookies": SAMPLE_COOKIES,
        "api_responses": SAMPLE_API_RESPONSES,
        "configs": SAMPLE_CONFIGS,
        "results": SAMPLE_AUTOMATION_RESULTS
    }
    
    data = data_map.get(data_type, {})
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Test selectors for web automation
TEST_SELECTORS = {
    "tavily_signup": {
        "email_input": "#email",
        "password_input": "#password", 
        "signup_button": "button[type='submit']",
        "login_link": "a[href='/login']"
    },
    "tavily_dashboard": {
        "api_key_element": "#api-key",
        "copy_button": "button:has-text('Copy')",
        "welcome_heading": "h1:has-text('Welcome')"
    },
    "email_inbox": {
        "email_rows": ".email-row",
        "unread_emails": ".email-row.unread",
        "sender_elements": ".sender",
        "subject_elements": ".subject"
    }
}


# Mock browser responses
MOCK_BROWSER_RESPONSES = {
    "page_load_success": {"status": "success", "url": "https://app.tavily.com"},
    "element_found": {"status": "found", "element": "mock_element"},
    "element_not_found": {"status": "not_found", "element": None},
    "click_success": {"status": "clicked", "element": "button"},
    "type_success": {"status": "typed", "text": "test@example.com"}
}
