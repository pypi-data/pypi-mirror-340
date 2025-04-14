# yyAutoAiframework

## 创建虚拟环境
uv venv .venv

# 激活虚拟环境（根据你的 shell）
# Bash/Zsh:
source .venv/bin/activate
# Fish:
source .venv/bin/activate.fish
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# 然后在虚拟环境中安装依赖
uv pip install -e .

## 打包
pip install twine
python setup.py sdist bdist_wheel  # 生成 `dist/` 目录

twine upload dist/*