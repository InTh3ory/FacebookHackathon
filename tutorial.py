import web
import binascii
from PIL import Image
import cStringIO as StringIO
import copycat


urls = (
	'/','index',
    '/upload', 'upload',
	)

my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'), )

class index:
	def GET(self):
		form = my_form()
		return render.index(form, "Index")

class upload:
    def GET(self):
        form = my_form()
        return render.index(form, "")

    def POST(self):
        x = web.input(myfile={})
        filename = x['myfile'].filename

        filedir = 'C:\Dev\FacebookHackathon\static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        copycat.LoadImage(filename)

        return filename



render = web.template.render('templates/')

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


