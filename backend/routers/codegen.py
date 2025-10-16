from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

# Simple code generation logic for demonstration
CODE_TEMPLATES = {
    "Python": "import requests\nresponse = requests.{method.lower()}('{url}', data={body})\nprint(response.text)",
    "JavaScript": "fetch('{url}', { method: '{method.upper()}', body: JSON.stringify({body}) })\n  .then(res => res.text())\n  .then(console.log);",
    "Go": "package main\nimport (\n  \"net/http\"\n  \"fmt\"\n)\nfunc main() {\n  resp, err := http.NewRequest(\"{method.upper()}\", \"{url}\", nil)\n  if err != nil { fmt.Println(err); return }\n  fmt.Println(resp)\n}",
    "Java": "import java.net.*;\npublic class Main {\n  public static void main(String[] args) throws Exception {\n    HttpURLConnection con = (HttpURLConnection) new URL(\"{url}\").openConnection();\n    con.setRequestMethod(\"{method.upper()}\");\n    // Add body handling\n    System.out.println(con.getResponseCode());\n  }\n}",
    "C#": "using System.Net.Http;\nvar client = new HttpClient();\nvar response = await client.SendAsync(new HttpRequestMessage(HttpMethod.{method.capitalize()}, \"{url}\"));\nConsole.WriteLine(await response.Content.ReadAsStringAsync());"
}

@router.post("/codegen")
def generate_code(payload: dict):
    try:
        lang = payload.get("language", "Python")
        method = payload.get("method", "GET")
        url = payload.get("url", "https://api.example.com")
        body = payload.get("body", "{}")
        template = CODE_TEMPLATES.get(lang)
        if not template:
            raise HTTPException(status_code=400, detail="Language not supported")
        code = template.format(method=method, url=url, body=body)
        return JSONResponse(content={"code": code})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
