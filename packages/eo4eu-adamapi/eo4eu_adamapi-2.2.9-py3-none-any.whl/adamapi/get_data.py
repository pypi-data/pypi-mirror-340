"""
Copyright (c) 2023 MEEO s.r.l.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



import os
import time
import json
import errno
import requests
from datetime import datetime
import re
import logging
logger=logging.getLogger('adamapi')

from . import AdamApiError,AdamApiMessage


def _format_error(response) -> str:
    error_message = f"HTTP status code: {response.status_code}"
    try:
       return f"{error_message} {response.json()}"
    except Exception:
       return f"{error_message} (failed to decode message json)"


def _format_message(response) -> str:
    try:
       return response.json()
    except Exception:
        return {"status": response.status_code, "error": "bad HTTP status code"}


class GetData(object):
    def __init__(self,client):
        self.LOG=logger
        self.client=client

    def getData(self,datasetId,request,asynchronous=False,compress=False,rest=True,filters={},options={},**kwargs):
        """
        Method to retrive:
        1) data in native format and native temporal resolution
        2) a subset of data in native format and native temporal resolution
        3) a timeseries of data in native format and native temporal resolution
        4) a processing on a specific datasetId
        @ datasetId, the datase identifier as resource_id:dataseId or the dataset oid (_id["$oid"])
        @asynchronous required (default False)
        @startDate required
        @endDate required
        @schema optional ( required only for subset,timeseries and processing )
        @geometry optional ( if schema is set, geometry param skipped in favor of the geometry param inside the schema if set )
        @outputDir optional ( set a different download directory inside adamapiresult main directory
        """
        #version 2.1-dev
        #step 1 check params
        #step 2 manage synchronously and asynchronously different temporal resolution datasets in the same way
        #asynchronous management

        resource_id = datasetId.split(":")[0]

        if "outputDir" in kwargs:
            output_dir = os.path.join("adamapiresult",kwargs["outputDir"])
        else:
            output_dir = "adamapiresult/"
        self._checkDir(output_dir)
        params,fname=self.checkParams( request,asynchronous, compress,rest,filters,options,kwargs)
        startIndex=0
        maxRecords=10
        if asynchronous == True and "id" in params:
            #get the order status
            url=os.path.join( "apis", "v2", "orders", resource_id, str(params["id"]) )
            response_order_status=self.client.client(url,params,"GET",force_raise=True,enable_stream=False)
            if response_order_status.status_code == 200:
                return AdamApiMessage(response_order_status.json())
            else:
                raise AdamApiError(response_order_status.json())

        #request management - the order submit url
        url=os.path.join( "apis", "v2", "orders", resource_id )
        #POST the order requests
        response_order_submit = self.client.client(url,params,"POST",force_raise=False,enable_stream=False)
        if response_order_submit.status_code==200:
            if asynchronous == False:
                #get the order status
                url=os.path.join( "apis", "v2", "orders", resource_id, str(response_order_submit.json()["id"]) )
                response_order_status=self.client.client(url,{},"GET",force_raise=True,enable_stream=False)
                if response_order_status.status_code == 200:
                    while response_order_status.json()["status"] != "completed" and "tasks" not in response_order_status.json():
                        time.sleep(1)
                        response_order_status=self.client.client(url,params,"GET",force_raise=True,enable_stream=False)
                    for elem in response_order_status.json()["tasks"]:
                        url=elem[ "download"]["url"]
                        print(f"Downloading {url}")
                        response_download=self.client.client(url,{},"GET",force_raise=False,enable_stream=False)
                        if response_download.status_code != 200:
                            print(AdamApiMessage(_format_message(response_download)))
                        else:
                            outname=re.findall('filename="(.+)"', response_download.headers['content-disposition'])[0]
                            with open(os.path.join(output_dir,outname), 'wb' ) as f:
                                f.write( response_download.content )
                return AdamApiMessage(_format_message(response_order_status))
            else:
                return AdamApiMessage(_format_message(response_order_submit))
        else:
            raise AdamApiError(_format_error(response_order_submit))


    def checkParams(self, request,asynchronous, compress,rest,filters,options,kwargs):
        params={}
        fname=None
        op_kwargs = kwargs.copy()
        #manage outDir
        if "outputDir" in op_kwargs:
            del(op_kwargs["outputDir"])
        #manage filters
        params["filters"] = {}
        filt = {}
        for(key,value)in filters.items():
            if key == "geometry":
                if isinstance(value,str):
                    filt[key]=value
                else:
                    filt[key]=json.dumps(value)
            else:
                filt[key]=value
        #manage options
        opt = {}
        for(key,value)in options.items():
            opt[key]=value

        for (key,value) in op_kwargs.items():
            params[key] = value

        #check date
        if "startDate" in filt and not self._checkDate(filt["startDate"]):
            raise AdamApiError("Parameter Error. Invalid date format [%Y-%m-%d,%Y-%m-%dT%H:%M:%SZ,%Y-%m-%dT%H:%M:%S]")
        if "endDate" in filt and not self._checkDate(filt["endDate"]):
            raise AdamApiError("Parameter Error. Invalid date format [%Y-%m-%d,%Y-%m-%dT%H:%M:%SZ,%Y-%m-%dT%H:%M:%S]")
        if "startDate" in filt and "endDate" in filt:
            if filt["startDate"] > filt["endDate"]:
                raise AdamApiError("Parameter Error. startDate > endDate")
        #check Getfile
        if "format" in opt and request == "GetFile":
            raise AdamApiError("invalid option for GetFile request. remove format")

        params["options"] = json.dumps(opt)
        params["filters"] = json.dumps(filt)
        params["client"] = "adamapi"
        params["rest"] = rest
        params["compress"] = compress
        params["request"] = request
        params["asynchronous"] = asynchronous
        return params,fname

    def _checkDate(self,date):
        test=False
        pattern=[
                "%Y-%m-%d",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S"
                ]
        for p in pattern:
            try:
                datetime.strptime(date,p)
                test=True
            except:
                pass
        return test

    def _checkDir(selfi,dirname):
        try:
            os.makedirs( dirname )
        except OSError as ose:
            if ose.errno!=errno.EEXIST:
                raise AdamApiError( ose )
