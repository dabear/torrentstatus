import TheSubDB
import BierDopje
import logging
import SubScene
import Addic7ed
logging.basicConfig(level=logging.DEBUG)

filename = "H:/Series/continuum/continuum.s01e05.repack.720p.hdtv.x264-2hd.mkv"


#source = TheSubDB.TheSubDB
source = Addic7ed.Addic7ed
#source = SubScene.SubScene

p = source(None, None)

logging.info("Processing %s" % filename)
subs = p.process(filename, ["no", "en"])

print "subs: ", subs
if subs:
    for sub in subs:
        sub["filename"] = filename
        p.createFile(sub)
        raw_input("press any key to try the next..")

#if not subs:
 #   p.uploadFile(filename, subfname, 'en')
 #   subs = p.process(filename, ["en", "pt"])
 #   print subs


#bd = BierDopje.BierDopje()
#subs = bd.process(filename, ["en"])



