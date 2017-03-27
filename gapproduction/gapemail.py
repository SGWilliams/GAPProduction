## This module facilitates the sending of email messages.
##
## The sole public function is:
## Email()
##
##
##

import os, email, smtplib, collections, gapageconfig
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart


class EmailAccount:
    '''
    A class for objects representing the GAP email account.
    '''
    def __init__(self):
        self.address = gapageconfig.emailAddress
        self.pwd = gapageconfig.emailPwd
        self.accountServer = gapageconfig.emailAccountServer
        self.defaultToAddress = gapageconfig.emailDefaultToAddress


class EmailObject:
    '''
    A class for email objects, including the account to be used, the content,
        subject, attachments, etc.
    '''
    def __init__(self, toAddress, subject, content, attachment=False):
        # Set the email's attributes
        self.ea = EmailAccount()
        self.subject = subject
        self.content = content
        self.attachment = attachment
        self.toAddress = toAddress

        # If the to address is blank, use the default address
        if self.toAddress == '':
            self.toAddress = self.ea.defaultToAddress

        # If there are attachments...
        if self.attachment:
            # Call the function to set the email for attachments
            _SetForAttachments(self)
        # Otherwise,
        else:
            # Set the plain message
            self.msg = MIMEText(self.content)

        # Set the subject and addresses for the email
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.ea.address
        self.msg['To'] = str(self.toAddress)



def Email(toAddress, subject, content, attachment=False):
    '''
    (str/list/tuple, str, str, [str/list]) -> boolean

    Sends an email.

    Arguments:
    toAddress -- The address(es) to which you wish to send the email. Can be
        a string representing a single email address or a list/tuple with many
        addresses.
    subject -- The subject line for the email.
    content -- The content of the email.
    attachment -- An optional parameter containing the path/paths to a file/files
        that you wish to attach to the email. Can be a string representing a
        single file or a list/tuple with many files.

    Examples:
    >>> Email('tlaon@gmail.com', 'test subject', 'test message')
    >>> Email(['tlaon@gmail.com','tlaon@uidaho.edu'], 'Test Subject', 'Test message', 'readme.txt')
    '''

    try:
        # Instantiate the email object
        eo = EmailObject(toAddress, subject, content, attachment)
        # Log in and send the email
        __LogInAndSend(eo)

        return True

    except:
        return False


def _SetForAttachments(eo):
    '''
    Set the email up to contain attachments
    '''
    try:
        # Set the message accordingly
        eo.msg = MIMEMultipart()
        # Add the message's content
        eo.msg.attach(MIMEText(eo.content))
        # And call the function to attach the files
        _Attach(eo)
    except Exception as e:
        print e


def _Attach(eo):
    '''
    Attach the files to the email
    '''
    try:
        # If there is a single attachment (the variable is a string)
        if isinstance(eo.attachment, basestring):
            # Call the function to encode and attach the file
            _IncludeAttachment(eo, eo.attachment)
        # Otherwise,
        else:
            # If the attachment variable is a list or tuple...
            if isinstance(eo.attachment, collections.Iterable):
                # For each item in the list...
                for att in eo.attachment:
                    # ...call the function to encode and attach the file
                    _IncludeAttachment(eo, att)
    except Exception as e:
        print e


def _IncludeAttachment(eo, attachment):
    '''
    Encode and attach the passed file to the message
    '''
    try:
        # Read the file and encode it into base64 format
        with open(attachment, "rb") as att:
            attContent = att.read()
        part = email.MIMEBase.MIMEBase('application', 'octect-stream')
        part.set_payload(attContent)
        email.Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        # Add the attachment to the message:
        eo.msg.attach(part)

        return True

    except Exception as e:
        print e
        return False



def __LogInAndSend(eo):
    try:
        # Connect to the server, log in, and send the message
        server = smtplib.SMTP(eo.ea.accountServer)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(eo.ea.address, eo.ea.pwd)
        # Send the email
        server.sendmail(eo.ea.address, eo.toAddress, eo.msg.as_string())
        # Close the server connection
        server.quit()

        return True

    except Exception as e:
        print e
        return False




def main():
    pass



if __name__ == '__main__':
    main()
