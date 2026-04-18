global:
  resolve_timeout: 5m

templates:
  - /etc/alertmanager/templates/*.tmpl

route:
  receiver: telegram
  group_by: [alertname, severity]
  group_wait: 15s
  group_interval: 1m
  repeat_interval: 3h

receivers:
  - name: telegram
    telegram_configs:
      - bot_token: "__TELEGRAM__BOT_TOKEN__"
        chat_id: __TELEGRAM__CHAT_ID__
        parse_mode: HTML
        send_resolved: true
        message: '{{ template "telegram.message" . }}'
