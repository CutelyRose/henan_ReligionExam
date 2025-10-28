import requests
from loguru import logger
import ddddocr
import base64
import json
import time
import sqlite3
DB_FILE = 'quiz.db'

def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def get_answer(qid: str) -> str:
    with get_conn() as conn:
        cur = conn.execute('SELECT right_answer FROM questions WHERE qid=?', (qid,))
        row = cur.fetchone()
        return row[0] if row else ''
class ReligionExam:
    def __init__(self,school,username,password):
        self.school=school
        self.username=username
        self.password=password
        self.headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://hnjingsai.cn',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://hnjingsai.cn/cbt/login/2025',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }
        self.schools=[{"key":"10001","value":"河南大学"},{"key":"10002","value":"商丘师范学院"},{"key":"10003","value":"周口师范学院"},{"key":"10004","value":"商丘工学院"},{"key":"10005","value":"商丘学院"},{"key":"10006","value":"河南开封科技传媒学院"},{"key":"10007","value":"河南科技职业大学"},{"key":"10008","value":"黄河水利职业技术大学"},{"key":"10009","value":"开封大学"},{"key":"10010","value":"商丘职业技术学院"},{"key":"10011","value":"周口职业技术学院"},{"key":"10012","value":"商丘医学高等专科学校"},{"key":"10013","value":"永城职业学院"},{"key":"10014","value":"开封文化艺术职业学院"},{"key":"10015","value":"兰考三农职业学院"},{"key":"10016","value":"周口文理职业学院"},{"key":"10017","value":"河南对外经济贸易职业学院"},{"key":"10018","value":"商丘幼儿师范高等专科学校"},{"key":"10019","value":"周口理工职业学院"},{"key":"10020","value":"开封职业学院"},{"key":"10021","value":"周口城市职业学院"},{"key":"10022","value":"开封工程职业学院"},{"key":"10023","value":"开封智慧健康职业学院"},{"key":"10024","value":"周口智慧能源职业学院"},{"key":"10025","value":"华北水利水电大学"},{"key":"10026","value":"河南中医药大学"},{"key":"10027","value":"郑州航空工业管理学院"},{"key":"10028","value":"河南牧业经济学院"},{"key":"10029","value":"河南财政金融学院"},{"key":"10030","value":"中原科技学院"},{"key":"10031","value":"河南职业技术学院"},{"key":"10032","value":"河南司法警官职业学院"},{"key":"10033","value":"河南开放大学"},{"key":"10034","value":"河南经贸职业学院"},{"key":"10035","value":"郑州幼儿师范高等专科学校"},{"key":"10036","value":"河南测绘职业学院"},{"key":"10037","value":"河南地矿职业学院"},{"key":"10038","value":"河南农业大学"},{"key":"10039","value":"河南财经政法大学"},{"key":"10040","value":"河南警察学院"},{"key":"10041","value":"郑州工商学院"},{"key":"10042","value":"郑州美术学院"},{"key":"10043","value":"郑州电力高等专科学校"},{"key":"10044","value":"郑州铁路职业技术学院"},{"key":"10045","value":"河南交通职业技术学院"},{"key":"10046","value":"河南农业职业学院"},{"key":"10047","value":"河南艺术职业学院"},{"key":"10048","value":"郑州旅游职业学院"},{"key":"10049","value":"郑州电子信息职业技术学院"},{"key":"10050","value":"郑州电力职业技术学院"},{"key":"10051","value":"郑州警察学院"},{"key":"10052","value":"郑州师范学院"},{"key":"10053","value":"郑州工程技术学院"},{"key":"10054","value":"河南体育学院"},{"key":"10055","value":"郑州财经学院"},{"key":"10056","value":"河南水利与环境职业学院"},{"key":"10057","value":"河南信息统计职业学院"},{"key":"10058","value":"河南轻工职业学院"},{"key":"10059","value":"河南物流职业学院"},{"key":"10060","value":"河南科技大学"},{"key":"10061","value":"洛阳师范学院"},{"key":"10062","value":"洛阳理工学院"},{"key":"10063","value":"河南推拿职业学院"},{"key":"10064","value":"河南林业职业学院"},{"key":"10065","value":"济源职业技术学院"},{"key":"10066","value":"三门峡职业技术学院"},{"key":"10067","value":"洛阳职业技术学院"},{"key":"10068","value":"三门峡社会管理职业学院"},{"key":"10069","value":"洛阳科技职业学院"},{"key":"10070","value":"洛阳文化旅游职业学院"},{"key":"10071","value":"洛阳商业职业学院"},{"key":"10072","value":"河南师范大学"},{"key":"10073","value":"河南理工大学"},{"key":"10074","value":"河南医药大学"},{"key":"10075","value":"河南科技学院"},{"key":"10076","value":"河南工学院"},{"key":"10077","value":"新乡学院"},{"key":"10078","value":"豫北医学院"},{"key":"10079","value":"新乡工程学院"},{"key":"10080","value":"黄河交通学院"},{"key":"10081","value":"河南工业和信息化职业学院"},{"key":"10082","value":"焦作大学"},{"key":"10083","value":"焦作师范高等专科学校"},{"key":"10084","value":"新乡职业技术学院"},{"key":"10085","value":"焦作工贸职业学院"},{"key":"10086","value":"长垣烹饪职业技术学院"},{"key":"10087","value":"河南女子职业学院"},{"key":"10088","value":"焦作新材料职业学院"},{"key":"10089","value":"河南新乡工商职业学院"},{"key":"10090","value":"安阳师范学院"},{"key":"10091","value":"安阳工学院"},{"key":"10092","value":"安阳学院"},{"key":"10093","value":"河南护理职业学院"},{"key":"10094","value":"濮阳职业技术学院"},{"key":"10095","value":"鹤壁职业技术学院"},{"key":"10096","value":"安阳职业技术学院"},{"key":"10097","value":"安阳幼儿师范高等专科学校"},{"key":"10098","value":"濮阳医学高等专科学校"},{"key":"10099","value":"鹤壁汽车工程职业学院"},{"key":"10100","value":"鹤壁能源化工职业学院"},{"key":"10101","value":"林州建筑职业技术学院"},{"key":"10102","value":"濮阳石油化工职业技术学院"},{"key":"10103","value":"濮阳科技职业学院"},{"key":"10104","value":"信阳师范大学"},{"key":"10105","value":"黄淮学院"},{"key":"10106","value":"信阳农林学院"},{"key":"10107","value":"信阳学院"},{"key":"10108","value":"信阳职业技术学院"},{"key":"10109","value":"驻马店职业技术学院"},{"key":"10110","value":"驻马店幼儿师范高等专科学校"},{"key":"10111","value":"信阳涉外职业技术学院"},{"key":"10112","value":"信阳航空职业学院"},{"key":"10113","value":"信阳艺术职业学院"},{"key":"10114","value":"驻马店农业工程职业学院"},{"key":"10115","value":"信阳科技职业学院"},{"key":"10116","value":"信阳工程职业学院"},{"key":"10117","value":"南阳师范学院"},{"key":"10118","value":"南阳理工学院"},{"key":"10119","value":"河南工业职业技术学院"},{"key":"10120","value":"南阳医学高等专科学校"},{"key":"10121","value":"南阳农业职业学院"},{"key":"10122","value":"南阳职业学院"},{"key":"10123","value":"南阳科技职业学院"},{"key":"10124","value":"南阳工艺美术职业学院"},{"key":"10125","value":"郑州大学"},{"key":"10126","value":"河南工业大学"},{"key":"10127","value":"郑州轻工业大学"},{"key":"10128","value":"郑州科技学院"},{"key":"10129","value":"郑州商学院"},{"key":"10130","value":"河南建筑职业技术学院"},{"key":"10131","value":"河南应用技术职业学院"},{"key":"10132","value":"郑州职业技术学院"},{"key":"10133","value":"郑州卫生健康职业学院"},{"key":"10134","value":"嵩山少林武术职业学院"},{"key":"10135","value":"郑州健康学院"},{"key":"10136","value":"郑州城市职业学院"},{"key":"10137","value":"郑州信息工程职业学院"},{"key":"10138","value":"郑州商贸旅游职业学院"},{"key":"10139","value":"郑州黄河护理职业学院"},{"key":"10140","value":"郑州体育职业学院"},{"key":"10141","value":"郑州城建职业学院"},{"key":"10142","value":"郑州医药健康职业学院"},{"key":"10143","value":"郑州汽车工程职业学院"},{"key":"10144","value":"郑州亚欧交通职业学校"},{"key":"10145","value":"中原工学院"},{"key":"10146","value":"河南工程学院"},{"key":"10147","value":"黄河科技学院"},{"key":"10148","value":"郑州工业应用技术学院"},{"key":"10149","value":"郑州升达经贸管理学院"},{"key":"10150","value":"郑州经贸学院"},{"key":"10151","value":"郑州西亚斯学院"},{"key":"10152","value":"河南检察职业学院"},{"key":"10153","value":"河南工业贸易职业学院"},{"key":"10154","value":"河南机电职业学院"},{"key":"10155","value":"河南医学高等专科学校"},{"key":"10156","value":"郑州工业安全职业学院"},{"key":"10157","value":"郑州财税金融职业学院"},{"key":"10158","value":"郑州理工职业学院"},{"key":"10159","value":"郑州电子商务职业学院"},{"key":"10160","value":"郑州轨道工程职业学院"},{"key":"10161","value":"郑州软件职业技术学院"},{"key":"10162","value":"郑州智能科技职业学院"},{"key":"10163","value":"郑州食品工程职业学院"},{"key":"10164","value":"许昌学院"},{"key":"10165","value":"河南城建学院"},{"key":"10166","value":"平顶山学院"},{"key":"10167","value":"许昌职业技术学院"},{"key":"10168","value":"平顶山工业职业技术学院"},{"key":"10169","value":"河南质量工程职业学院"},{"key":"10170","value":"漯河职业技术学院"},{"key":"10171","value":"漯河医学高等专科学校"},{"key":"10172","value":"许昌电气职业学院"},{"key":"10173","value":"平顶山职业技术学院"},{"key":"10174","value":"漯河食品工程职业大学"},{"key":"10175","value":"许昌陶瓷职业学院"},{"key":"10176","value":"平顶山文化艺术职业学院"},{"key":"10177","value":"汝州职业技术学院"},{"key":"10178","value":"平顶山科技职业学院"}]
    
    def convert_png(self,captcha_value):
        image = captcha_value.split(",")[1]  # 只需要captcha_value中“base64”后面的
        img = base64.b64decode(image)  # 将base64转换成图片
        with open('captcha.png', 'wb') as f:  # 打开图片
            f.write(img)  # 保存图片

        ocr = ddddocr.DdddOcr()  # 实例化对象
        code = ocr.classification(img)  # 识别图片上的字符
        return code


    def login(self):

        yzm_res = requests.post('https://hnjingsai.cn/api/onlineExam/getCaptcha', headers=self.headers, json={})
        cid=yzm_res.json()["result"]["cid"]
        code=self.convert_png(yzm_res.json()["result"]["base64"])
        logger.info(f'获取验证码成功:{code}')
        name2key = {d["value"]: d["key"] for d in self.schools}
        id=name2key.get(self.school, None)
        if id is None:
            return False

        json_data = {
            'plan': '2025',
            'num': id+self.username,
            'pwd': self.password,
            'code': code,
            'cid': cid,
        }

        response = requests.post('https://hnjingsai.cn/api/onlineExam/login', headers=self.headers, json=json_data)
        logger.info(response.text)
        # logger.info(f'获取验证码成功:{code}')
        if(response.json()['success']):
            token=response.json()["result"]["jwt"]
            logger.info(f'获取token成功{token}')
            self.headers.update({'Authorization': f'Bearer {token}'})
            return True
        logger.info(f'登陆失败{response.json()["msg"]}')
        return False
    def getLoginUser(self):
        response = requests.post('https://hnjingsai.cn/api/onlineExam/getLoginUser', headers=self.headers, json={})
        logger.info(response.text)
    def exam(self):
        response = requests.post('https://hnjingsai.cn/api/onlineExam/getPaper', headers=self.headers, json={})
        data = json.loads(response.text)
        json_data = {"answers": [], "duration": 300}  # duration 按需改

        for q in data["result"]["questions"]:
            qid = q["id"]
            # ans = q["rightAnswer"].upper()
            ans= get_answer(qid)
            # 如果是多选题，ans 已经是类似 "ABCD" 的字符串，直接可用
            json_data["answers"].append({"id": qid, "answer": ans})
        print(json_data)
        logger.info('延迟300秒')
        time.sleep(300)
        response = requests.post('https://hnjingsai.cn/api/onlineExam/submitPaper', headers=self.headers, json=json_data)
        logger.info(response.text)

    def run(self):
        islogin=self.login()
        if not islogin:
            logger.info('信息错误')
            return None
        self.getLoginUser()
        self.exam()

if __name__ == '__main__':
    religion_exam = ReligionExam('','','')
    religion_exam.run()
