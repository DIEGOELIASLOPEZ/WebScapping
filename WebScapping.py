from bs4 import BeautifulSoup
import requests
from urllib.parse import quote


def obtener_precio():
    url = requests.get(
        "https://www.amazon.com.mx/Hbada-P5-P501BMA/dp/B0BWDQX8RH/ref=sr_1_22_sspa?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=G705EH7XD8G0&dib=eyJ2IjoiMSJ9.Y1B58p6R5SrxAWh5XG27txT6yZIKfEhUx8aowau7EBM9iSpvDrv61QV_M4knhd3Q-IumhCWTGKUD3bjR-5U4b9wWeQznVAK82V1xVzjc68zCIMYCZrQG9TthCgx88-nrZAuE7cLbcUNjCU6heOPeB5GAIXCEqScuC7jZbwJBXbmakchZkbLvmIL-naQcyrJb4WOQ1y9Smwzli6DquKz6fn9IX9T1bszgzQiVEs3PoZc-2AcbvaAT6TGogE8BGf5Q-jYixERRJSSF9006jpCk75OcquXnUgvF4_sPFKvymjE.lQSYQF2LgBUnpoNQgjeZL3DlDY7icqbL-olvXw_EoME&dib_tag=se&keywords=silla%2Bde%2Boficina&qid=1724039782&sprefix=silla%2Bde%2Boficin%2Caps%2C152&sr=8-22-spons&ufe=app_do%3Aamzn1.fos.12c28adc-ede4-4180-8d9e-3d9cc50fec69&sp_csd=d2lkZ2V0TmFtZT1zcF9tdGY&th=1")

    soup = BeautifulSoup(url.content, "html.parser")
    entero = soup.find("span", {"class": "a-price-whole"})
    centavos = soup.find("span", {"class": "a-price-fraction"})

    # Limpieza de partes del precio
    precioInicio_text = entero.text.strip().replace(",", "").replace(".", "")
    precioCentavos_text = centavos.text.strip()

    # Combinar partes del precio
    precio_texto_completo = f"{precioInicio_text}.{precioCentavos_text}"

    # Convertir a flotante
    precioInicial = float(precio_texto_completo)

    return precioInicial


def enviar_mensaje_telegram(bot_message):
    bot_token = '7227192469:AAGlC7iPqe-FStQJyVTX6qS0fpXDK58qpvw'
    bot_chatID = '7133851943'
    bot_message = quote(bot_message)  # Codifica el mensaje para la URL

    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&text={bot_message}'

    response = requests.get(send_text)

    # Imprimir la respuesta para depurar
    print("Respuesta del servidor de Telegram:", response.json())

    return response.json()


def main():
    precioInicial = obtener_precio()
    precioDeseado = 5000

    if precioInicial is not None:
        if precioInicial <= precioDeseado:
            mensaje = (f"Existe una oferta disponible de la silla que deseas\nEl precio está en: ${precioInicial:.2f}\n"
                       f"Enlace: https://www.amazon.com.mx/Hbada-P5-P501BMA/dp/B0BWDQX8RH")
            enviar_mensaje_telegram(mensaje)
        else:
            enviar_mensaje_telegram("No hay oferta")
    else:
        enviar_mensaje_telegram("No se pudo obtener el precio del producto.")


if __name__ == '__main__':
    main()
