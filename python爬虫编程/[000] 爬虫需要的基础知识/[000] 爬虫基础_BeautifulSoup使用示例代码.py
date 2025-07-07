
'''
    # 安装beautifulsoup:
    # pip install beautifulsoup4

    # BeautifulSoup 是 Python 中用于 解析 HTML/XML 文档 的库,
    # 主要功能是从网页中高效提取结构化数据,
    # 它常与网络请求库（如 requests）配合使用,是爬虫开发的核心工具之一.

    # BeautifulSoup 的核心功能
    # BeautifulSoup 主要完成以下任务
    #     解析文档: 将 HTML/XML 文档转换为树形结构(解析树)
    #     修复错误: 自动修复不规范的 HTML (如未闭合的标签、缺失的标签)
    #     数据提取: 提供多种方法搜索和提取特定元素(获取标签内的文本、属性值等内容.)
    #     文档操作: 支持修改、删除和添加元素
    #     导航文档树: 通过标签名、属性、文本内容等快速定位节点.
'''


'''
soup(BeautifulSoup)的函数有哪些？
1. 核心搜索方法
    说明             方法              描述                                                   示例
    查找单个元素       find()          返回第一个匹配的标签（等价于 find_all(..., limit=1)）        soup.find(id='main')
    查找多个元素       find_all()      返回所有匹配条件的标签（列表）                               soup.find_all('div', class_='header')
    CSS选择器         select()        使用 CSS 选择器返回匹配列表                                soup.select('div.header > a')
    select_one()     select_one()    使用 CSS 选择器返回第一个匹配的标签                          soup.select_one('.logo')

2. 层级关系导航
    方法                               描述
    parent / parents                  获取父标签 / 递归获取所有祖先标签
    next_sibling / previous_sibling   下一个/上一个兄弟标签
    next_element / previous_element   解析顺序的下一个/上一个元素（含文本节点）
    contents                          子节点列表（含换行等文本节点）
    children                          子节点的迭代器
    descendants                       递归遍历所有子孙节点

3. 定向搜索（基于位置）
    方法                               描述
    find_next()                       查找之后第一个匹配的标签
    find_all_next()	                  查找之后所有匹配的标签
    find_previous()	                  查找之前第一个匹配的标签
    find_all_previous()	              查找之前所有匹配的标签

4. 文本内容提取
    方法                               描述
    get_text()	                      提取标签内所有文本（合并子标签文本）
    strings	                          生成器: 逐行返回子节点的文本（保留空白）
    stripped_strings	              生成器: 返回去除空白的文本

5. 属性操作
    方法                               描述
    get('attr')	                      获取属性值（如 tag.get('href')）
    ['attr']	                      直接访问属性（属性不存在时报错）
    has_attr('attr')	              检查属性是否存在
    attrs	                          返回属性字典 (如 {'class': ['header']})

6. 文档树修改
    方法                               描述
    append()	                      添加子节点
    extract()	                      移除标签 (返回被移除的标签)
    decompose()	                      销毁标签 (从内存中移除)
    replace_with()	                  替换标签内容
    new_tag()	                      创建新标签 (需配合 append 使用)

# -----------------------------------------------------------------------------------------------------------
    # find()函数参数使用示例
    element = soup.find (name, attrs, recursive=True, string=None, **kwargs)
        name:       标签名 (字符串),              例如 'div', 'a', 'p'
        attrs:      属性字典 (或关键字参数) ,       如 class_, id, href 等
        recursive:  是否递归搜索子节点 (默认 True)
        string:     按文本内容匹配
    
    result = soup.find(
        name=None, attrs={}, recursive=True, string=None, 
        **kwargs
    )
    
    组合规律表
    查找目标	        代码示例
    特定标签	        find('div')
    标签+ID	        find('div', id='content')
    标签+Class	    find('div', class_='header')
    标签+自定义属性	find('a', data_track='click')
    标签+多个属性	    find('input', type='text', name='email')
    文本内容	        find(string='Submit')
    标签+文本	    find('button', string='Submit')

# -----------------------------------------------------------------------------------------------------------
    BeautifulSoup()的核心输入参数有哪些:
    1. 解析器参数
    # 不同解析器的使用
        soup_lxml = BeautifulSoup(html_doc, 'lxml')             # 需要安装 lxml (pip install lxml)
        soup_html5lib = BeautifulSoup(html_doc, 'html5lib')     # 需要安装 html5lib (pip install html5lib)
    解析器	        速度	    特点	            依赖
    html.parser	    中	    Python标准库	    无需额外安装
    lxml	        快	    高效解析	        需要 lxml
    html5lib	    慢	    最接近浏览器解析	需要 html5lib
    
    2. 其他重要参数
    soup = BeautifulSoup(
        markup,                             # HTML/XML 文档内容
        features='html.parser',             # 指定解析器
        from_encoding='utf-8',              # 指定文档编码
        exclude_encodings=[],               # 排除特定编码
        parse_only=None,                    # 仅解析部分文档
        on_duplicate_attribute='replace'    # 处理重复属性
    )

# -----------------------------------------------------------------------------------------------------------
    HTML 处理流程
    BeautifulSoup 处理 HTML 的完整过程：
        输入处理: 接收字符串或文件对象
        编码检测: 自动检测或使用指定编码
        解析构建: 创建文档树结构
        树形转换: 生成包含 Tag、NavigableString 等对象的树
        修复处理: 修正不规范 HTML（如自动闭合标签）
        输出准备: 提供访问和操作方法

    # 查找第一个 <div> 标签
    div = soup.find('div')
    # 获取标签文本（自动去除空白）
    text = div.text
    # 获取标签名
    tag_name = div.name
    # 获取父节点
    parent = div.parent
    # 获取直接子节点
    children = div.contents
    # 获取兄弟节点
    next_sib = div.next_sibling
    prev_sib = div.previous_sibling

# -----------------------------------------------------------------------------------------------------------
    CSS 选择器基础
    BeautifulSoup 的 select() 方法使用 CSS 选择器语法：
        # 选择器示例
        soup.select('div')              # 所有div
        soup.select('.header')          # class="header" 的元素
        soup.select('#search-box')      # id="search-box" 的元素
        soup.select('div.item > a')     # div.item 下的直接子元素a标签
'''

import re # 正则表达式
import requests
from bs4 import BeautifulSoup

# -------------------------------------------------------------------------------
# 基础用法___基础代码框架,
# 1. 获取网页内容
url = "https://example.com"
response = requests.get(url)
html_content = response.text
# 2. 创建 BeautifulSoup 对象（指定解析器）
soup = BeautifulSoup(html_content, 'html.parser')  # 或 'lxml'
# 3. 使用查找方法提取数据
# ...
# -------------------------------------------------------------------------------
# 基础功能用法___查找单个元素
# 查找第一个 <div> 标签
div = soup.find('div')
# 查找第一个 class="header" 的 <div>
div_header = soup.find('div', class_='header')
# 查找 id="main" 的标签
main_content = soup.find(id='main')

# -------------------------------------------------------------------------------
# 基础功能用法___查找多个元素
# 查找所有 <a> 标签
all_links = soup.find_all('a')

# 查找所有 class="item" 的 <li>
items = soup.find_all('li', class_='item')

# 限制返回数量 (前3个)
first_three_links = soup.find_all('a', limit=3)

# -------------------------------------------------------------------------------
# 基础功能用法___CSS选择器
# 选择所有 class="title" 的 <h2> 标签
titles = soup.select('h2.title')

# 选择 id="footer" 内的所有 <a> 标签
footer_links = soup.select('#footer a')

# 选择属性包含 "example" 的链接
special_links = soup.select('a[href*="example"]')

# -------------------------------------------------------------------------------
# 基础功能用法___提取数据
# 获取标签文本（自动去除空白）
text = div.text

# 获取属性值
# link = a_tag['href']          # 直接访问属性（可能报错）
# safe_link = a_tag.get('href')  # 安全获取（属性不存在返回 None）

# 获取标签名
tag_name = div.name  # 返回 'div'

# -------------------------------------------------------------------------------
# 基础功能用法___层级导航
# 获取父节点
parent = div.parent

# 获取直接子节点
children = div.contents       # 包含换行符等
clean_children = div.children # 迭代器（过滤空白节点）

# 获取兄弟节点
next_sib = div.next_sibling
prev_sib = div.previous_sibling
# -------------------------------------------------------------------------------
# 高级功能用法___处理嵌套结构

# 链式查找：先找 <div class="container">，再找内部所有 <p>
paragraphs = soup.find('div', class_='container').find_all('p')

# -------------------------------------------------------------------------------
# 高级功能用法___正则表达式匹配
# 查找 href 包含 "download" 的链接
download_links = soup.find_all('a', href=re.compile(r'download'))

# -------------------------------------------------------------------------------
# 高级功能用法___提取结构化数据
# 提取所有链接的文本和URL
links_data = []
for a in soup.find_all('a'):
    links_data.append({
        'text': a.text.strip(),
        'url': a.get('href')
    })

# -------------------------------------------------------------------------------
# 高级功能用法___处理编码问题
# 自动处理编码（推荐使用 lxml 解析器）
soup = BeautifulSoup(html_content, 'lxml', from_encoding='utf-8')

# -------------------------------------------------------------------------------
# 完整用法___爬取名言网站
url = "http://quotes.toscrape.com"
response = requests.get(url)
soup_intact = BeautifulSoup(response.text, 'lxml')  # 对爬取到的HTML文本进行处理

# 提取所有名言文本和作者
quotes = []
for quote in soup_intact.select('div.quote'):
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    quotes.append({'text': text, 'author': author})

print(quotes[0])  # 输出第一条结果

# ---------------------
# 代码示例
from bs4 import BeautifulSoup

html = """
<div class="container">
    <p>First <b>bold</b> text.</p>
    <p>Second <a href="#">link</a></p>
</div>
"""
soup = BeautifulSoup(html, 'html.parser')

# 1. 使用 find_all 获取所有 <p> 标签
all_p = soup.find_all('p')  # 返回包含两个 <p> 的列表
# 2. 使用 CSS 选择器
links = soup.select('p > a')  # 返回 [<a href="#">link</a>]
# 3. 提取文本
first_p_text = soup.p.get_text()  # "First bold text."
# 4. 层级导航
second_p = soup.find_all('p')[1]
parent_div = second_p.parent  # 获取父标签 <div class="container">
# 5. 属性操作
link_tag = soup.find('a')
href = link_tag.get('href')  # "#"
link_tag['target'] = '_blank'  # 添加新属性

