whitelist_minion:
  runner.state.orch:
    - mods: orch.whitelist
    - pillar:
        mac: {{ data.data['mac'] }}
        minion_id: {{ data.data['minion_id'] }}
        mac: {{ data.data['mac_addr'] }}
        name: {{ data.data['user'] }}
        email: {{ data.data['email'] }}
        description: {{ data.data['description'] }}
