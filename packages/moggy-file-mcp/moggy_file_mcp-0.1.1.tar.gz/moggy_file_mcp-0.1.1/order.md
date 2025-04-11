# 开发环境
uv init moggy-file-mcp
cd moggy-file-mcp
uv add "mcp[cli]"
# 安装工具包
python3 -m pip install --upgrade build
pip3 install hatchling
python -m build
### 安装工具包
"""
    用于使用其中的工具如: playwright
"""
pip install -U "autogen-agentchat" "autogen-ext[openai]"

pip install -U "autogenstudio"



### 上传工具包


pip install twine
twine upload dist/*

pypi-AgEIcHlwaS5vcmcCJDk3YjkzMTExLTZkMWEtNGJiYy04YTJmLTU5YWYwN2FhMGE5YgACKlszLCI3MWNiZmI1Yy03YzExLTRkYjgtYjA3Ny0xNGYyNWYwNThhNWMiXQAABiDeFR3XAJEG5ALXkAaSU4Pa_E9xnrYHQhVobNAXlpaxhg

### 上传后地址
https://pypi.org/project/moggy-mcp-server/0.1.0/

twine upload --repository-url https://test.pypi.org/legacy/ dist/*



testpypi: pip install --index-url https://test.pypi.org/simple/ scrapy-redis-bf
pypi: pip install --index-url https://pypi.org/simple/ scrapy-redis-bf
