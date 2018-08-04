——————————————————2018.8.5——————————————————————

# 批量下载云课堂内的课件0.80

> 懒惰是进步的源泉（雾

[TOC]



## 结构支持

- python3
- pycharm
- chrome(68.0.3440.84)(64bit）

## 配置项 & 注意事项

1. selenium 中的webdriver工具请自行按照浏览器类型和版本号进行下载，Part4 中涉及到webdriver的目录，请自行更改（笔者放在了桌面）
2. 笔者调用browser.get()时访问资源页，由于之前下载时选择了默认保存（而不是打开XPS阅读器），所以每访问一个资源页，程序会自动保存一个xps文件，在`C:/Users/HP/Downloads/`里，这个需要自行配置。
3. 因为主要考虑自用，且暑期学校的视频预览好像出了问题，直接筛除了媒体文件。
4. 如果要问为什么全部命名为pdf文件，是因为下载下来后用doc/docx打不开，发现文件头部是PDF1.5，惊了，那就全部存为pdf吧。
5. 休眠时设置为了3s，不知道为什么这样的时候完成成功率最高，建议使用校园网（CCNU成功率最高），不然会有很高的报错率。
6. 如果下载到一半报错那就得重新执行第四部分，而且一定要记得删掉或转移download里面的已下载文件不然一定会报错！

## 寻求改进

- [ ] 在处理异常方面仍然有很多工作要做
- [ ] 在选择方法上，一定还有更好的路径可走
- [ ] 在获取文件上，需要新的思路，能尽可能避免异常出现
- [ ] 媒体文件，目前处于暑期，视频文件的预览似乎出现了异常，下载也没有响应。（这样的话也没办法进行下载模式选择）
- [ ] 选择文件保存目录，怎么让用户自行配置
- [ ] 永恒不变的，怎么让这个项目做到新手友好？（看一眼女票

以上都是以后要更新和改进的，还请各位大佬指教！

改进意见请发邮件到个人邮箱:natsu@mails.ccnu.edu.cn

## 鸣谢

- @ [wwyqianqian][https://github.com/wwyqianqian/wwyqianqian.github.io] : 提供了完美登录的方法，感激！！！
- @[ba0zhi][https://github.com/ba0zhi] :让我了解到如何从网页源代码里提取资源，的启蒙人（哲学符号）（撒花
