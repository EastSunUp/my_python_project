import socket

'''
检查电脑空闲端口:
    方法1:使用命令提示符 (推荐)
        1.打开命令提示符
            Win+R 输入 cmd 回车
        2.执行端口扫描命令:
                netstat -ano | findstr :端口号
            示例:
                netstat -ano | findstr :8080
            结果解读:
                1.无输出 → 端口空闲
                2.有输出 → 端口被占用 (显示进程ID)
    方法2:使用 PowerShell (更强大)
        打开电脑的powershell并输入以下内容:
            # 检查单个端口
            Test-NetConnection -Port 8080 -ComputerName localhost
            # 扫描常用端口范围（1024-9000）
            1..9000 | Where { Test-NetConnection localhost -Port $_ -InformationLevel Quiet } | Format-Table
        ✅ 绿色显示 TcpTestSucceeded : True 表示被占用
    方法3:图形化工具 (任务管理器)
        1.Ctrl+Shift+Esc 打开任务管理器
        2.切换到 "性能" 标签 → 底部 "打开资源监视器"
        3.在 "网络" 标签页 → "侦听端口" 列表查看所有占用端口
    方法4使用python代码进行端口检查:
        import socket

        def check_port(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(('localhost', port)) == 0  # 返回True表示被占用

        # 检查单个端口
        print("8080端口状态:", "占用" if check_port(8080) else "空闲")

        # 扫描多个端口
        for port in [8080, 3000, 5000, 8888]:
            status = "占用" if check_port(port) else "空闲"
            print(f"端口 {port}: {status}")

'''

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0  # 返回True表示被占用

# 检查单个端口
print("8080端口状态:", "占用" if check_port(8080) else "空闲")

# 扫描多个端口
for port in [8080, 3000, 5000, 8888]:
    status = "占用" if check_port(port) else "空闲"
    print(f"端口 {port}: {status}")
