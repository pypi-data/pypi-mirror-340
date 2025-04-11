from pathlib import Path
from setuptools import setup, find_packages
from magic_pdf.libs.version import __version__


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    requires = []

    for line in lines:
        if "http" in line:
            pkg_name_without_url = line.split('@')[0].strip()
            requires.append(pkg_name_without_url)
        else:
            requires.append(line)

    return requires


if __name__ == '__main__':
    with Path(Path(__file__).parent,
              'README.md').open(encoding='utf-8') as file:
        long_description = file.read()
    setup(
        name="xh_pdf_parser",  # 项目名
        version=__version__+".2",  # 自动从tag中获取版本号
        packages=find_packages() + ["magic_pdf.resources"]+["magic_pdf.model.sub_modules.ocr.paddleocr2pytorch.pytorchocr.utils.resources"],  # 包含所有的包
        package_data={
            "magic_pdf.resources": ["**"],  # 包含magic_pdf.resources目录下的所有文件
            "magic_pdf.model.sub_modules.ocr.paddleocr2pytorch.pytorchocr.utils.resources": ["**"],  # pytorchocr.resources目录下的所有文件
        },
        install_requires=[
        'boto3>=1.28.43',
        'Brotli>=1.1.0',
        'click>=8.1.7',
        'fast-langdetect>=0.2.3,<0.3.0',
        'loguru>=0.6.0',
        'numpy>=1.21.6',
        'pydantic>=2.7.2,<2.11',
        'PyMuPDF>=1.24.9,<1.25.0',
        'scikit-learn>=1.0.2',
        'torch>=2.2.2,!=2.5.0,!=2.5.1,<=2.6.0',
        'torchvision',
        'transformers>=4.49.0,!=4.51.0,<5.0.0',
        'pdfminer.six==20231228',
        'tqdm>=4.67.1',
        "matplotlib>=3.10",
        "ultralytics>=8.3.48",  # yolov8,公式检测
        "doclayout_yolo==0.0.2b1",  # doclayout_yolo
        # "dill>=0.3.9,<1",  # doclayout_yolo
        "dill>=0.3.8,<1",  # doclayout_yolo
        "rapid_table>=1.0.5,<2.0.0",  # rapid_table
        "PyYAML>=6.0.2,<7",  # yaml
        "ftfy>=6.3.1,<7", # unimernet_hf
        "openai>=1.70.0,<2",  # openai SDK
        "shapely>=2.0.7,<3",  # imgaug-paddleocr2pytorch
        "pyclipper>=1.3.0,<2",  # paddleocr2pytorch
        "omegaconf>=2.3.0,<3",  # paddleocr2pytorch
    ],  # 项目依赖的第三方库
        extras_require={},
        description="A practical tool for converting PDF to Markdown",  # 简短描述
        long_description=long_description,  # 详细描述
        long_description_content_type="text/markdown",  # 如果README是Markdown格式
        url="https://github.com/opendatalab/MinerU",
        python_requires=">=3.9",  # 项目依赖的 Python 版本
        find_links=[
        "https://www.paddlepaddle.org.cn/packages/stable/cu118/",
    ],
        entry_points={
            "console_scripts": [
                "magic-pdf = magic_pdf.tools.cli:cli",
                "magic-pdf-dev = magic_pdf.tools.cli_dev:cli" 
            ],
        },  # 项目提供的可执行命令
        include_package_data=True,  # 是否包含非代码文件，如数据文件、配置文件等
        zip_safe=False,  # 是否使用 zip 文件格式打包，一般设为 False
    )
