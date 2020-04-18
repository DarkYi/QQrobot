import requests
import re
from lxml import etree
from itertools import chain


def weather(area):
    # 天气预报函数
    # 获取温度情况
    # 天气数据获取地址 http://www.weather.com.cn/weather1d/101060201.shtml
    # 爬虫header加入了更多伪装的信息
    # return返回str类型的天气信息
    # author:达克dark
    # email:darkwangdy@protonmail.com
    header = {
        #'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        #'Accept-Language': 'zh-CN,zh;q=0.9',
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    # 字典形式保存了城市和城市对应的code
    # 可以修改此字典来增加或删除城市
    area_dic = {
	'百色市': '101301001',
        '吉林': '101060201',
        '舒兰': '101060202',
        '永吉': '101060203',
        '蛟河': '101060204',
        '磐石': '101060205',
        '桦甸': '101060206',
        '昌邑': '101060207',
        '龙潭': '101060208',
        '船营': '101060209',
        '丰满': '101060210',
        '宁德': '101230301',
        '古田': '101230302',
        '霞浦': '101230303',
        '寿宁': '101230304',
        '周宁': '101230305',
        '福安': '101230306',
        '柘荣': '101230307',
        '福鼎': '101230308',
        '屏南': '101230309',
        '蕉城' : '101230310',
        '常州' : '101191101',
        '溧阳' : '101191102',
        '金坛' : '101191103',
        '武进' : '101191104',
        '天宁' : '101191105',
        '钟楼' : '101191106',
        '新北' : '101191107',
        '厦门' : '101230201',
        '同安' : '101230202',
        '思明' : '101230203',
        '海沧' : '101230204',
        '湖里' : '101230205',
        '集美' : '101230206',
        '西安' : '101110101',
        '长安' : '101110102',
        '临潼' : '101110103',
        '蓝田' : '101110104',
        '周至' : '101110105',
        '高陵' : '101110107',
        '新城' : '101110108',
        '碑林' : '101110109',
        '莲湖' : '101110110',
        '灞桥' : '101110111',
        '未央' : '101110112',
        '雁塔' : '101110113',
        '阎良' : '101110114',
        '鄠邑' : '101110106',
        '翔安' : '101230207',
        '盘锦' : '101071301',
        '大洼' : '101071302',
        '盘山' : '101071303',
        '双台子': '101071304',
        '兴隆台': '101071305',
        '武汉' : '101200101',
        '蔡甸' : '101200102',
        '黄陂' : '101200103',
        '新洲' : '101200104',
        '江夏' : '101200105',
        '东西湖': '101200106',
        '江岸' : '101200107',
        '江汉' : '101200108',
        '硚口' : '101200109',
        '汉阳' : '101200110',
        '武昌' : '101200111',
        '青山' : '101200112',
        '洪山' : '101200113',
        '汉南' : '101200114',
        '南宁': '101300101', 
        '兴宁': '101300102', 
        '邕宁': '101300103', 
        '横县': '101300104', 
        '隆安': '101300105', 
        '马山': '101300106', 
        '上林': '101300107', 
        '武鸣': '101300108', 
        '宾阳': '101300109', 
        '青秀': '101300110', 
        '江南': '101300111', 
        '西乡塘': '101300112', 
        '良庆': '101300113',
        '唐山': '101090501', 
        '丰南': '101090502', 
        '丰润': '101090503', 
        '滦县': '101090504', 
        '滦南': '101090505', 
        '乐亭': '101090506', 
        '迁西': '101090507', 
        '玉田': '101090508', 
        '曹妃甸': '101090509', 
        '遵化': '101090510', 
        '迁安': '101090511', 
        '路南': '101090513', 
        '路北': '101090514', 
        '古冶': '101090515', 
        '开平': '101090516',
        '重庆': '101040100', 
        '永川': '101040200', 
        '合川': '101040300', 
        '南川': '101040400', 
        '江津': '101040500', 
        '渝北': '101040700', 
        '北碚': '101040800', 
        '巴南': '101040900', 
        '长寿': '101041000', 
        '黔江': '101041100', 
        '渝中': '101041200', 
        '万州': '101041300', 
        '涪陵': '101041400', 
        '城口': '101041600', 
        '云阳': '101041700', 
        '巫溪': '101041800', 
        '奉节': '101041900', 
        '巫山': '101042000', 
        '潼南': '101042100', 
        '垫江': '101042200', 
        '梁平': '101042300', 
        '忠县': '101042400', 
        '石柱': '101042500', 
        '大足': '101042600', 
        '荣昌': '101042700', 
        '铜梁': '101042800', 
        '璧山': '101042900', 
        '丰都': '101043000', 
        '武隆': '101043100', 
        '彭水': '101043200', 
        '綦江': '101043300', 
        '酉阳': '101043400', 
        '大渡口': '101043500', 
        '秀山': '101043600', 
        '江北': '101043700', 
        '沙坪坝': '101043800', 
        '九龙坡': '101043900', 
        '南岸': '101044000', 
        '开州': '101044100',
        '常州': '101191101', 
        '溧阳': '101191102', 
        '金坛': '101191103', 
        '武进': '101191104', 
        '天宁': '101191105', 
        '钟楼': '101191106', 
        '新北': '101191107',}
    # 获取天气信息
    try:
        # try保护起来，以免用户输入的城市不在字典内而返回错误的信息
        r = requests.get('http://www.weather.com.cn/weather1d/'+area_dic[area]+'.shtml', headers=header)
    except:
        # 发生错误返回str
        return '目前不支持该城市'
    weather_html = r.content.decode('utf8')  # bytes类型解码
    weath_lxml = etree.HTML(weather_html)  # 转换lxml格式
    # 提取温度的信息 tem=list
    weather_list = []
    for var in range(1,3):
        weather_path = "//ul[@class='clearfix']/li["+str(var)+"]/"
        weather_date = weath_lxml.xpath(weather_path+"h1/text()")
        weather_wea = weath_lxml.xpath(weather_path+"p[@class='wea']/text()")
        weather_tem = weath_lxml.xpath(weather_path+"p[@class='tem']/span/text()")
        wind = weath_lxml.xpath(weather_path+"p[@class='win']/span/@title")
        wind_power = weath_lxml.xpath(weather_path+"p[@class='win']/span/text()")
        weather_list.append(weather_date[0]+weather_wea[0]+weather_tem[0]+'°c'+wind[0]+wind_power[0]+'\n')
    weather_mess = weather_list[0]+weather_list[1]
    #print(weather_mess)
    return(weather_mess)

def drame(dname):
    header = {
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            #'Accept-Language': 'zh-CN,zh;q=0.9',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    drame_dic = {
        '邪恶力量 第十五季': '2360'
    }
    if dname in drame_dic:
        url = "https://91mjw.com/video/"+drame_dic[dname]+".htm"
        html = requests.get(url, headers=header)
        html = html.content.decode("utf8")
        html = etree.HTML(html)
        drame_episodes = html.xpath("//div[@class='video_list_li']//a[last()]/text()")
        new_drame_episoder = '您追的'+dname+'已更新到'+str(drame_episodes)+'\n'+'观看地址：'+str(url)
        return new_drame_episoder
    else:
        return "你没有订阅该剧"

def virusNcp(a):

    # 追踪国内外新冠肺炎实时数据
    # 数据来源网址 https://voice.baidu.com/act/newpneumonia/newpneumonia
    # 数据来源百度 “新型冠状病毒肺炎 疫情实时大数据报告”
    
    # ----------------------------------
    # 特殊的注释：
    # 感谢钟南山医生和战斗在一线的医护人员
    # 2020年4月4日举行全国性哀悼活动
    # 悼念牺牲的医护人员和遇难的同胞
    # 永远怀念李文亮医生
    # ----------------------------------

    header = {
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            #'Accept-Language': 'zh-CN,zh;q=0.9',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    html = requests.get("https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0", headers=header)
    html = html.content.decode("utf8")
    num = re.search(r'"countRemark":"","currentConfirmedCount":(\d*),"confirmedCount":(\d*),"suspectedCount":(\d*),"curedCount":(\d*),"deadCount":(\d*),"seriousCount":(\d*),"suspectedIncr":(\d*),"currentConfirmedIncr":([-, \d]*),"confirmedIncr":(\d*),"curedIncr":(\d*),"deadIncr":(\d*),"seriousIncr":(\d*)', html)
    now_diagnosis = str(num.group(1)) # 现存确诊
    #diagnosis_yesterday = str(num.group(8)) # 对比昨天现存确诊数据
    cumulative_diagnosis = str(num.group(2))  # 累计确诊
    #cumulative_yesterday = str(num.group(9))  # 累计确诊对比昨天数据
    returnees = str(num.group(3))  # 境外输入
    #returnees_yesterday = str(num.group(7))  # 境外输入对比昨天数据
    cure_count = str(num.group(4))  # 治愈人数
    #cure_yesterday = str(num.group(10))  # 对比昨天治愈人数
    death_count = str(num.group(5))  # 死亡人数
    #death_yesterday = str(num.group(11))
    asymptomatic = str(num.group(6))  # 无症状患者
    #asymptomatic_yesterday = str(num.group(12))  # 无症状患者对比昨天输数据
    epidemic_mess = '变化的不是数字，而是生命'+ \
        '\n现存确诊人数：'+now_diagnosis+ \
            '\n累计确诊人数：'+cumulative_diagnosis+ \
                '\n境外输入人数：'+returnees+ \
                    '\n治愈人数：'+cure_count+ \
                        '\n死亡人数：'+death_count+ \
                            '\n无症状患者'+asymptomatic+\
                                '\n数据来源丁香园 丁香医生疫情疫情实时动态'+ \
                                    '\nhttps://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
    return epidemic_mess
    
def movies(a):
    html = requests.get('https://www.ygdy8.net/html/gndy/dyzz/index.html')
    html.encoding = "GBK"
    html = html.text
    html = etree.HTML(html)
    new_movies_list = []
    # 提取每个电影名
    new_movies = html.xpath("//div[@class='co_content8']/ul//a/text()")
    # 提取每个电影地址
    movies_url = html.xpath("//div[@class='co_content8']/ul//a/@href")
    for var in movies_url:
        # 把每个url加上“https://www.ygdy8.net”
        url = "https://www.ygdy8.net"+str(var)
        new_movies_list.append(url)
    # 交错合并电影名和电影地址
    movies_list = list(chain.from_iterable(zip(new_movies, new_movies_list)))
    movies_list = "\n".join(movies_list)
    print(type(movies_list))
    return movies_list

      

if __name__ == "__main__":
    movies(1)