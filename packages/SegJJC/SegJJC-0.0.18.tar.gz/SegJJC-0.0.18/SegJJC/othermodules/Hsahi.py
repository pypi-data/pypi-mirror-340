import os
import yaml
from PIL import Image
import numpy as np

class HSAHI_det:
    def __init__(self, yaml_path=None,slice_height=256, slice_width=256, overlap_height_ratio=0.25, overlap_width_ratio=0.25,sahi_datadir=None,roi=None):
        self.slice_height_ = slice_height
        self.slice_width_ = slice_width
        self.overlap_height_ratio_ = overlap_height_ratio
        self.overlap_width_ratio_ = overlap_width_ratio
        self.yaml_path=yaml_path
        self.output_yaml_path=None
        self.slice_regions = []
        self.Data_sahi_dir=sahi_datadir
        self.roi=[roi[0],roi[1],roi[2]-roi[0],roi[3]-roi[1]] if roi else roi
    def calculate_slice_regions(self, image_height, image_width,roi=None):
        #是否有roi，有的话使用
        if roi:
            image_width=roi[2]
            image_height=roi[3]
        # 是否有roi，有的话使用
        self.slice_regions = []
        step_height = self.slice_height_ - int(self.slice_height_ * self.overlap_height_ratio_)
        step_width = self.slice_width_ - int(self.slice_width_ * self.overlap_width_ratio_)
        index = 0

        # 如果图像的高度或宽度小于切图尺寸，调整切图尺寸
        if image_height < self.slice_height_:
            self.slice_height_ = image_height
        if image_width < self.slice_width_:
            self.slice_width_ = image_width

        # 使用一个集合来跟踪已添加的切片区域
        seen_regions = set()

        for y in range(0, image_height, step_height):
            for x in range(0, image_width, step_width):
                width = self.slice_width_
                height = self.slice_height_

                temp_x = x
                temp_y = y

                if x + width > image_width:
                    temp_x -= (x + width) - image_width
                if y + height > image_height:
                    temp_y -= (y + height) - image_height

                # 创建当前切片区域
                # 是否有roi，有的话使用
                if roi:
                    region = (temp_x+roi[0], temp_y+roi[1], width, height)
                else:
                    region = (temp_x, temp_y, width, height)
                # 使用元组作为唯一标识符，添加到集合中
                if region not in seen_regions:
                    seen_regions.add(region)
                    self.slice_regions.append((region, index))
                    index += 1
###获取切图区域内的标注框####
    def bbox_in_slice(self, bbox, slice_region):
        slice_x, slice_y, slice_w, slice_h = slice_region
        bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox

        new_bbox_x1 = max(bbox_x1 - slice_x, 0)
        new_bbox_y1 = max(bbox_y1 - slice_y, 0)
        new_bbox_x2 = min(bbox_x2 - slice_x, slice_w)
        new_bbox_y2 = min(bbox_y2 - slice_y, slice_h)

        if new_bbox_x1 < new_bbox_x2 and new_bbox_y1 < new_bbox_y2:
            return new_bbox_x1, new_bbox_y1, new_bbox_x2, new_bbox_y2
        else:
            return None

    def convert_to_original(self, size, box):
        width, height = size
        x = box[0] * width
        y = box[1] * height
        w = box[2] * width
        h = box[3] * height

        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2

        return x1, y1, x2, y2
    def process_imgs(self, image_paths, output_dir):
        output_folder = os.path.join(output_dir, 'images')
        txt_outdir=os.path.join(output_dir,'labels')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(txt_outdir):
            os.makedirs(txt_outdir)
        new_image_paths = []  # 用于存储新的图片路径

        for image_path in image_paths:
            ##获取图片格式
            imgtype = os.path.basename(image_path).split('.')[-1]
            txt_path = image_path.replace(f".{imgtype}", ".txt").replace("images", "labels")
            with open(txt_path, "r") as f:
                annotations = f.readlines()

            with Image.open(image_path) as img:
                img.load()
                width, height = img.size
                self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)

                for slice_region, index in self.slice_regions:
                    slice_x, slice_y, slice_w, slice_h = slice_region
                    slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))

                    slice_img_filename = os.path.join(output_folder, f"{os.path.basename(image_path).replace(f'.{imgtype}', '')}_slice_{index}.{imgtype}")
                    slice_img.save(slice_img_filename)

                    slice_txt_filename = os.path.join(txt_outdir, f"{os.path.basename(image_path).replace(f'.{imgtype}', '')}_slice_{index}.txt")
                    with open(slice_txt_filename, "w") as slice_f:
                        has_bbox = False
                        for annotation in annotations:
                            elements = annotation.strip().split()
                            bbox_id = int(elements[0])
                            normalized_bbox = list(map(float, elements[1:]))

                            bbox = self.convert_to_original((width, height), normalized_bbox)

                            new_bbox = self.bbox_in_slice(bbox, slice_region)
                            ###归一化标注框
                            if new_bbox:
                                has_bbox = True
                                x_center = (new_bbox[0] + new_bbox[2]) / 2 / slice_w
                                y_center = (new_bbox[1] + new_bbox[3]) / 2 / slice_h
                                bbox_w = (new_bbox[2] - new_bbox[0]) / slice_w
                                bbox_h = (new_bbox[3] - new_bbox[1]) / slice_h

                                slice_f.write(f"{bbox_id} {x_center} {y_center} {bbox_w} {bbox_h}\n")

                        if not has_bbox:
                            slice_f.write("")

                    new_image_paths.append(slice_img_filename)  # 添加新的图片路径

        return new_image_paths
    def update_yaml(self, train_paths, val_paths,test_paths):
        with open(self.yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        train_paths = train_paths.replace("\\", "/")
        val_paths = val_paths.replace("\\", "/")
        test_paths = test_paths.replace("\\", "/")
        data['train'] = train_paths
        data['val'] = val_paths
        data['test'] = test_paths
        with open(self.output_yaml_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

    def save_image_paths(self, image_paths, output_txt_path):
        with open(output_txt_path, 'w') as f:
            for path in image_paths:
                f.write(f"{path}\n")
    def read_yaml(self):
        with open(self.yaml_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        train_txt_path = config['train']
        val_txt_path = config['val']
        test_txt_path=train_txt_path.replace("train.txt",'test.txt')
        # 3. 读取 train 和 val 的文件路径
        train_image_paths = [line.strip() for line in open(train_txt_path, 'r')]
        val_image_paths = [line.strip() for line in open(val_txt_path, 'r')]
        # 检查 test.txt 文件是否存在
        if os.path.exists(test_txt_path):
            test_image_paths = [line.strip() for line in open(test_txt_path, 'r')]
        else:
            # 如果 test.txt 文件不存在，则返回空列表
            test_image_paths = []
            print(f"Warning: {test_txt_path} does not exist. Returning empty test image paths.")
        return train_image_paths, val_image_paths, test_image_paths


    def process_data(self):
        # 5. 处理 train 和 val 图片
        train_image_paths, val_image_paths, test_image_paths=self.read_yaml()
        if self.Data_sahi_dir:
            Data_sahi_dir=self.Data_sahi_dir
        else:
        # 获取上层路径
            parent_dir = os.path.dirname(self.yaml_path)
            Data_sahi_dir=os.path.join(parent_dir,'Data_det_sahi')
        if not os.path.exists(Data_sahi_dir):
            os.makedirs(Data_sahi_dir)
        trainval_outdir=os.path.join(Data_sahi_dir,'paper_data')
        if not os.path.exists(trainval_outdir):
            os.makedirs(trainval_outdir)
        new_train_paths = self.process_imgs(train_image_paths,Data_sahi_dir)
        new_val_paths = self.process_imgs(val_image_paths, Data_sahi_dir)
        #
        # ###和train、val一样使用切图切分，然后输出切图后的路径
        # new_test_paths = self.process_imgs(test_image_paths, Data_sahi_dir)
        # ###对test数据集不使用切图，直接给出原来一样的路径
        new_test_paths =test_image_paths
        #
        # 6. 保存新的 train.txt 和 val.txt 文件
        output_train_txt=os.path.join(trainval_outdir,'train.txt')
        output_val_txt=os.path.join(trainval_outdir,'val.txt')
        output_test_txt = os.path.join(trainval_outdir, 'test.txt')
        self.save_image_paths(new_train_paths, output_train_txt)
        self.save_image_paths(new_val_paths, output_val_txt)
        self.save_image_paths(new_test_paths, output_test_txt)
        # 7. 更新 YAML 文件
        self.output_yaml_path=os.path.join(Data_sahi_dir,'mydata.yaml')
        self.update_yaml(output_train_txt, output_val_txt,output_test_txt)

    ##predict_slice_imgs切分文件夹所有图片
    def predict_slice_imgs(self, image_paths):
        sliced_images = []  # 存储切割后的图片数据
        for image_path in os.listdir(image_paths):
            # 获取图片格式
            sliced_image=[]
            image_path = os.path.join(image_paths,image_path)
            with Image.open(image_path) as img:
                width, height = img.size
                self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)

                for slice_region, index in self.slice_regions:
                    slice_x, slice_y, slice_w, slice_h = slice_region
                    slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))

                    # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
                    slice_img_array = np.array(slice_img)
                    sliced_image.append(slice_img_array)
            sliced_images.append(sliced_image)
        # 返回所有切割后的图片列表
        return sliced_images

    ##predict_slice_oneimg切分单个文件图片
    def predict_slice_oneimg(self, image_path_or_image):
        # 根据参数的类型来决定如何处理
        if isinstance(image_path_or_image, str):
            sliced_images = []  # 存储切割后的图片数据
            image_path=image_path_or_image
            with Image.open(image_path) as img:
                width, height = img.size
                self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)

                for slice_region, index in self.slice_regions:
                    slice_x, slice_y, slice_w, slice_h = slice_region
                    slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))

                    # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
                    slice_img_array = np.array(slice_img)
                    sliced_images.append(slice_img_array)
            # 返回所有切割后的图片列表
            return sliced_images
        elif isinstance(image_path_or_image, Image.Image):
            sliced_images = []  # 存储切割后的图片数据
            img = image_path_or_image
            width, height = img.size
            self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)

            for slice_region, index in self.slice_regions:
                slice_x, slice_y, slice_w, slice_h = slice_region
                slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))

                # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
                slice_img_array = np.array(slice_img)
                sliced_images.append(slice_img_array)
            # 返回所有切割后的图片列表
            return sliced_images
        else:
            raise TypeError("image_path_or_image 必须是字符串或 PIL.Image.Image")

# # 1. 初始化 SAHI 类
# slice_height = 256
# slice_width = 256
# overlap_height_ratio = 0.2
# overlap_width_ratio = 0.2
#
# sahi = SAHI(slice_height, slice_width, overlap_height_ratio, overlap_width_ratio)

# 2. 读取 YAML 文件
# yaml_path = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\Data_det\mydata.yaml"
# with open(yaml_path, 'r', encoding='utf-8') as file:
#     config = yaml.safe_load(file)
#
# train_txt_path = config['train']
# val_txt_path = config['val']
#
# # 3. 读取 train 和 val 的文件路径
# train_image_paths = [line.strip() for line in open(train_txt_path, 'r')]
# val_image_paths = [line.strip() for line in open(val_txt_path, 'r')]

# # 4. 指定输出文件夹
# output_image_folder = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\out\imgs"
# output_train_txt = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\out\paper_data\train.txt"
# output_val_txt = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\out\paper_data\val.txt"
# output_yaml_path = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\out\output_config.yaml"

# # 5. 处理 train 和 val 图片
# new_train_paths = sahi.process_txt_files(train_image_paths, os.path.dirname(train_txt_path), output_image_folder)
# new_val_paths = sahi.process_txt_files(val_image_paths, os.path.dirname(val_txt_path), output_image_folder)
#
# # 6. 保存新的 train.txt 和 val.txt 文件
# sahi.save_image_paths(new_train_paths, output_train_txt)
# sahi.save_image_paths(new_val_paths, output_val_txt)
#
# # 7. 更新 YAML 文件
# sahi.update_yaml(yaml_path, output_train_txt, output_val_txt, output_yaml_path)
# yamlpath=r'E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\Data_pest\mydata2\mydata.yaml'
# sahi=SAHI(yamlpath)
# sahi.process_data()
# print("处理完成！")
