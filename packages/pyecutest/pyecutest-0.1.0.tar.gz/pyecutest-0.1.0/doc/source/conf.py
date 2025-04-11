import os
import sys

# 修改为项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# 项目信息
project = 'PyECUTest'
copyright = '2024, Your Name'
author = 'Your Name'

# 语言设置
language = 'zh_CN'

# HTML输出设置
html_theme = 'sphinx_rtd_theme'  # 使用Read the Docs主题
html_theme_options = {
    'display_version': True,
}

# 文件编码设置
source_encoding = 'utf-8'
html_output_encoding = 'utf-8'

# 扩展设置
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
    'sphinx_rtd_theme',
]

# autodoc设置
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# napoleon设置
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# LaTeX设置（支持中文PDF输出）
latex_elements = {
    'preamble': r'''
    \usepackage{xeCJK}
    \setCJKmainfont{SimSun}
    ''',
}

# 设置主文档
master_doc = 'index'


