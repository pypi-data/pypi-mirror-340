from mitmproxy import http

# لتخزين الطلبات
requests_list = []
MODE_FILE = "proxy_mode.txt"

def get_mode():
    try:
        with open(MODE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "forward"

class ProxyAddon:
    def request(self, flow: http.HTTPFlow):
        mode = get_mode()
        if mode == "drop":
            flow.kill()
            print(f"Request dropped: {flow.request.pretty_url}")
        elif mode == "intercept":
            flow.intercept()
            print(f"Intercepted request: {flow.request.pretty_url}")
        else:
            request_data = {
                "method": flow.request.method,
                "url": flow.request.pretty_url,
                "headers": dict(flow.request.headers),
                "body": flow.request.get_text(),
            }
            requests_list.append(request_data)
            print(f"Captured request to: {flow.request.pretty_url}")

    def response(self, flow: http.HTTPFlow):
        mode = get_mode()
        if mode == "intercept":
            flow.intercept()
            print(f"Intercepted response from: {flow.request.pretty_url}")
        elif mode == "drop":
            flow.kill()
            print(f"Response dropped: {flow.request.pretty_url}")
        else:
            print(f"Captured response from: {flow.request.pretty_url}")


addons = [
    ProxyAddon()
]

def main():
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__])
