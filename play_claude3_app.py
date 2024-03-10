import streamlit as st
import play_claude3_lib as glib

st.set_page_config(layout="wide", page_title="薛以致用 - Claude3 初体验")
st.title("薛以致用 - Claude3 初体验")

_9th_grade_exercise_dict = {
    "物理压强问题": {"file":"images/初三物理19题.png","prompt":"第一步，请仔细审题，尤其是涉及的物理量、公式等，并提取所有已知条件和待求解问题，如有表格请将表格数据输出成 Markdown 格式，并作为已知条件；第二步，每个问题给出详细解答过程和结果；第三步，总结涉及到的知识点，公式，定理等"},
    "物理功率问题": {"file":"images/物理计算题17.png","prompt":"第一步，请仔细审题，尤其是涉及的物理量、公式等,并提取所有已知条件和待求解问题；第二步，每个问题给出详细解答过程和结果；第三步，总结涉及到的知识点，公式，定理等"},
    "英语阅读首字母填空": {"file":"images/初三英语阅读填空.png","prompt":"在短文的空格内，根据首字母填入最匹配上下文单词，每空限填一词，请仔细推敲，使内容其通顺"},
    "英语阅读选择最合适单词": {"file":"images/初三英语阅读选词.png","prompt":"请选择最恰当的选项完成短文，请仔细推敲所有选项，选出最合适的一个答案"},
    "数学概率问题": {"file":"images/初三数学概率.png","prompt":"第一步，请仔细审题，尤其是数字、公式、不同的变量代号,并提取所有已知条件和待求解问题；第二步，每个问题给出详细解答过程和结果；第三步，总结涉及到的知识点，公式，定理等"},
    "数学加油卡问题": {"file":"images/初三数学-加油卡.png","prompt":"第一步，请仔细审题，所有的尤其是数字、公式、不同的变量代号, 并提取所有已知条件；第二步，识别所有待求解问题，如有变量，请仔细说明，每一个求解变量在题目中的含义；第三步，给出详细推导过程和结果；第四步，总结涉及到的知识点，公式，定理等"},
    "其他":{"file":"images/初三数学-加油卡.png","prompt":"第一步，请仔细审题，所有的尤其是数字、公式、不同的变量代号, 并提取所有已知条件；第二步，识别所有待求解问题，如有变量，请仔细说明，每一个求解变量在题目中的含义；第三步，给出详细推导过程和结果；第四步，总结涉及到的知识点，公式，定理等"}
}

execise_options = list(_9th_grade_exercise_dict)

colRole, colScenario,colResult = st.columns(3)

with colRole:
    st.subheader("设定你的角色")
    role_selection = st.radio(label="设定你的角色",options=["初三家长","业余技术作家","财报分析"],label_visibility="hidden")
    if role_selection == "初三家长":
        sys_prompt = "你是一名初三家长，具有高等教育知识，请以老师角度帮孩子梳理知识点，讲解解题过程和给出最终答案，请用中文回答"
        pdfCont = -1 # 初始化 PDF 文档内容为空，-1 表示提交 Button点击后，不需要额外处理
        st.write(sys_prompt)
        execise_selection = st.radio("选择一个题目", execise_options)
        if execise_selection == '其他':
            uploaded_file = st.file_uploader("选择一个题目图片", type=['png', 'jpg'], label_visibility="collapsed")
        else:
            uploaded_file = None
        
        if uploaded_file and execise_selection == '其他':
            uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_file.getvalue())
            st.image(uploaded_image_preview)
        else:
            st.image(_9th_grade_exercise_dict[execise_selection]["file"])   
        
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
        else:
            image_bytes = glib.get_bytes_from_file(_9th_grade_exercise_dict[execise_selection]["file"])        
        user_prompt = _9th_grade_exercise_dict[execise_selection]["prompt"]#"请仔细审题，第一步，将图片中的题目主干和待求解的问题识别出来；第二步，给出该题目考察的知识点；第三步，尝试至少两种方法进行分析对照，并给出最贴合第二步知识点，且符合初三学生认知的解题过程；"

    elif role_selection == "业余技术作家":
        sys_prompt="你是业余技术作家，经常阅读和引用公开的论文材料，作为素材构思新的技术博客文章"
        st.write(sys_prompt)
        st.write("请上传参考文档:")
        uploaded_file1 = st.file_uploader("选择参考资料A", type=['pdf'], label_visibility="collapsed")
        user_prompt = ""
        image_bytes = None
        pdfCont = 1  # 初始化 PDF 文档内容，1 表示“业余作家”标签，且提交 Button点击后，，需要加载 PDF 文档内容
        # if uploaded_file1:
        #pdfCont = glib.load_pdf_data_from_bytes(uploaded_file1.getvalue())
        user_prompt = """文章内容如下 <document>{pdfCont}</document>; 我请你基于以下规则进行改写和总结：
                        <instructions>
                            1. 改成一篇中文博客文章，分为6个段落导读、遇到哪些挑战、如何分析这些挑战、采取了哪些措施、取得了什么样的成果、总结
                            2. 导读部分，300字以内，吸引读者注意力，并提醒读者整个博客内容长度，估算读完需要的时间
                            3. 遇到哪些挑战部分，300～500字，描述现状，以及遇到的挑战或故障影响等
                            4. 如何分析这些挑战部分，800字左右，定位到这些挑战，如何深度分析和量化分析这些挑战背后的根因？
                            5. 采取了哪些措施部分，800字左右，基于分析，团队采取了哪些应对措施？以及如何验证对策的有效性？
                            6. 取得了什么样的成果部分，300到500字，采取了这些措施，有哪些优化成果？
                            7. 总结部分，300以内，总结整篇博客文章，重点提示客户可以借鉴的建议
                        </instructions>"""
            

    elif role_selection == "财报分析":
        sys_prompt="你是一个财经专栏作家，具有专业的财务知识。"
        st.write(sys_prompt)
        fin_report_url = st.text_input(label="财报PDF链接（以Amazon.com 2023Q4 为例））",value="https://s2.q4cdn.com/299287126/files/doc_financials/2023/q4/AMZN-Q4-2023-Earnings-Release.pdf")
        image_bytes = None
        pdfCont = 2  # 初始化 PDF 文档内容为空，2 表示“财报分析”，且提交 Button点击后，需要加载 PDF 文档内容
        # pdfCont = glib.load_pdf_from_internet(fin_report_url)
        user_prompt = """财报内容如下 <document>{pdfCont}</document>; 我请你基于以下规则进行分析和总结：
                        <instructions>
                            1. 总结成一篇中文财经博客文章，分为5个段落导读、整体业务亮点和挑战、AWS云业务业绩和趋势、人员和基础设施支出分析、总结，请结合财报数据进行量化分析和解读；
                            2. 导读部分，300字以内，吸引读者注意力，分析该财报时间段，并提醒读者整个博客内容长度，估算读完需要的时间
                            3. 整体业务亮点和挑战，300～500字，描述经济环境，业务增长亮点，各业务营收占比，环比或同比增长率，竞争对手的一些数据，以及遇到的挑战等
                            4. AWS云业务业绩和趋势，500字左右，针对 Amazon Web Services 云业务，业绩如何？是否符合预期？市场趋势？未来增长方向？
                            5. 人员和基础设施支出分析，500字左右，研发投入分析，基础设施投入分析
                            6. 总结部分，300以内，总结整篇博客文章，重点提示客户关注的3条财报核心要点
                        </instructions>"""


with colScenario:
    st.subheader("指导 Claude3 如何帮你完成任务")
    
    prompt_text = st.text_area("Prompt",
        #value=,
        value=user_prompt,
        height=500,
        help="有什么可以帮你？",
        label_visibility="collapsed")
    
    go_button = st.button("提交", type="primary")

with colResult:
    st.subheader("结果输出")
    is_claude_go = True
    if go_button:
        with st.spinner("思考进行中......"):
            if pdfCont == 2: # 财报分析
                try:
                    pdfCont = glib.load_pdf_from_internet(fin_report_url)
                    prompt_text = user_prompt.format(pdfCont=pdfCont)
                except Exception as e:
                    st.error("请检查财报PDF链接是否正确！")
                    is_claude_go = False
                # pdfCont = glib.load_pdf_from_internet(fin_report_url)
                
            elif pdfCont == 1: # 业余作家
                if uploaded_file1:
                    pdfCont = glib.load_pdf_data_from_bytes(uploaded_file1.getvalue())
                    prompt_text = user_prompt.format(pdfCont=pdfCont)   
                else:
                    st.warning("请上传参考文档!", icon="⚠️")
                    is_claude_go = False
            
            if is_claude_go:
                response = glib.get_stream_response_from_model(
                    prompt_content=prompt_text, 
                    image_bytes=image_bytes,
                    system_prompt = sys_prompt,
                )
        
        st.write_stream(response)

col1, col2, col3 = st.columns(3)

prompt_options_dict = {
    "Image caption": "Please provide a brief caption for this image.",
    "Detailed description": "Please provide a thoroughly detailed description of this image.",
    "Image classification": "Please categorize this image into one of the following categories: People, Food, Other. Only return the category name.",
    "Object recognition": "Please create a comma-separated list of the items found in this image. Only return the list of items.",
    "Subject identification": "Please name the primary object in the image. Only return the name of the object in <object> tags.",
    "Writing a story": "Please write a fictional short story based on this image.",
    "Answering questions": "What emotion are the people in this image displaying?",
    "Transcribing text": "Please transcribe any text found in this image.",
    "Translating text": "Please translate the text in this image to French.",
    "Other": "",
}

st.image(caption="更多精彩，欢迎关注薛以致用公众号！",image="images/qrcode_wechat.jpg", width=200)