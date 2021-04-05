import os

import html2text
import pdfkit
from markdown import markdown
from pymdownx import superfences

from Workplatform.settings import MEDIA_FILE
from adminq.models import OperatingLog


def write_sys_log(acte_info, user):
    try:
        print(user.name, acte_info)
        OperatingLog.objects.create(
            content=acte_info,
            operator_id=user.id
        )
        return True
    except Exception as e:
        print(e)
        return False


def handle_repet_name(file_name):
    init_name = file_name
    save_file_path = os.path.join(MEDIA_FILE, file_name)
    init_num = 0
    while True:
        init_num += 1
        if os.path.exists(save_file_path):
            file_name = f'({init_num})' + init_name
            save_file_path = os.path.join(MEDIA_FILE, file_name)
        else:
            break
    return save_file_path, file_name


def delete_note_image(content):
    try:
        for i in content.split('/media/images/'):
            for j in i.split(')'):
                if not j:
                    continue
                path_img = os.path.abspath('./media/images/') + '/' + j
                if os.path.exists(path_img):
                    print(path_img)
                    os.remove(path_img)
    except Exception as e:
        print(e)
        raise


class MarkdownPdf:
    def __init__(self):

        self.html = '''
            <!DOCTYPE html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
                    <title>文件下载</title>
                </head>
                <body>
                    <article class="markdown-body">
                        {}
                    </article>
                </body>
            </html>
            '''
        self.extensions = [
                'toc',  # 目录，[toc]
                'extra',  # 缩写词、属性列表、释义列表、围栏式代码块、脚注、在HTML的Markdown、表格
            ]
        self.third_party_extensions = [
                'mdx_math',  # KaTeX数学公式，$E=mc^2$和$$E=mc^2$$
                'markdown_checklist.extension',  # checklist，- [ ]和- [x]
                'pymdownx.magiclink',  # 自动转超链接，
                'pymdownx.caret',  # 上标下标，
                'pymdownx.superfences',  # 多种块功能允许嵌套，各种图表
                'pymdownx.betterem',  # 改善强调的处理(粗体和斜体)
                'pymdownx.mark',  # 亮色突出文本
                'pymdownx.highlight',  # 高亮显示代码
                'pymdownx.tasklist',  # 任务列表
                'pymdownx.tilde',  # 删除线
            ]
        self.extensions.extend(self.third_party_extensions)
        self.extension_configs = {
                'mdx_math': {
                    'enable_dollar_delimiter': True  # 允许单个$
                },
                'pymdownx.superfences': {
                    "custom_fences": [
                        {
                            'name': 'mermaid',  # 开启流程图等图
                            'class': 'mermaid',
                            'format': superfences.fence_div_format
                        }
                    ]
                },
                'pymdownx.highlight': {
                    'linenums': True,  # 显示行号
                    'linenums_style': 'pymdownx-inline'  # 代码和行号分开
                },
                'pymdownx.tasklist': {
                    'clickable_checkbox': True,  # 任务列表可点击
                }
            }
        self.options = {
            'page-size': 'A4',
            'margin-top': '10mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            # 'orientation':'Landscape',#横向
            'encoding': "UTF-8",
            'no-outline': None,
            'footer-right': '[page]'  # 设置页码
        }

    def md_to_html(self, content):
        # MarkDown转HTML
        html_content = markdown(
            content, output_format='html', extensions=self.extensions, extension_configs=self.extension_configs)
        return html_content

    def html_to_pdf(self, text, save_path):
        # HTML转PDF
        content_html = self.html.format(text)
        pdfkit.from_string(content_html, save_path, options=self.options)

    @classmethod
    def html_to_markdown(cls, html_text):
        # HTML 转 MD
        text_maker = html2text.HTML2Text()
        text_maker.bypass_tables = False
        markdown_text = text_maker.handle(html_text)
        return markdown_text


