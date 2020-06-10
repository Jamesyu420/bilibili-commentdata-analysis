# 哔哩哔哩评论数据分析

这是一份《程序设计与人工智能》课程大作业，由[余柏辰](https://baichenyu.me)独立完成。

## 背景

灵感来自互联网上对哔哩哔哩官方视频[《后浪》](https://www.bilibili.com/video/BV1FV411d7u7)的广泛争论，我想要对[哔哩哔哩视频网](https://www.bilibili.com/)（以下简称b站）评论区的反应进行数据分析。刚好这时b站推出了第二弹视频[《入海》](https://www.bilibili.com/video/BV1tC4y1H7yz)，我想可以进行对比分析。然而听说还可能有第三弹，于是决定干脆将其做成一个对b站任意视频评论区进行数据分析的小工具，然后用它进行分析研究。

## 技术路线

1. requests爬取数据
2. numpy和pandas实现数据预处理
3. jieba分词，wordcloud辅助Pillow库实现词云
4. 调用snowNLP以进行情感分析
5. 依靠matplotlib实现图像输出

## 实现功能

1. BV号与av号的互转。由于b站后台序号更新，引入了BV号，造成了用户寻找视频的一些不便。这里提供了转换功能。
2. 对于输入的av号，通过api爬取评论区所有有效信息。
3. 通过分词进一步挖掘其中信息。
4. 制作特色词云。
5. 对用户评论的情感态度进行分析。
6. 对用户的等级分布和评论发布时间进行分析。
7. 提供GUI图形接口，便于查询。

## 展望

1. 大规模的API爬取耗时过长，可以通过多线程爬虫高速爬取
2. 自己构建更准确的分类器，以实现更好的情感分析效果
3. 挖掘更多的描述性统计图表
4. 可以对比不同平台（如网易云音乐）评论区的热词频率，进而分析不同软件受众的特点

## 写在后面

注：所有markdown文档的图片均需科学上网查看。

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[MIT](LICENSE) © Jamesyu420
