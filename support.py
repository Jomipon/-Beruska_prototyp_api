from io import BytesIO
import pycurl


def download_get_url(url, headers):
    client = pycurl.Curl()
    #client.setopt(client.URL, url)
    client.setopt(pycurl.URL, url.encode("utf-8"))
    buffer = BytesIO()
    client.setopt(client.WRITEDATA, buffer)
    client.setopt(pycurl.USERAGENT, "BeruskaApp/1.2 (+tomas.vlasaty8@gmail.cz; https://jomipon-beruska-prototyp.streamlit.app/)")
    if headers is not None and len(headers) > 0:
        client.setopt(pycurl.HTTPHEADER, headers)
    # Volitelně debug:
    # client.setopt(pycurl.VERBOSE, True)
    client.perform()
    status = client.getinfo(pycurl.RESPONSE_CODE)
    #print(status)
    client.close()
    body = buffer.getvalue()
    return body



