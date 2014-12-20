import sendgrid
from junction.settings import SENDGRID_FROM_EMAIL, SENDGRID_EMAIL_USERNAME,SENDGRID_EMAIL_PASSWORD

class EmailEngine():
  
    def send_email(self, content):    
        '''It takes email content, subject, to address, cc-list in a dictionary. Optionally 
        it t from-email address. Format to send the dictionary is as follows
        content = {}
        content['body'] = email body [text or html]
        content['subject'] = subject
        content['to_email'] = ['ab@c.com'] or ['ab@c.com','dc@m.com']
        content['cc_email'] = ['ab@c.com'] or ['ab@c.com','dc@m.com']
        content['from_email'] = "from_email@zz.com"  optional, since this would have been configured in 
                                                     settings file
        '''
        
        to_list = content['to_email']
        subject = content['subject']
        body = content['body']
        cc_list = content.get('cc_email', default=None)
        from_address = content.get('from_email', default=None)
        from_address = SENDGRID_FROM_EMAIL or from_address 
            
        
        sg_handler = sendgrid.SendGridClient(SENDGRID_EMAIL_USERNAME, SENDGRID_EMAIL_PASSWORD, raise_errors=True)
        message = sendgrid.Mail()
        
        message.add_to(to_list)
        message.set_subject(subject)
        message.set_html(body)
        message.set_from(from_address)
        if cc_list is not None:
            message.add_bcc(cc_list)
        
        status, msg = sg_handler.send(message)
      
        return status
    