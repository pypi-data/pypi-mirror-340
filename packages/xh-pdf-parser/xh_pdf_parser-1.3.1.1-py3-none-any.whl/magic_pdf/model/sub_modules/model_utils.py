import time
import torch
from loguru import logger
import numpy as np
from magic_pdf.libs.clean_memory import clean_memory


def crop_img(input_res, input_np_img, crop_paste_x=0, crop_paste_y=0):

    crop_xmin, crop_ymin = int(input_res['poly'][0]), int(input_res['poly'][1])
    crop_xmax, crop_ymax = int(input_res['poly'][4]), int(input_res['poly'][5])

    # Calculate new dimensions
    crop_new_width = crop_xmax - crop_xmin + crop_paste_x * 2
    crop_new_height = crop_ymax - crop_ymin + crop_paste_y * 2

    # Create a white background array
    return_image = np.ones((crop_new_height, crop_new_width, 3), dtype=np.uint8) * 255

    # Crop the original image using numpy slicing
    cropped_img = input_np_img[crop_ymin:crop_ymax, crop_xmin:crop_xmax]

    # Paste the cropped image onto the white background
    return_image[crop_paste_y:crop_paste_y + (crop_ymax - crop_ymin),
    crop_paste_x:crop_paste_x + (crop_xmax - crop_xmin)] = cropped_img

    return_list = [crop_paste_x, crop_paste_y, crop_xmin, crop_ymin, crop_xmax, crop_ymax, crop_new_width,
                   crop_new_height]
    return return_image, return_list


# Select regions for OCR / formula regions / table regions
def get_res_list_from_layout_res(layout_res):
    ocr_res_list = []
    table_res_list = []
    single_page_mfdetrec_res = []
    for res in layout_res:
        if int(res['category_id']) in [13, 14]:
            single_page_mfdetrec_res.append({
                "bbox": [int(res['poly'][0]), int(res['poly'][1]),
                         int(res['poly'][4]), int(res['poly'][5])],
            })
        elif int(res['category_id']) in [0, 1, 2, 4, 6, 7]:
            ocr_res_list.append(res)
        elif int(res['category_id']) in [5]:
            table_res_list.append(res)
    return ocr_res_list, table_res_list, single_page_mfdetrec_res


def clean_vram(device, vram_threshold=8):
    total_memory = get_vram(device)
    if total_memory and total_memory <= vram_threshold:
        gc_start = time.time()
        clean_memory(device)
        gc_time = round(time.time() - gc_start, 2)
        logger.info(f"gc time: {gc_time}")


def get_vram(device):
    if torch.cuda.is_available() and str(device).startswith("cuda"):
        total_memory = torch.cuda.get_device_properties(device).total_memory / (1024 ** 3)  # 将字节转换为 GB
        return total_memory
    elif str(device).startswith("npu"):
        import torch_npu
        if torch_npu.npu.is_available():
            total_memory = torch_npu.npu.get_device_properties(device).total_memory / (1024 ** 3)  # 转为 GB
            return total_memory
    else:
        return None