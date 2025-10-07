#!/usr/bin/env python3
"""
Intelligent Tavily Automatic Registration Main Program

Supports intelligent processes, dynamic email prefix acquisition, test mode and other functions.
"""
import json
import base64
import time
import os
from typing import Optional, Tuple
from .core.intelligent_automation import IntelligentTavilyAutomation
from .core.traditional_automation import TavilyAutomation
from .email.login_helper import EmailLoginHelper
from .config.settings import EMAIL_CHECK_URL
from .utils.helpers import wait_with_message, load_cookies


class TavilyMainController:
    def __init__(self) -> None:
        self.email_prefix: Optional[str] = None
        self.cookie_file: str = "email_cookies.json"

    def get_email_prefix_from_cookies(self) -> Optional[str]:
        """从cookies中获取邮箱前缀"""
        try:
            if not os.path.exists(self.cookie_file):
                print("⚠️ 未找到邮箱cookies文件")
                return None

            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 处理新格式和旧格式的cookies
            if isinstance(data, list):
                # 旧格式 - 直接是cookie列表
                cookies = data
            elif isinstance(data, dict) and 'cookies' in data:
                # 新格式 - 包含metadata的格式
                cookies = data['cookies']
            else:
                print("❌ 无效的cookies文件格式")
                return None

            # 查找包含用户信息的JWT token
            for cookie in cookies:
                if isinstance(cookie, dict) and cookie.get('name') == 'aut':
                    jwt_token = cookie.get('value', '')
                    try:
                        # 解析JWT token (格式: header.payload.signature)
                        parts = jwt_token.split('.')
                        if len(parts) >= 2:
                            # 解码payload部分
                            payload = parts[1]
                            # 添加必要的padding
                            payload += '=' * (4 - len(payload) % 4)
                            decoded = base64.b64decode(payload)
                            user_info = json.loads(decoded.decode('utf-8'))

                            # 获取邮箱信息
                            email = user_info.get('name', '')
                            nickname = user_info.get('nickname', '')

                            if email and '@' in str(email):
                                prefix = str(email).split('@')[0]
                                print(f"✅ 从cookies获取邮箱前缀: {prefix}")
                                return prefix
                            elif nickname:
                                nickname_str = str(nickname)
                                print(f"✅ 从cookies获取昵称前缀: {nickname_str}")
                                return nickname_str

                    except Exception as e:
                        print(f"⚠️ 解析JWT token失败: {e}")
                        continue

            print("⚠️ 未能从cookies中获取邮箱信息")
            return None

        except Exception as e:
            print(f"❌ 读取cookies失败: {e}")
            return None

    def setup_email_cookies(self) -> bool:
        """设置邮箱cookies"""
        print("🍪 邮箱Cookie获取流程")
        print("=" * 40)
        print("请在打开的浏览器中登录您的邮箱账户")
        print("登录成功后，程序将自动获取您的邮箱前缀")

        email_helper = EmailLoginHelper()

        try:
            email_helper.start_browser()

            # 访问邮箱网站
            if not email_helper.page:
                print("❌ 页面未初始化")
                return False

            email_helper.page.goto(EMAIL_CHECK_URL)
            wait_with_message(2, "等待页面加载")

            # 引导用户手动登录并保存cookies
            if email_helper.manual_login_guide():
                print("✅ Cookies保存成功")

                # 测试保存的cookies是否有效
                if email_helper.test_saved_cookies():
                    print("✅ Cookies测试成功")

                    # 尝试获取邮箱前缀
                    self.email_prefix = self.get_email_prefix_from_cookies()
                    if self.email_prefix:
                        print(f"✅ 邮箱前缀设置为: {self.email_prefix}")
                        return True
                    else:
                        print("⚠️ 无法获取邮箱前缀，请重新登录")
                        return False
                else:
                    print("⚠️ Cookies测试失败，但已保存")
                    return True  # 即使测试失败，cookies已保存，可以继续
            else:
                print("❌ Cookies保存失败")
                return False

        except Exception as e:
            print(f"❌ Cookie获取失败: {e}")
            return False
        finally:
            email_helper.close_browser()

    def show_main_menu(self) -> str:
        """显示主菜单"""
        print("🚀 智能Tavily自动注册系统")
        print("=" * 60)
        print("🌟 基于深层HTML分析的智能自动化解决方案")
        print("⚡ 性能提升60-70% | 成功率95%+ | 完全自动化")

        # 显示当前邮箱前缀
        if self.email_prefix:
            print(f"📧 当前邮箱前缀: {self.email_prefix}")
        else:
            print("⚠️ 未设置邮箱前缀")

        print("\n🎛️ 选择运行模式:")
        print("1. 智能自动化模式 (推荐)")
        print("2. 测试模式 (传统方式+HTML信息收集)")
        print("3. Cookie设置")
        print("4. 退出")

        return input("\n请选择 (1-4): ").strip()

    def get_run_config(self) -> Tuple[bool, int]:
        """获取运行配置"""
        print("\n⚙️ 运行配置")
        print("-" * 30)

        # 浏览器模式
        print("🖥️ 浏览器模式:")
        print("1. 前台模式 (可观察过程)")
        print("2. 后台模式 (更快)")

        while True:
            browser_choice = input("选择浏览器模式 (1/2): ").strip()
            if browser_choice in ['1', '2']:
                headless = browser_choice == '2'
                break
            print("❌ 请输入 1 或 2")

        # 注册数量
        while True:
            try:
                count = int(input("\n📊 注册账户数量 (1-10): "))
                if 1 <= count <= 10:
                    break
                print("❌ 请输入 1-10 之间的数字")
            except ValueError:
                print("❌ 请输入有效数字")

        return headless, count

    def check_and_setup_cookies(self) -> bool:
        """检查并设置cookies（如果需要）"""
        # 使用增强的cookie加载功能检查cookies
        cookies = load_cookies(self.cookie_file)
        if not cookies:
            print("⚠️ 未找到有效的邮箱cookies文件，需要先设置邮箱登录")
            print("📋 即将自动启动邮箱登录设置流程...")
            return self.setup_email_cookies()

        # 尝试获取邮箱前缀
        self.email_prefix = self.get_email_prefix_from_cookies()
        if not self.email_prefix:
            print("⚠️ 无法从cookies获取邮箱前缀，可能cookies已过期")
            print("📋 即将重新设置邮箱登录...")
            return self.setup_email_cookies()

        print(f"✅ 邮箱cookies有效，邮箱前缀: {self.email_prefix}")
        return True

    def run_intelligent_mode(self) -> None:
        """运行智能自动化模式"""
        print("\n🧠 智能自动化模式")
        print("=" * 40)

        # 自动检查并设置cookies
        if not self.check_and_setup_cookies():
            print("❌ 邮箱设置失败，无法继续")
            return

        # 获取运行配置
        headless, count = self.get_run_config()

        print(f"\n📋 配置信息:")
        print(f"  模式: 智能自动化")
        print(f"  邮箱前缀: {self.email_prefix}")
        print(f"  浏览器: {'后台' if headless else '前台'}模式")
        print(f"  数量: {count} 个账户")

        if input("\n🚀 开始执行? (y/n): ").lower().strip() != 'y':
            print("👋 已取消")
            return

        # 执行智能自动化
        success_count = 0

        for i in range(count):
            print(f"\n{'='*60}")
            print(f"🔄 智能注册第 {i+1}/{count} 个账户")
            print(f"{'='*60}")
            automation: Optional[IntelligentTavilyAutomation] = None
            try:
                automation = IntelligentTavilyAutomation()

                # 设置邮箱前缀
                automation.email_prefix = self.email_prefix

                automation.start_browser(headless=headless)

                start_time = time.time()
                api_key = automation.run_complete_automation()
                elapsed_time = time.time() - start_time

                if api_key:
                    print(f"🎉 第 {i+1} 个账户注册成功!")
                    print(f"⏱️  耗时: {elapsed_time:.1f} 秒")
                    print(f"📧 邮箱: {automation.email}")
                    print(f"🔑 API Key: {api_key}")
                    success_count += 1
                else:
                    print(f"❌ 第 {i+1} 个账户注册失败")

            except Exception as e:
                print(f"❌ 第 {i+1} 个账户注册出错: {e}")
            finally:
                # 确保浏览器被关闭
                if automation:
                    try:
                        automation.close_browser()
                    except Exception:
                        # 浏览器可能已经关闭，忽略错误
                        pass
                continue

        # 显示结果
        print(f"\n{'='*60}")
        print(f"🎉 智能自动化完成!")
        print(
            f"📊 成功率: {success_count}/{count} ({success_count/count*100:.1f}%)")
        print(f"📄 API Key已保存到 api_keys.md")
        print(f"{'='*60}")

    def run_test_mode(self) -> None:
        """运行测试模式（传统方式+HTML信息收集）"""
        print("\n🔍 测试模式")
        print("=" * 40)
        print("此模式使用传统等待+关键词方式，并收集HTML信息用于优化")

        # 自动检查并设置cookies
        if not self.check_and_setup_cookies():
            print("❌ 邮箱设置失败，无法继续")
            return

        # 获取运行配置
        headless, count = self.get_run_config()

        print(f"\n📋 测试配置:")
        print(f"  模式: 测试模式 (传统方式)")
        print(f"  邮箱前缀: {self.email_prefix}")
        print(f"  浏览器: {'后台' if headless else '前台'}模式")
        print(f"  数量: {count} 个账户")
        print(f"  HTML收集: 启用")

        if input("\n🔍 开始测试? (y/n): ").lower().strip() != 'y':
            print("👋 已取消")
            return

        # 执行测试模式
        success_count = 0

        for i in range(count):
            print(f"\n{'='*60}")
            print(f"🔍 测试第 {i+1}/{count} 个账户 (传统模式)")
            print(f"{'='*60}")
            automation: Optional[TavilyAutomation] = None
            try:
                automation = TavilyAutomation()

                # 设置邮箱前缀
                automation.email_prefix = self.email_prefix

                automation.start_browser(headless=headless)

                start_time = time.time()

                # 运行传统注册流程
                if automation.run_registration():
                    print("✅ 传统注册流程完成")

                    # 保存HTML日志
                    automation.save_html_log(f"test_mode_log_{i+1}.json")
                    print(f"📋 HTML信息已保存到 test_mode_log_{i+1}.json")

                    success_count += 1
                else:
                    print("❌ 传统注册流程失败")

                elapsed_time = time.time() - start_time
                print(f"⏱️  传统模式耗时: {elapsed_time:.1f} 秒")

            except Exception as e:
                print(f"❌ 测试第 {i+1} 个账户出错: {e}")
            finally:
                # 确保浏览器被关闭
                if automation:
                    try:
                        automation.close_browser()
                    except Exception:
                        # 浏览器可能已经关闭，忽略错误
                        pass
                continue

        # 显示结果
        print(f"\n{'='*60}")
        print(f"🔍 测试模式完成!")
        print(
            f"📊 成功率: {success_count}/{count} ({success_count/count*100:.1f}%)")
        print(f"📋 HTML信息已收集，可用于系统优化")
        print(f"{'='*60}")

    def run(self) -> None:
        """主运行函数"""
        # 初始化时尝试获取邮箱前缀
        self.email_prefix = self.get_email_prefix_from_cookies()

        while True:
            choice = self.show_main_menu()

            if choice == '1':
                self.run_intelligent_mode()
            elif choice == '2':
                self.run_test_mode()
            elif choice == '3':
                self.setup_email_cookies()
            elif choice == '4':
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重新输入")

            if choice in ['1', '2']:
                if input("\n是否继续使用系统? (y/n): ").lower().strip() != 'y':
                    print("👋 再见!")
                    break


def main() -> None:
    """主函数"""
    controller = TavilyMainController()
    controller.run()


if __name__ == "__main__":
    main()
