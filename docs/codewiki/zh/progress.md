# 进度跟踪器

进度跟踪器提供带有 ETA 估算的 CLI 进度指示器。

## 概述

进度跟踪器提供：
- 基于阶段的进度跟踪
- ETA 估算
- 模块的进度条

## 类

### ProgressTracker

跟踪文档生成各阶段的进度：

```python
class ProgressTracker:
    STAGE_WEIGHTS = {
        1: 0.40,  # Dependency Analysis
        2: 0.20,  # Module Clustering
        3: 0.30,  # Documentation Generation
        4: 0.05,  # HTML Generation
        5: 0.05,  # Finalization
    }
```

### ModuleProgressBar

逐个生成模块的进度条：

```python
class ModuleProgressBar:
    def __init__(self, total_modules: int, verbose: bool = False):
        self.total_modules = total_modules

    def update(self, module_name: str, cached: bool = False):
        """Update progress for a module."""
```

## 用法

```python
tracker = ProgressTracker(total_stages=5, verbose=True)

# Stage 1: Dependency Analysis
tracker.start_stage(1, "Dependency Analysis")
tracker.update_stage(0.5, "Parsing files...")
tracker.complete_stage()

# Stage 2: Module Clustering
tracker.start_stage(2, "Module Clustering")
...
```

## 输出示例

```
[1/5] 阶段 1: 依赖分析
[00:05]   正在解析文件...
[00:12]   依赖分析完成 (12.5s)

[2/5] 阶段 2: 模块聚类
...
```

## 相关文档

- [CLI 概述](cli_overview.md)