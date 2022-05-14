from web import create_app # can import function from web folder since it is in python __init__.py file

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=443) # debug on for test env