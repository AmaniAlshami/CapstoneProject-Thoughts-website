# Flask App config
export FLASK_APP=app
export FLASK_ENV=development

# Auth0
export AUTH0_DOMAIN='dev-gctheugr.us.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='ThoughtsApp'

#Database

export DB_HOST = os.getenv('DB_HOST','localhost:5432')  
export DB_USER = os.getenv('DB_USER', '')  
export DB_PASSWORD = os.getenv('DB_PASSWORD', '')  
export DB_NAME = os.getenv('DB_NAME', 'thoughts')  
export DB_PATH = 'postgres://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
