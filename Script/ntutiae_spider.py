from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import os

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
            rows.append(
                [td.text.replace('\n', '').replace('\xa0', '').replace(" ", "").replace('\r', '').replace('\t',
                                                                                                          '')])  # .replace("]", "").replace("[", "")
    # print(rows)

    return rows


def md_format(ser):
    temp = []

    for i in ser:

        if type(i) == list:
            i = i[0]
        temp.append(i)

    ser = temp

    # print(ser)

    str_content = "---\ncoursen_name:{0[2]}\ncourse_eng_name:{0[3]}\nyear:{0[0]}\ncatctory:{0[1]}\n" \
                  "course_number:{0[4]}\ncredits:{0[5]}\nhours:{0[6]}\ncourse_url:{0[9]}\nteacher:\n" \
                  "---\n\n## 課程大綱\n\n{0[7]}\n" \
                  "\n\n## Course Outline\n\n{0[8]}\n".format(ser)

    base = "iae/{}/".format(ser[0])
    if not os.path.exists(base):
        os.makedirs(base)
    pathname = base + '{0}_{1}.md'.format(ser[0], ser[2].replace("/", ""))
    f = open(pathname, 'w', encoding="utf-8")
    print(str_content, file=f)
    f.close()


for btn_group in semester:

    semester_year = btn_group.find("span", style="font-family:微軟正黑體;")  # 印出幾年級
    print("-------------------------------------")
    print(semester_year.text, "\n")

    catctory = btn_group.find_all("button", class_=accordion_i)  # 找課程類別

    accordion_i = "accordion" + str(i)

    count_catctory = 0

    courseS = btn_group.find_all("div", class_="btn-group")  # 找到課程的區塊

    for courses in courseS:

        print(catctory[count_catctory].text, "\n")  # 印出課程類別
        catctory_text = catctory[count_catctory].text
        count_catctory = count_catctory + 1

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
            ser = [semester_year.text, catctory_text, c.text, rows[2], rows[0], rows[3], rows[4], rows[5], rows[6],
                   href]
            print(ser)
            # s = pd.Series(ser,index=["year", 'catctory', 'coursen_name', 'course_eng_name', 'course_number', 'course_score',
            # 'course_hours', 'course_dis_chn', 'course_dis_eng', 'href'])
            md_format(ser)
            # 準備儲存
            # df = df.append(s,ignore_index=True)

    i = i + 1
# print(df)
# df.to_csv("iae_course.csv", encoding="utf-8", index=False)
