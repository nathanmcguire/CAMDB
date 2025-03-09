from app import create_app

# Create the app instance using the factory method
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)