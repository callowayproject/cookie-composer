# Accessing templates in private repositories

Cookie composer can integrate with some third-party services in order to access private repositories.

```{note}
Currently only GitHub is supported.
```

## GitHub

At your terminal, enter `cookie-composer auth login`:

```console
$ cookie-composer auth login
First copy your one-time code: A25E-0A58
Then visit https://github.com/login/device in your browser, and paste the code when prompted.
Press Enter to open github.com in your browser...
```

Copy the one-time code (`A25E-0A58` in this example), and press Enter or Return to open your browser to the correct page.

You will arrive at a page similar to this:

![Activate the device](/_static/img/device-activation.png)

Paste the code (or enter each character individually) and press the continue button.

You will see an authorization page, similar to:

![Authorize cookie-composer](/_static/img/authorize-composer.png)

Press the "Authorize callowayproject" button to allow cookie-composer read-only access to your repositories.

Then you will see:

![All done!](/_static/img/authorize-done.png)

And you can close the browser window.

Your terminal will now look like:

```console
$ cookie-composer auth login
First copy your one-time code: A25E-0A58
Then visit https://github.com/login/device in your browser, and paste the code when prompted.
Press Enter to open github.com in your browser...
Waiting for authorization.............Authenticated to GitHub
```

Now when you provide any GitHub template link, Cookie Composer is able to access them as you with read-only access. 
