import pdfplumber

pdf = pdfplumber.open('./test.pdf')
print(type(pdf.pages))
print('------------------------------')
p2 = pdf.pages[1]  # 获取第二页

# 获取图片信息
img_info = p2.images[0]
print("图片信息:", img_info)

# 获取页面边界（防止裁剪超出范围）
page_bbox = p2.bbox
#
# # 安全裁剪：将坐标限制在页面范围内
# x0 = max(img_info['x0'], page_bbox[0])
# top = max(img_info['top'], page_bbox[1])
# x1 = min(img_info['x1'], page_bbox[2])
# bottom = min(img_info['bottom'], page_bbox[3])

# 提取并保存图片
img = p2.images[0]
p2.crop((max(img_info['x0'], page_bbox[0]), max(img_info['top'], page_bbox[1]), min(img_info['x1'], page_bbox[2]), min(img_info['bottom'], page_bbox[3]))).to_image(antialias=True, resolution=1080).save('./test_image.png')


print("图片已保存为: test_image.png")
