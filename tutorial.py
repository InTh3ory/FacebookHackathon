import web


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

        return x['myfile'].filename



render = web.template.render('templates/')

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


