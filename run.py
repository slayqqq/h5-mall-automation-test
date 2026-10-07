# -*- coding: utf-8 -*-
"""一键运行全部自动化用例并生成 Allure 报告数据"""
import subprocess
import sys


def main():
    cmd = [
        sys.executable, "-m", "pytest", "testcases",
        "-v", "--alluredir=reports/allure-results",
    ]
    print("运行命令:", " ".join(cmd))
    subprocess.run(cmd)
    print("\n执行完毕。")
    print("查看 Allure 报告（需先安装 allure 命令，见 README）: allure serve reports/allure-results")


if __name__ == "__main__":
    main()
