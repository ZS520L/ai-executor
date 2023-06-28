# ai-executor
With the ability of AI to generate code, let Python execute the non -existent way!

1. Experimental goals
* To make python execute methods that don't exist with the power of AI generated code!
* To strengthen code programming skills and verify the feasibility of ideas!

2. Reference links:
* https://www.bilibili.com/video/BV1na4y1K7H5/?spm_id_from=333.880.my_history.page.click
* https://www.bilibili.com/video/BV1ET41187m9/?spm_id_from=333.880.my_history.page.click

3. Final effect
* You can execute methods that don't exist, so be careful to name the methods properly.
* Methods that work can be saved to avoid duplicate generation

# Quickly start
```
pip install ai-executor==0.2.6 #安装库
```

示例代码：
```
from ai_executor import AI

# 用例
ai1 = AI("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")
ai1.a_add_b(3, 4)
ai1.a的b次幂(3, 4)
```
