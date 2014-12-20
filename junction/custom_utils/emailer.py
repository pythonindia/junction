import sendgrid
from junction.settings import SENDGRID_FROM_EMAIL, SENDGRID_EMAIL_USERNAME,SENDGRID_EMAIL_PASSWORD

class EmailEngine():
    '''Send the email Body,Subject,To_Address as list, CC_Emails as list IN A DICTIONARY. Optionally 
        you can even send the from_email '''
  
    def send_email(self, content):    
        
        to_list = content['to_email']
        
        FROM_ADDRESS = content.get('from_email', default=None)
        if FROM_ADDRESS == None:
            FROM_ADDRESS = SENDGRID_FROM_EMAIL
        
        sg = sendgrid.SendGridClient(SENDGRID_EMAIL_USERNAME, SENDGRID_EMAIL_PASSWORD, raise_errors=True)
        message = sendgrid.Mail()
        
        message.add_to(to_list)
        message.set_subject(content['subject'])
        message.set_html(content['body'])
        message.set_from(FROM_ADDRESS)
        
        cc_list = content.get('cc_email', default=None)
        if cc_list != None:
            message.add_bcc(cc_list)
        
        status, msg = sg.send(message)
      
        return status
    