import json
import urllib.request
import os
import pymysql
import boto3
from PIL import Image
from urllib.parse import unquote
import sys


bucket_name = 'cashmission-prod'


# Configuration Part Start

# result_path = 'C:/Users/gener/Desktop/PyCharm/플젝/마젠타/2714'
result_path = r"C:/Users/selectstar/Desktop/pm/엠폴시스템/1_2913"
json_file = r'C:/Users/selectstar/Desktop/pm/엠폴시스템/2913/2913_labeling_found_complete_7a4d4821-69f8-4c55-afb8-71b11e1d7656.json'

# Configuration Part End


part_dict = {
    "고글": "Goggles",
    "방독면": "Gas Mask",
    "실험복": "Lab Coat"
}


def get_file_name(url):
    return unquote(url.split('/')[-1])


def download_img(url, file_path):
    urllib.request.urlretrieve(url, file_path)


def download(url):
    file_name = get_file_name(url)
    file_path = result_path + '/' + file_name
    if os.path.isfile(file_path):
        print("File Already Downloaded: %s" % file_name)
    else:
        download_img(url, file_path)
        print("Downloading... %s" % file_name)
    return file_path


def labelmeData(labels, categories, image):
    result = {}
    result['version'] = '4.5.6'
    result['flags'] = {}
    shapes = []
    image_height = Image.open(image).height
    image_width = Image.open(image).width
    for label in labels:
        one_dict = {}
        one_dict['label'] = getCategoryName(categories, label['categoryId'])
        one_dict['points'] = [[label['coordinates']['x1'] * image_width, label['coordinates']['y1'] * image_height],
                              [label['coordinates']['x2'] * image_width, label['coordinates']['y2'] * image_height]]
        # one_dict['group_id'] = None
        one_dict['shape_type'] = 'rectangle'
        one_dict['flags'] = {}
        shapes.append(one_dict)

    result['shapes'] = shapes
    result['imagePath'] = image.split('/')[-1]
    result['imageData'] = None
    result['imageHeight'] = image_height
    result['imageWidth'] = image_width
    return result


def getCategoryName(categories, id):
    for category in categories:
        if category['id'] == id:
            try:
                return part_dict[category['name']]
            except KeyError:
                print("14개 부위와 일치하지 않는 카테고리명이 있음: {}".format(category['name']))
                sys.exit(1)

    raise Exception('해당하는 Id가 없습니다')


with open(json_file, 'r', encoding='utf-8') as j:
    all_list = json.load(j)
    for one_dict in all_list:
        file_path = download(one_dict['content'])
        labelme = labelmeData(one_dict['labels'], one_dict['categories'], file_path)
        json_file = file_path.split('/')[-1].split('.')[0] + '.json'
        with open(result_path + '/' + json_file, 'w', encoding='utf-8') as one_json:
            json.dump(labelme, one_json, ensure_ascii=False)