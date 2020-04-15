import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import json
import re
import os
import csv

url = "http://www.mse.buaa.edu.cn/szdw/jslb.htm"
html_path = "./html"
json_path = "./json"
csv_file = "./名单.csv"


def remove_attrs(soup):
    """ 移除 HTML 多余信息 """
    for tag in soup.findAll(True):
        for attr in ['class', 'id', 'style']:
            if attr in tag.attrs:
                del tag.attrs[attr]
    return soup


class Teacher:
    def __init__(self):
        # 姓名
        self.name = ""
        # 性别(male, female)
        self.gender = ""
        # 出生年月
        self.birthday = ""
        # 毕业院校
        self.graduated_from = ""
        # 学位/最高学历
        self.degree = ""
        # 职称
        self.title = ""
        # 荣誉称号
        self.honorary_titles = ""
        # 所在高校
        self.organization = ""
        # 所在学院(学院/学部/研究所/部门)
        self.department = ""
        # 所在专业/学科
        self.major = ""
        # 所属实验室/课题组
        self.library = ""
        # 研究方向/兴趣方向
        self.research_areas = ""
        # 个人履历/个人简历
        self.personal_introduction = ""
        # 教育经历
        self.education_history = ""
        # 工作经历
        self.work_history = ""
        # 获奖经历
        self.honor_history = ""
        # 讲授课程
        self.courses = ""
        # 社会兼职
        self.social_position = ""
        # 学术兼职
        self.academical_position = ""
        # 代表性研究成果/论文
        self.achievements = ""
        # 专利情况
        self.patents = ""
        # 主持项目
        self.projects = ""
        # 参加会议情况
        self.conferences = ""
        # 手机号
        self.mobile = ""
        # 联系方式
        self.contact = ""
        # 联系邮箱
        self.email = ""
        # 省
        self.province = ""
        # 市
        self.city = ""
        # 办公地址/联系地址/具体地址
        self.address = ""


def append_csv_file(teacher, teacher_detail_href):
    """ 将教师信息添加到 名单.csv 中 """
    data = list()
    data.append("北京师范大学")
    data.append(teacher.name)
    data.append(teacher_detail_href)
    fh = open(csv_file, "a+", encoding="utf-8", newline="")
    writer = csv.writer(fh)
    writer.writerow(data)
    fh.close()


def save_teacher_json(teacher):
    """ 保存教师信息 JSON """
    teacher_json = teacher.__dict__
    fh = open(json_path + "/" + teacher.name + ".json", "w", encoding="utf-8")
    fh.write(json.dumps(teacher_json, indent=2, ensure_ascii=False))
    fh.close()


def save_teacher_html(teacher, teacher_detail_soup):
    """ 保存教师 HTML """
    clean_soup = remove_attrs(teacher_detail_soup)
    fh = open(html_path + "/" + teacher.name + ".html", "w", encoding="utf-8")
    fh.write(clean_soup.prettify())
    fh.close()


def handle_href(base_href, href):
    """ 处理链接 """
    if href.startswith("../"):
        start = href.find("/")
        href = href[start + 1:]
    return base_href + "/" + href

    # for teacher_info in teacher_list_info:
    #     teacher_info = "".join(str(teacher_info.text).split())
    #     match_info = re.match(r'教育与研究经历(.*)', str(teacher_info))
    #     if match_info:
    #         teacher.education_history = match_info.group(1)
    #         continue
    #     match_info = re.match(r"承担项目与课题(.*)", str(teacher_info))
    #     if match_info:
    #         teacher.projects = match_info.group(1)
    #         continue
    #     match_info = re.match(r"个人简介(.*)", str(teacher_info))
    #     if match_info:
    #         teacher.personal_introduction = match_info.group(1)
    #         continue
    #     match_info = re.match(r"学术兼职(.*)", str(teacher_info))
    #     if match_info:
    #         teacher.academical_position = match_info.group(1)
    #     match_info = re.match(r"研究领域与兴趣(.*)", str(teacher_info))
    #     if match_info:
    #         teacher.research_areas = match_info.group(1)
    # 将教师信息追加到 名单.csv 中
    # append_csv_file(teacher, teacher_href)

    # 保存教师 HTML
    # save_teacher_html(teacher, teacher_detail_soup)

    # 保存教师信息 JSON
    # save_teacher_json(teacher)


def crawl_teacher_detail(teacher_href):
    teacher = Teacher()
    teacher.organization = "北京航空航天大学"
    teacher.department = "材料科学与工程学院"

    teacher_detail_response = urllib.request.urlopen(teacher_href)
    teacher_detail_html = teacher_detail_response.read()
    teacher_detail_html = teacher_detail_html.decode("utf-8", "ignore")
    teacher_detail_soup = BeautifulSoup(teacher_detail_html, "html.parser")

    # 获取教师姓名
    name_h2 = teacher_detail_soup.select_one("div.rwjstopleft.auto > h2")
    if name_h2:
        teacher.name = str(name_h2.text).replace(" ", "")
    else:
        return

    # 获取教师个人信息
    p_tag = teacher_detail_soup.select_one("div.rwjstopleft.auto > p")
    list_info_fragment = str(p_tag.prettify()).split("<br/>")
    for info_fragment in list_info_fragment:
        info_fragment = info_fragment.replace(" ", "").replace("<p>", ""). \
            replace("<b>", "").replace("</b>", "").replace("\n", "").replace("</p>", "")
        match_info = re.match(r'职称职务：(.*)', info_fragment)
        if match_info:
            teacher.title = match_info.group(1)
            continue
        match_info = re.match(r'所在单位：(.*)', info_fragment)
        if match_info:
            teacher.major = match_info.group(1)
            continue
        match_info = re.match(r'联系电话：(.*)', info_fragment)
        if match_info:
            teacher.contact = match_info.group(1)
            continue
        match_info = re.match(r'电子邮箱：(.*)', info_fragment)
        if match_info:
            teacher.email = match_info.group(1)
            continue
        match_info = re.match(r'办公地点：(.*)', info_fragment)
        if match_info:
            teacher.address = match_info.group(1)

    # 获取教师其他介绍信息
    # 基本情况
    personal_introduction = teacher_detail_soup.select_one("table:nth-of-type(1) p")
    if personal_introduction:
        teacher.personal_introduction = personal_introduction.text
    # 主讲课程
    courses = teacher_detail_soup.select_one("table:nth-of-type(2) p")
    if courses:
        teacher.courses = courses.text
    # 研究方向
    research_areas = teacher_detail_soup.select_one("table:nth-of-type(3) p")
    if research_areas:
        teacher.research_areas = research_areas.text
    # 研究成果
    achievements = teacher_detail_soup.select_one("table:nth-of-type(4) p")
    if achievements:
        teacher.achievements = achievements.text

    # 将教师信息追加到 名单.csv 中
    append_csv_file(teacher, teacher_href)

    # 保存教师 HTML
    save_teacher_html(teacher, teacher_detail_soup)

    # 保存教师信息 JSON
    save_teacher_json(teacher)


# 获取所有教师详情链接
teacher_list_response = urllib.request.urlopen(url)
teacher_list_html = teacher_list_response.read()
teacher_list_html = teacher_list_html.decode("utf-8", "ignore")
teacher_list_soup = BeautifulSoup(teacher_list_html, "html.parser")
teacher_list_detail_a = teacher_list_soup.select("td > a")

# 创建 html、json 目录，名单.csv 文件
if not os.path.exists(html_path):
    os.makedirs(html_path)
if not os.path.exists(json_path):
    os.makedirs(json_path)

if not os.path.exists(csv_file):
    open(csv_file, "wb").close()

print("北京航空航天大学信息爬取开始...")
crawl_count = 0
crawl_total = len(teacher_list_detail_a)
# 解析教师详情页面
for teacher_detail_a in teacher_list_detail_a:
    detail_href = handle_href("http://www.mse.buaa.edu.cn/", teacher_detail_a["href"])
    crawl_teacher_detail(detail_href)
    crawl_count = crawl_count + 1
    print("当前爬取进度：" + str(crawl_count) + "/" + str(crawl_total) + "\t" + detail_href)
print("北京航空航天大学信息爬取完毕!!!")
