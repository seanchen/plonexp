# webutil.py

import urllib
from sgmllib import SGMLParser
import datetime

from gdata import service
import gdata
import atom


# customize the SGMLParser to extract the content from a url.
class WebExtractor(SGMLParser):

    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
        # each movie's title.
        self.movieTitle = ''
        # each movie's show time.
        self.movieTime = []
        # all movies dict, title:showtime
        self.movies = {}
        self.isMovieDesc = False
        self.isMovieTitle = False

    def start_a(self, attributes):
        for name, value in attributes:
            if name == 'href':
                self.hyperlinks.append(value)

    def start_li(self, attributes):
        for name, value in attributes:
            if name == 'class' and value == 'col14':
                self.isMovieDesc = True

    # for any span tag
    def start_span(self, attributes):
        for name, value in attributes:
            if name == 'id' and value == 'large_bold_text':
                self.isMovieTitle = True

    # the end of any span tag
    def end_span(self):
        self.isMovieTitle = False

    # for each select tag
    def start_select(self, attributes):
        # do nothing for now.
        for name, value in attributes:
            if name == 'name' and value == 'selectedStartDate':
                inSelectElement = True

    # for each option tag
    def start_option(self, attributes):
        # we need the value a the move show time.
        for name, value in attributes:
            if name == 'value':
                # save the time.
                self.movieTime.append(value)

    # the end of each select tag
    def end_select(self):
        self.movies[self.movieTitle] = self.movieTime
        self.movieTime = []
        self.movieTitle = ''

    def handle_data(self, data):

        if self.isMovieTitle:
            self.movieTitle = self.movieTitle + data

    def get_hyperlinks(self):
        return self.hyperlinks

    def getMovies(self):
        return self.movies



DISH_PPV_URL = 'https://customersupport.dishnetwork.com/customercare/payperview/prepFutureMovieList.do'

# feed the url to the web extractor.
class MoviesCalendar:

    # extract movies title and show time from the url.
    def extractMovies(self):

        page = urllib.urlopen(DISH_PPV_URL).read()
        extractor = WebExtractor()

        extractor.parse(page)

        # movies showtime:title
        movies = {}
        for movieTitle, showTimes in extractor.getMovies().items():
            # for each show time.
            for showTime in showTimes:
                # TODO: need change to datetime.
                if not movies.has_key(showTime):
                    movies[showTime] = []
                movies[showTime].append(movieTitle)

        return movies

    # build the html calendar
    def buildCalendar(self):

        movies = self.extractMovies()

        showTimes = []
        showTimePattern = '%s %02d, %d'
        today = datetime.datetime.date(datetime.datetime.now())

        i = 0
        while i < 3:
            theDate = today + datetime.timedelta(1 + i)
            showTimes.append(theDate)
            i = i + 1

        # The table
        table = "<table><tbody>"
        for showTime in showTimes:
            theShowTime = showTimePattern % (self.getMonthName(showTime.month), showTime.day, showTime.year)

            movieTitles = movies[theShowTime]
            movieTitles.sort()
            table = table + '<tr><td style="background: #6699cc"><strong>%s, %s</strong></th></tr>' % (self.getWeekday(showTime.weekday()), theShowTime)
            n = 1
            for movieTitle in movieTitles:
                if (n % 2) == 1:
                    table = table + '<tr><td>'
                else:
                    table = table + '<tr><td style="background: #d8d8d8">'
                table = table + "<strong><i><a href='#' onclick='document.forms[0].q.value=\"movie \" + innerHTML; document.forms[0].submit();'>%s</a></i></strong>" % movieTitle
                table = table + '</td></tr>'
                n = n + 1

        table = table + '</tbody></table>'

        title = "%s's DISH Pay Per View Movies" % (today + datetime.timedelta(1))

        self.createPost(title, table, 'OPEN KEYS', False)

        return table

    # return the full name for the given month
    def getMonthName(self, monthNumber):
        """ monthNumber starts from 1."""
        if monthNumber == 1:
            return 'January'
        elif monthNumber == 2:
            return 'February'
        elif monthNumber == 3:
            return 'March'
        elif monthNumber == 4:
            return 'April'
        elif monthNumber == 5:
            return 'May'
        elif monthNumber == 6:
            return 'June'
        elif monthNumber == 7:
            return 'July'
        elif monthNumber == 8:
            return 'Augest'
        elif monthNumber == 9:
            return 'September'
        elif monthNumber == 10:
            return 'October'
        elif monthNumber == 11:
            return 'November'
        elif monthNumber == 12:
            return 'December'

    # return the weekday's name
    def getWeekday(self, day):
        if day == 0:
            return 'Monday'
        elif day == 1:
            return 'Tuesday'
        elif day == 2:
            return 'Wednesday'
        elif day == 3:
            return 'Thursday'
        elif day == 4:
            return 'Friday'
        elif day == 5:
            return 'Saturday'
        elif day == 6:
            return 'Sunday'

    # create blogspot post.
    def createPost(self, title, content, author_name, is_draft):
        
        """This method creates a new post on a blog.  The new post can be stored as
        a draft or published based on the value of the is_draft parameter.  The
        method creates an GDataEntry for the new post using the title, content,
        author_name and is_draft parameters.  With is_draft, True saves the post as
        a draft, while False publishes the post.  Then it uses the given
        GDataService to insert the new post.  If the insertion is successful, the
        added post (GDataEntry) will be returned.
        """

        # Authenticate using ClientLogin.
        self.service = service.GDataService('user', 'password')
        self.service.source = 'Blogger_Python_Sample-1.0'
        self.service.service = 'blogger'
        self.service.server = 'www.blogger.com'
        self.service.ProgrammaticLogin()

        # Get the blog ID for the first blog.
        feed = self.service.Get('/feeds/default/blogs')
        self_link = feed.entry[0].GetSelfLink()
        if self_link:
            self.blog_id = self_link.href.split('/')[-1]

        # Create the entry to insert.
        entry = gdata.GDataEntry()
        entry.author.append(atom.Author(atom.Name(text=author_name)))
        entry.title = atom.Title(title_type='xhtml', text=title)
        entry.content = atom.Content(content_type='html', text=content)
        if is_draft:
          control = atom.Control()
          control.draft = atom.Draft(text='yes')
          entry.control = control
    
        # Ask the service to insert the new entry.
        return self.service.Post(entry, 
          '/feeds/' + self.blog_id + '/posts/default')

    def blogerLogin(self):

        self.service = service.GDataService('user', 'password')
        self.service.source = 'Blogger_Python_Sample-1.0'
        self.service.service = 'blogger'
        self.service.server = 'www.blogger.com'
        self.service.ProgrammaticLogin()

    def getOneBlog(self, id=0):

        # Get the blog ID for the first blog.
        feed = self.service.Get('/feeds/default/blogs')
        self_link = feed.entry[id].GetSelfLink()
        if self_link:
            self.blog_id = self_link.href.split('/')[-1]

    def updatePost(self, start_time, end_time, new_content):

        self.blogerLogin()
        self.getOneBlog(0)

        # find the update entry.
        query = service.Query()
        query.feed = '/feeds/' + self.blog_id + '/posts/default'
        query.updated_min = start_time
        query.updated_max = end_time
        feed = self.service.Get(query.ToUri())

        feed.content = atom.Content(content_type='html', text=new_content)
