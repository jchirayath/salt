# Orchestration state to add accept new minion key

# Get Data from Pillar
{% set minion_id = salt['pillar.get']('minion_id', None) %}
{% set email_admin = salt['pillar.get']('email_admin', None) %}

minion_add:
  salt.wheel:
    - name: key.accept
    - match: {{ minion_id }}

pause:
  salt.runner:
    - name: test.sleep
    - s_time: 5
    - require:
      - salt: minion_add

deploy_modules:
  salt.function:
    - name: saltutil.sync_modules
    - tgt: {{ minion_id }}
    - require:
      - salt: minion_add

send_email_admin_new_minion:
  module.run:
    - name: mime.send_msg
    - profile: mysmtp
    - recipient: "{{ email_admin }}"
    - subject: SaltStack Server Message
    - template: salt://master/files/email/new_minion_registered.txt
    - context:
        name: {{ minion_data.name }}
        description: New Minion registration activated
        mac: {{ minion_macs.macs[0] }}
        minion_id: {{ minion_id }}
        num_fails: 0
        reason: New Minion connected to Salt Master
        email_admin: {{ email_admin }}
