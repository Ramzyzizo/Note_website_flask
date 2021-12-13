from website import create_app

app = create_app()

if __name__=='__main__': #to sure it run from main file
    app.run(debug=True) #to if i change in python code will affect 