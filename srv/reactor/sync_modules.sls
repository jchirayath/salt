##
# syncall to the minion

sync_all:
  local.module.run:
    - tgt: {{ data['id'] }}
    - arg:
        saltutil.sync_all
