from re import split
from rasterio.warp import transform_bounds
from rayspatial.serve.common import constants
def _calcate_paralle_num(bbox,scale):
    bbox_3857 = transform_bounds(
            constants.EPSG_4326,
            constants.EPSG_3857,
            *bbox,
        )
    width = (bbox_3857[2] - bbox_3857[0])/scale
    height = (bbox_3857[3] - bbox_3857[1])/scale
    area = width * height
    limit_area = 512 * 512
    area_num = area / limit_area
    sqrt_area_num = area_num ** 0.5
    return int(sqrt_area_num+1) if int(sqrt_area_num) > 1 else 1

def _split_bbox(bbox, scale, paralle_num):
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]
    sub_width = bbox_width / paralle_num
    sub_height = bbox_height / paralle_num
    sub_bboxes = []
    for i in range(paralle_num):
        for j in range(paralle_num):
            x_min = bbox[0] + i * sub_width
            y_min = bbox[1] + j * sub_height
            x_max = bbox[0] + (i + 1) * sub_width
            y_max = bbox[1] + (j + 1) * sub_height
            if i == paralle_num - 1:
                x_max = bbox[2]
            if j == paralle_num - 1:
                y_max = bbox[3]
            sub_bboxes.append([x_min, y_min, x_max, y_max])
    
    # 确保至少返回一个bbox
    if not sub_bboxes:
        sub_bboxes.append(bbox)
        
    return sub_bboxes