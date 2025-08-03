import winreg
import ctypes
import subprocess
import os
import win32serviceutil  # 需要安装 pywin32 模块


def is_admin():
    """检查是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_registry_keys():
    """删除限制更新的注册表项"""
    try:
        # 打开 Chrome 策略注册表项
        policy_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Google\Chrome",
            0, winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY
        )

        # 尝试删除特定值
        for value_name in ["UpdateDefault", "AutoUpdateCheckPeriodMinutes"]:
            try:
                winreg.DeleteValue(policy_key, value_name)
                print(f"✅ 已删除注册表值: {value_name}")
            except FileNotFoundError:
                pass  # 如果值不存在则跳过

        winreg.CloseKey(policy_key)

        # 检查是否还有其他策略存在
        try:
            subkey_count, value_count, _ = winreg.QueryInfoKey(policy_key)
            if value_count == 0 and subkey_count == 0:
                # 如果项为空则删除整个项
                winreg.DeleteKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Policies\Google\Chrome"
                )
                print("✅ 已删除空策略注册表项")
        except:
            pass

    except FileNotFoundError:
        print("ℹ️ 未找到策略注册表项，无需操作")
    except Exception as e:
        print(f"❌ 注册表操作失败: {str(e)}")


def enable_update_services():
    """启用并启动 Google 更新服务"""
    services = ["gupdate", "gupdatem"]

    for service in services:
        try:
            # 设置服务为自动启动
            win32serviceutil.ChangeServiceConfig(
                None, service,
                startType=win32serviceutil.SERVICE_AUTO_START
            )

            # 启动服务
            win32serviceutil.StartService(service)
            print(f"✅ 已启动服务: {service}")

        except Exception as e:
            print(f"❌ 服务 {service} 操作失败: {str(e)}")


def reset_chrome_update_settings():
    """重置 Chrome 内部更新设置"""
    try:
        # 创建 Chrome 的用户数据目录路径
        app_data = os.getenv("LOCALAPPDATA")
        chrome_user_data = os.path.join(app_data, "Google", "Chrome")

        # 删除更新相关文件
        for file in ["Update", "Last Version"]:
            file_path = os.path.join(chrome_user_data, file)
            try:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        os.rmdir(file_path)
                    else:
                        os.remove(file_path)
                    print(f"✅ 已删除: {file}")
            except Exception as e:
                print(f"⚠️ 无法删除 {file}: {str(e)}")

    except Exception as e:
        print(f"❌ 重置设置失败: {str(e)}")


def verify_update_status():
    """验证更新功能是否恢复"""
    try:
        # 检查注册表项是否已移除
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Policies\Google\Chrome"
            )
            winreg.CloseKey(key)
            print("❌ 注册表策略项仍然存在")
        except FileNotFoundError:
            print("✅ 注册表策略项已移除")

        # 检查服务状态
        for service in ["gupdate", "gupdatem"]:
            try:
                status = win32serviceutil.QueryServiceStatus(service)
                if status[1] == 4:  # 4 表示运行中
                    print(f"✅ 服务 {service} 正在运行")
                else:
                    print(f"⚠️ 服务 {service} 未运行 (状态: {status[1]})")
            except Exception as e:
                print(f"❌ 无法检查服务 {service}: {str(e)}")

        # 尝试手动触发更新检查
        try:
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not os.path.exists(chrome_path):
                chrome_path = os.path.join(os.getenv("ProgramFiles(x86)"), "Google", "Chrome", "Application",
                                           "chrome.exe")

            subprocess.run([chrome_path, "--update-now"], check=True, timeout=30)
            print("✅ 已触发 Chrome 更新检查")
        except Exception as e:
            print(f"⚠️ 无法触发更新检查: {str(e)}")

        print("\n请手动检查更新状态:")
        print("1. 打开 Chrome")
        print("2. 在地址栏输入: chrome://settings/help")
        print("3. 应显示 'Chrome 是最新版本' 或正在检查更新")

    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")


def main():
    if not is_admin():
        # 请求管理员权限重新运行
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "python", __file__, None, 1
        )
        return

    print("=" * 50)
    print("Chrome 自动更新解除工具")
    print("=" * 50)

    print("\n[步骤 1/4] 移除注册表限制...")
    remove_registry_keys()

    print("\n[步骤 2/4] 启用更新服务...")
    enable_update_services()

    print("\n[步骤 3/4] 重置 Chrome 更新设置...")
    reset_chrome_update_settings()

    print("\n[步骤 4/4] 验证更新功能...")
    verify_update_status()

    print("\n操作完成! 建议重启电脑使所有更改生效")


if __name__ == "__main__":
    main()