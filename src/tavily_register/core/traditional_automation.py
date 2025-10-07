"""
Tavily Traditional Automation Module

Traditional automation approach for Tavily registration.
"""
import json
import time
from typing import Any, Optional, Dict, List, cast
from playwright.sync_api import sync_playwright, Playwright, Browser, Page
from ..config.settings import *
from ..utils.helpers import generate_email, wait_with_message, save_api_key


class TavilyAutomation:
    def __init__(self) -> None:
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.email: Optional[str] = None
        self.password: str = DEFAULT_PASSWORD
        self.html_log: List[Dict[str, Any]] = []  # 用于记录HTML信息
        self.email_prefix: Optional[str] = None  # 动态邮箱前缀

    def start_browser(self, headless: Optional[bool] = None) -> None:
        """启动浏览器"""
        self.playwright = sync_playwright().start()

        # 使用传入的headless参数，如果没有则使用配置文件的值
        headless_mode = headless if headless is not None else HEADLESS

        # 根据配置选择浏览器类型
        if BROWSER_TYPE == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=headless_mode)
        elif BROWSER_TYPE == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=headless_mode)
        else:  # chromium
            # 配置浏览器启动参数，解决macOS上的兼容性问题
            browser_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
            self.browser = self.playwright.chromium.launch(
                headless=headless_mode,
                args=browser_args
            )

        if self.browser:
            self.page = self.browser.new_page()
            self.page.set_default_timeout(BROWSER_TIMEOUT)

    def collect_element_info(self, element: Any, action_type: str, element_name: str) -> None:
        """收集元素的深层HTML信息"""
        try:
            # 收集当前元素的完整信息
            element_info = {
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'action_type': action_type,
                'element_name': element_name,
                'page_url': self.page.url if self.page else "",
                'page_title': self.page.title() if self.page else "",

                # 当前元素信息
                'current_element': self._get_detailed_element_info(element),

                # 父级元素信息（3层）
                'parent_hierarchy': self._get_parent_hierarchy(element, levels=3),

                # 兄弟元素信息
                'siblings_info': self._get_siblings_info(element),

                # 子元素信息
                'children_info': self._get_children_info(element),

                # 位置和上下文信息
                'position_context': self._get_position_context(element),

                # 表单上下文（如果在表单中）
                'form_context': self._get_form_context(element),

                # 完整的选择器路径
                'selector_paths': self._generate_selector_paths(element)
            }

            self.html_log.append(element_info)
            print(f"📋 收集深层HTML信息: {action_type} - {element_name}")
            if isinstance(element_info, dict) and 'current_element' in element_info:
                current_elem = element_info['current_element']
                if isinstance(current_elem, dict):
                    print(f"   标签: {current_elem.get('tag_name', 'N/A')}")
                    text_content = current_elem.get('text_content', '')
                    if isinstance(text_content, str):
                        print(f"   文本: {text_content[:50]}...")
                    attrs = current_elem.get('attributes', {})
                    if isinstance(attrs, dict):
                        print(f"   稳定属性: {self._get_stable_attributes(attrs)}")
                parent_hierarchy = element_info.get('parent_hierarchy', [])
                if parent_hierarchy is not None:
                    print(f"   父级层次: {len(parent_hierarchy)} 层")

        except Exception as e:
            print(f"⚠️ 收集HTML信息失败: {e}")

    def _get_detailed_element_info(self, element: Any) -> Dict[str, Any]:
        """获取元素的详细信息"""
        result = element.evaluate('''el => {
            const attrs = {};
            for (let attr of el.attributes) {
                attrs[attr.name] = attr.value;
            }

            return {
                tag_name: el.tagName.toLowerCase(),
                text_content: el.textContent ? el.textContent.trim() : '',
                inner_text: el.innerText ? el.innerText.trim() : '',
                inner_html: el.innerHTML.substring(0, 200),
                outer_html: el.outerHTML.substring(0, 300),
                attributes: attrs,
                computed_styles: {
                    display: getComputedStyle(el).display,
                    visibility: getComputedStyle(el).visibility,
                    position: getComputedStyle(el).position
                },
                properties: {
                    id: el.id,
                    className: el.className,
                    name: el.name,
                    type: el.type,
                    value: el.value,
                    placeholder: el.placeholder,
                    disabled: el.disabled,
                    readonly: el.readOnly,
                    required: el.required
                }
            };
        }''')
        return cast(Dict[str, Any], result)

    def _get_parent_hierarchy(self, element: Any, levels: int = 3) -> Optional[List[Any]]:
        """获取父级元素层次结构"""
        result = element.evaluate(f'''el => {{
            const hierarchy = [];
            let current = el.parentElement;
            let level = 0;

            while (current && level < {levels}) {{
                const attrs = {{}};
                for (let attr of current.attributes) {{
                    attrs[attr.name] = attr.value;
                }}

                hierarchy.push({{
                    level: level + 1,
                    tag_name: current.tagName.toLowerCase(),
                    attributes: attrs,
                    text_content: current.textContent ? current.textContent.trim().substring(0, 100) : '',
                    class_list: Array.from(current.classList),
                    id: current.id,
                    role: current.getAttribute('role'),
                    data_attributes: Object.fromEntries(
                        Array.from(current.attributes)
                            .filter(attr => attr.name.startsWith('data-'))
                            .map(attr => [attr.name, attr.value])
                    )
                }});

                current = current.parentElement;
                level++;
            }}

            return hierarchy;
        }}''')
        return cast(Optional[List[Any]], result)

    def _get_siblings_info(self, element: Any) -> Dict[str, Any]:
        """获取兄弟元素信息"""
        result = element.evaluate('''el => {
            const parent = el.parentElement;
            if (!parent) return null;

            const siblings = Array.from(parent.children);
            const currentIndex = siblings.indexOf(el);

            return {
                total_siblings: siblings.length,
                current_index: currentIndex,
                same_tag_siblings: siblings.filter(s => s.tagName === el.tagName).length,
                same_tag_index: siblings.filter(s => s.tagName === el.tagName).indexOf(el),
                previous_sibling: currentIndex > 0 ? {
                    tag_name: siblings[currentIndex - 1].tagName.toLowerCase(),
                    text_content: siblings[currentIndex - 1].textContent ? siblings[currentIndex - 1].textContent.trim().substring(0, 50) : '',
                    class_name: siblings[currentIndex - 1].className
                } : null,
                next_sibling: currentIndex < siblings.length - 1 ? {
                    tag_name: siblings[currentIndex + 1].tagName.toLowerCase(),
                    text_content: siblings[currentIndex + 1].textContent ? siblings[currentIndex + 1].textContent.trim().substring(0, 50) : '',
                    class_name: siblings[currentIndex + 1].className
                } : null
            };
        }''')
        return cast(Dict[str, Any], result)

    def _get_children_info(self, element: Any) -> Dict[str, Any]:
        """获取子元素信息"""
        result = element.evaluate('''el => {
            const children = Array.from(el.children);

            return {
                has_children: children.length > 0,
                children_count: children.length,
                children_tags: children.map(child => child.tagName.toLowerCase()),
                first_child: children.length > 0 ? {
                    tag_name: children[0].tagName.toLowerCase(),
                    text_content: children[0].textContent ? children[0].textContent.trim().substring(0, 50) : '',
                    class_name: children[0].className
                } : null
            };
        }''')
        return cast(Dict[str, Any], result)

    def _get_position_context(self, element: Any) -> Dict[str, Any]:
        """获取位置和上下文信息"""
        result = element.evaluate('''el => {
            const rect = el.getBoundingClientRect();

            return {
                bounding_rect: {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                },
                is_visible: rect.width > 0 && rect.height > 0,
                scroll_position: {
                    scrollTop: window.pageYOffset,
                    scrollLeft: window.pageXOffset
                },
                viewport_position: {
                    in_viewport: rect.top >= 0 && rect.left >= 0 &&
                                rect.bottom <= window.innerHeight &&
                                rect.right <= window.innerWidth
                }
            };
        }''')
        return cast(Dict[str, Any], result)

    def _get_form_context(self, element: Any) -> Optional[Dict[str, Any]]:
        """获取表单上下文信息"""
        result = element.evaluate('''el => {
            const form = el.closest('form');
            if (!form) return null;

            const formInputs = Array.from(form.querySelectorAll('input, select, textarea'));
            const currentIndex = formInputs.indexOf(el);

            return {
                form_exists: true,
                form_action: form.action,
                form_method: form.method,
                form_id: form.id,
                form_class: form.className,
                total_inputs: formInputs.length,
                current_input_index: currentIndex,
                input_types: formInputs.map(input => input.type || input.tagName.toLowerCase()),
                form_buttons: Array.from(form.querySelectorAll('button, input[type="submit"]')).map(btn => ({
                    type: btn.type,
                    text: btn.textContent ? btn.textContent.trim() : btn.value,
                    class_name: btn.className
                }))
            };
        }''')
        return cast(Optional[Dict[str, Any]], result)

    def _generate_selector_paths(self, element: Any) -> Dict[str, Any]:
        """生成多种选择器路径"""
        result = element.evaluate('''el => {
            // 生成CSS选择器路径
            function getCSSPath(element) {
                const path = [];
                let current = element;

                while (current && current.nodeType === Node.ELEMENT_NODE) {
                    let selector = current.tagName.toLowerCase();

                    if (current.id) {
                        selector += '#' + current.id;
                        path.unshift(selector);
                        break;
                    } else if (current.className) {
                        const classes = current.className.trim().split(/\\s+/);
                        if (classes.length > 0 && classes[0]) {
                            selector += '.' + classes[0];
                        }
                    }

                    // 添加nth-child选择器
                    const parent = current.parentElement;
                    if (parent) {
                        const siblings = Array.from(parent.children);
                        const index = siblings.indexOf(current) + 1;
                        selector += ':nth-child(' + index + ')';
                    }

                    path.unshift(selector);
                    current = current.parentElement;
                }

                return path.join(' > ');
            }

            // 生成XPath
            function getXPath(element) {
                const path = [];
                let current = element;

                while (current && current.nodeType === Node.ELEMENT_NODE) {
                    let index = 1;
                    let sibling = current.previousElementSibling;

                    while (sibling) {
                        if (sibling.tagName === current.tagName) {
                            index++;
                        }
                        sibling = sibling.previousElementSibling;
                    }

                    const tagName = current.tagName.toLowerCase();
                    path.unshift(tagName + '[' + index + ']');
                    current = current.parentElement;
                }

                return '//' + path.join('/');
            }

            return {
                css_path: getCSSPath(el),
                xpath: getXPath(el),
                simple_selectors: {
                    by_id: el.id ? '#' + el.id : null,
                    by_name: el.name ? '[name="' + el.name + '"]' : null,
                    by_type: el.type ? '[type="' + el.type + '"]' : null,
                    by_class: el.className ? '.' + el.className.split(' ')[0] : null,
                    by_text: el.textContent ? ':has-text("' + el.textContent.trim().substring(0, 30) + '")' : null
                }
            };
        }''')
        return cast(Dict[str, Any], result)

    def _get_stable_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """获取稳定的属性"""
        stable = {}
        for key, value in attributes.items():
            if key in ['id', 'name', 'type', 'placeholder', 'role', 'autocomplete'] and value:
                if not any(pattern in str(value).lower() for pattern in ['css-', 'emotion-', 'chakra-', 'random']):
                    stable[key] = value
        return stable

    def _get_key_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """获取关键属性"""
        key_attrs = {}
        for key in ['id', 'class', 'name', 'type', 'placeholder', 'role', 'data-testid']:
            if key in attributes and attributes[key]:
                key_attrs[key] = attributes[key]
        return key_attrs

    def save_html_log(self, filename: str = "tavily_elements_log.json") -> None:
        """保存HTML信息日志"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.html_log, f, ensure_ascii=False, indent=2)
            print(f"✅ HTML信息已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存HTML信息失败: {e}")

    def close_browser(self) -> None:
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def navigate_to_signup(self) -> bool:
        """导航到注册页面"""
        try:
            print("🌐 正在访问Tavily主页...")
            if not self.page:
                print("❌ 页面未初始化")
                return False
            self.page.goto(TAVILY_HOME_URL)
            wait_with_message(WAIT_TIME_MEDIUM, "等待页面加载")

            # 查找并点击Sign Up按钮
            signup_selectors = [
                'a[href*="sign-up"]',
                'button:has-text("Sign Up")',
                'a:has-text("Sign Up")',
                '.signup-btn',
                '#signup',
                'button:has-text("注册")',
                'a:has-text("注册")'
            ]

            signup_button = None
            for selector in signup_selectors:
                try:
                    signup_button = self.page.wait_for_selector(
                        selector, timeout=5000)
                    if signup_button:
                        break
                except:
                    continue

            if signup_button:
                print("✅ 找到Sign Up按钮，正在点击...")
                # 收集HTML信息
                self.collect_element_info(
                    signup_button, 'click', 'signup_button')
                signup_button.click()
                wait_with_message(WAIT_TIME_MEDIUM, "等待注册页面加载")
                return True
            else:
                # 尝试直接访问注册页面
                print("⚠️ 未找到Sign Up按钮，尝试直接访问注册页面...")
                self.page.goto(TAVILY_SIGNUP_URL)
                wait_with_message(WAIT_TIME_MEDIUM, "等待注册页面加载")
                return True

        except Exception as e:
            print(f"❌ 导航到注册页面失败: {e}")
            return False

    def fill_registration_form(self) -> bool:
        """填写注册表单"""
        try:
            # 生成随机邮箱（使用动态前缀）
            self.email = generate_email(self.email_prefix)
            print(f"📧 生成的注册邮箱: {self.email}")

            if not self.page:
                print("❌ 页面未初始化")
                return False

            # 查找邮箱输入框
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email"]',
                '#email',
                '.email-input'
            ]

            email_input = None
            for selector in email_selectors:
                try:
                    email_input = self.page.wait_for_selector(
                        selector, timeout=5000)
                    if email_input:
                        break
                except:
                    continue

            if not email_input:
                print("❌ 未找到邮箱输入框")
                return False

            # 输入邮箱
            # 收集HTML信息
            self.collect_element_info(email_input, 'fill', 'email_input')
            email_input.fill(self.email)
            print(f"✅ 已输入邮箱: {self.email}")
            wait_with_message(WAIT_TIME_SHORT, "等待输入完成")

            # 查找下一步按钮或继续按钮
            next_selectors = [
                'button:has-text("Next")',
                'button:has-text("Continue")',
                'button:has-text("下一步")',
                'button:has-text("继续")',
                'button[type="submit"]',
                '.next-btn',
                '.continue-btn'
            ]

            next_button = None
            for selector in next_selectors:
                try:
                    next_button = self.page.wait_for_selector(
                        selector, timeout=5000)
                    if next_button:
                        break
                except:
                    continue

            if next_button:
                print("✅ 找到下一步按钮，正在点击...")
                # 收集HTML信息
                self.collect_element_info(next_button, 'click', 'next_button')
                next_button.click()
                wait_with_message(WAIT_TIME_MEDIUM, "等待密码页面加载")
            else:
                print("⚠️ 未找到下一步按钮，尝试按Enter键...")
                email_input.press('Enter')
                wait_with_message(WAIT_TIME_MEDIUM, "等待密码页面加载")

            return True

        except Exception as e:
            print(f"❌ 填写邮箱失败: {e}")
            return False

    def fill_password(self) -> bool:
        """填写密码"""
        try:
            print("🔐 正在填写密码...")

            if not self.page:
                print("❌ 页面未初始化")
                return False

            # 查找密码输入框
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[placeholder*="password"]',
                '#password',
                '.password-input'
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.page.wait_for_selector(
                        selector, timeout=10000)
                    if password_input:
                        break
                except:
                    continue

            if not password_input:
                print("❌ 未找到密码输入框")
                return False

            # 输入密码
            # 收集HTML信息
            self.collect_element_info(password_input, 'fill', 'password_input')
            password_input.fill(self.password)
            print(f"✅ 已输入密码")
            # 密码输入后立即继续，不需要等待

            # 查找确认密码输入框（如果有的话）
            confirm_password_selectors = [
                'input[name="confirmPassword"]',
                'input[name="confirm_password"]',
                'input[placeholder*="confirm"]',
                '#confirmPassword',
                '#confirm_password'
            ]

            for selector in confirm_password_selectors:
                try:
                    confirm_input = self.page.wait_for_selector(
                        selector, timeout=3000)
                    if confirm_input:
                        confirm_input.fill(self.password)
                        print("✅ 已输入确认密码")
                        break
                except:
                    continue

            # 查找提交按钮（减少等待时间）
            submit_selectors = [
                'button:has-text("Sign Up")',
                'button:has-text("Register")',
                'button:has-text("Create Account")',
                'button:has-text("注册")',
                'button:has-text("创建账户")',
                'button[type="submit"]',
                '.submit-btn',
                '.register-btn'
            ]

            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.page.wait_for_selector(
                        selector, timeout=2000)  # 减少到2秒
                    if submit_button:
                        print(f"✅ 找到提交按钮: {selector}")
                        break
                except:
                    continue

            if submit_button:
                print("✅ 找到注册按钮，正在提交...")
                # 收集HTML信息
                self.collect_element_info(
                    submit_button, 'click', 'submit_button')
                submit_button.click()
                wait_with_message(WAIT_TIME_LONG, "等待注册完成")
            else:
                print("⚠️ 未找到注册按钮，尝试按Enter键...")
                password_input.press('Enter')
                wait_with_message(WAIT_TIME_LONG, "等待注册完成")

            return True

        except Exception as e:
            print(f"❌ 填写密码失败: {e}")
            return False

    def run_registration(self) -> bool:
        """
        运行完整的传统注册流程。
        """
        try:
            print("🚀 开始传统注册流程...")

            if not self.navigate_to_signup():
                print("❌ 导航到注册页面失败")
                return False

            if not self.fill_registration_form():
                print("❌ 填写注册表单失败")
                return False

            if not self.fill_password():
                print("❌ 填写密码失败")
                return False

            print("🎉 传统注册流程完成!")
            return True

        except Exception as e:
            print(f"❌ 传统注册流程失败: {e}")
            return False

    def verify_email(self, verification_link: str) -> bool:
        """验证邮箱"""
        try:
            print(f"🔗 正在访问验证链接...")
            if not self.page:
                print("❌ 页面未初始化")
                return False
            self.page.goto(verification_link)
            wait_with_message(WAIT_TIME_LONG, "等待邮箱验证完成")

            # 检查是否验证成功
            success_indicators = [
                'text=verified',
                'text=success',
                'text=confirmed',
                'text=activated',
                '.success',
                '.verified'
            ]

            for indicator in success_indicators:
                try:
                    if self.page.wait_for_selector(indicator, timeout=5000):
                        print("✅ 邮箱验证成功!")
                        return True
                except:
                    continue

            print("✅ 邮箱验证完成（未找到明确的成功指示器，但页面已加载）")
            return True

        except Exception as e:
            print(f"❌ 邮箱验证失败: {e}")
            return False

    def get_api_key(self) -> Optional[str]:
        """获取API key"""
        try:
            print("🔑 正在查找API key...")

            if not self.page:
                print("❌ 页面未初始化")
                return None

            # 等待页面完全加载
            wait_with_message(WAIT_TIME_MEDIUM, "等待页面加载")

            # 尝试导航到API设置页面
            api_page_selectors = [
                'a[href*="api"]',
                'a[href*="key"]',
                'a[href*="settings"]',
                'text=API',
                'text=Settings',
                '.api-key',
                '.settings'
            ]

            for selector in api_page_selectors:
                try:
                    api_link = self.page.wait_for_selector(
                        selector, timeout=3000)
                    if api_link:
                        print(f"✅ 找到API相关链接，正在点击...")
                        api_link.click()
                        wait_with_message(WAIT_TIME_MEDIUM, "等待API页面加载")
                        break
                except:
                    continue

            # 查找API key
            api_key_selectors = [
                'input[value*="tvly-"]',
                'code:has-text("tvly-")',
                'span:has-text("tvly-")',
                '.api-key',
                '[data-testid*="api"]',
                'input[readonly]'
            ]

            api_key = None
            for selector in api_key_selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    for element in elements:
                        text = element.inner_text() or element.get_attribute('value') or ''
                        if 'tvly-' in text:
                            api_key = text.strip()
                            break
                    if api_key:
                        break
                except:
                    continue

            if api_key:
                print(f"✅ 成功获取API key: {api_key}")
                if self.email:
                    save_api_key(self.email, api_key, self.password)
                return api_key
            else:
                print("⚠️ 未找到API key，可能需要手动查找")
                # 截图保存当前页面状态
                if self.page:
                    self.page.screenshot(path="api_key_page.png")
                    print("📸 已截图保存当前页面: api_key_page.png")
                return None

        except Exception as e:
            print(f"❌ 获取API key失败: {e}")
            return None
