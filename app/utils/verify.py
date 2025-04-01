from app.schemas.email import VerifyEmail
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.config.verify import verification_email_conf, pwd_context


def generate_verification_email(user, token):
    verification_email = VerifyEmail(
        recipients=[user.email],
        subject="Habit Tracker Account Verification",
        body=f"""
        <body>
            <h1>Habit Tracker Account Verification</h1>
            <p>Hi {user.username}.</p>
            <p>Thanks for creating an account. Click the link below to verify.</p>
            <hr/>
            <a href="https://localhost:8000/api/verify?token={token.verify_token}">Verify</a>
        </body>
        """,
    )
    return verification_email


def send_verification_email(email, background_tasks):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.recipients,
        body=email.body,
        subtype=MessageType.html,
    )

    fm = FastMail(verification_email_conf)

    background_tasks.add_task(fm.send_message, message)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password):
    return pwd_context.hash(password)
