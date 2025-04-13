import os
import re
import shutil
import subprocess
import tempfile

from Cython.Build import cythonize
from Cython.Distutils import Extension
from setuptools import setup, find_packages, Distribution
from setuptools.command.install import install

def clean_dist_folder():
    """自动清理 dist 文件夹，避免旧文件干扰"""
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        print(f"清理旧 dist 文件夹: {dist_dir}")
        shutil.rmtree(dist_dir)

def update_version(version_file="ntsulib/__init__.py"):
    """自动将版本号 +0.0.1，并返回新版本号"""
    try:
        with open(version_file, "r+", encoding="utf-8") as f:
            content = f.read()
            # 使用正则匹配版本号（格式：x.y.z）
            version_match = re.search(r'__version__\s*=\s*["\'](\d+\.\d+\.\d+)["\']', content)
            if not version_match:
                raise ValueError("无法找到版本号！请确保 __init__.py.py 中有 __version__='x.y.z'")

            old_version = version_match.group(1)
            major, minor, patch = map(int, old_version.split('.'))
            new_version = f"{major}.{minor}.{patch + 1}"  # 自动 +0.0.1

            # 替换为新版本号
            new_content = re.sub(
                r'__version__\s*=\s*["\'][^"\']*["\']',
                f'__version__ = "{new_version}"',
                content
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()

            print(f"版本号从 {old_version} 更新为 {new_version}")
            return new_version
    except Exception as e:
        print(f"版本号更新失败: {e}")
        return None

def generate_pyproject_toml(version):
    """根据 setup.py 配置自动生成 pyproject.toml"""
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42"]
build-backend = "setuptools.build_meta"

[project]
name = "{setup_params['name']}"
version = "{version}"
authors = [
    {{ name = "{setup_params['author']}", email = "{setup_params['author_email']}" }}
]
description = "{setup_params['description']}"
dependencies = {setup_params['install_requires']}
"""
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    print("已生成 pyproject.toml")

def get_install_requires():
    """从 requirements.txt 读取依赖（如果文件存在）"""
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


def compile_pyd(path: str):
    path = os.path.abspath(path)
    temp_build = tempfile.mkdtemp()

    original_cwd = os.getcwd()
    os.chdir(path)

    try:
        py_files = []
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    full_path = os.path.join(root, file)
                    py_files.append(full_path)

        extensions = []
        for file_path in py_files:
            module_path = os.path.normpath(file_path)
            module_name = module_path[:-3].replace(os.path.sep, '.').lstrip('.')
            extensions.append(Extension(module_name, [file_path]))

            target_dir = os.path.dirname(file_path)
            os.makedirs(target_dir, exist_ok=True)

        setup(
            script_args=['build_ext', '--inplace'],
            ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
            script_name='setup.py',
            options={'build': {'build_base': temp_build}},
            packages=[],
            distclass=BinaryDistribution,
        )
    finally:
        os.chdir(original_cwd)

    # 重命名所有带平台标识的.pyd文件
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.pyd'):
                original_path = os.path.join(root, file)
                # 使用正则表达式匹配平台标识部分
                new_name = re.sub(
                    r'\.cp\d+-.+?\.pyd$',  # 匹配 .cp311-win_amd64.pyd 等格式
                    '.pyd',
                    file
                )
                # 只有当文件名确实包含平台标识时才重命名
                if new_name != file:
                    new_path = os.path.join(root, new_name)
                    # 确保目标文件不存在
                    if os.path.exists(new_path):
                        os.remove(new_path)
                    os.rename(original_path, new_path)
                    print(f"Renamed: {file} -> {new_name}")

    shutil.rmtree(temp_build)

def delete_pyd(path: str):
    """
    递归删除文件夹内所有.pyd文件
    """
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.pyd'):
                pyd_path = os.path.join(root, file)
                try:
                    os.remove(pyd_path)
                    print(f"已删除: {pyd_path}")
                except Exception as e:
                    print(f"删除失败 {pyd_path}: {str(e)}")

def delete_c(path: str):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.c'):
                pyd_path = os.path.join(root, file)
                try:
                    os.remove(pyd_path)
                    print(f"已删除: {pyd_path}")
                except Exception as e:
                    print(f"删除失败 {pyd_path}: {str(e)}")


# delete_pyd('./ntsulib')
# delete_c('./ntsulib')
# exit()

# 预执行清理
clean_dist_folder()

# 尝试自动更新版本号
current_version = update_version()
if current_version is None:
    current_version = "1.0.0"  # 默认版本（需手动修复）
    print(f"使用默认版本号: {current_version}")

def generate_requirements_file():
    """自动生成 requirements.txt 文件"""
    print("正在生成 requirements.txt...")
    try:
        # 执行 pip freeze 命令获取当前环境所有依赖
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)

        # 过滤掉不需要的行（注释、可编辑安装等）
        dependencies = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and not line.startswith(('#', '-e'))
        ]

        # 写入 requirements.txt
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(dependencies))

        print(f"已生成 requirements.txt，包含 {len(dependencies)} 个依赖")
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"生成 requirements.txt 失败: {e.stderr}")
        return []

generate_requirements_file()

def get_pyinstaller_hook_dir():
    """动态获取 PyInstaller 的 hooks 目录路径（兼容 venv 和全局安装）"""
    import sys
    from pathlib import Path
    # 获取当前 Python 环境的 site-packages 路径
    site_packages = Path(sys.prefix) / "Lib" / "site-packages"  # Windows
    if not site_packages.exists():
        site_packages = Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"  # Linux/macOS
    # 检查 PyInstaller 是否存在
    pyinstaller_hooks = site_packages / "PyInstaller" / "hooks"
    if not pyinstaller_hooks.exists():
        raise FileNotFoundError("PyInstaller hooks 目录未找到，请确保已安装 PyInstaller")
    return str(pyinstaller_hooks)

def _clean_old_hooks():
    """清理旧版本的 Hook 文件"""
    try:
        import PyInstaller
        hook_path = os.path.join(os.path.dirname(PyInstaller.__file__), "hooks", "hook-ntsulib.py")
        if os.path.exists(hook_path):
            os.remove(hook_path)
    except:
        pass

# 在 setup() 前清理旧文件
_clean_old_hooks()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # 先执行标准安装
        # 检查 hook 文件是否已正确安装
        hook_src = "pyinstaller_hooks/hook-ntsulib.py"  # 你的 hook 文件路径
        hook_dest = os.path.join(get_pyinstaller_hook_dir(), "hook-ntsulib.py")
        if not os.path.exists(hook_dest):
            print(f"Hook 文件未正确安装到: {hook_dest}")
            # 尝试手动复制（如果 data_files 未生效）
            try:
                shutil.copy(hook_src, hook_dest)
                print(f"手动复制 hook 文件到: {hook_dest}")
            except Exception as e:
                print(f"无法复制 hook 文件: {e}")
        else:
            print(f"Hook 文件已正确安装到: {hook_dest}")

        p = "./ntsulib"
        delete_pyd(p)
        delete_c(p)
        # 生成pyd文件
        print('正在生成pyd文件')
        compile_pyd(p)
        delete_c(p)
        print('生成pyd文件完成!')

        # 手动安装PyPi文件
        print('正在安装.pyi文件')
        # 确保 pyi 文件递归复制
        source_root = os.path.join(os.path.dirname(__file__), "stubs", "ntsulib")
        target_root = os.path.join(self.install_lib, "ntsulib")

        if os.path.exists(source_root):
            for root, _, files in os.walk(source_root):
                relative_path = os.path.relpath(root, source_root)
                target_dir = os.path.join(target_root, relative_path)

                os.makedirs(target_dir, exist_ok=True)  # 确保目标路径存在

                for file in files:
                    if file.endswith(".pyi"):
                        shutil.copy(os.path.join(root, file), target_dir)


# 定义 setup() 的参数
setup_params = {
    "name": "ntsulib",
    "version": current_version,  # 使用自动更新的版本号
    "author": "NTsukine",
    "author_email": "398339897@qq.com",
    "description": "ntsulib",
    "long_description": open("README.md", encoding="utf-8").read(),
    "long_description_content_type": "text/markdown",
    "url": "",
    # 修改的部分
    "packages": find_packages(exclude=["测试", "命令","注意","备份","ntsulib_dll"]),
    # "package_data": {
    #     "ntsulib": ["libs/*.dll","py.typed","*.pyd"],
    # },
    # 直接解压操作
    # "zip_safe": False,
    "cmdclass": {
        'install': PostInstallCommand,  # 覆盖默认 install 命令
    },
    # 关键修改：添加 data_files 自动安装 Hook
    "data_files": [
        (get_pyinstaller_hook_dir(), ["pyinstaller_hooks/hook-ntsulib.py"]),
    ],
    "include_package_data": True,  # 确保 MANIFEST.in 生效
    "install_requires": get_install_requires(),
    "classifiers": [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # 修改为GPLv3
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    "python_requires": ">=3.9",
    "keywords": ['utility', 'library', 'python', 'ntsulib'],
}

# 生成 pyproject.toml（使用更新后的版本号）
generate_pyproject_toml(current_version)

# 调用 setup()
setup(**setup_params)
