import urllib2
import re
import zlib
import cv2
import random
from scapy.all import *


n = 1
def get_headers(ret):
    try:
        header_raw = ret[:ret.index("\r\n\r\n")+2]
        headers = dict(re.findall(r"(?P<name>.*?):(?P<value>.*?)\r\n",header_raw))
        #print headers
    except:
        return None
    
    if "Content-Type" not in headers:
        return None
        
    return headers
    

    
    

def packet_handler(packet):
    global n
    n = n + 1
    try:
        if packet[TCP].payload:
            ret = str(packet[TCP].payload)
            if "HTTP" in ret: 
                #print "---"
                headers = get_headers(ret)
                #print headers
                if "image" in headers["Content-Type"]:
                    image = ret[ret.index("\r\n\r\n")+4:]
                    #print image
                    try:
                        if "Content-Encoding" in headers.keys():
                            if headers["Content-Encoding"] == "gzip":    
                                image = zlib.decompress(image,16+zlib.MAX_WBITS)
                                
                                
                            if headers["Content-Encoding"] == "deflate":
                                
                                image = zlib.decompress(image)

                        print "decompressed"
                        if image is not None and image is not None:
                            tail = headers["Content-Type"].split("/")[1]
                            if tail == "jpeg":
                                tail = "jpg"
                            file_name = "asdf%d.%s" % (n,tail)
                            print file_name
                            
                        try :
                            fd = open(file_name,"wb")
                            fd.write(image)
                            fd.close()
                        except:
                            print "fail to write"
                            
                    except:
                        pass
                    
                    
                    
                    
    except:
        pass
    
sniff(prn=packet_handler)