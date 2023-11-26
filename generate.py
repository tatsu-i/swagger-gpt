import sys
import json
import yaml
from openai import OpenAI


def generate_swagger(prompt):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4-1106-preview", 
        messages=[
            {"role": "system", "content": "あなたは入力されたログ内容から`OpenAPI 3.0.0`のJSONを生成するアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
        response_format={ "type": "json_object" },
    )
    return response.choices[0].message.content
    
with open(sys.argv[1]) as f:
    prompt = f.read()
    swagger_json = generate_swagger(prompt)
    swagger_yaml = yaml.dump(json.loads(swagger_json))
    print(swagger_yaml)

# 以下のように実行すると入力されたmitmdumpのログファイルの内容からOpenAPI 3.0.0形式の仕様が出力されます。
# python generate.py mitmproxy.log > openapi.yaml