<div align='center'>

# 刻晴办公桌

[![GitHub downloads](https://img.shields.io/github/downloads/SkeathyTomas/genshin_artifact_auxiliary/total?style=flat-square)](https://github.com/SkeathyTomas/genshin_artifact_auxiliary/releases)
[![GitHub release (latest by date)](https://img.shields.io/github/downloads/SkeathyTomas/genshin_artifact_auxiliary/latest/total?style=flat-square)](https://github.com/SkeathyTomas/genshin_artifact_auxiliary/releases/latest)

</div>

## 简介

帮你在游戏中整理圣遗物背包时更便捷地了解、查阅圣遗物的评分，然后把评分最高的圣遗物装配给希望的角色，同时支持背包面板和角色面板。多角色适配，帮你省去了记各角色有效词条、口算/按计算器的时间。

相比于其他评分工具的优势：

1. 与游戏本身有更好的贴合性，可以让玩家对于圣遗物好坏有更加方便直观的判断。
2. 省去了一些截图、角色装配调来调去、游戏内外来回对比的麻烦。

[demo&教程视频](https://www.bilibili.com/video/BV14g411W79L/)

![背包面板圣遗物](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220929234442.png)

![角色面板圣遗物](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220810004718.png)

## 环境与准备

### OCR引擎

1. OCR引擎[tesserect](https://github.com/tesseract-ocr/tesseract)，安装过程详见原项目，或者参考[这篇文章](https://www.jianshu.com/p/f7cb0b3f337a)，安装链接[tesseract-ocr-w64-setup-v5.3.0.20221214.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.3.0.20221214.exe)(64位)。如果你使用`scoop`，可以使用`scoop install tesseract`快速安装。安装完成后，可在命令行输入`tesseract`检验是否安装成功。
2. [tesseract中文简体数据文件](https://github.com/tesseract-ocr/tessdata_fast/blob/main/chi_sim.traineddata)，下载完成后保存到tesseract数据目录`tessdata`中（如果是`scoop`安装的话，放在`./scoop/persist/tesseract/tessdata`文件夹中）。

### 如果你需要直接运行python程序

1. Python 3.7+ (作者开发环境Python 3.11)。
2. 必备的Python包：
   1. PySide6，GUI框架
   2. pynput，监听游戏窗口内鼠标操作
   3. pywin32，获取设备分辨率、缩放信息，用于兼容不同分辨率
   4. Pillow，截图
   5. pytesseract，tesseract的python接口
   6. pyqtdarktheme，GUI样式
   7. requests，联网查询最新版本信息

### 使用打包的exe文件

1. 在release中下载最新的压缩包。
   1. 含with-tesseract的打包文件已包含tesseract引擎，无需再自行安装。
   2. 若已手动安装OCR引擎，可下载不含OCR引擎的压缩包。
2. 解压。

## 使用教程

1. 打开游戏，使用`ALT+ENTER`使游戏窗口切换为窗口模式（顶部出现标题栏，因为全屏状态下评分结果贴图无法置顶。），或手动在设置-图像-显示模式中调整为窗口模式。现已支持自定义窗口模式，支持窗口16:10, 16:9, 3:2分辨率，**请确定游戏窗口化打开且不要最小化，在工具启动后也不要移动游戏窗口，否则捕捉窗口定位错误会使识别出错**。

2. 方式1：运行打包好的程序。解压压缩包完成后，找到并用管理员模式运行keqing.exe（必须，否则程序运行中无法监听游戏中的鼠标操作）。

![keqing.exe](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20220805144258.png)

3. 方式2：下载源码，使用管理员模式打开命令行工具（必须，否则程序运行中无法监听游戏中的鼠标操作），并打开程序目录，使用命令`python app.py`运行程序。
4. 在主窗口中选择角色（不选的话，默认评估双爆+攻击词条）。
5. 打开背包-圣遗物或角色-圣遗物装配（需在主程序中对应选择背包或角色），随意选择圣遗物，点击`右键`进行圣遗物评分，评分结果随后标记在对应圣遗物右下角，并在主程序展示副词条识别结果。
6. 选中某个贴图结果，使用快捷键`Ctrl+Z`删除该贴图；使用全局快捷键`Ctrl+Shift+Z`删除所有贴图，可进行新一批圣遗物的评估。
7. 支持对选中的圣遗物（主面板跟随更新）进行手动修正识别结果，点击`确认修改`可保存修改结果，不过我觉得还是再点一次右键比较方便。
8. 当前屏幕上的贴图结果可通过取一个名称（比如「火伤杯」），再通过保存按钮本地储存（`src/archive.json`），可从下拉框中选择已保存的结果并贴图展示（包括下次打开程序）。

![主程序示意](https://raw.githubusercontent.com/SkeathyTomas/img/main/img/20221212182324.png)

## 评分方法

更新了[圣遗物评分方法](https://mp.weixin.qq.com/s/DxyS8Rll3_eLSelvjiwKwQ)，调整了角色的有效词条，增加了每个角色相对于固定词条的二级系数（如同样是大攻击对于一般主C和胡桃的评分系数就有所不同），删除了不同打法流派的角色。

具体每一个角色的有效词条和词条的评分系数可参考[character.json](src/character.json)和[score.py](score.py)中的配置，如与需求不符可自行前往源文件修改参数。

评分结果参考：

- 30分：勉强够用
- 40分：准毕业水平
- 50分：极品

（单个圣遗物评分结果仅供参考，具体角色强度还是要以整体角色面板和具体配队玩法为准。）

## 已知问题

### 分辨率适配

已适配游戏窗口16：10，16：9分辨率。分辨率适配框架已经搭好，若有分辨率适配问题，可查看程序目录中的`src/grab.png`识别截图是否准确，并提供一些不同分辨率的截图做坐标定位和测试了。

如使用多屏设备（如笔记本外接显示器），请把游戏窗口置于第一屏。

目前已验证无问题的分辨率：

16:10：

- [x] 2560 * 1600
- [x] 3840 * 2400

16:9：

- [x] 2560 * 1440
- [x] 1920 * 1080
- [x] 3840 * 2160

3:2:

- [x] 2160 * 1440

其他不支持的分辨率可在游戏内将显示模式调整为1920`*`1080窗口，然后重启该软件。

### 角色面板识别问题

背景飘过的白点和文字重叠可能会导致识别出错（感觉这个解决起来还是有点难度的，就算人眼去识别遮挡的文字可能也会出错，可能需要上下文，牵扯到数字可能就更没办法了）。

一般情况下再识别一次即可，可根据主程序面板的识别结果对比识别是否准确，手动校正与本地储存已识别结果功能~~正在筹备中~~已上线。

### 关于GUI

暂未对滚动条进行适配，若下拉滚动条使第一行圣遗物显示不全，或者在角色面板点击靠下的圣遗物，因为游戏系统自动会移动滚动条，贴图结果可能会有垂直方向的偏移。

使用了默认的组件，某些高级整合/自改组件Bug一堆，问就是还在学，不过就问你能不能用吧。UI美化、Bug修复等1.0版本再考虑。

### 语言支持

- [x] 中文简体

## 声明与支持

- 本程序不收集任何用户信息，所有数据保留在本地。
- 理论上未对任何游戏数据进行非法获取和修改，仅通过截图和OCR技术实现相关分析，且没有使用自动化程序帮助玩家获取游戏内资源，应该不在官方打击范围。如若官方觉得不妥，我就删库跑路。
- 最近在xx软件园之类的网站看到了自己的软件，并看到了完全对不上的功能介绍。在此声明并非本人上传，不确定是否做过恶意修改，请谨慎在release以外渠道下载本软件/工具（除了本人b站视频贴的方便GitHub访问困难用户的度盘链接）。

如果觉得有用/帮到了您的话，欢迎推荐给您的好友！

## 问题反馈

使用中有任何问题可以提Issue，最好提供下命令行的输出（如识别错误、环境错误等）。有人的话可以考虑建个交流群什么的。

## 需求来源

1. [如何做一个圣遗物管理系统：产品调研与分析](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E8%B0%83%E7%A0%94%E4%B8%8E%E5%88%86%E6%9E%90/)
2. [如何做一个圣遗物管理系统：产品需求文档](https://skeathytomas.github.io/post/%E5%A6%82%E4%BD%95%E5%81%9A%E4%B8%80%E4%B8%AA%E5%9C%A3%E9%81%97%E7%89%A9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%9A%E4%BA%A7%E5%93%81%E9%9C%80%E6%B1%82%E6%96%87%E6%A1%A3/)