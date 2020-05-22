# 哔哩哔哩评论数据分析

这是一份《程序设计与人工智能》课程大作业，由[余柏辰](https://baichenyu.me)独立完成。

## 背景

灵感来自互联网上对哔哩哔哩官方视频[《后浪》](https://www.bilibili.com/video/BV1FV411d7u7)的广泛争论，我想要对[哔哩哔哩视频网](https://www.bilibili.com/)（以下简称b站）评论区的反应进行数据分析。刚好这时b站推出了第二弹视频[《入海》](https://www.bilibili.com/video/BV1tC4y1H7yz)，我想可以进行对比分析。然而听说还可能有第三弹，于是决定干脆将其变为一个对b站任意视频评论区进行数据分析的小工具。

## 技术路线

## 实现功能

1. BV号与av号的互转。由于b站后台序号更新，引入了BV号，造成了用户寻找视频的一些不便。这里提供了转换功能。
2. 对于输入的av号，通过官方api爬取评论区所有有效信息。
3. 通过分词进一步挖掘其中信息。
4. 制作特色词云。
5. 对用户评论的情感态度进行分析。
6. 对用户的等级分布和评论发布时间进行分析。
7. 提供GUI图形接口，便于查询。（进行中）

##  写在后面

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

[MIT](LICENSE) © Jamesyu420