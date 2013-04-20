import web
import binascii
from PIL import Image
import cStringIO as StringIO
import copycat
import os


urls = (
	'/','index',
    '/upload', 'upload',
    '/detect', 'detect',
    '/cats', 'cats',
    '/blur', 'blur',
    '/sharpen', 'sharpen',
    '/sepia', 'sepia',
	)

my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'), )

class index:
	def GET(self):
		form = my_form()
		return render.index(form, "Index")

class blur:
    def GET(self):
        form = my_form()
        return render.index(form, "Index")

    def POST(self):
        user_input = web.input();   
        filename = user_input.filename

        copycat.GaussFilter(filename)

        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        print name + "_blur_" + extension
        return name + "_blur_" + extension 

class sharp:
    def GET(self):
        form = my_form()
        return render.index(form, "Index")

    def POST(self):
        user_input = web.input();   
        filename = user_input.filename

        copycat.SharpFilter(filename)

        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        print name + "_sharp_" + extension
        return name + "_sharp_" + extension 

class emboss:
    def GET(self):
        form = my_form()
        return render.index(form, "Index")

    def POST(self):
        user_input = web.input();   
        filename = user_input.filename

        copycat.EmbossFilter(filename)

        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        print name + "_emboss_" + extension
        return name + "_emboss_" + extension

class cats:
    def GET(self):
        form = my_form()
        return render.index(form, "Index")

    def POST(self):
        print "Cats - Post"

        user_input = web.input();   
        filename = user_input.filename

        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        print name + "_cats_" + extension
        return name + "_cats_" + extension 

class detect:
    def GET(self):
        form = my_form()
        return render.index(form, "Index")

    def POST(self):
        print "Detect - Post"
        
        user_input = web.input();   
        filename = user_input.filename

        copycat.LoadImage(filename)

        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        print name + "_faces_" + extension
        return name + "_faces_" + extension 


class upload:
    def GET(self):
        form = my_form()
        return render.index(form, "")

    def POST(self):
        print "Entering Post"
        x = web.input(myfile={})
        filename = x['myfile'].filename

        currentDir = os.getcwd() + "/static/"
        filedir = currentDir # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        return filename



render = web.template.render('templates/')

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()




