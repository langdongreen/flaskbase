# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import boto3
import email
import sdb

from s3cache import S3cache


class S3mail():
        s3 = None
        bucket = None
        cache = None

        base_dir = '/usr/home/lg/private/lg/projects/software/s3mail/'
        cache_folder = 'cache/'
        cache_ttl = 64480
        
        def __init__(self,bucket,cache=None):
            self.s3 = boto3.resource('s3')
#resource.meta.client
            self.bucket = self.s3.Bucket(bucket)
            self.cache = S3cache(self.base_dir+self.cache_folder,self.cache_ttl)

        
        def cache_all_emails(self):
            '''Download all emails'''
            return self.cache.cache_all(self.bucket,self.bucket.objects.all())

      
        def get_email(self,key):
            '''Return a file pointer from cache'''
            if not self.cache.cache_hit(key):
                self.cache.cache_file(self.bucket,key)
            
            return self.cache.get_cache_file(key)
            
            
            #return email.message_from_bytes(self.s3.Object(self.bucket.name,key).get()['Body'].read())
        
        def save_email(self,file):
            '''Copy email to s3'''
            return self.bucket.upload_file(file,'sci/test.txt')
        
        def delete_email(self,key):
            '''delete email from s3'''
            if self.cache.delete_cache_file(key) and\
                self.bucket.delete_key(key):
                    return True
            else:
                return None
            
            
            
            
        def read_email(self,key):
            pass
            
        def parse_email(self,file):
            '''parse email file and return dictionary of fields'''
            attachments = []
            text = None
            html = None
            subject = None
            to = None
            sender = None
            date = None
            
            message = email.message_from_bytes(file.read())
            subject = message.get('subject')
            to =  message.get('to')
            sender =  message.get('from')
            date = message.get('date')


            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    disposition = part.get('Content-Disposition')
                    if content_type == "text/plain":
                       text = part.get_payload(decode=True)
                       
                    elif content_type == "text/html":
                        html = part.get_payload(decode=True)
                    elif disposition and disposition.split(';')[0] == "attachment":
                        
                        attachments.append(part.get_payload(decode=True))                 
                                        
            else:
                text = message.get_payload(decode=True)
                
            return {'key': file.name.replace(self.base_dir+self.cache_folder,""),
                    'attachments': attachments, 'text': text,'html':html, 
                    'subject': subject, 'to': to, 'from': sender, 'date': date}
            
        def save_attachment(self,attachment,file):
            '''Write attachment (data) to file path'''
            return open(file,'wb').write(attachment)
        
        def store_metadata(self,domain,data):
            
            '''Store email metadata in amazon simpledb'''
            sdb.add_attribute(domain,data['key'],('subject',data['subject']))
            sdb.add_attribute(domain,data['key'],('to',data['to']))
            sdb.add_attribute(domain,data['key'],('from',data['from']))
            sdb.add_attribute(domain,data['key'],('date',data['date']))

            
        def get_metadata(self,domain,key):
            return sdb.get_attributes(domain,key)['Attributes']
            
mail = S3mail('sciosemail')

#cache.delete_cache_file('sci/t9u0vi6v8d0bof3vodi4ik39f6ccpafd7ckbn181')
#all_emails = mail.get_all_emails()
mail.cache_all_emails()
#print(mail.parse_email(mail.get_email('sci/e31c9n8nf96omkldbg5hslk513krrmrnhj2lcq01')))
message = mail.get_email('sci/t9u0vi6v8d0bof3vodi4ik39f6ccpafd7ckbn181')
parsed = mail.parse_email(message)

print(parsed['to'])
print(parsed['from'])

mail.store_metadata("sciose",parsed)
print(mail.get_metadata("sciose",'sci/t9u0vi6v8d0bof3vodi4ik39f6ccpafd7ckbn181'))
#mail.save_attachment(parsed['attachments'][0],'/home/lg/test.png')
#
#mail.cache_email('sci/t9u0vi6v8d0bof3vodi4ik39f6ccpafd7ckbn181')
