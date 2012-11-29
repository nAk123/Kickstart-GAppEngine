import webapp2
import cgi

form = """
	<form method="post">
		What is your birthday?
		<br>

		<label>
			Month
			<input type="text" name="month" value="%(month)s">
		</label>

		<label>
			Day
			<input type="text" name="day" value="%(day)s">
		</label>

		<label>
			Year
			<input type="text" name="year" value="%(year)s">
		</label>
		
		<div style="color:red">%(error)s</div>

		<br>
		<br>
		<input type="submit">
	</form>
"""


months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_day(day):
    if day and day.isdigit():
        day=int(day)
        if day>0 and day<=31:
            return day
        
month_ipl = dict((m[:3].lower(),m) for m in months)
  
def valid_month(month):
    short_m = month[:3].lower()
    return month_ipl.get(short_m)
   
def valid_year(year):
    if year and year.isdigit():
        year=int(year)
        if year>1900 and year<2020:
            return year

#def escape_html(s):
#    for(i,j) in (("&","&amp;"),
#                 (">","&gt;"),
#                 ("<","&lt;"),
#                 ("\"","&quot;")):
#        s=s.replace(i,j)
#    return s

def escape_html(s):
    return cgi.escape(s,quote=True)

class MainHandler(webapp2.RequestHandler):

  def write_form(self,error="",month="",year="",day=""):
    self.response.out.write(form%{"error":error,
				  "month":escape_html(month),
				  "year":escape_html(year),
				  "day":escape_html(day)})

  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    self.write_form()

  def post(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    user_month = self.request.get('month')
    user_year = self.request.get('year')
    user_day = self.request.get('day')

    month = valid_month(user_month)
    year = valid_year(user_year)
    day = valid_day(user_day)

    if(month and year and day):
	self.redirect("/thanks")
    else:
	self.write_form("That doesn't look valid to me, my friend",
			user_month,user_year,user_day)

class ThanksHandler(webapp2.RequestHandler):

  def get(self):
    #self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("Thanks. That's a totally valid date")

app = webapp2.WSGIApplication([('/', MainHandler),('/thanks', ThanksHandler)], debug=True)
