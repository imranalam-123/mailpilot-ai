import smtplib

EMAIL = "imran.bkhpr@gmail.com"
APP_PASSWORD = "cgbc ttdl tpsg osmr"

try:
    print("Connecting...")

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587,
        timeout=30
    )

    server.starttls()

    print("Logging in...")

    server.login(
        EMAIL,
        APP_PASSWORD
    )

    print("LOGIN SUCCESS!")

    server.quit()

except Exception as e:
    print("ERROR:", e)