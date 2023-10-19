FastAPI Crud project

1. Clone the repository to your local machine
2. Open Docker desktop
3. Inside terminal, run `docker-compose up -d --build`
4. Open http://localhost/docs
5. For testing run `docker-compose run test`

Configuration:
Data validation for email and password fields added:
    1.Email address must be valid.
    2.Password must be at least 8 characters long including at least one upper 
        case, one lower case letters and special character.
