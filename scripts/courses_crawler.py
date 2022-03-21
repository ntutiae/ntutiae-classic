from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import os
import string

df = pd.DataFrame(columns=["year", 'catctory', 'coursen_name', 'course_eng_name', 'course_number', 'course_score',
                           'course_hours', 'course_dis_chn', 'course_dis_eng', 'href'])

response = urlopen("https://iae.ntut.edu.tw/p/404-1068-90028.php?Lang=zh-tw")

html = BeautifulSoup(response)

semester = html.find_all("div", class_="column")  # 找到年級格

i = 1
accordion_i = "accordion"


def course_contants(href):
    columns = []
    course_response = urlopen(href)
    course_contant_html = BeautifulSoup(course_response)
    table = course_contant_html.find('table')
    for tr in table.find_all('tr'):
        for th in tr.find_all('th'):
            columns.append(th.text.replace('\n', ''))  # .replace(" ", "").replace("]", "").replace("[", "")
    # print(columns)

    trs = table.find_all('tr')[1:]
    rows = []
    for tr in trs:
        for td in tr.find_all('td'):
            rows.append(td.text.strip())
    # print(rows)

    return rows


def md_format(**kwargs):
    tpl = string.Template("""
---
title: "$name"
course_eng_name: "$name_en"
year: "$year"
categories: ["$categories"]
course_number: "$course_number"
credits: $credits
hours: $hours
course_url: "$course_url"
image: "/images/portfolio/item-2.png"
---

## 課程大綱

$outline

## Course Outline

$outline_en
""")
    result = tpl.substitute(**kwargs)

    base = f'iae/{kwargs["year"]}'

    if not os.path.exists(base):
        os.makedirs(base)
    pathname = f'{base}/{kwargs["year"]}_{kwargs["name"].replace("/", "-")}.md'
    with open(pathname, 'w', encoding="utf-8") as f:
        f.write(result)


for btn_group in semester:

    semester_year = btn_group.find("span", style="font-family:微軟正黑體;")  # 印出幾年級
    print("-------------------------------------")
    print(semester_year.text, "\n")

    category = btn_group.find_all("button", class_=accordion_i)  # 找課程類別

    accordion_i = "accordion" + str(i)

    count_category = 0

    courseS = btn_group.find_all("div", class_="btn-group")  # 找到課程的區塊

    for courses in courseS:

        print(category[count_category].text, "\n")  # 印出課程類別
        category_text = category[count_category].text
        count_category = count_category + 1

        cours = courses.find_all("button", class_="button")  # 找到區塊裡面的課程

        for c in cours:
            print(c.text)  # 抓課程名稱
            href = c["onclick"]  # 抓網址
            # 過濾出網址
            href = href.split("=", 1)
            h = href[1].split("'")
            href = h[1].replace("	", "")
            print(href)
            print("\n")
            rows = course_contants(href)
            rows.append(href)
            # print(rows)
            ser = [semester_year.text, category_text, c.text, rows[2], rows[0], rows[3], rows[4], rows[5], rows[6],
                   href]
            # s = pd.Series(ser,index=["year", 'catctory', 'coursen_name', 'course_eng_name', 'course_number', 'course_score',
            # 'course_hours', 'course_dis_chn', 'course_dis_eng', 'href'])
            md_format(
                name=c.text,
                name_en=rows[2],
                year=semester_year.text,
                categories=category_text,
                course_number=rows[0],
                credits=rows[3],
                hours=rows[4],
                course_url=href,
                outline=rows[5],
                outline_en=rows[6],
            )
            # 準備儲存
            # df = df.append(s,ignore_index=True)

    i = i + 1
# print(df)
# df.to_csv("iae_course.csv", encoding="utf-8", index=False)
