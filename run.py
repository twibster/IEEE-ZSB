from website import app

def getApp():
    return app

if __name__ == '__main__':
    app.run(debug=True)