import resend
from config import get_config


config = get_config()

resend.api_key = config.RESEND_API_KEY

def send_email_to_user(name, email, message):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Playfair+Display:wght@600&display=swap');
      </style>
    </head>
    <body style="background-color: #F5F1E8; margin: 0; padding: 40px 20px; font-family: 'Open Sans', Arial, sans-serif; color: #1A1A1A;">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #FDFAF4; border: 1px solid #DDD0BB; border-radius: 8px; overflow: hidden;">
        <tr>
          <td style="background-color: #3E2F23; padding: 30px; text-align: center;">
            <h1 style="color: #C2A15A; margin: 0; font-family: 'Playfair Display', Georgia, serif; font-size: 28px; font-weight: 600;">
              El Baúl Viejo
            </h1>
          </td>
        </tr>
        <tr>
          <td style="padding: 40px 30px;">
            <h2 style="color: #5C4535; margin-top: 0; font-family: 'Playfair Display', Georgia, serif; font-size: 22px;">Nueva Consulta</h2>
            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 25px;">
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #DDD0BB;"><strong style="color: #8C6A3B;">Nombre:</strong> {name}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #DDD0BB;"><strong style="color: #8C6A3B;">Correo:</strong> <a href="mailto:{email}" style="color: #1A1A1A; text-decoration: none;">{email}</a></td>
              </tr>
            </table>
            <div style="background-color: #F5F1E8; border-left: 4px solid #C2A15A; padding: 20px; border-radius: 0 4px 4px 0;">
              <h3 style="margin-top: 0; color: #3E2F23; font-size: 16px; margin-bottom: 10px; font-family: 'Open Sans', Arial, sans-serif;">Mensaje:</h3>
              <p style="margin: 0; line-height: 1.6; color: #1A1A1A; white-space: pre-wrap; font-family: 'Open Sans', Arial, sans-serif;">{message}</p>
            </div>
          </td>
        </tr>
        <tr>
          <td style="background-color: #EDE7D9; padding: 20px; text-align: center; font-size: 12px; color: #7A6A5A; font-family: 'Open Sans', Arial, sans-serif;">Este es un mensaje automático generado desde el formulario de contacto de El Baúl Viejo.</td>
        </tr>
      </table>
    </body>
    </html>
    """

    params = {
        "from": f"Notificaciones {config.SENDER_EMAIL}",
        "to": config.RECEIVER_EMAIL,
        "reply_to": [email],
        "subject": f"El Baúl Viejo - Mensaje de {name}",
        "html": html_content
    }

    return resend.Emails.send(params)
