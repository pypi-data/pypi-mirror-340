"""
Talos Loader 命令行工具
"""

import os
import sys
import click
import inquirer
import shutil
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pkg_resources


def create_project_structure(project_path, project_name):
    """创建项目结构"""
    # 创建主目录
    project_dir = os.path.join(project_path, project_name)
    os.makedirs(project_dir, exist_ok=True)
    
    # 创建与项目同名的子目录
    sub_project_dir = os.path.join(project_dir, project_name)
    os.makedirs(sub_project_dir, exist_ok=True)
    
    # 创建 loaders 目录
    loaders_dir = os.path.join(sub_project_dir, "loaders")
    os.makedirs(loaders_dir, exist_ok=True)
    
    # 设置 Jinja2 环境
    templates_path = pkg_resources.resource_filename('talos_loader', 'templates')
    env = Environment(loader=FileSystemLoader(templates_path))
    
    # 渲染并创建 README.md
    readme_template = env.get_template('README.md.j2')
    readme_content = readme_template.render(project_name=project_name)
    readme_path = os.path.join(project_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 渲染并创建 pyproject.toml
    pyproject_template = env.get_template('pyproject.toml.j2')
    pyproject_content = pyproject_template.render(project_name=project_name)
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    with open(pyproject_path, "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    
    # 渲染并创建项目子目录的 __init__.py
    init_template = env.get_template('init.py.j2')
    init_content = init_template.render(project_name=project_name)
    init_file = os.path.join(sub_project_dir, "__init__.py")
    with open(init_file, "w", encoding="utf-8") as f:
        f.write(init_content)
    
    # 渲染并创建 loaders 的 __init__.py
    loaders_init_template = env.get_template('loaders_init.py.j2')
    loaders_init_content = loaders_init_template.render()
    loaders_init = os.path.join(loaders_dir, "__init__.py")
    with open(loaders_init, "w", encoding="utf-8") as f:
        f.write(loaders_init_content)
    
    # 渲染并创建示例加载器文件
    loader_template = env.get_template('my_custom_loaders.py.j2')
    loader_content = loader_template.render()
    loader_file = os.path.join(loaders_dir, "my_custom_loaders.py")
    with open(loader_file, "w", encoding="utf-8") as f:
        f.write(loader_content)
    
    # 渲染并创建 dry_run.py 文件
    dry_run_template = env.get_template('dry_run.py.j2')
    dry_run_content = dry_run_template.render(project_name=project_name)
    dry_run_path = os.path.join(project_dir, "dry_run.py")
    with open(dry_run_path, "w", encoding="utf-8") as f:
        f.write(dry_run_content)
    
    # 渲染并创建 check.py 文件
    check_template = env.get_template('check.py.j2')
    check_content = check_template.render()
    check_path = os.path.join(project_dir, "check.py")
    with open(check_path, "w", encoding="utf-8") as f:
        f.write(check_content)
    # 设置 check.py 为可执行文件
    os.chmod(check_path, 0o755)
    
    # 配置 Poetry 强制使用虚拟环境
    try:
        click.echo("配置 Poetry 强制使用虚拟环境...")
        # 创建 poetry.toml 文件，强制使用虚拟环境
        poetry_toml_content = """[virtualenvs]
# 强制创建虚拟环境，即使用户全局配置了不创建
create = true
# 将虚拟环境创建在项目目录内的 .venv 文件夹中
in-project = true
# 确保虚拟环境总是被激活
prefer-active-python = true
# 使用项目名称作为虚拟环境名称
clear-name = true
"""
        poetry_toml_path = os.path.join(project_dir, "poetry.toml")
        with open(poetry_toml_path, "w", encoding="utf-8") as f:
            f.write(poetry_toml_content)
        click.echo("Poetry 虚拟环境配置完成")
    except Exception as e:
        click.echo(f"配置 Poetry 虚拟环境失败: {e}")
        click.echo("请手动创建 poetry.toml 文件并配置虚拟环境")


@click.group()
def main():
    """Talos Loader 命令行工具"""
    pass


@main.command()
def init():
    """初始化一个新的 loader 项目"""
    questions = [
        inquirer.Path(
            'project_path',
            message="请输入项目路径",
            path_type=inquirer.Path.DIRECTORY,
            default=os.path.expanduser("~/Downloads"),
            exists=True
        ),
        inquirer.Text(
            'project_name',
            message="请输入项目名称",
            validate=lambda _, x: len(x) > 0
        )
    ]
    
    answers = inquirer.prompt(questions)
    
    if not answers:
        click.echo("初始化已取消")
        return
    
    project_path = answers['project_path']
    project_name = answers['project_name']
    
    # 检查项目目录是否已存在
    full_path = os.path.join(project_path, project_name)
    if os.path.exists(full_path):
        overwrite = inquirer.confirm(
            message=f"项目 {project_name} 已存在，是否覆盖?",
            default=False
        )
        if overwrite:
            shutil.rmtree(full_path)
        else:
            click.echo("初始化已取消")
            return
    
    click.echo(f"正在创建项目 {project_name} 在 {project_path}")
    create_project_structure(project_path, project_name)
    click.echo(f"项目创建成功！")
    click.echo(f"项目路径: {os.path.join(project_path, project_name)}")
    click.echo("提示: 该项目要求 Python 3.10 或更高版本")
    click.echo("使用方法: cd {0} && poetry install --no-root".format(os.path.join(project_path, project_name)))


if __name__ == "__main__":
    main()
