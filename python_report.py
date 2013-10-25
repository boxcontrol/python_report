#!/usr/local/bin/python
import commands
import smtplib, os, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


logfile = open('/pyth/to/message.txt', 'w')
logfile.truncate()
#logfile.close()


comm_list = ['uptime', 'vnstat -d', 'free -m', 'df -h', "cat /var/log/auth.log | grep 'sshd.*Invalid'", "cat /var/log/auth.log | grep 'sshd.*opened'"]
for i in comm_list:
    stat, out = commands.getstatusoutput(i)
    if not stat:
        logfile.write(out)

logfile.close()

#send email
def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

send_mail('root@example.com', ['personal@mail.com'], 'Daily Server Report', 'Your Daily Server Report:', ['/path/to/message.txt'])
