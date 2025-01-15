from bs4 import BeautifulSoup

with open('html2.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
# 假设你的HTML文件内容已经被读取到变量html_content中  百度网盘.html
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有的<a>标签
links = soup.find_all('a')

# 提取每个<a>标签的title属性值
titles = [link.get('title') for link in links if link.get('title') is not None]
unique_data = list(set(titles))
# print(unique_data)
# 打印提取到的title值
# print(titles)
print(len(unique_data))

markdown_table = "| CN_NAME  |\n| ---- |\n"
for name in unique_data:
    markdown_table += f"| {name} |\n"
print(markdown_table)