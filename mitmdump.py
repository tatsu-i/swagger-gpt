from mitmproxy import ctx, http
import sys

api_host = sys.argv[3]
api_path = sys.argv[4] if len(sys.argv) > 4 else "/"
ctx.log.info(f"API : {api_host}{api_path}")
log_file = "mitmproxy.log"  # ログを保存するファイル名

def write_log(message: str):
    with open(log_file, "a") as file:
        file.write(message + "\n")

def format_headers(headers):
    masked_headers = {}
    for name, value in headers.items():
        if name.lower() in ['authorization', 'cookie']:
            masked_headers[name] = '*' * 8  # 8文字のアスタリスクでマスク
        else:
            masked_headers[name] = value
    return '\n'.join(f'{name}: {value}' for name, value in masked_headers.items())

def request(flow: http.HTTPFlow) -> None:
    if flow.request.host == api_host and flow.request.path.find(api_path) != -1:
        # リクエストメソッドとPathのログ
        log_msg = f"---\n{flow.request.method} {flow.request.path}"
        write_log(log_msg)

        # リクエストヘッダーのログ
        headers = format_headers(flow.request.headers)
        log_msg  = f"\nDomain: {flow.request.host}"
        log_msg += f"Request Headers:\n{headers}"
        write_log(log_msg)

        # リクエストのbodyを出力
        if flow.request.content:
            log_msg = "Request Body:\n" + flow.request.content.decode('utf-8', 'ignore')
            write_log(log_msg)

def response(flow: http.HTTPFlow) -> None:
    if flow.request.host == api_host and flow.request.path.find(api_path) != -1 and flow.response:
        # ステータスコード
        if flow.response.status_code:
            log_msg = f"\nStatus Code: {flow.response.status_code}"
            write_log(log_msg)
        # レスポンス
        log_msg = "Response:\n" + flow.response.text
        write_log(log_msg)


# スクリプトを実行するためにmitmdumpにこのファイルのパスとホストを指定する
# 例: mitmdump -s mitmdump.py api.example.com /v1
