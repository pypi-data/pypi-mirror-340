# 说明

## 安装与使用

1. 安装uv：`pip install uv`
2. 安装第三方依赖库：`uv add <package_name>`
3. 更新第三方依赖库：`uv add -U <package_name>`
4. 卸载第三方依赖库：`uv remove <package_name>`
5. 使用uv运行脚本：`uv run app.py`

## 换源

在pyproject.toml中添加以下内容：

```toml
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

## 打包

1. 配置pyproject.toml：# TODO:xiedali@2025/04/12 目前还不知道怎么配置
2. 打包：`uv build`
3. 上传：`uv publish`
