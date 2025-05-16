"""standard freeze script"""

from flask_frozen import Freezer
from Hunt4TheMurderer import create_app
from flask_login import login_user
from Hunt4TheMurderer.models import User

app = create_app()[0]
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
app.config['FREEZER_IGNORE_500_ERRORS'] = True
app.config['FREEZER_IGNORE_REDIRECTS'] = True

# Configure the freezer
freezer = Freezer(app)

# Define which URLs to freeze
@freezer.register_generator
def public_urls():
    # Add your public routes here
    yield '/'
    yield '/about'
    yield '/contact'
    yield '/login'
    yield '/register'
    # Add any other public routes that don't require authentication

if __name__ == '__main__':
    # Create a test context to handle authentication
    with app.test_request_context():
        # Freeze the site
        freezer.freeze()