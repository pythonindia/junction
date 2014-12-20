import sendgrid
from junction.settings import SENDGRID_FROM_EMAIL, SENDGRID_EMAIL_USERNAME,SENDGRID_EMAIL_PASSWORD

class EmailEngine():
  
    def send_email(self,to_list,body,subject=None,cc_list=None,from_address=None):    
        '''It takes email body, to address and Optionally it takes cc-list, subject 
        and from-email address. Format to send the dictionary is as follows
        email body  can be text or html
        to_email = ['ab@c.com'] or ['ab@c.com','dc@m.com']
        cc_email = ['ab@c.com'] or ['ab@c.com','dc@m.com']
        from_email = "from_email@zz.com"  optional, since this would have been configured in settings file
                                                     
        '''
        
        subject = subject or ""
        verified_from_address = from_address or SENDGRID_FROM_EMAIL[0]
       
        sg_handler = sendgrid.SendGridClient(SENDGRID_EMAIL_USERNAME, SENDGRID_EMAIL_PASSWORD, raise_errors=True)
        message = sendgrid.Mail()
        
        message.add_to(to_list)
        message.set_subject(subject)
        message.set_html(body)
        message.set_from(verified_from_address)
        if cc_list is not None:
            message.add_bcc(cc_list)
        
        status, msg = sg_handler.send(message)
      
        return status
    