from typing import Dict, Optional
from requests import Response, get
from settings import BACKEND_HOST, BACKEND_PORT


def server_get(path:str, query_params: Optional[Dict[str,str]]  = None) -> Response:
    url = "http://" + BACKEND_HOST + ":" + BACKEND_PORT + path
    if query_params is not None:
        url += "?"
        for key, value in query_params.items():
            url += key + "=" + value + "&"
        url = url[:-1] #removes last "&"


    res = get(url)
    if res.status_code != 200:
        print(res.content)
        raise Exception("Server not responding")

    return res
        
        
        

