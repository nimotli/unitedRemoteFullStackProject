from app import app,db
#from app.models import createDB
import app.router as router

#createDB()

if __name__=='__main__':
    app.run(debug=True)