from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

def identificar_formularios(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    campos_de_entrada = []

    for form in forms:
        inputs = form.find_all('input')
        for input_tag in inputs:
            tipo = input_tag.get('type')
            if tipo in ['text', 'password', 'email', 'checkbox', 'radio', 'submit']:
                campos_de_entrada.append((form.get('action'), input_tag.get('name'), tipo))
    
    return campos_de_entrada

def identificar_urls(html_content, url_base):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    urls = []

    for link in links:
        href = link.get('href')
        if href:
            url_completa = urlparse(href, scheme='http')
            if url_completa.netloc:
                urls.append(url_completa.geturl())
            else:
                urls.append(urlparse(url_base)._replace(path=href).geturl())
    
    return urls

def identificar_cookies(response):
    cookies = response.cookies
    return cookies

# Exemplo de uso:
url = 'https://example.com'
response = requests.get(url)
html_content = response.text

formularios = identificar_formularios(html_content)
print("Campos de entrada encontrados nos formulários:")
for formulario in formularios:
    print(formulario)

urls = identificar_urls(html_content, url)
print("\nURLs encontradas:")
for url_encontrada in urls:
    print(url_encontrada)

cookies = identificar_cookies(response)
print("\nCookies encontrados:")
for cookie in cookies:
    print(cookie.name, cookie.value)
