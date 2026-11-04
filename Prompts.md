# PROMPTS.md

# AirAware – Smart Monitor
## Retrospective AI Development Conversation Log

**Important Note:** This document is a retrospective reconstruction of the AI-assisted development process based on the existing AirAware source code, project documentation, and implemented features. It is not a verbatim transcript of the original conversations.

---

## Conversation 1: Project Planning and Requirements

**User Prompt:**

I want to develop a smart environmental monitoring application called AirAware Smart Monitor. The application should monitor temperature and humidity readings collected from a Raspberry Pi and display the information in a simple dashboard. I want users to enter their name and phone number before accessing the monitoring screen.

**AI Response:**

We can develop the application using Python and Flet. The application will contain a login interface and a monitoring dashboard. Firebase Firestore will be used to receive sensor readings. The main features will include real-time monitoring, temperature alerts, and notifications.

**Development Objective:**

Establish the main application requirements and identify the technologies needed for the project.

---

## Conversation 2: Creating the Application Interface

**User Prompt:**

Create a login screen for AirAware using Python Flet. The screen should include the application name, a username field, a phone number field, and a login button. Use a modern dark theme with green accent colors.

**AI Response:**

The interface can be built using Flet components such as Text, TextField, Column, Container, and FilledButton. A dark theme with green highlights will provide a clear and modern appearance.

The login screen should collect the user's information and display the monitoring dashboard after successful input.

**Implementation Reference:**

The existing application uses:
- `ft.TextField` for username and phone number.
- `ft.FilledButton` for login.
- `page.theme_mode = ft.ThemeMode.DARK` for dark mode.

---

## Conversation 3: Developing the Monitoring Dashboard

**User Prompt:**

Develop a dashboard that displays the current temperature and humidity readings. The temperature should appear prominently in large text, while humidity should be displayed underneath. Include a system status indicator and a clean monitoring card.

**AI Response:**

A dashboard can be created using Flet containers, rows, and columns. Temperature and humidity values can be represented by Text components. A status message and a colored indicator can communicate whether the system is operating normally or detecting high temperature.

**Implementation Reference:**

The application includes:
- Temperature display.
- Humidity display.
- System status message.
- Monitoring card.
- Visual status indicator.

---

## Conversation 4: Firebase Firestore Integration

**User Prompt:**

Connect AirAware to Firebase Firestore. I want the application to receive temperature and humidity readings automatically from the Raspberry Pi without manually refreshing the dashboard.

**AI Response:**

Firebase Admin SDK can be used to connect Python to Firestore. After initializing Firebase, the application can subscribe to document updates using Firestore's snapshot listener.

The application listens to the `air_aware` collection and the `latest` document. When new sensor information arrives, the dashboard can update its displayed values.

**Implementation Reference:**

The project uses:
- `firebase_admin`
- `credentials.Certificate`
- `firestore.client()`
- `document("latest").on_snapshot(on_snapshot)`

---

## Conversation 5: Implementing Real-Time Updates

**User Prompt:**

Make sure the dashboard updates automatically whenever new temperature or humidity data is received from Firebase. The user should not need to restart the application or refresh the page.

**AI Response:**

The Firestore `on_snapshot` listener can receive real-time document changes. The callback function should extract the latest document data, convert the temperature value to a numeric format, update the interface components, and refresh the page.

A background thread can also be used for additional rendering support.

**Implementation Reference:**

The existing code uses:
- `on_snapshot(doc_snapshot, changes, read_time)`.
- `doc.to_dict()` to retrieve document data.
- `temp_txt.value` to update temperature.
- `hum_txt.value` to update humidity.
- `page.update()` to refresh the interface.

---

## Conversation 6: Developing the Temperature Alert System

**User Prompt:**

Implement a smart temperature alert system. When the temperature reaches 27 degrees Celsius, the dashboard should change its appearance and display a critical warning. When the temperature returns to normal, the dashboard should return to its original appearance.

**AI Response:**

A conditional temperature monitoring mechanism can be implemented inside the Firestore snapshot callback.

When the temperature is greater than or equal to 27°C:
- Change the monitoring card background to red.
- Display a critical temperature warning.
- Change the status indicator color.
- Trigger a desktop notification.

When the temperature falls below the threshold, restore the normal dashboard colors and status message.

**Implementation Reference:**

The existing code uses:
`if t >= 27.0:`

The normal state is restored through the corresponding `else` condition.

---

## Conversation 7: Adding Desktop Notifications

**User Prompt:**

Add desktop notifications to AirAware. Whenever the temperature reaches the critical threshold, the user should receive a notification containing the current temperature.

**AI Response:**

The Plyer notification library can be used to display desktop notifications. The notification should include the application name, a warning message, and the current temperature.

To avoid repeatedly notifying the user while the temperature remains high, a Boolean flag can track whether a notification has already been sent.

**Implementation Reference:**

The project uses:
- `from plyer import notification`
- `notification.notify()`
- `page.notification_sent`

---

## Conversation 8: Integrating WhatsApp Alerts

**User Prompt:**

Add a WhatsApp alert feature. When the temperature reaches 30°C or higher, send an alert message to the phone number entered by the user during login.

**AI Response:**

PyWhatKit can be used to send WhatsApp messages. The phone number should be formatted with the international country code before sending.

The WhatsApp operation should run in a separate background thread so that the dashboard remains responsive.

A Boolean flag can prevent repeated WhatsApp alerts while the temperature remains above the threshold.

**Implementation Reference:**

The project uses:
- `pywhatkit`
- `kit.sendwhatmsg_instantly()`
- `send_whatsapp_fast(temp)`
- `page.whatsapp_sent`

---

## Conversation 9: Improving Application Responsiveness

**User Prompt:**

Improve the responsiveness of the application. Background operations such as WhatsApp messages and desktop notifications should not block the main interface or interrupt real-time monitoring.

**AI Response:**

Python threading can be used to run time-consuming operations separately from the main application flow.

The application uses daemon threads for background rendering, WhatsApp operations, and desktop notifications. This allows the dashboard to continue receiving updates while background tasks are running.

**Implementation Reference:**

The existing code imports:
- `threading`
- `time`

It uses `threading.Thread()` for background operations.

---

## Conversation 10: Cross-Platform Interface and Application Access

**User Prompt:**

Configure AirAware to run through a browser-based interface and make the application suitable for monitoring from different devices.

**AI Response:**

Flet provides browser-based application access. The application can be launched using the Flet runtime with a configured host and port.

The actual accessibility from other devices depends on the host configuration and network settings.

**Implementation Reference:**

The current source code uses:
- `ft.AppView.WEB_BROWSER`
- `host="127.0.0.1"`
- `port=8080`

---

## Conversation 11: Managing Dependencies and Installation

**User Prompt:**

Prepare the installation requirements for AirAware and identify the Python libraries required to run the application.

**AI Response:**

The main dependencies required by the existing implementation are:

- Flet for the user interface.
- Firebase Admin SDK for Firestore integration.
- Plyer for desktop notifications.
- PyWhatKit for WhatsApp alerts.

The dependencies can be installed using pip.

**Installation Command:**

```bash
pip install flet firebase-admin plyer pywhatkit
```

The Firebase service account credentials must be configured securely before running the application.

---

## Conversation 12: Code Review and Security

**User Prompt:**

Review the AirAware source code and identify possible improvements related to code organization, security, and reliability.

**AI Response:**

The application should protect Firebase service account credentials and avoid publishing private JSON credential files in a public repository.

Additional improvements include:
- Replacing broad exception handling with specific error handling.
- Managing Firestore listener subscriptions.
- Improving logging and error reporting.
- Validating user input.
- Managing background threads safely.
- Avoiding hardcoded sensitive configuration values.

**Development Objective:**

Improve the reliability and security of the application.

---

## Conversation 13: Project Documentation

**User Prompt:**

Prepare project documentation explaining the purpose of AirAware, its main features, architecture, dependencies, installation process, and execution instructions.

**AI Response:**

The README should explain the application workflow, technology stack, Firebase integration, dashboard functionality, alert thresholds, and installation requirements.

It should also provide instructions for configuring Firebase credentials and launching the application.

---

## Conversation 14: Final Project Review

**User Prompt:**

Review the AirAware Smart Monitor project as a complete application. Summarize its main functionality and identify areas that may require further development or testing.

**AI Response:**

AirAware is a Python-based environmental monitoring application developed with Flet and Firebase Firestore.

Its main functionality includes:
- User login interface.
- Real-time temperature and humidity monitoring.
- Firebase Firestore integration.
- Visual temperature warnings.
- Desktop notifications.
- WhatsApp alerts.
- Background processing.

Further development can focus on improving error handling, security, automated testing, device compatibility, and application architecture.

---

## Final Note

This retrospective document was prepared after the original AI conversation history became unavailable. The conversations are reconstructed from the existing source code and project documentation and should not be interpreted as original historical prompts or proof that every proposed improvement was implemented or tested.
