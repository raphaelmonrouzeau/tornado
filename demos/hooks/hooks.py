#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Raphaël Monrouzeau
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.request.finished_at = datetime.datetime.utcnow()

    def get(self):
        self.write(
         """<html>
          <head/>
          <body>
           <h3>Request body upload took """
           +str(self.request.finished_at-self.request.started_at)+
           """ to process</h3>
           <form method='post'>
            <input type='text' name='a'>
            <input type='submit'>
           </form>
          </body>
         </html>""")
    
    def post(self):
        self.write(
         """<html>
          <head/>
          <body>
           <h3>Request body upload took """
           +str(self.request.finished_at-self.request.started_at)+
           """ to process</h3>
           <p>That time was to upload:</p>
           <pre>"""+self.get_argument("a")+"""</pre>
         </html>""")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    def on_connect(request):
        request.started_at = datetime.datetime.utcnow()
    http_server.on("connect", on_connect)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
