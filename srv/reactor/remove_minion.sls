# reactor/remove_minion.sls
#
# reactor state that triggers the orch/remove_minion orchestration
remove_minion:
  runner.state.orch:
    - mods: orch.remove_minion
    - pillar:
        minion_id: {{ data.data['minion_id'] }}
        mac: {{ data.data['mac_addr'] }}
        name: {{ data.data['user'] }}
        email: {{ data.data['email'] }}
        description: {{ data.data['description'] }}
