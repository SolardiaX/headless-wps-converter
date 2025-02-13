from pywpsrpc.rpcwppapi import createWppRpcInstance, wppapi
from pywpsrpc.common import S_OK

from .common import ConvertException


g_rpc = None
g_app = None


def convert(src: str, dest: str):
    global g_rpc, g_app

    if g_rpc is None:
        hr, rpc = createWppRpcInstance()
        if hr != S_OK:
            raise ConvertException("Can't create the rpc instance", hr)
        
        g_rpc = rpc
    
    if g_app is None:
        hr, app = rpc.getWppApplication()
        if hr != S_OK:
            raise ConvertException("Can't get the application", hr)
        
        g_app = app
    
    # we don't need the gui
    # app.Visible = False

    docs = g_app.Presentations

    hr, doc = docs.Open(src, ReadOnly=True)
    if hr != S_OK:
        raise ConvertException("Can't open the source presentation", hr)

    hr = doc.ExportAsFixedFormat(dest, wppapi.PpFixedFormatType.ppFixedFormatTypePDF)

    # always close the doc
    doc.Close()
    del doc

    if hr != S_OK:
        raise ConvertException("Can't export presentation to pdf", hr)
