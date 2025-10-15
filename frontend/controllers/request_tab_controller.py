from ..views.request_tab import RequestTab
from .api_client import APIClient
from PySide6.QtWidgets import QApplication

class RequestTabController:
    def __init__(self, tab):
        self.tab = tab
        self.tab.send_btn.clicked.connect(self.send_request)

    def send_request(self):
        method = self.tab.method_box.currentText()
        url = self.tab.url_input.text()
        body = self.tab.body_edit.toPlainText()
        headers = {}
        params = {}
        auth_type = self.tab.auth_type.currentText()
        auth_value = self.tab.auth_input.text()
        if auth_type == "Bearer Token" and auth_value:
            headers["Authorization"] = f"Bearer {auth_value}"
        elif auth_type == "Basic Auth" and auth_value:
            headers["Authorization"] = f"Basic {auth_value}"
        # Optionally parse query params from URL
        if "?" in url:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(url)
            url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
        import time
        start_time = time.time()
        self.tab.log_terminal(f"[SEND] {method} {url} | Headers: {headers} | Params: {params}")
        # Show loading indicator in info bar
        self.tab.response_info.setText("⏳ Sending request...")
        QApplication.processEvents()
        # Show loading indicator in info bar and progress bar
        self.tab.response_progress.setVisible(True)
        self.tab.response_progress.setRange(0, 0)  # Indeterminate
        self.tab.send_btn.setEnabled(False)
        try:
            self.tab.log_terminal("[INFO] Sending request to backend API...")
            result = APIClient.execute_request(method, url, body, headers, params)
            elapsed = time.time() - start_time
            self.tab.log_terminal(f"[RESPONSE] Time: {elapsed:.2f}s | Result: {result}")
            if "error" in result:
                error_msg = result["error"]
                self.tab.log_terminal(f"[ERROR] {error_msg}")
                self.tab.update_response_panel(
                    status=result.get('status', 'Error'),
                    headers=result.get('headers', {}),
                    body=result.get('body', ''),
                    elapsed=elapsed,
                    error=error_msg,
                    request_data={
                        'method': method,
                        'url': url,
                        'headers': headers,
                        'params': params,
                        'body': body
                    }
                )
            else:
                body = result.get('body', '')
                status = result.get('status', '')
                headers_resp = result.get('headers', {})
                self.tab.update_response_panel(
                    status=status,
                    headers=headers_resp,
                    body=body,
                    elapsed=elapsed,
                    request_data={
                        'method': method,
                        'url': url,
                        'headers': headers,
                        'params': params,
                        'body': body
                    }
                )
                # Add to history
                history_item = {
                    "id": 0,
                    "method": method,
                    "url": url,
                    "status": result.get('status', 0),
                    "response": body
                }
                APIClient.add_history(history_item)
                self.tab.log_terminal(f"[HISTORY] Request saved to history.")
                # hide progress and re-enable send
                self.tab.response_progress.setVisible(False)
                self.tab.response_progress.setRange(0, 100)
                self.tab.send_btn.setEnabled(True)
        except Exception as e:
            elapsed = time.time() - start_time
            self.tab.log_terminal(f"[EXCEPTION] {str(e)}")
            self.tab.update_response_panel(
                status='Exception',
                headers={},
                body='',
                elapsed=elapsed,
                error=str(e),
                request_data={
                    'method': method,
                    'url': url,
                    'headers': headers,
                    'params': params,
                    'body': body
                }
            )
            self.tab.response_progress.setVisible(False)
            self.tab.response_progress.setRange(0, 100)
            self.tab.send_btn.setEnabled(True)
