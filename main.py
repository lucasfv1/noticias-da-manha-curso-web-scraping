# Importar bibliotecas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import smtplib

# Função para obter as principais noticias do Olhar Digital
def get_olhar_digital_news():
    url = "https://www.olhardigital.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news = []

    # Selecionar o container principal que contêm as notícias
    feature_grid = soup.select_one("#featuredGrid")

    # Selecionar todas as tags a de featuredGrid
    feature_grid = feature_grid.find_all(name="a")

    # Iterar sobre as tags a do feature_grid e adicioná-las na lista news
    for item in feature_grid:
        news.append({"title": item.get("title"), "link": item["href"]})

    return news


# Função para obter as principais noticias do CNN Brasil
def get_cnn_news():
    url = "https://www.cnnbrasil.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news = []

    # Seleciona o first_level_block
    first_level_block = soup.select_one(".block_style_first-level")
    # Seleciona a div principal do bloco com a notícia em destaque
    first_level_block_destaque = first_level_block.find("div", class_="block--manchetes-highlights-title-items")
    # Adicionar a notícia destaque na lista de notícias
    news.append({"title": first_level_block_destaque.get_text(strip=True), "link": first_level_block_destaque.find("a")["href"]})
    # Selecionar sub-destaques
    sub_destaques = first_level_block.select(".block__news__related")
    # Iterar sobre os sub-destaques
    for item in sub_destaques:
        news.append({"title": item.find(name="h4").get_text(), "link": item.find(name="a")["href"]})

    # Seleciona o second_level_block
    second_level_block = soup.select_one(".block_style_second-level")
    # Selecionar todos os itens de machete
    manchetes = second_level_block.find_all(name="li", class_="block__news__item--manchetes")
    # Iterar sobre as manchetes
    for manchete in manchetes:
        news.append({"title": manchete.find(name="h3").get_text(), "link": manchete.find(name="a")["href"]})

    return news


# Função para formatar o corpo do e-mail
def format_email_content(olhar_digital, cnn):
    content = "<html><body>"

    content += "<h3>--- OLHAR DIGITAL ---</h3>"
    for news in olhar_digital:
        content += f"<p><strong>Notícia:</strong> {news['title']}<br><strong>Link:</strong> <a href='{news['link']}'>{news['link']}</a></p>"

    content += "<p>.....</p>"

    content += "<h3>--- CNN BRASIL ---</h3>"
    for news in cnn:
        content += f"<p><strong>Notícia:</strong> {news['title']}<br><strong>Link:</strong> <a href='{news['link']}'>{news['link']}</a></p>"

    content += "</body></html>"

    return content


# Função para enviar o e-mail com as notícias
def send_email(subject, body, sender_email, receiver_email, smtp_server, smtp_port, password):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Corpo do e-mail em HTML
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        print("Email enviado com sucesso!")


# Obter as notícias
olhar_digital_news = get_olhar_digital_news()
cnn_news = get_cnn_news()

# Formatar o conteúdo do email
email_content = format_email_content(olhar_digital_news, cnn_news)

# Configurações para envio do e-mail
sender_email = "EMAIL_PARA_ENVIO"
receiver_email = "EMAIL_PARA_RECEBIMENTO"
smtp_server = "smtp.gmail.com"
smtp_port = 465
password = "SENHA_EMAIL_PARA_ENVIO"

# Enviar o email
send_email("Resumo de Notícias - Olhar Digital e CNN Brasil", email_content, sender_email, receiver_email, smtp_server, smtp_port, password)
