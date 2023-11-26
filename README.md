# Swagger GPT

## プロジェクトの概要
このプロジェクトは、特定のAPIのリクエストとレスポンスをログに記録し、そのログを元に`OpenAPI 3.0.0`形式の仕様を生成します。

## 必要なパッケージのインストール
```
pip install openai
```

## 使用方法
1. `mitmdump.py`を使用してAPIのリクエストとレスポンスをログに記録します。

```bash
mitmdump -s mitmdump.py api.example.com /v1
```

2. `generate.py`を使用して、ログからOpenAPI 3.0.0形式の仕様を生成します。

```bash
python generate.py mitmproxy.log > openapi.yaml
```
