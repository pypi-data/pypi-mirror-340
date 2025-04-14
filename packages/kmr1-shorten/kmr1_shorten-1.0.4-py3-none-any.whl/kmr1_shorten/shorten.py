import sys
import argparse
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen
import json
import pyperclip

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def shorten_url(url, custom_characters=None):
    api_url = "https://api.kmr1.org/v1/"
    data = {"url": url}
    if custom_characters:
        data["custom_characters"] = custom_characters
    post_data = urlencode(data).encode("utf-8")
    try:
        with urlopen(api_url, data=post_data) as response:
            json_response = json.loads(response.read().decode("utf-8"))
            if "short_url" in json_response and "tracking_id" in json_response:
                short_url = json_response['short_url']
                tracking_id = json_response['tracking_id']
                print(f"Short_URL: {short_url}")
                print(f"Tracking_ID: {tracking_id}")
                pyperclip.copy(short_url)
                print("✅ 短縮URLをクリップボードにコピーしました。")
            elif "error" in json_response:
                print(f"エラー: {json_response['error']}")
            else:
                print("エラー: APIレスポンスにバグが発生している又は既に使用されているカスタム文字列です。")
    except Exception as e:
        print(f"リクエストエラー: {e}")

def main():
    cmd_name = sys.argv[0].split('/')[-1].split('\\')[-1]
    if "kmr1-shorten" in cmd_name:
        usage = "kmr1-shorten <URL> [-c <カスタム文字列>]"
    elif "k1s" in cmd_name:
        usage = "k1s <URL> [-c <カスタム文字列>]"
    else:
        usage = "<command> <URL> [-c <カスタム文字列>]"

    parser = argparse.ArgumentParser(
        description="Kmr¹ APIを使用してURLを短縮します。Kmr¹API公式ドキュメント https://api.kmr1.org/v1/use",
        usage=usage
    )
    parser.add_argument("url", help="短縮したいURL")
    parser.add_argument("-c", "--custom", help="カスタム文字列（オプション）")
    
    args = parser.parse_args()

    if not is_valid_url(args.url):
        print("エラー: 無効なURLです。")
        sys.exit(1)

    shorten_url(args.url, args.custom)

if __name__ == "__main__":
    main()
