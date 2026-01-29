#!/usr/bin/env python3
"""
Multi-Platform Transformer Core
核心转换引擎
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib


@dataclass
class Platform:
    """平台配置"""
    code: str
    name: str
    tech_stack: Dict[str, Any]
    enabled: bool = True


@dataclass
class Requirement:
    """需求定义"""
    id: str
    name: str
    description: str
    features: List[Dict]
    pages: List[Dict]
    models: List[Dict]
    apis: List[Dict]
    flows: List[Dict]


@dataclass
class TransformContext:
    """转换上下文"""
    project_name: str
    requirements: Requirement
    platforms: List[Platform]
    output_dir: Path
    cache_dir: Path
    language: str = "zh-CN"


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, base_path: str = ".multi-platform"):
        self.base_path = Path(base_path)
        self.config_file = self.base_path / "config.yaml"
    
    def load(self) -> Dict:
        """加载配置文件"""
        if not self.config_file.exists():
            return self._default_config()
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "project": {
                "name": "my-app",
                "version": "1.0.0"
            },
            "platforms": {
                "enabled": ["android", "ios", "wechat-mp", "h5"]
            },
            "tech_stack": {},
            "output": {
                "directory": ".multi-platform/output",
                "include_tests": True,
                "include_docs": True,
                "language": "zh-CN"
            }
        }


class RequirementParser:
    """需求文档解析器"""
    
    def __init__(self, requirements_dir: Path):
        self.requirements_dir = requirements_dir
    
    def parse(self) -> Optional[Requirement]:
        """解析需求文档"""
        # 查找 PRD 文件
        prd_files = list(self.requirements_dir.glob("*.md"))
        if not prd_files:
            return None
        
        prd_file = prd_files[0]
        content = prd_file.read_text(encoding='utf-8')
        
        # 解析需求（简化版本，实际由 AI 完成复杂解析）
        return Requirement(
            id=self._generate_id(content),
            name=prd_file.stem,
            description="",
            features=[],
            pages=[],
            models=[],
            apis=[],
            flows=[]
        )
    
    def _generate_id(self, content: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:8]


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.cache_dir / "manifest.json"
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """加载缓存清单"""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"files": {}, "last_updated": None}
    
    def _save_manifest(self):
        """保存缓存清单"""
        self.manifest["last_updated"] = datetime.now().isoformat()
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2)
    
    def get_file_hash(self, file_path: Path) -> str:
        """获取文件哈希"""
        if not file_path.exists():
            return ""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
    
    def is_cached(self, file_path: Path) -> bool:
        """检查文件是否已缓存且未变化"""
        key = str(file_path)
        if key not in self.manifest["files"]:
            return False
        cached_hash = self.manifest["files"][key].get("hash", "")
        current_hash = self.get_file_hash(file_path)
        return cached_hash == current_hash
    
    def update_cache(self, file_path: Path, output_files: List[str]):
        """更新缓存"""
        key = str(file_path)
        self.manifest["files"][key] = {
            "hash": self.get_file_hash(file_path),
            "output_files": output_files,
            "timestamp": datetime.now().isoformat()
        }
        self._save_manifest()
    
    def backup(self, output_dir: Path):
        """备份当前输出"""
        backup_dir = self.cache_dir / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_dir.exists():
            import shutil
            shutil.copytree(output_dir, backup_dir)
            print(f"Backup created: {backup_dir}")


class Transformer:
    """多端转换器"""
    
    PLATFORM_NAMES = {
        "android": "Android",
        "ios": "iOS",
        "harmony": "HarmonyOS",
        "wechat-mp": "微信小程序",
        "alipay-mp": "支付宝小程序",
        "baidu-mp": "百度智能小程序",
        "quick-app": "快应用",
        "h5": "H5/Web",
        "flutter": "Flutter",
        "react-native": "React Native",
        "uni-app": "Uni-app",
        "taro": "Taro"
    }
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.multi_platform_dir = self.base_path / ".multi-platform"
        self.config_loader = ConfigLoader(str(self.multi_platform_dir))
        self.config = self.config_loader.load()
    
    def initialize(self):
        """初始化项目结构"""
        directories = [
            self.multi_platform_dir,
            self.multi_platform_dir / "requirements",
            self.multi_platform_dir / "output",
            self.multi_platform_dir / "cache",
            self.multi_platform_dir / "reports",
            self.multi_platform_dir / "i18n"
        ]
        
        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 复制默认配置
        if not (self.multi_platform_dir / "config.yaml").exists():
            self._create_default_config()
        
        print(f"Initialized multi-platform project at {self.multi_platform_dir}")
    
    def _create_default_config(self):
        """创建默认配置文件"""
        default_config = self.config_loader._default_config()
        with open(self.multi_platform_dir / "config.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
    
    def get_enabled_platforms(self) -> List[Platform]:
        """获取启用的平台"""
        enabled = self.config.get("platforms", {}).get("enabled", [])
        tech_stacks = self.config.get("tech_stack", {})
        
        platforms = []
        for code in enabled:
            platforms.append(Platform(
                code=code,
                name=self.PLATFORM_NAMES.get(code, code),
                tech_stack=tech_stacks.get(code, {}),
                enabled=True
            ))
        return platforms
    
    def transform(self, platforms: Optional[List[str]] = None):
        """
        执行转换
        
        实际的代码生成由 AI Agent 根据 SKILL.md 和各平台插件指令完成
        此方法主要用于初始化和验证
        """
        # 加载配置
        config = self.config
        
        # 确定目标平台
        if platforms:
            target_platforms = platforms
        else:
            target_platforms = config.get("platforms", {}).get("enabled", [])
        
        print(f"Target platforms: {', '.join(target_platforms)}")
        
        # 检查需求文档
        requirements_dir = self.multi_platform_dir / "requirements"
        if not any(requirements_dir.glob("*.md")):
            print("Warning: No requirement documents found in requirements/")
            print("Please add your PRD.md or other requirement documents.")
            return
        
        # 初始化缓存
        cache_manager = CacheManager(self.multi_platform_dir / "cache")
        
        # 备份现有输出
        output_dir = self.multi_platform_dir / "output"
        if output_dir.exists() and any(output_dir.iterdir()):
            cache_manager.backup(output_dir)
        
        # 创建平台输出目录
        for platform in target_platforms:
            (output_dir / platform).mkdir(parents=True, exist_ok=True)
        
        # 创建共享资源目录
        (output_dir / "_shared").mkdir(parents=True, exist_ok=True)
        
        print("\nReady for transformation.")
        print("AI Agent will now analyze requirements and generate platform-specific code.")
        print("\nTell your AI Agent:")
        print('  🤖 "generate code for all platforms"')
        print('  🤖 "transform to android"')
        print('  🤖 "生成多端代码"')


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Platform Transformer")
    parser.add_argument("action", choices=["init", "transform", "status"],
                       help="Action to perform")
    parser.add_argument("--platforms", "-p", nargs="+",
                       help="Target platforms (e.g., android ios wechat-mp)")
    parser.add_argument("--path", default=".", help="Project path")
    
    args = parser.parse_args()
    
    transformer = Transformer(args.path)
    
    if args.action == "init":
        transformer.initialize()
    
    elif args.action == "transform":
        transformer.transform(args.platforms)
    
    elif args.action == "status":
        platforms = transformer.get_enabled_platforms()
        print(f"\nEnabled platforms ({len(platforms)}):")
        for p in platforms:
            print(f"  - {p.name} ({p.code})")


if __name__ == "__main__":
    main()
