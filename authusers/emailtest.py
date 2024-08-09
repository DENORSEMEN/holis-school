import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('venvictor602@gmail.com', 'lcuo mbfz plok lavf')
    print("Connected to SMTP server successfully!")
    server.quit()
except Exception as e:
    print(f"Failed to connect: {e}")