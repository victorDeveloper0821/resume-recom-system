import os
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import pdfplumber
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class ResumeParser(ABC):
    """履歷解析基底類別"""

    def __init__(self, file_path=None, text=None):
        self.file_path = file_path
        self.text = text

    @abstractmethod
    def extract_text(self):
        """抽象方法，子類別需實作此方法來解析文本"""
        pass


class HtmlResumeParser(ResumeParser):
    """HTML 履歷解析類別"""

    def extract_text(self):
        try:
            # Parse HTML from text or file
            if self.text:
                soup = BeautifulSoup(self.text, "html.parser")
            elif self.file_path:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "html.parser")
            else:
                raise ValueError("HTML content not provided")

            ## html section extract
            sections = soup.find_all("div", class_="section")
            
            results = {}
            html_text = ''
            
            for i, sec in enumerate(sections, 1):
                
                # Extract section title
                title_tag = sec.find('div', class_='sectiontitle')
                if title_tag:
                    title = title_tag.get_text(strip=True)

                # Extract all paragraph divs within this section
                paragraph_tags = sec.find_all('div', class_='paragraph')
                for para in paragraph_tags:
                    paragraph_text = para.get_text(strip=True)
                    
                if title_tag and title_tag.get_text(strip=True) != "":
                    results[title] = paragraph_text
                    html_text = html_text + '\n' + title+ '\n' + paragraph_text
                    
            ## html_text for concatinate the html text in html file or html text into plain text 
            ## embedding the text
            embeddings = model.encode(html_text)  
            results["embedded_vector"] = embeddings.tolist()
            
            return results

        except Exception as e:
            print(f"HTML Parse error: {e}")
            return []


class PdfResumeParser(ResumeParser):
    """PDF 履歷解析類別"""

    def extract_text(self):
        """使用 pdfplumber 解析 PDF 文件"""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return full_text.strip()
        except Exception as e:
            print(f"PDF 解析錯誤: {e}")
            return ""
        

def get_resume_parser(file_path=None, html_text=None):
    """
    根據文件副檔名或傳入 HTML 文字選擇適當的解析器
    """
    if html_text:
        return HtmlResumeParser(text=html_text)

    if file_path:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == ".pdf":
            return PdfResumeParser(file_path=file_path)
        elif ext in [".html", ".htm"]:
            return HtmlResumeParser(file_path=file_path)
        else:
            raise ValueError("不支援的履歷格式: " + ext)

    raise ValueError("請提供檔案路徑或 HTML 文本。")
