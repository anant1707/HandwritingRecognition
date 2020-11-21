def ocr_azure():
    import json
    import time
    import requests
    image=open("temp.jpeg","rb").read()
    endpoint="https://2020answerlyminorproject.cognitiveservices.azure.com/"
    subscription_key="c46df8cef6ae42e3a72fde64fdc5f6d6"
    text_recognition_url = endpoint + "/vision/v3.0/read/analyze"
    params={'language':'en','detectOrientation':'true'}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    response=requests.post(text_recognition_url,params=params,headers=headers,data=image)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    analysis={}
    poll=True
    while(poll):
        response_final=requests.get(operation_url,headers=headers)
        analysis=response_final.json()
        # print(json.dumps(analysis,indent=4))
        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    return analysis
#
def get_text(path):
    from pdf2image import convert_from_path
    import requests
    
    images=convert_from_path(path)
    ocr_text=""
    for temp_image in images:
        temp_image.save("temp.jpeg")
        json_file=ocr_azure()
        lines=json_file['analyzeResult']['readResults'][0]['lines']
        for line in lines:
            ocr_text=ocr_text+line['text']+" "
    return ocr_text


print(get_text("rahul_asg.pdf"))