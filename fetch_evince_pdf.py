import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger
import datetime
import subprocess as sp

# 1. 取得先URL
url = "https://www.hbc.co.jp/weather/pro-weather.html"

# 2. ページを取得
response = requests.get(url)
response.raise_for_status()  # 取得に失敗した場合は例外を出す

# 3. BeautifulSoupでHTMLを解析
soup = BeautifulSoup(response.content, "html.parser")

# 4. PDFリンクを収集
pdf_urls = []
for a_tag in soup.find_all("a", href=True):
    link = a_tag["href"]
    # PDFファイルへのリンクかどうか確認
    if link.lower().endswith(".pdf"):
        # 絶対URLでなければ、サイトのドメインを付けるなどの処理が必要
        if link.startswith("http"):
            pdf_urls.append(link)
        else:
            pdf_urls.append("https://www.hbc.co.jp" + link)

# 5. PDFを保存するフォルダを作成（存在しない場合のみ）
pdf_folder = "pdfs_temp"
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# 6. 各PDFをダウンロード
for i, pdf_url in enumerate(pdf_urls):
    print(f"Downloading PDF: {pdf_url}")
    pdf_data = requests.get(pdf_url)
    pdf_data.raise_for_status()
    
    pdf_filename = f"document_{i}.pdf"
    with open(os.path.join(pdf_folder, pdf_filename), "wb") as f:
        f.write(pdf_data.content)

# 7. PDFを結合
# PyPDF2のPdfMergerを使う方法
merger = PdfMerger()

# ダウンロードした順番で結合
for i in range(len(pdf_urls)):
    pdf_path = os.path.join(pdf_folder, f"document_{i}.pdf")
    merger.append(pdf_path)

# 結合結果のファイル名

now = datetime.datetime.now()
formatted_date = now.strftime("%y%m%d")
formatted_time = now.strftime("%H%M")

directory_name = "/mnt/c/Users/omary/OneDrive - 国立大学法人東北大学/Laboratory_msodrive/weathermap/"
pdf_name = formatted_date + "_" + formatted_time + "_mergedmap.pdf"
merged_pdf_name = directory_name + pdf_name
merger.write(merged_pdf_name)
merger.close()

print(f"PDFが結合されました: {merged_pdf_name}")

dir_here = "weathermap/"
if not os.path.exists(dir_here):
    os.makedirs(dir_here)

sp.run(["cp",merged_pdf_name,dir_here])
sp.run(["evince",dir_here+pdf_name])


