from abc import ABC, abstractmethod
import os 
class ResumeParser():
    """履歷解析基底類別"""
    
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def extract_text(self):
        """抽象方法，子類別需實作此方法來解析文本"""
        pass

class PdfResumeParser(ResumeParser):
    """PDF 履歷解析類別"""
    
    def extract_text(self):
        """使用 textract 解析 PDF 文本"""
        try:
            text = textract.process(self.file_path, method='pdftotext').decode('utf-8')
            return text.strip()
        except Exception as e:
            print(f"PDF 解析錯誤: {e}")
            return ""

class HtmlResumeParser(ResumeParser):
    """HTML 履歷解析類別"""

    def extract_text(self):
        """使用 BeautifulSoup 解析 HTML 文本"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                return soup.get_text().strip()
        except Exception as e:
            print(f"HTML 解析錯誤: {e}")
            return ""

def get_resume_parser(file_path):
    """根據文件副檔名選擇適當的解析器"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return PdfResumeParser(file_path)
    elif ext == ".html" or ext == ".htm":
        return HtmlResumeParser(file_path)
    else:
        raise ValueError("不支援的履歷格式: " + ext)