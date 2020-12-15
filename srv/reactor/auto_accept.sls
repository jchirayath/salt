{% if 'act' in data and data['act'] == 'pend' %}
add_minion:
  runner.state.orch:
    - mods: orch.new_minion
    - pillar:
        minion_id: {{ data['id'] }}

{% endif %}
