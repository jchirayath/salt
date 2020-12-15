# Test Module to confirm that e-mail is working with most parameters in template
{% set email_admin = 'jchirayath@testing-labs.net' %}
{% set name =  'Lab Admins' %}
{% set description = 'SaltStack Test e-mail' %}

send_email:
  module.run:
    - name: mime.send_msg
    - profile: mysmtp
    - recipient: '{{ email_admin }}'
    - subject: SaltStack E-mail Test Function
    - template: salt://master/files/email/test_email.txt
    - context:
        name: {{ name }}
        description: {{ description }}
