#!/usr/bin/env python3
"""
Multi-Platform Transformer Plugin Manager
管理插件的安装、更新、启用和禁用
"""

import os
import sys
import yaml
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Plugin:
    """插件信息"""
    name: str
    version: str
    description: str
    enabled: bool
    builtin: bool
    hooks: List[str]
    config: Dict


class PluginManager:
    """插件管理器"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.plugins_dir = self.base_path / "plugins"
        self.registry_file = self.plugins_dir / "_registry.yaml"
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """加载插件注册表"""
        if self.registry_file.exists():
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {"version": "1.0.0", "plugins": {}}
    
    def _save_registry(self):
        """保存插件注册表"""
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.registry, f, default_flow_style=False, allow_unicode=True)
    
    def list_plugins(self, show_all: bool = False) -> List[Plugin]:
        """列出所有插件"""
        plugins = []
        for name, info in self.registry.get("plugins", {}).items():
            if show_all or info.get("enabled", False):
                plugins.append(Plugin(
                    name=name,
                    version=info.get("version", "1.0.0"),
                    description=info.get("description", ""),
                    enabled=info.get("enabled", False),
                    builtin=info.get("builtin", False),
                    hooks=info.get("hooks", []),
                    config=info.get("config", {})
                ))
        return plugins
    
    def install_plugin(self, source: str) -> bool:
        """
        安装插件
        
        支持的来源:
        - GitHub: owner/repo
        - URL: https://example.com/plugin.zip
        - Local: ./path/to/plugin
        """
        print(f"Installing plugin from: {source}")
        
        if source.startswith("http://") or source.startswith("https://"):
            return self._install_from_url(source)
        elif "/" in source and not source.startswith("."):
            return self._install_from_github(source)
        else:
            return self._install_from_local(source)
    
    def _install_from_github(self, repo: str) -> bool:
        """从 GitHub 安装插件"""
        try:
            # 克隆仓库到临时目录
            temp_dir = self.plugins_dir / "_temp"
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            url = f"https://github.com/{repo}.git"
            subprocess.run(["git", "clone", "--depth", "1", url, str(temp_dir)], check=True)
            
            # 读取插件信息
            plugin_md = temp_dir / "PLUGIN.md"
            if not plugin_md.exists():
                print(f"Error: PLUGIN.md not found in {repo}")
                return False
            
            # 移动到插件目录
            plugin_name = repo.split("/")[-1]
            target_dir = self.plugins_dir / plugin_name
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.move(str(temp_dir), str(target_dir))
            
            # 注册插件
            self._register_plugin(plugin_name, {
                "name": plugin_name,
                "description": f"Plugin from {repo}",
                "version": "1.0.0",
                "enabled": False,
                "builtin": False,
                "hooks": [],
                "source": repo
            })
            
            print(f"Successfully installed plugin: {plugin_name}")
            return True
            
        except Exception as e:
            print(f"Error installing from GitHub: {e}")
            return False
    
    def _install_from_url(self, url: str) -> bool:
        """从 URL 安装插件"""
        print(f"Installing from URL is not yet implemented: {url}")
        return False
    
    def _install_from_local(self, path: str) -> bool:
        """从本地路径安装插件"""
        source_path = Path(path)
        if not source_path.exists():
            print(f"Error: Path not found: {path}")
            return False
        
        plugin_name = source_path.name
        target_dir = self.plugins_dir / plugin_name
        
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(str(source_path), str(target_dir))
        
        self._register_plugin(plugin_name, {
            "name": plugin_name,
            "description": f"Local plugin from {path}",
            "version": "1.0.0",
            "enabled": False,
            "builtin": False,
            "hooks": [],
            "source": "local"
        })
        
        print(f"Successfully installed plugin: {plugin_name}")
        return True
    
    def _register_plugin(self, name: str, info: Dict):
        """注册插件到注册表"""
        if "plugins" not in self.registry:
            self.registry["plugins"] = {}
        self.registry["plugins"][name] = info
        self._save_registry()
    
    def enable_plugin(self, name: str) -> bool:
        """启用插件"""
        if name not in self.registry.get("plugins", {}):
            print(f"Error: Plugin not found: {name}")
            return False
        
        self.registry["plugins"][name]["enabled"] = True
        self._save_registry()
        print(f"Enabled plugin: {name}")
        return True
    
    def disable_plugin(self, name: str) -> bool:
        """禁用插件"""
        if name not in self.registry.get("plugins", {}):
            print(f"Error: Plugin not found: {name}")
            return False
        
        self.registry["plugins"][name]["enabled"] = False
        self._save_registry()
        print(f"Disabled plugin: {name}")
        return True
    
    def update_plugin(self, name: str) -> bool:
        """更新插件"""
        if name not in self.registry.get("plugins", {}):
            print(f"Error: Plugin not found: {name}")
            return False
        
        plugin_info = self.registry["plugins"][name]
        source = plugin_info.get("source", "")
        
        if not source or source == "local":
            print(f"Cannot update local plugin: {name}")
            return False
        
        # 重新安装
        return self.install_plugin(source)
    
    def get_enabled_plugins_for_hook(self, hook: str) -> List[Plugin]:
        """获取特定 hook 的已启用插件"""
        plugins = []
        for name, info in self.registry.get("plugins", {}).items():
            if info.get("enabled", False) and hook in info.get("hooks", []):
                plugins.append(Plugin(
                    name=name,
                    version=info.get("version", "1.0.0"),
                    description=info.get("description", ""),
                    enabled=True,
                    builtin=info.get("builtin", False),
                    hooks=info.get("hooks", []),
                    config=info.get("config", {})
                ))
        return plugins


def main():
    parser = argparse.ArgumentParser(description="Multi-Platform Transformer Plugin Manager")
    parser.add_argument("action", choices=["list", "install", "update", "enable", "disable"],
                       help="Action to perform")
    parser.add_argument("target", nargs="?", help="Plugin name or source")
    parser.add_argument("--all", "-a", action="store_true", help="Show all plugins (including disabled)")
    parser.add_argument("--path", "-p", default=".", help="Base path for plugins")
    
    args = parser.parse_args()
    
    manager = PluginManager(args.path)
    
    if args.action == "list":
        plugins = manager.list_plugins(show_all=args.all)
        if not plugins:
            print("No plugins found.")
        else:
            print(f"\n{'Name':<25} {'Version':<10} {'Status':<10} {'Hooks'}")
            print("-" * 70)
            for p in plugins:
                status = "✅ Enabled" if p.enabled else "❌ Disabled"
                hooks = ", ".join(p.hooks) if p.hooks else "-"
                print(f"{p.name:<25} {p.version:<10} {status:<10} {hooks}")
    
    elif args.action == "install":
        if not args.target:
            print("Error: Please specify plugin source")
            sys.exit(1)
        success = manager.install_plugin(args.target)
        sys.exit(0 if success else 1)
    
    elif args.action == "update":
        if not args.target:
            print("Error: Please specify plugin name")
            sys.exit(1)
        success = manager.update_plugin(args.target)
        sys.exit(0 if success else 1)
    
    elif args.action == "enable":
        if not args.target:
            print("Error: Please specify plugin name")
            sys.exit(1)
        success = manager.enable_plugin(args.target)
        sys.exit(0 if success else 1)
    
    elif args.action == "disable":
        if not args.target:
            print("Error: Please specify plugin name")
            sys.exit(1)
        success = manager.disable_plugin(args.target)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
