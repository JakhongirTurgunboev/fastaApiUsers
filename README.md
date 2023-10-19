FastAPI Crud project

1. Clone the repository to your local machine
2. Open Docker desktop
3. Inside terminal, run `docker-compose up -d --build`
4. Open http://localhost/docs
5. For testing run `docker-compose run fastapi pytest`

Configuration:
1.Data validation for email and password fields added.
2.Valid email address should be inserted.
3.Password must be at least 8 characters long including at least one upper 
    case, one lower case letters and special character
