import requests
import base64
import urllib.parse

URL = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"

def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return base64.b64decode(data).decode('utf-8', errors='ignore')

def main():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        raw_text = response.text.strip()
        decoded_text = decode_base64(raw_text)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    configs = decoded_text.splitlines()
    unique_base_uris = set()
    final_configs = []

    for config in configs:
        config = config.strip()
        
        if not config.startswith("vless://"):
            continue
            
        if '#' in config:
            base_uri = config.split('#', 1)[0]
        else:
            base_uri = config
            
        try:
            parsed_url = urllib.parse.urlparse(base_uri)
            params = urllib.parse.parse_qs(parsed_url.query)
            
            if params.get('type', [''])[0] == 'ws':
                if base_uri not in unique_base_uris:
                    unique_base_uris.add(base_uri)
                    final_config = f"{base_uri}#FaMo"
                    final_configs.append(final_config)
        except Exception:
            continue

    # ذخیره به صورت فایل متنی خام بدون هیچ کاراکتر اضافه
    with open('famo_configs.json', 'w', encoding='utf-8') as f:
        for c in final_configs:
            f.write(c + '\n')
        
    print(f"Successfully processed {len(final_configs)} unique Vless WS configs.")

if __name__ == "__main__":
    main()
