"""
uTorrentConnection
"""

from base64 import b64encode
import http.client
import http.cookiejar
import json
import re
import socket
import urllib.request
import time
import errno
import email.generator
import urllib.parse
import torrentstatus.utorrent 
import torrentstatus.utorrent.uTorrent


class Connection( http.client.HTTPConnection ):
	_host = ""
	_login = ""
	_password = ""

	_request = None
	_cookies = http.cookiejar.CookieJar( )
	_token = ""

	_retry_max = 3

	_utorrent = None

	@property
	def request_obj( self ):
		return self._request

	def __init__( self, host, login, password ):
		self._host = host
		self._login = login
		self._password = password
		self._url = "http://{}/".format( self._host )
		self._request = urllib.request.Request( self._url )
		self._request.add_header( "Authorization",
		                          "Basic " + b64encode( "{}:{}".format( self._login, self._password ).encode( "latin1" ) ).decode( "ascii" ) )
		http.client.HTTPConnection.__init__( self, self._request.host, timeout = 10 )
		self._fetch_token( )


	def _make_request( self, loc, headers, data = None, retry = True ):
		last_e = None
		utserver_retry = False
		retries = 0
		max_retries = self._retry_max if retry else 1
		try:
			while retries < max_retries or utserver_retry:
				try:
					self._request.add_data( data )
					self.request( self._request.get_method( ), self._request.get_selector( ) + loc, self._request.get_data( ), headers )
					resp = self.getresponse( )
					if resp.status == 400:
						last_e = torrentstatus.utorrent.uTorrentError( resp.read( ).decode( "utf8" ).strip( ) )
						# if uTorrent server alpha is bound to the same port as WebUI then it will respond with "invalid request" to the first request in the connection
						# apparently this is no longer the case, TODO: remove this hack
						if ( not self._utorrent or type( self._utorrent ) == torrentstatus.utorrent.uTorrent.LinuxServer ) and not utserver_retry:
							utserver_retry = True
							continue
						raise last_e
					elif resp.status == 404 or resp.status == 401:
						raise torrentstatus.utorrent.uTorrentError( "Request {}: {}".format( loc, resp.reason ) )
					elif resp.status != 200 and resp.status != 206:
						raise torrentstatus.utorrent.uTorrentError( "{}: {}".format( resp.reason, resp.status ) )
					self._cookies.extract_cookies( resp, self._request )
					if len( self._cookies ) > 0:
						self._request.add_header( "Cookie",
						                          "; ".join( ["{}={}".format( torrentstatus.utorrent._url_quote( c.name ), torrentstatus.utorrent._url_quote( c.value ) ) for c in
						                                      self._cookies] ) )
					return resp
				# retry when utorrent returns bad data
				except ( http.client.CannotSendRequest, http.client.BadStatusLine ) as e:
					last_e = e
					self.close( )
				# name resolution failed
				except socket.gaierror as e:
					raise torrentstatus.utorrent.uTorrentError( e.strerror + ",loc:{0}, host:{1}".format(loc, self._host) )
				# socket errors
				except socket.error as e:
					# retry on timeout
					if str( e ) == "timed out": # some peculiar handling for timeout error
						last_e = torrentstatus.utorrent.uTorrentError( "Timeout after {} tries".format( max_retries ) )
						self.close( )
					# retry after pause on specific windows errors
					elif e.errno == 10053 or e.errno == 10054:
						# Windows specific socket errors:
						# 10053 - An established connection was aborted by the software in your host machine
						# 10054 - An existing connection was forcibly closed by the remote host
						last_e = e
						self.close( )
						time.sleep( 2 )
					elif e.errno == errno.ECONNREFUSED or e.errno == errno.ECONNRESET or errno == errno.EHOSTUNREACH:
						raise torrentstatus.utorrent.uTorrentError( e.strerror )
					else:
						raise e
				retries += 1
			if last_e:
				raise last_e
		except Exception as e:
			self.close( )
			raise e
		return None

	def _get_data( self, loc, data = None, retry = True, range_start = None, range_len = None, save_buffer = None, progress_cb = None ):
		headers = { k: v for k, v in self._request.header_items( ) }
		if data:
			bnd = email.generator._make_boundary( data )
			headers["Content-Type"] = "multipart/form-data; boundary={}".format( bnd )
			data = data.replace( "{{BOUNDARY}}", bnd )
		if range_start is not None:
			if range_len is None or range_len == 0:
				range_end = ""
			else:
				range_end = range_start + range_len - 1
			headers["Range"] = "bytes={}-{}".format( range_start, range_end )
		resp = self._make_request( loc, headers, data, retry )
		if save_buffer:
			read = 0
			resp_len = resp.length
			content_range = resp.getheader( "Content-Range" )
			if content_range is not None:
				m = re.match( "^bytes (\\d+)-\\d+/(\\d+)$", content_range )
				if m is not None:
					read = int( m.group( 1 ) ) - 1
					resp_len = int( m.group( 2 ) )
			while True:
				buf = resp.read( 10240 )
				read += len( buf )
				if progress_cb:
					progress_cb( read, resp_len )
				if len( buf ) == 0:
					break
				save_buffer.write( buf )
			self.close( )
			return None
		out = resp.read( ).decode( "utf8" )
		self.close( )
		return out

	def _fetch_token( self ):
		data = self._get_data( "gui/token.html" )
		match = re.search( "<div .*?id='token'.*?>(.+?)</div>", data )
		if match is None:
			raise torrentstatus.utorrent.uTorrentError( "Can't fetch security token" )
		self._token = match.group( 1 )

	def _action_val( self, val ):
		if isinstance( val, bool ):
			val = int( val )
		return str( val )

	def _action( self, action, params = None, params_str = None ):
		args = []
		if params:
			for k, v in params.items( ):
				if torrentstatus.utorrent.is_list_type( v ):
					for i in v:
						args.append( "{}={}".format( torrentstatus.utorrent._url_quote( str( k ) ), torrentstatus.utorrent._url_quote( self._action_val( i ) ) ) )
				else:
					args.append( "{}={}".format( torrentstatus.utorrent._url_quote( str( k ) ), torrentstatus.utorrent._url_quote( self._action_val( v ) ) ) )
		if params_str:
			params_str = "&" + params_str
		else:
			params_str = ""
		if action == "list":
			args.insert( 0, "token=" + self._token )
			args.insert( 1, "list=1" )
			section = "gui/"
		elif action == "proxy":
			section = "proxy"
		else:
			args.insert( 0, "token=" + self._token )
			args.insert( 1, "action=" + torrentstatus.utorrent._url_quote( str( action ) ) )
			section = "gui/"
		return section + "?" + "&".join( args ) + params_str

	def do_action( self, action, params = None, params_str = None, data = None, retry = True, range_start = None, range_len = None, save_buffer = None,
	               progress_cb = None ):
		# uTorrent can send incorrect overlapping array objects, this will fix them, converting them to list
		def obj_hook( obj ):
			out = { }
			for k, v in obj:
				if k in out:
					out[k].extend( v )
				else:
					out[k] = v
			return out

		res = self._get_data(
			self._action( action, params, params_str ),
			data = data,
			retry = retry,
			range_start = range_start,
			range_len = range_len,
			save_buffer = save_buffer,
			progress_cb = progress_cb
		)
		if res:
			return json.loads( res, object_pairs_hook = obj_hook )
		else:
			return ""

	def utorrent( self, api = None ):
		if api == "linux":
			return torrentstatus.utorrent.uTorrent.LinuxServer( self )
		elif api == "desktop":
			return torrentstatus.utorrent.uTorrent.Desktop( self )
		elif api == "falcon":
			return torrentstatus.utorrent.uTorrent.Falcon( self )
		else: # auto-detect
			try:
				ver = torrentstatus.utorrent.uTorrent.Version( self.do_action( "getversion", retry = False ) )
			except torrentstatus.utorrent.uTorrentError as e:
				if e.args[0] == "invalid request": # windows desktop uTorrent client
					ver = utorrent.uTorrent.Version.detect_from_settings( self.do_action( "getsettings" ) )
				else:
					raise e
			if ver.product == "server":
				return torrentstatus.utorrent.uTorrent.LinuxServer( self, ver )
			elif ver.product == "desktop":
				if ver.major == 3:
					return torrentstatus.utorrent.uTorrent.Falcon( self, ver )
				else:
					return torrentstatus.utorrent.uTorrent.Desktop( self, ver )
			else:
				#raise torrentstatus.utorrent.uTorrentError( "Unsupported WebUI API" )
				return torrentstatus.utorrent.uTorrent.Falcon( self, ver )
