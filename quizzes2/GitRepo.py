# coding:utf8
# author:winton

import httplib
import urllib
import base64
import json
import logging


class GitRepo:
    def __init__(self, config):
        self.rootToken = config['root_token']
        self.hostname = config['hostname']
        self.port = config['port']
        self.repoId = config['repo_id']
        self.fileOperUrl = config['file_operation_url']
        self.ref = config['ref']
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}

    def readContent(self, filepath):
        '''
        从gitlab上获取指定路径的文件内容,如果文件不存在或者发生其他问题，则返回None
        '''
        url = self.fileOperUrl % {
            'root_token': self.rootToken,
            'repo_id': self.repoId,
            'ref': self.ref,
            'filepath': filepath
        }
        conn = httplib.HTTPConnection(self.hostname, self.port, timeout=10)
        content = None
        try:
            conn.request("GET", url, None, self.headers)
            response = conn.getresponse()

            if response.status == 200:
                content = json.loads(base64.b64decode(json.loads(response.read())["content"]))
            else:
                msg = json.loads(response.read())['message']
                logging.info('readContent: wrong status returned [status=%d] [msg=%s] [filepath=%s]' % (response.status, msg, filepath))
        except httplib.HTTPException as e:
            logging.warning('Exception when get file from remote repo [%s]' % str(e))
        finally:
            conn.close()
        return content

    def createContent(self, content, filepath):
        '''
        在gitlab指定路径上新建文件，返回服务器返回的信息
        '''
        url = self.fileOperUrl % {
            'root_token': self.rootToken,
            'repo_id': self.repoId,
            'ref': self.ref,
            'filepath': filepath
        }
        conn = httplib.HTTPConnection(self.hostname, self.port, timeout=10)
        conn.request("POST", url, urllib.urlencode(content))
        response = conn.getresponse()
        result = json.loads(response.read())
        if response.status == 200 or response.status == 201:
            logging.info('createContent: file created successfully [filepath=%s]' % (filepath))
        else:
            logging.warning('createContent: wrong status returned [status=%d] [msg=%s] [filepath=%s]' % (response.status, result['message'], filepath))
            raise Exception('wrong status [status=%d]' % response.status)
        return result

    def updateContent(self, content, filepath):
        '''
        在gitlab上更新指定路径的文件，返回服务器返回的信息
        '''
        url = self.fileOperUrl % {
            'root_token': self.rootToken,
            'repo_id': self.repoId,
            'ref': self.ref,
            'filepath': filepath
        }
        conn = httplib.HTTPConnection(self.hostname, self.port, timeout=10)
        conn.request("PUT", url, urllib.urlencode(content))
        response = conn.getresponse()
        result = json.loads(response.read())
        if response.status == 200 or response.status == 201:
            logging.info('updateContent: file updated successfully [filepath=%s]' % (filepath))
        else:
            logging.warning('updateContent: wrong status returned [status=%d] [msg=%s] [filepath=%s]' % (response.status, result['message'], filepath))
            raise Exception('wrong status [status=%d]' % response.status)
        return result
