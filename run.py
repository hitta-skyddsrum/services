from HittaSkyddsrum import app
import os

# We only need this for local development.
if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', False))