# User_Authentication-Django

Project Overview
This project implements a simple user authentication system in Django, where users can register, log in, reset their passwords. A key feature is email verification during the signup process to enhance security. The system ensures that only verified users can access their accounts, providing a secure and reliable authentication flow.

Key Features:
User Registration: Users can sign up by providing their email, username, and password. Upon registering, a verification link is sent to their email for account activation.
Email Verification: After registration, the system sends a verification link to the user's email. The user must verify the email address to activate the account.
Login: Users can log in using their email and password, but only after verifying their email.
Password Reset: Users can request to reset their password, which will trigger a password reset link sent to their registered email.
Secure Authentication: The system incorporates best practices in password management, such as hashed passwords and validation checks.
MailGun: Used mailgun sandbox api to send email for verification.

