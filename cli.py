import os
from PIL import Image
from confusion import confuse, deconfuse
from config import *


is_nt = os.name == 'nt'

while True:
    os.system('cls' if is_nt else 'clear')

    print('欢迎使用图片混淆工具！')
    print('1. 混淆图片')
    print('2. 解混淆图片')
    print('3. 退出')

    choice = input('请输入选项：').strip()
    while choice not in ['1', '2', '3']:
        choice = input('\r请输入正确的选项：').strip()

    if choice == '3':
        exit()

    img_path = input('请输入图片路径或拖动文件到 shell：').strip()
    while not os.path.isfile(img_path):
        img_path = input('\r请输入正确的图片路径或拖动文件到 shell：').strip()

    img = Image.open(img_path)

    seed = input('请输入随机种子：').strip()

    if choice == '1':
        output = confuse(img, (BLOCK_SIZE, BLOCK_SIZE), GRID_WIDTH, RULER_SIZE, seed)
    else:
        output = deconfuse(img, seed)

    output.save('output.png')
    print('图片已保存为 output.png')

    input('按回车键继续...')

