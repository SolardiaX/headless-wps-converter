from pywpsrpc.rpcwpsapi import createWpsRpcInstance, wpsapi
from pywpsrpc.common import S_OK

from .common import ConvertException


g_rpc = None
g_app = None


def convert(src: str, dest: str):
    global g_rpc, g_app

    if g_rpc is None:
        hr, rpc = createWpsRpcInstance()
        if hr != S_OK:
            raise ConvertException("Can't create the document rpc instance", hr)
        
        g_rpc = rpc

    if g_app is None:
        hr, app = rpc.getWpsApplication()
        if hr != S_OK:
            raise ConvertException("Can't get the application", hr)
        
        g_app = app
        # we don't need the gui
        g_app.Visible = False
    
    docs = g_app.Documents

    hr, doc = docs.Open(src, ReadOnly=True)
    if hr != S_OK:
        raise ConvertException("Can't open the source document", hr)

    hr = doc.ExportAsFixedFormat(dest, wpsapi.WdExportFormat.wdExportFormatPDF)

    # always close the doc
    doc.Close(wpsapi.wdDoNotSaveChanges)
    del doc

    if hr != S_OK:
        raise ConvertException("Can't export document to pdf", hr)

    
