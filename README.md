<div align='center'>

# 刻晴办公桌

[![GitHub downloads](https://img.shields.io/github/downloads/SkeathyTomas/genshin_artifact_auxiliary/total?style=flat-square)](https://github.com/SkeathyTomas/genshin_artifact_auxiliary/releases)[![GitHub release (latest by date)](https://img.shields.io/github/downloads/SkeathyTomas/genshin_artifact_auxiliary/latest/total?style=flat-square)](https://github.com/SkeathyTomas/genshin_artifact_auxiliary/releases/latest)

</div>

## 简介

帮你在游戏中整理圣遗物背包时更便捷地了解、查阅圣遗物的评分，然后把评分最高的圣遗物装配给希望的角色，同时支持背包面板和角色面板。多角色适配，帮你省去了记各角色有效词条、口算/按计算器的时间。

相比于其他评分工具的优势：

1. 与游戏本身有更好的贴合性，可以让玩家对于圣遗物好坏有更加方便直观的判断。
2. 省去了一些截图、角色装配调来调去、游戏内外来回对比的麻烦。

[demo视频](https://www.bilibili.com/video/BV1XB4y1k7au/)

![背包面板圣遗物](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220801125435.png)

![角色面板圣遗物](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220810004718.png)

## 环境与准备

### OCR引擎

1. OCR引擎[tesserect](https://github.com/tesseract-ocr/tesseract)，安装过程详见原项目，或者参考[这篇文章](https://www.jianshu.com/p/f7cb0b3f337a)，安装链接[tesseract-ocr-w64-setup-v5.2.0.20220712.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.2.0.20220712.exe)(64位)。如果你使用`scoop`，可以使用`scoop install tesseract`快速安装。安装完成后，可在命令行输入`tesseract`检验是否安装成功。
2. [tesseract中文简体数据文件](https://github.com/tesseract-ocr/tessdata/blob/main/chi_sim.traineddata)，下载完成后保存到tesseract数据目录`tessdata`中（如果是`scoop`安装的话，放在`./scoop/persist/tesseract/tessdata`文件夹中）。

### 如果你需要直接运行python程序

1. Python 3.6+ (作者开发环境Python 3.10.5)。
2. 必备的Python包：
   1. PySide6，GUI框架
   2. pynput，监听窗口外鼠标操作
   3. pywin32，获取设备分辨率、缩放信息，用于兼容不同分辨率
   4. Pillow，截图
   5. pytesseract，tesseract的python接口

### 使用打包的exe文件

1. 在release中下载最新的压缩包。
   1. 含with-tesseract的打包文件已包含tesseract引擎，无需再自行安装。
   2. 若已手动安装OCR引擎，可下载不含OCR引擎的压缩包。
2. 解压。

## 使用教程

1. 方式1：运行打包好的程序。解压压缩包完成后，找到并用管理员模式运行keqing.exe（必须，否则程序运行中无法监听游戏中的鼠标操作）。

![keqing.exe](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220805144258.png)

2. 方式2：下载源码，使用管理员模式打开命令行工具（必须，否则程序运行中无法监听游戏中的鼠标操作），并打开程序目录，使用命令`python app.py`运行程序。
3. 在主窗口中选择角色（不选的话，默认评估双爆+攻击词条）。
4. 打开游戏，调整窗口大小为非全屏下最大的一档。（因为全屏状态下评分结果贴图无法置顶。）
5. 打开背包-圣遗物，随意选择圣遗物，点击**右键**进行圣遗物评分，评分结果随后标记在对应圣遗物右下角。（暂未对滚动条进行适配，若下拉滚动条使第一行圣遗物显示不全，贴图结果可能会有偏离。）
6. 选中某个贴图结果，使用快捷键`Ctrl+Z`删除该贴图；使用全局快捷键`Ctrl+Shift+Z`删除所有贴图，可进行新一批圣遗物的评估。

## 评分方法

~~参考[圣遗物评分方法](https://mp.weixin.qq.com/s/EUc-o95gpovHv5ctKaQNFw)。~~
更新了[圣遗物评分方法](https://mp.weixin.qq.com/s/DxyS8Rll3_eLSelvjiwKwQ)，调整了角色的有效词条，增加了每个角色相对于固定词条的二级系数（如同样是大攻击对于一般主C和胡桃的评分系数就有所不同），删除了不同打法流派的角色。

具体每一个角色的有效词条和词条的评分系数可参考[img_process.py](img_process.py)中的配置，如与需求不符可自行前往源文件修改参数。

## 已知问题

### 分辨率适配

已适配在16：10，16：9分辨率。分辨率适配框架已经搭好，若有分辨率适配问题，可提供一些不同分辨率的截图做坐标定位和测试了。需要把游戏窗口化为非全屏下最大的一档，打开背包-圣遗物，别去调窗口位置，然后全屏截图私发一下我。

如使用多屏设备（如笔记本外接显示器），请把游戏窗口置于第一屏。

目前已适配分辨率：

16:10

- [x] 2560 * 1600

16:9

- [x] 2560 * 1440
- [x] 1920 * 1080等

### 能不能在角色面板使用

本来一开始确实是按照这个开发的，后来发现这个界面识别老是出错，背景飘过的白点和文字重叠基本就会识别出错（感觉这个解决起来还是有点难度的，就算人眼去识别遮挡的文字可能也会出错，可能需要上下文，牵扯到数字可能就更没办法了）。

已在主程序中适配了角色面板的圣遗物选择，可通过在主窗口中手动切换至「角色」选项进行使用（默认选的是「背包」）。在手动校验功能出来前此功能都不会特别好用，可能需要多次重新识别。

~~有兴趣可以运行`python test/app_character.py`尝试下效果，~~

### 关于GUI

使用了默认的组件，某些高级整合/自改组件Bug一堆，问就是还在学，不过就问你能不能用吧。UI美化、Bug修复等1.0版本再考虑。

### 语言支持

- [x] 中文简体

## 风险和声明

本程序不收集任何用户信息，所有数据保留在本地。

理论上未对任何游戏数据进行非法获取和修改，仅通过截图和OCR技术实现相关分析，且没有使用自动化程序帮助玩家获取游戏内资源，应该不在官方打击范围。

如若官方觉得不妥，我就删库跑路。

## 问题反馈

提Issue，最好提供下命令行的输出（如识别错误、环境错误等）。有人的话可以考虑建个交流群什么的。

## 需求来源

1. [如何做一个圣遗物管理系统：产品调研与分析](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E8%B0%83%E7%A0%94%E4%B8%8E%E5%88%86%E6%9E%90/)
2. [如何做一个圣遗物管理系统：产品需求文档](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E9%9C%80%E6%B1%82%E6%96%87%E6%A1%A3/)