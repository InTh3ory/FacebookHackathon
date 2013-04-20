import web


urls = (
	'/(.*)','index',
    '/upload', 'Upload'
	)

my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'), )

class index:
	def GET(self, name):
		form = my_form()
		return render.index(form, "Index")

class Upload:
    def GET(self):
        form = my_form()
        return render.upload(form, "Hacha")

    def POST(self, test):
        form = my_form()
        form.validates()
        s = form.value['textfield']
        return make_text(s)



render = web.template.render('templates/')

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


