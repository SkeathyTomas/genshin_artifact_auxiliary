# 刻晴办公桌

## 简介

帮你在游戏中整理圣遗物背包时更便捷地了解、查阅圣遗物的评分。[demo视频](https://www.bilibili.com/video/BV1XB4y1k7au/)

![使用截图](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220801125435.png)

## 环境与准备

1. Python 3 (开发环境Python 3.10.5)。
2. OCR引擎[tesserect](https://github.com/tesseract-ocr/tesseract)，安装过程详见原项目。如果你使用`scoop`，可以使用`scoop install tesseract`快速安装。
3. [tesseract中文简体数据文件](https://github.com/tesseract-ocr/tessdata/blob/main/chi_sim.traineddata)，下载完成后保存到tesseLract数据目录（如果是`scoop`安装的话，放在`./scoop/persist/tesseract/tessdata`文件夹中）。
4. 必备的Python包：
   1. PySide6，GUI框架
   2. pynput，监听窗口外鼠标操作
   3. pywin32，获取设备分辨率、缩放信息，用于兼容不同分辨率
   4. Pillow，截图
   5. pytesseract，tesseract的python接口

## 使用教程

1. 使用管理员模式打开命令行工具（必须，否则程序运行中无法监听游戏中的鼠标操作），并打开程序目录。
2. 使用命令`python app.py`运行程序。
3. 在主窗口中选择角色（不选的话，默认评估双爆+攻击词条）。
4. 打开游戏，调整窗口大小为非全屏下最大的一档（当前适配了2560*1600分辨率）。（因为全屏状态下评分结果贴图无法置顶。）
5. 打开背包-圣遗物，随意选择圣遗物，点击**右键**进行圣遗物评分，评分结果随后标记在对应圣遗物右下角。（暂未对滚动条进行适配，若下拉滚动条使第一行圣遗物显示不全，贴图结果可能会有偏离。）
6. 选中某个贴图结果，使用快捷键`Z`删除该贴图；使用全局快捷键`Ctrl+Z`删除所有贴图，可进行新一批圣遗物的评估。

## 评分方法

参考[圣遗物评分方法](https://mp.weixin.qq.com/s/EUc-o95gpovHv5ctKaQNFw)。具体每一个角色的有效词条和词条的评分系数可参考[img_process.py](img_process.py)中的配置，如与需求不符可自行修改参数。

## 已知问题

### 分辨率适配

当前仅在自己的机子上做了分辨率适配，所以理论上只有2560*1600分辨率下可以较为正常的运行。不过分辨率适配框架已经搭好，就差热心玩家给一些不同分辨率的截图做坐标定位和测试了。

需要把游戏窗口化为非全屏下最大的一档，打开背包-圣遗物，别去调窗口位置，然后全屏截图私发一下我。

### 能不能在圣遗物装配中使用

本来一开始确实是按照这个开发的，后来发现这个界面识别老是出错。背景飘过的白点和文字重叠基本就识别不出来了，所以基本就放弃了。

有兴趣可以运行`python app_character.py`尝试下效果，当然角色配置还未同步过去。

## 风险和声明

理论上未对任何游戏数据进行非法获取和修改，仅通过截图和OCR技术实现相关分析，且没有使用自动化程序帮助玩家获取游戏内资源，应该不在官方打击范围。

如若官方觉得不妥，我就删库跑路。

## 需求来源

1. [如何做一个圣遗物管理系统：产品调研与分析](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E8%B0%83%E7%A0%94%E4%B8%8E%E5%88%86%E6%9E%90/)
2. [如何做一个圣遗物管理系统：产品需求文档](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E9%9C%80%E6%B1%82%E6%96%87%E6%A1%A3/)