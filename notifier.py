from plyer import notification


notification_title= 'hey user '
notification_msg= "Welcome..! "
notification.notify(
    title = notification_title,
    message = notification_msg,
    timeout = "50",
    toast = False,
)