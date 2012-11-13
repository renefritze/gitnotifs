import smtplib
from email.mime.text import MIMEText

def notify(header, body, cfg):
    if cfg['mail.ssl']:
        smtp = smtplib.SMTP_SSL
    else:
        smtp = smtplib.SMTP
    conn = smtp(host=cfg['mail.server'], port=cfg['mail.port'])
    conn.set_debuglevel(1)
    conn.login(cfg['mail.login'], cfg['mail.pw'])
    recipients = cfg['mail.recipients'].split()
    
    msg = MIMEText(body)
    msg['Subject'] = header
    msg['From'] = cfg['mail.sender']
    msg['To'] = ', '.join(recipients) 

    conn.sendmail(cfg['mail.sender'], recipients, msg.as_string())
    conn.quit()
    