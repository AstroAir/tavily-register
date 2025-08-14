# Examples

This section provides practical examples and code samples for using Tavily Register in various scenarios. From basic usage to advanced automation workflows, these examples will help you get the most out of the tool.

## Example Categories

<div class="grid cards" markdown>

-   :material-play:{ .lg .middle } **Basic Examples**

    ---

    Simple usage patterns for getting started

    [:octicons-arrow-right-24: Basic Examples](basic.md)

-   :material-cog:{ .lg .middle } **Advanced Examples**

    ---

    Complex workflows and automation patterns

    [:octicons-arrow-right-24: Advanced Examples](advanced.md)

-   :material-settings:{ .lg .middle } **Configuration Examples**

    ---

    Custom configurations for different environments

    [:octicons-arrow-right-24: Configuration Examples](configurations.md)

</div>

## Quick Start Examples

### Single API Key Registration

The simplest way to get an API key:

```python
#!/usr/bin/env python3
"""Simple API key registration example."""

from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def main():
    # Create automation instance
    automation = IntelligentTavilyAutomation()
    
    try:
        print("🚀 Starting API key registration...")
        
        # Run the automation
        success = automation.run_automation()
        
        if success:
            print(f"✅ Success!")
            print(f"📧 Email: {automation.email}")
            print(f"🔑 API Key: {automation.api_key}")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Always clean up
        automation.close_browser()

if __name__ == "__main__":
    main()
```

### Command Line Usage

Using the main application interface:

```bash
# Interactive mode
python main.py

# Follow the prompts:
# 1. Choose "智能自动化模式 (推荐)"
# 2. Wait for completion
# 3. Check api_keys.md for results
```

### Environment Configuration

Set up your environment for automation:

```bash
# Create .env file
cat > .env << EOF
EMAIL_PREFIX=example_user
BROWSER_TYPE=firefox
HEADLESS=false
DEBUG=true
EOF

# Run automation
python main.py
```

## Common Use Cases

### Development Workflow

Perfect for developers who need API keys for testing:

```python
#!/usr/bin/env python3
"""Development workflow example."""

import os
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def get_dev_api_key(project_name):
    """Get API key for development project."""
    
    # Use project name as email prefix
    email_prefix = f"dev_{project_name}_{os.getenv('USER', 'unknown')}"
    
    automation = IntelligentTavilyAutomation(email_prefix=email_prefix)
    
    try:
        print(f"🔧 Getting API key for project: {project_name}")
        
        success = automation.run_automation()
        
        if success:
            # Save to project-specific file
            with open(f"{project_name}_api_key.txt", "w") as f:
                f.write(f"EMAIL={automation.email}\n")
                f.write(f"API_KEY={automation.api_key}\n")
            
            print(f"✅ API key saved to {project_name}_api_key.txt")
            return automation.api_key
        else:
            print("❌ Failed to get API key")
            return None
            
    finally:
        automation.close_browser()

# Usage
if __name__ == "__main__":
    import sys
    project = sys.argv[1] if len(sys.argv) > 1 else "my_project"
    api_key = get_dev_api_key(project)
```

### Batch Registration

Register multiple API keys for different purposes:

```python
#!/usr/bin/env python3
"""Batch registration example."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def register_single_key(prefix):
    """Register a single API key."""
    automation = IntelligentTavilyAutomation(email_prefix=prefix)
    
    try:
        success = automation.run_automation()
        
        if success:
            return {
                'prefix': prefix,
                'email': automation.email,
                'api_key': automation.api_key,
                'success': True
            }
        else:
            return {
                'prefix': prefix,
                'success': False,
                'error': 'Registration failed'
            }
            
    except Exception as e:
        return {
            'prefix': prefix,
            'success': False,
            'error': str(e)
        }
    finally:
        automation.close_browser()

def batch_register(prefixes, max_workers=3):
    """Register multiple API keys concurrently."""
    results = []
    
    print(f"🚀 Starting batch registration for {len(prefixes)} keys...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_prefix = {
            executor.submit(register_single_key, prefix): prefix 
            for prefix in prefixes
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_prefix):
            prefix = future_to_prefix[future]
            try:
                result = future.result()
                results.append(result)
                
                if result['success']:
                    print(f"✅ {prefix}: {result['api_key']}")
                else:
                    print(f"❌ {prefix}: {result['error']}")
                    
            except Exception as e:
                print(f"❌ {prefix}: Exception - {e}")
                results.append({
                    'prefix': prefix,
                    'success': False,
                    'error': str(e)
                })
    
    return results

# Usage example
if __name__ == "__main__":
    # Define prefixes for different projects
    prefixes = [
        "project_alpha",
        "project_beta", 
        "project_gamma",
        "testing_env",
        "staging_env"
    ]
    
    # Register all keys
    results = batch_register(prefixes, max_workers=2)
    
    # Summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n📊 Summary:")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n🔑 API Keys:")
        for result in successful:
            print(f"  {result['prefix']}: {result['api_key']}")
```

### CI/CD Integration

Integrate with continuous integration pipelines:

```python
#!/usr/bin/env python3
"""CI/CD integration example."""

import os
import sys
import json
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def ci_register_api_key():
    """Register API key in CI/CD environment."""
    
    # Get CI environment info
    ci_provider = os.getenv('CI_PROVIDER', 'unknown')
    build_id = os.getenv('BUILD_ID', os.getenv('GITHUB_RUN_ID', 'local'))
    branch = os.getenv('BRANCH', os.getenv('GITHUB_REF_NAME', 'main'))
    
    # Create unique prefix for CI
    email_prefix = f"ci_{ci_provider}_{branch}_{build_id}"
    
    automation = IntelligentTavilyAutomation(email_prefix=email_prefix)
    
    try:
        print(f"🔄 CI/CD API Key Registration")
        print(f"   Provider: {ci_provider}")
        print(f"   Build ID: {build_id}")
        print(f"   Branch: {branch}")
        print(f"   Email Prefix: {email_prefix}")
        
        success = automation.run_automation()
        
        if success:
            # Output for CI/CD consumption
            result = {
                'success': True,
                'email': automation.email,
                'api_key': automation.api_key,
                'prefix': email_prefix,
                'ci_info': {
                    'provider': ci_provider,
                    'build_id': build_id,
                    'branch': branch
                }
            }
            
            # Save to CI artifacts
            with open('api_key_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            
            # Set environment variable for subsequent steps
            if ci_provider == 'github':
                print(f"::set-output name=api_key::{automation.api_key}")
                print(f"::set-output name=email::{automation.email}")
            
            print(f"✅ API Key registered successfully")
            print(f"🔑 API Key: {automation.api_key}")
            
            return 0
        else:
            print("❌ API Key registration failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        automation.close_browser()

if __name__ == "__main__":
    sys.exit(ci_register_api_key())
```

### Testing and Validation

Example for testing the automation:

```python
#!/usr/bin/env python3
"""Testing and validation example."""

import pytest
from unittest.mock import Mock, patch
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

class TestTavilyAutomation:
    """Test cases for Tavily automation."""
    
    def test_initialization(self):
        """Test automation initialization."""
        automation = IntelligentTavilyAutomation()
        assert automation is not None
        assert automation.email_prefix is not None
    
    def test_custom_prefix(self):
        """Test custom email prefix."""
        custom_prefix = "test_prefix"
        automation = IntelligentTavilyAutomation(email_prefix=custom_prefix)
        assert automation.email_prefix == custom_prefix
    
    @patch('src.tavily_register.core.intelligent_automation.sync_playwright')
    def test_browser_start(self, mock_playwright):
        """Test browser startup."""
        mock_browser = Mock()
        mock_playwright.return_value.__enter__.return_value.firefox.launch.return_value = mock_browser
        
        automation = IntelligentTavilyAutomation()
        automation.start_browser()
        
        # Verify browser was launched
        mock_playwright.return_value.__enter__.return_value.firefox.launch.assert_called_once()
    
    def test_email_generation(self):
        """Test email generation."""
        automation = IntelligentTavilyAutomation(email_prefix="test")
        email = automation.email
        
        assert "@2925.com" in email
        assert email.startswith("test")
    
    @pytest.mark.integration
    def test_full_automation(self):
        """Integration test for full automation."""
        # Note: This requires actual browser and network access
        automation = IntelligentTavilyAutomation(email_prefix="integration_test")
        
        try:
            # This would run actual automation
            # result = automation.run_automation()
            # assert isinstance(result, bool)
            pass
        finally:
            automation.close_browser()

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## Interactive Examples

### Jupyter Notebook Integration

Use Tavily Register in Jupyter notebooks:

```python
# Cell 1: Setup
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
import pandas as pd

# Cell 2: Register API Key
automation = IntelligentTavilyAutomation(email_prefix="notebook_demo")

try:
    success = automation.run_automation()
    if success:
        print(f"✅ API Key: {automation.api_key}")
        api_key = automation.api_key
    else:
        print("❌ Registration failed")
        api_key = None
finally:
    automation.close_browser()

# Cell 3: Use API Key
if api_key:
    # Use the API key for your research/analysis
    print(f"Using API key: {api_key}")
    # Your Tavily API calls here...
```

### Web Dashboard Integration

Example for web applications:

```python
#!/usr/bin/env python3
"""Web dashboard integration example."""

from flask import Flask, request, jsonify
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
import threading
import uuid

app = Flask(__name__)
registration_status = {}

def background_registration(task_id, email_prefix):
    """Run registration in background."""
    try:
        registration_status[task_id] = {'status': 'running', 'progress': 0}
        
        automation = IntelligentTavilyAutomation(email_prefix=email_prefix)
        
        registration_status[task_id]['progress'] = 25
        success = automation.run_automation()
        
        if success:
            registration_status[task_id] = {
                'status': 'completed',
                'progress': 100,
                'api_key': automation.api_key,
                'email': automation.email
            }
        else:
            registration_status[task_id] = {
                'status': 'failed',
                'progress': 0,
                'error': 'Registration failed'
            }
            
    except Exception as e:
        registration_status[task_id] = {
            'status': 'failed',
            'progress': 0,
            'error': str(e)
        }
    finally:
        automation.close_browser()

@app.route('/register', methods=['POST'])
def register_api_key():
    """Start API key registration."""
    data = request.json
    email_prefix = data.get('email_prefix')
    
    if not email_prefix:
        return jsonify({'error': 'email_prefix required'}), 400
    
    task_id = str(uuid.uuid4())
    
    # Start background task
    thread = threading.Thread(
        target=background_registration,
        args=(task_id, email_prefix)
    )
    thread.start()
    
    return jsonify({'task_id': task_id, 'status': 'started'})

@app.route('/status/<task_id>')
def get_status(task_id):
    """Get registration status."""
    status = registration_status.get(task_id, {'status': 'not_found'})
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)
```

## Next Steps

Explore more examples:

- [Basic Examples](basic.md) - Simple usage patterns
- [Advanced Examples](advanced.md) - Complex workflows
- [Configuration Examples](configurations.md) - Environment setups

Or dive deeper into the documentation:

- [API Reference](../api/index.md) - Complete API documentation
- [User Guide](../user-guide/index.md) - Comprehensive usage guide
- [Troubleshooting](../troubleshooting/index.md) - Problem solving
