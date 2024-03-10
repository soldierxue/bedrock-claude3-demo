import boto3
import json
import base64
from io import BytesIO
from botocore.exceptions import ClientError
# from langchain_community.document_loaders import PyPDFLoader
from pypdf import PdfReader
import urllib3

#get a BytesIO object from file bytes
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


#get a base64-encoded string from file bytes
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


#load the bytes from a file on disk
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes

http = urllib3.PoolManager()
# load pdf text from an internet address
def load_pdf_from_internet(file_url):
    req = http.request("GET",file_url,preload_content=False)
    pdfBytes = req.read()
    return load_pdf_data_from_bytes(pdfBytes)

# load pdf data from a file on disk
def load_pdf_data_from_bytes(pdfBytes):
    reader = PdfReader(BytesIO(pdfBytes))
    # reader = PdfReader("nsdi20-paper-brooker-EBS-2020.pdf")
    pdfCnt = ""
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        # pdfCnt += page.extract_text() + "\n"
        pdfCnt += "\n" + page.extract_text()
    return pdfCnt

#get the stringified request body for the InvokeModel API call
def get_image_understanding_request_body(prompt, image_bytes=None, system_prompt="",mask_prompt=None, negative_prompt=None):

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0.9,
        "system" : system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    }
    if image_bytes is not None:
        input_image_base64 = get_base64_from_bytes(image_bytes)
        img_msg =   {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg", #this doesn't seem to matter?
                            "data": input_image_base64,
                        },
                    }
        body["messages"][0]["content"].append(img_msg)   
    
    return json.dumps(body)



#generate a response using Anthropic Claude
def get_response_from_model(prompt_content, image_bytes, system_prompt="", mask_prompt=None):
    session = boto3.Session()
    
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    body = get_image_understanding_request_body(prompt_content, image_bytes, system_prompt = system_prompt, mask_prompt=mask_prompt)
    
    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-sonnet-20240229-v1:0", contentType="application/json", accept="application/json")
    
    response_body = json.loads(response.get('body').read()) # read the response
    
    output = response_body['content'][0]['text']
    
    return output

def get_stream_response_from_model(prompt_content, image_bytes, system_prompt="", mask_prompt=None):
    session = boto3.Session()
    
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    body = get_image_understanding_request_body(prompt_content, image_bytes, system_prompt = system_prompt, mask_prompt=mask_prompt)
    output = ""
    try:
        response = bedrock.invoke_model_with_response_stream(body=body, modelId="anthropic.claude-3-sonnet-20240229-v1:0", contentType="application/json", accept="application/json")
        usage = ""
        for event in response.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])

            if chunk['type'] == 'message_start':
                usage = usage + f"\n \n   Input tokens: {chunk['message']['usage']['input_tokens']}, "
            if chunk['type'] == 'message_delta':
                usage = usage +  f"Output tokens: {chunk['usage']['output_tokens']}"

            if chunk['type'] == 'content_block_delta':
                if chunk['delta']['type'] == 'text_delta':
                    yield output + chunk['delta']['text']

        yield output + usage

    except ClientError as err:
        message = err.response["Error"]["Message"]
        return message
    
    return output    

