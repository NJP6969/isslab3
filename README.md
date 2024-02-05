Steps to Run in Virtual Environment:

    Navigate to the directory where isslab3.py exists in the terminal.

    In the terminal, execute the following commands:

    ```bash

    python3 -m venv venv
    source venv/bin/activate
    export FLASK_APP=isslab3.py
    flask run
    ```

    Details about the website being opened will be displayed in the terminal.

    To access the site, type in the link provided in the terminal. For example, it might show http://127.0.0.1:5000.

    Happy logging!

Note:

    You can log in either using the user/user credentials or by using the login button.
    Registration and login are separate processes.
    Only the hashed password is displayed; otherwise, your username becomes your password.
    The assumption is that email IDs don't need to be hashed, but in real-life scenarios, hashing emails for privacy is recommended.

Additional Information:

If Flask is not working, you can refer to this link for installation on Ubuntu 20.04: How to Install Flask on Ubuntu 20.04.