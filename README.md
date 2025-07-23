# 抗压缩图片混淆

本混淆算法使用图片标尺解决压缩大小带来的坐标错位问题。

## 使用

```sh
python -m pip install -r requirements.txt
python __main__.py
```

## 示例

示例均使用默认设置：

![](example/image.png)

![](example/confused.png)

缩放 1/2，质量 50：

![](example/compressed.jpg) → ![](example/final.jpg)

> [!CAUTION]
> 若标尺损坏，将无法正确地解混淆图片。
