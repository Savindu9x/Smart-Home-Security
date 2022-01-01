from Website import create_app

# Calling function in __init__ py
app = create_app()


# debug mode is ON, for production turn OFF
if __name__ == '__main__':
    app.run(debug=True)
    

