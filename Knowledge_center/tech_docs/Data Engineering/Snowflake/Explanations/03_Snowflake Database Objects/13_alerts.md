## Alerts

### What is it?
- Monitors a condition and sends a notification when it becomes true
- Like a scheduled check — if condition met → fire alert via Snowflake Notification Integration

```
-- Create notification integration (email/webhook/SNS)
CREATE NOTIFICATION INTEGRATION my_email_integration
    TYPE = EMAIL
    ENABLED = TRUE;

-- Create alert
CREATE ALERT high_error_rate_alert
    WAREHOUSE = 'MONITORING_WH'
    SCHEDULE = '10 MINUTE'          -- check every 10 minutes
    IF (EXISTS (
        SELECT 1 FROM error_logs
        WHERE error_time > DATEADD(minute, -10, CURRENT_TIMESTAMP)
          AND severity = 'CRITICAL'
    ))
    THEN CALL SYSTEM$SEND_EMAIL(
        'my_email_integration',
        'alerts@company.com',
        'Critical errors detected',
        'Check error_logs table immediately'
    );

-- Alerts start suspended
ALTER ALERT high_error_rate_alert RESUME;
```

### Key Things to Remember
- Alerts use warehouse or serverless compute to run the condition check
- Alert fires only when condition transitions from FALSE → TRUE (not repeatedly)
- Check alert history:

```
SELECT * FROM snowflake.account_usage.alert_history
ORDER BY scheduled_time DESC;
```