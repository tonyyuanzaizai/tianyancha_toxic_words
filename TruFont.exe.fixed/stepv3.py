from fontTools.ttLib import TTFont
import csv
import os
import PIL.Image, PIL.ImageFont, PIL.ImageDraw
from aip import AipOcr
import time
#下面3个变量请自行更改
APP_ID = '15144487'
API_KEY = ''
SECRET_KEY = ' '
aipOcr  = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
aipocr_options = {
  'detect_direction': 'true',
  'language_type': 'CHN_ENG',
}

def getResultWord(wordidx):
    filePath = "E:/lee/TruFont.exe.fixed/pic/tyc-" + str(wordidx) + ".png"
    # 调用通用文字识别接口
    result = aipOcr.basicAccurate(get_file_content(filePath), aipocr_options)
    print(result)
    # 免费一天只能调用500次
    #{'error_code': 17, 'error_msg': 'Open api daily request limit reached'}
    word = ''
    try:
        result = result['words_result']
        if len(result) == 1:
            word = result[0]['words']
        else:
            #识别失败
            print('ocr failed wordidx:',wordidx)
    except:

    print(word)
    return word
#getResultWord(70)

# 生成对应的图片
def genImg(textustr, number):
    image=PIL.Image
    ImageDraw=PIL.ImageDraw
    ImageFont=PIL.ImageFont

    #textustr = u"念"   # 混淆前的文字, 上面一排是 真正的 下面是正确的文字 念-->按, 9-->0

    im = image.new("RGB", (300, 50), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "E:/lee/TruFont.exe.fixed/tyc-num.woff"), 14) # font path 只能使用绝对路径
    dr.text((10, 5), textustr, font=font, fill="#000000")
    #im.show()
    im.save("E:/lee/TruFont.exe.fixed/tyc-" + str(number) + ".png")  # 真正的文字 的 图片

def write_to_csv(csvfilename, rowdata):
    out = open(csvfilename + '.csv', 'a', newline='', encoding="UTF-8")
    # 设定写入模式
    csv_write = csv.writer(out, dialect='excel')
    # 写入具体内容
    csv_write.writerow(rowdata)
    out.close()


font = TTFont('./tyc-num.woff')     # 打开文件
gly_list = font.getGlyphOrder()     # 获取 GlyphOrder 字段的值
gly_list = gly_list[2:]             # 前两个值不是我们要的，切片去掉

step1dict = {}
# 枚举, number是下标，gly是乱码
for number, gly in enumerate(gly_list):
    # 把 gly 改成网页中的格式
    #gly = gly.replace('uni', '&#x').lower() + ';'
    # 如果 gly 在字符串中，用对应数字替换
    #if gly in data:
    #    data = data.replace(gly, str(number))
    print(number, gly)                      # 打印
    rowdata = [number, gly]
    step1dict[gly] = number
    #write_to_csv('step1', rowdata)
step2dict = {}
csv_reader = csv.reader(open("step2.csv"))
for row in csv_reader:
    print(row)
    word_key = row[0]
    word_a = row[2]
    step2dict[row[0]] = row[2]
    wordidx = step1dict[row[0]]
    #genImg(row[2], number)
    time.sleep(1) # 免费接口不能太快了{'error_code': 18, 'error_msg': 'Open api qps request limit reached'}
    word_b = getResultWord(wordidx)
    rowdata = [word_key, wordidx, word_a, word_b]
    write_to_csv('step3', rowdata) # 未识别和识别错误17个一共309个，正确率94.5%
