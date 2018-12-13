from fontTools.ttLib import TTFont
import csv
import os
import PIL.Image, PIL.ImageFont, PIL.ImageDraw


# 生成对应的图片
def genImg(textustr, wordidx):
    image=PIL.Image
    ImageDraw=PIL.ImageDraw
    ImageFont=PIL.ImageFont

    #textustr = u"念"   # 混淆前的文字, 上面一排是 真正的 下面是正确的文字 念-->按, 9-->0

    im = image.new("RGB", (100, 100), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "E:/lee/TruFont.exe.fixed/tyc-num.woff"), 50) # font path 只能使用绝对路径
    dr.text((20, 20), textustr, font=font, fill="#000000")
    #im.show()
    im.save("E:/lee/TruFont.exe.fixed/pic/tyc-" + str(wordidx) + ".png")  # 真正的文字 的 图片

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
for wordidx, gly in enumerate(gly_list):
    # 把 gly 改成网页中的格式
    #gly = gly.replace('uni', '&#x').lower() + ';'
    # 如果 gly 在字符串中，用对应数字替换
    print(wordidx, gly)                      # 打印
    rowdata = [wordidx, gly]
    step1dict[gly] = wordidx
    #write_to_csv('step1', rowdata)
step2dict = {}
csv_reader = csv.reader(open("step2.csv"))
for row in csv_reader:
    print(row)
    row[0]
    row[2]
    step2dict[row[0]] = row[2]
    wordidx = step1dict[row[0]]
    genImg(row[2], wordidx)
