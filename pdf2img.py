import os
import sys
import argparse
import fitz


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_path', type=str, default='input_pdf',
                        help='the path to the folder of the original pdf')
    parser.add_argument('--output_path', type=str, default='output', help='the path to the folder of the splited pdf')

    args = parser.parse_args()
    return args


def main():
    cfg = parse_args()
    input_path = cfg.input_path  # 源文件所在文件夹的绝对路径
    output_path = cfg.output_path
    print(os.path.join(sys.path[0], output_path))
    if not os.path.isdir(os.path.join(sys.path[0], output_path)):
        os.makedirs(output_path)
    if not os.path.isdir(os.path.join(sys.path[0], output_path, "pdf")):
        os.makedirs(os.path.join(output_path, "pdf"))

    docunames = os.listdir(input_path)
    for pdf in docunames:
        doc = fitz.open(os.path.join(input_path, pdf))
        pdf_name = os.path.splitext(pdf)[0]
        for pg in range(doc.pageCount):
            page = doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 2.0
            zoom_y = 2.0
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)
            pm.writePNG(os.path.join(output_path, 'pdf', '{}_{}.png'.format(pdf_name, pg)))


if __name__ == '__main__':
    main()
