delete_minion:
  wheel.key.delete:
    - match: {{ data.data['minion_id'] }}
