# 基于 Amazon Bedrock 学习 Claude3

日常三个场景，给大家一个快速体验 Claude 3 的实验样例，代码演示 （1）Python 通过 anthropic Claude Message API 进行多模态交互（图片，文本），（2）流式调用，（3）图片和PDF的处理（4）Streamlit 的 Web 前端交互
![Demo Homepage](/images/demo_home.png)

# 基本环境

* 开发环境：
    -（1）使用 Web IDE Cloud9 或
    -（2）本地的 VSCode + 远程 EC2 （建议 Amazon Linux 2）(**推荐**)

* 下载 Demo：
  `git clone https://github.com/soldierxue/bedrock-claude3-demo`
* 运行环境：
    * Python 3.9 + 
    * 依赖的 Python 库：
    `pip39 install -r ./requirements.txt -U`

* 启动 Demo:
  `streamlit run --server.port 8080 ./play_claude3_app.py`

# 样例说明

## 设定：初三家长

你是一名初三家长，具有高等教育知识，请以老师角度帮孩子梳理知识点，讲解解题过程和给出最终答案，请用中文回答

## 设定：业余作家

你是业余技术作家，经常阅读和引用公开的论文材料，作为素材构思新的技术博客文章

## 设定：财报解读

你是一个财经专栏作家，具有专业的财务知识。

# 更多资讯请关注公众号

![WeChat QCode](https://github.com/soldierxue/bedrock-claude3-demo/blob/main/images/qrcode_wechat.jpg)
