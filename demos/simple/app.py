import tornadoredis
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.gen
import logging


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('app')

CLIENT = tornadoredis.Client()


class MainHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        #c = tornadoredis.Client()
        #foo = yield tornado.gen.Task(c.get,'foo')
        foo = yield CLIENT.execute_command('GET', "foo")
        print foo
        if not foo:
            foo = "1"
        self.write(foo)
        self.flush()


application = tornado.web.Application([
    (r'/', MainHandler),
])


@tornado.gen.coroutine
def create_test_data():
    c = tornadoredis.Client()
    with c.pipeline() as pipe:
        pipe.set('foo', 'Lorem ipsum #1', 12 * 60 * 60)
        pipe.set('bar', 'Lorem ipsum #2', 12 * 60 * 60)
        pipe.set('zar', 'Lorem ipsum #3', 12 * 60 * 60)
        yield pipe.execute()
    print 'Test data initialization completed.'


if __name__ == '__main__':
    # Start the data initialization routine
    #create_test_data()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print 'Demo is runing at 0.0.0.0:8888\nQuit the demo with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
