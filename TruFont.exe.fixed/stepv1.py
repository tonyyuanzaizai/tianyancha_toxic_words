from fontTools.ttLib import TTFont
import csv
import os
import PIL.Image, PIL.ImageFont, PIL.ImageDraw


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
    write_to_csv('step1', rowdata)

font1 = TTFont('./tyc-num.woff')
cmap=font1['cmap']
cdict=cmap.getBestCmap()
print(cdict)
cdictkeys = cdict.keys() # 混淆前的unicode (十进制的utf-8编码)
print(len(cdictkeys))

# dict 说明 &#UNICODEVAL;
# 混淆前的unicode UNICODEVAL(十进制的utf-8编码) 和 对应的 用户编辑的key
for UNICODEVAL in cdictkeys:
    v = cdict[UNICODEVAL]
    if v == 'x':
        print('')
    else:
        UNICODEVALStr = '&#' + str(UNICODEVAL) + ';'   # UNICODEVAL(十进制的utf-8编码)
        rowdata = [v, UNICODEVALStr]
        write_to_csv('step2', rowdata)
#修正step2.csv 的中文
