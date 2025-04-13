"""AIVFS CLI 入口模块

提供文件系统命令行接口的入口点和主要命令实现。
"""
import asyncio
import logging
import click
from anytree import RenderTree
from click import Context
from typing import Optional


from aivk.api import AivkCLI, setup_logging

setup_logging(
    style="error",
    theme="dark",        # 使用深色主题
    icons="emoji",       # 使用emoji图标，更直观
    level=logging.INFO,  # 默认INFO级别
    show_time=True,     # 显示时间戳
    show_path=True      # 显示文件路径，方便调试
)

logger = logging.getLogger("aivk.fs.cli")



# 先定义命令组函数
@click.group(cls=AivkCLI.AivkGroup, name="fs", invoke_without_command=True, help="AIVK File System CLI")
@click.pass_context
def cli(ctx):
    """AIVFS CLI 命令行入口"""
    # 如果没有子命令被调用，则显示帮助信息
    if ctx.invoked_subcommand is None:
        logger.info("显示帮助信息:")
        logger.info(ctx.get_help())

fs = AivkCLI(id="fs")
fs.cli_parent = None  # 更新字段名为 cli_parent
fs.cli = cli  # 明确设置cli属性

@cli.command()
@click.option("--path", "-p", type=str, help="Path to load the file system", default="~/")
def load(path: str):
    """加载文件系统"""
    load_func = fs.on("load", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"加载文件系统，路径: {path}")
    if load_func:
        asyncio.run(load_func(**kwargs))
    else:
        logger.info("加载模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to unload the file system", default="~/")
def unload(path: str):
    """卸载文件系统"""
    unload_func = fs.on("unload", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"卸载文件系统，路径: {path}")
    if unload_func:
        asyncio.run(unload_func(**kwargs))
    else:
        logger.info("卸载模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to install the file system", required=True)
def install(path: str):
    """安装文件系统"""
    install_func = fs.on("install", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"安装文件系统，路径: {path}")
    if install_func:
        asyncio.run(install_func(**kwargs))
    else:
        logger.info("安装模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to uninstall the file system", required=True)
def uninstall(path: str):
    """卸载文件系统"""
    uninstall_func = fs.on("uninstall", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"卸载文件系统，路径: {path}")
    if uninstall_func:
        asyncio.run(uninstall_func(**kwargs))
    else:
        logger.info("卸载模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to update the file system", required=True)
def update(path: str):
    """更新文件系统"""
    update_func = fs.on("update", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"更新文件系统，路径: {path}")
    if update_func:
        asyncio.run(update_func(**kwargs))
    else:
        logger.info("更新模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to initialize the file system", required=True)
@click.option("--force", "-f", is_flag=True, help="Force initialization")
@click.option("--dev", "-d", is_flag=True, help="Development mode, initialize an aivk module (uv project)")
def init(path: str, force: bool, dev: bool):
    """初始化文件系统"""
    init_func = fs.on("init", "fs")
    kwargs = {
        "path": path,
        "force": force,
        "dev": dev
    }
    logger.info(f"初始化文件系统，路径: {path}, 强制: {force}, 开发模式: {dev}")
    if init_func:
        asyncio.run(init_func(**kwargs))
    else:
        logger.info("初始化模块完成")

@cli.command()
@click.option("--path", "-p", type=str, help="Path to check the file system", required=True)
def check(path: str):
    """检查文件系统"""
    check_func = fs.on("check", "fs")
    kwargs = {
        "path": path
    }
    logger.info(f"检查文件系统，路径: {path}")
    if check_func:
        asyncio.run(check_func(**kwargs))
    else:
        logger.info("检查模块完成")

@cli.command()
@click.argument('command', required=False)
@click.pass_context
def help(ctx: Context, command: Optional[str]):
    """显示帮助信息"""
    logger.info("显示树形结构:")
    print(RenderTree(fs))

    if command:
        cmd_obj = cli.get_command(ctx, command)
        if cmd_obj:
            logger.info(f"显示命令 '{command}' 的帮助信息:")
            click.echo(cmd_obj.get_help(ctx))
        else:
            logger.error(f"未找到命令: {command}")
            ctx.exit(1)
    else:
        logger.info("显示主要帮助信息:")
        click.echo(ctx.parent.get_help() if ctx.parent else ctx.get_help())

